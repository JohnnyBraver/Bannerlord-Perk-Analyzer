param(
    [string]$GameRoot = $env:BANNERLORD_GAME_ROOT
)

$ErrorActionPreference = 'Stop'

$workspace = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
if ([string]::IsNullOrWhiteSpace($GameRoot)) {
    throw 'Bannerlord game root is required. Pass -GameRoot or set BANNERLORD_GAME_ROOT.'
}
$GameRoot = (Resolve-Path -LiteralPath $GameRoot).Path
$bin = Join-Path $GameRoot 'bin\Win64_Shipping_Client'
$campaignDll = Join-Path $bin 'TaleWorlds.CampaignSystem.dll'
$coreDll = Join-Path $bin 'TaleWorlds.Core.dll'
if (-not (Test-Path -LiteralPath $campaignDll) -or -not (Test-Path -LiteralPath $coreDll)) {
    throw "Could not find Bannerlord assemblies under '$bin'. Check -GameRoot."
}
$rawPerksPath = Join-Path $workspace 'Data\raw\perks.json'
$generatedRowsPath = Join-Path $workspace 'Data\generated\classified-perk-effects.json'
$postprocessScript = Join-Path $workspace 'src\bannerlord_perk_analyzer\postprocess.py'

[System.AppDomain]::CurrentDomain.add_AssemblyResolve({
    param($sender, $args)
    $name = New-Object System.Reflection.AssemblyName($args.Name)
    $candidate = Join-Path $bin ($name.Name + '.dll')
    if (Test-Path -LiteralPath $candidate) {
        return [System.Reflection.Assembly]::LoadFrom($candidate)
    }
    return $null
})

function New-OpcodeMaps {
    $single = @{}
    $double = @{}
    [System.Reflection.Emit.OpCodes].GetFields([System.Reflection.BindingFlags]'Public,Static') | ForEach-Object {
        $op = $_.GetValue($null)
        $value = [int]$op.Value
        if ($value -lt 0) { $value += 65536 }
        if ($value -le 0xff) { $single[$value] = $op } else { $double[$value -band 0xff] = $op }
    }
    @{ Single = $single; Double = $double }
}

function Read-Operand {
    param($OpCode, [byte[]]$Bytes, [ref]$Index, $Module)
    switch ($OpCode.OperandType.ToString()) {
        'InlineNone' { return $null }
        'ShortInlineI' { $v = [sbyte]$Bytes[$Index.Value]; $Index.Value += 1; return $v }
        'InlineI' { $v = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4; return $v }
        'InlineI8' { $v = [BitConverter]::ToInt64($Bytes, $Index.Value); $Index.Value += 8; return $v }
        'ShortInlineR' { $v = [BitConverter]::ToSingle($Bytes, $Index.Value); $Index.Value += 4; return $v }
        'InlineR' { $v = [BitConverter]::ToDouble($Bytes, $Index.Value); $Index.Value += 8; return $v }
        'ShortInlineBrTarget' { $v = [sbyte]$Bytes[$Index.Value]; $Index.Value += 1; return $v }
        'InlineBrTarget' { $v = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4; return $v }
        'InlineSwitch' {
            $count = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            $targets = @()
            for ($n = 0; $n -lt $count; $n++) {
                $targets += [BitConverter]::ToInt32($Bytes, $Index.Value)
                $Index.Value += 4
            }
            return $targets
        }
        'InlineString' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            return $Module.ResolveString($token)
        }
        'InlineField' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            return $Module.ResolveField($token)
        }
        'InlineMethod' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            return $Module.ResolveMethod($token)
        }
        'InlineType' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            return $Module.ResolveType($token)
        }
        'InlineTok' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            return $Module.ResolveMember($token)
        }
        'InlineSig' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            return $token
        }
        'ShortInlineVar' { $v = $Bytes[$Index.Value]; $Index.Value += 1; return $v }
        'InlineVar' { $v = [BitConverter]::ToUInt16($Bytes, $Index.Value); $Index.Value += 2; return $v }
        default { return $null }
    }
}

function Get-Instructions {
    param($Method)
    $maps = New-OpcodeMaps
    $body = $Method.GetMethodBody()
    $bytes = $body.GetILAsByteArray()
    $instructions = @()
    $i = 0
    while ($i -lt $bytes.Length) {
        $offset = $i
        $b = $bytes[$i]
        $i++
        if ($b -eq 0xfe) {
            $op = $maps.Double[[int]$bytes[$i]]
            $i++
        } else {
            $op = $maps.Single[[int]$b]
        }
        $ref = [ref]$i
        $operand = Read-Operand -OpCode $op -Bytes $bytes -Index $ref -Module $Method.Module
        $i = $ref.Value
        $instructions += [pscustomobject]@{
            Offset = $offset
            OpCode = $op.Name
            Operand = $operand
        }
    }
    $instructions
}

function Strip-LocPrefix {
    param([string]$Text)
    if ($null -eq $Text) { return '' }
    ($Text -replace '^\{=[^}]+\}', '').Trim()
}

function Format-Number {
    param([double]$Value)
    if ([Math]::Abs($Value - [Math]::Round($Value)) -lt 0.0001) {
        return ([Math]::Round($Value)).ToString([Globalization.CultureInfo]::InvariantCulture)
    }
    return $Value.ToString('0.######', [Globalization.CultureInfo]::InvariantCulture)
}

function Render-Effect {
    param([string]$Template, [double]$Bonus)
    $text = Strip-LocPrefix $Template
    if ($text -match '\{VALUE\}%') {
        $value = Format-Number ($Bonus * 100.0)
    } else {
        $value = Format-Number $Bonus
    }
    $text.Replace('{VALUE}', $value)
}

function Convert-Role {
    param([int]$Value)
    $map = @{
        0 = 'none'
        1 = 'role_1'
        2 = 'clan leader'
        3 = 'governor'
        4 = 'army leader'
        5 = 'party leader'
        6 = 'role 6'
        7 = 'surgeon'
        8 = 'engineer'
        9 = 'scout'
        10 = 'quartermaster'
        11 = 'player'
        12 = 'personal'
        13 = 'captain'
    }
    if ($map.ContainsKey($Value)) { return $map[$Value] }
    "role $Value"
}

function Convert-Increment {
    param([int]$Value)
    $map = @{
        0 = 'add'
        1 = 'add_factor'
    }
    if ($map.ContainsKey($Value)) { return $map[$Value] }
    "increment_$Value"
}

function Convert-TroopMask {
    param([int]$Value)
    $parts = @()
    if ($Value -eq 65535) { return 'all' }
    if (($Value -band 1) -ne 0) { $parts += 'infantry' }
    if (($Value -band 2) -ne 0) { $parts += 'ranged' }
    if (($Value -band 4) -ne 0) { $parts += 'cavalry' }
    if (($Value -band 8) -ne 0) { $parts += 'horse_archer' }
    if (($Value -band 16) -ne 0) { $parts += 'heroes' }
    if (($Value -band 32) -ne 0) { $parts += 'non_hero' }
    if (($Value -band 64) -ne 0) { $parts += 'formation' }
    if (($Value -band 128) -ne 0) { $parts += 'melee' }
    if (($Value -band 256) -ne 0) { $parts += 'mounted' }
    if ($parts.Count -eq 0) { return 'none' }
    $parts -join ', '
}

function Get-SkillAttribute {
    param([string]$Skill)
    $map = @{
        'One Handed' = 'Vigor'
        'Two Handed' = 'Vigor'
        'Polearm' = 'Vigor'
        'Bow' = 'Control'
        'Crossbow' = 'Control'
        'Throwing' = 'Control'
        'Riding' = 'Endurance'
        'Athletics' = 'Endurance'
        'Smithing' = 'Endurance'
        'Scouting' = 'Cunning'
        'Tactics' = 'Cunning'
        'Roguery' = 'Cunning'
        'Charm' = 'Social'
        'Leadership' = 'Social'
        'Trade' = 'Social'
        'Steward' = 'Intelligence'
        'Medicine' = 'Intelligence'
        'Engineering' = 'Intelligence'
    }
    if ($map.ContainsKey($Skill)) { return $map[$Skill] }
    ''
}

Import-Module (Join-Path $PSScriptRoot 'PerkEffectClassifier.psm1') -Force -DisableNameChecking

function Get-PerkCreateMap {
    param($Instructions)
    $stack = New-Object System.Collections.Generic.List[object]
    $map = @{}
    foreach ($ins in $Instructions) {
        switch ($ins.OpCode) {
            'ldarg.0' { $stack.Add(@{ Kind = 'this' }) }
            'ldstr' { $stack.Add(@{ Kind = 'string'; Value = [string]$ins.Operand }) }
            'call' {
                $m = $ins.Operand
                if ($m.Name -eq 'Create') {
                    $arg = $stack[$stack.Count - 1]; $stack.RemoveAt($stack.Count - 1)
                    $stack.Add(@{ Kind = 'created_perk'; StringId = $arg.Value })
                }
            }
            'stfld' {
                $value = $stack[$stack.Count - 1]; $stack.RemoveAt($stack.Count - 1)
                if ($stack.Count -gt 0) { $stack.RemoveAt($stack.Count - 1) }
                if ($value.Kind -eq 'created_perk') {
                    $map[$ins.Operand.Name] = $value.StringId
                }
            }
        }
    }
    $map
}

function Get-PerkDefinitions {
    param($Instructions, $CreateMap)
    $stack = New-Object System.Collections.Generic.List[object]
    $defs = @()
    foreach ($ins in $Instructions) {
        switch -Regex ($ins.OpCode) {
            '^ldarg\.0$' { $stack.Add(@{ Kind = 'this' }); continue }
            '^ldnull$' { $stack.Add($null); continue }
            '^ldstr$' { $stack.Add([string]$ins.Operand); continue }
            '^ldc\.r4$' { $stack.Add([double]$ins.Operand); continue }
            '^ldc\.i4\.m1$' { $stack.Add(-1); continue }
            '^ldc\.i4\.0$' { $stack.Add(0); continue }
            '^ldc\.i4\.1$' { $stack.Add(1); continue }
            '^ldc\.i4\.2$' { $stack.Add(2); continue }
            '^ldc\.i4\.3$' { $stack.Add(3); continue }
            '^ldc\.i4\.4$' { $stack.Add(4); continue }
            '^ldc\.i4\.5$' { $stack.Add(5); continue }
            '^ldc\.i4\.6$' { $stack.Add(6); continue }
            '^ldc\.i4\.7$' { $stack.Add(7); continue }
            '^ldc\.i4\.8$' { $stack.Add(8); continue }
            '^ldc\.i4\.s$|^ldc\.i4$' { $stack.Add([int]$ins.Operand); continue }
            '^ldfld$' {
                if ($stack.Count -gt 0) { $stack.RemoveAt($stack.Count - 1) }
                $fieldName = $ins.Operand.Name
                $stack.Add(@{ Kind = 'field'; Field = $fieldName; StringId = $CreateMap[$fieldName] })
                continue
            }
            '^call$' {
                $m = $ins.Operand
                if ($m.Name -eq 'GetTierCost') {
                    $tier = [int]$stack[$stack.Count - 1]; $stack.RemoveAt($stack.Count - 1)
                    $stack.Add($tier * 25)
                } elseif ($m.Name -like 'get_*' -and $m.ReturnType.FullName -eq 'TaleWorlds.Core.SkillObject') {
                    $skill = $m.Name.Substring(4) -replace 'Crafting', 'Smithing'
                    $skill = $skill -creplace '([a-z])([A-Z])', '$1 $2'
                    $stack.Add($skill)
                } elseif ($m.Name -eq 'Create') {
                    $arg = $stack[$stack.Count - 1]; $stack.RemoveAt($stack.Count - 1)
                    $stack.Add(@{ Kind = 'created_perk'; StringId = $arg })
                }
                continue
            }
            '^callvirt$' {
                $m = $ins.Operand
                if ($m.Name -eq 'Initialize' -and $m.DeclaringType.FullName -eq 'TaleWorlds.CampaignSystem.CharacterDevelopment.PerkObject') {
                    $items = @()
                    for ($n = 0; $n -lt 15; $n++) {
                        $items = ,$stack[$stack.Count - 1] + $items
                        $stack.RemoveAt($stack.Count - 1)
                    }
                    $perkField = $items[0]
                    $altField = $items[4]
                    $defs += [pscustomobject]@{
                        Field = $perkField.Field
                        StringId = $perkField.StringId
                        NameRaw = $items[1]
                        Name = Strip-LocPrefix $items[1]
                        Skill = $items[2]
                        Level = [int]$items[3]
                        AlternativeField = if ($altField) { $altField.Field } else { '' }
                        AlternativeStringId = if ($altField) { $altField.StringId } else { '' }
                        PrimaryTemplate = $items[5]
                        PrimaryRoleValue = [int]$items[6]
                        PrimaryBonus = [double]$items[7]
                        PrimaryIncrementValue = [int]$items[8]
                        SecondaryTemplate = $items[9]
                        SecondaryRoleValue = [int]$items[10]
                        SecondaryBonus = [double]$items[11]
                        SecondaryIncrementValue = [int]$items[12]
                        PrimaryTroopMaskValue = [int]$items[13]
                        SecondaryTroopMaskValue = [int]$items[14]
                    }
                }
                continue
            }
        }
    }
    $defs
}

function Escape-Yaml {
    param($Value)
    if ($null -eq $Value) { return '""' }
    '"' + ([string]$Value).Replace('\', '\\').Replace('"', '\"') + '"'
}

function Format-YamlList {
    param(
        [string]$Name,
        [object[]]$Values
    )
    $items = @($Values | Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) } | Select-Object -Unique)
    if ($items.Count -eq 0) { return "$Name`: []" }
    $lines = @("$Name`:")
    foreach ($item in $items) {
        $lines += "  - $(Escape-Yaml $item)"
    }
    $lines
}

function Safe-FilePart {
    param([string]$Text)
    $safe = $Text -replace '[<>:"/\\|?*]', '-'
    $safe = $safe -replace '\s+', ' '
    $safe.Trim()
}

function Ensure-Directory {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Write-JsonFile {
    param($Value, [string]$Path)
    Ensure-Directory -Path (Split-Path -Parent $Path)
    $json = $Value | ConvertTo-Json -Depth 12
    [System.IO.File]::WriteAllText($Path, "$json`n", [System.Text.UTF8Encoding]::new($false))
}

function Convert-RawEffectSlot {
    param($Perk, [string]$Slot)
    if ($Slot -eq 'primary') {
        $template = $Perk.PrimaryTemplate
        $roleValue = $Perk.PrimaryRoleValue
        $bonus = $Perk.PrimaryBonus
        $incrementValue = $Perk.PrimaryIncrementValue
        $maskValue = $Perk.PrimaryTroopMaskValue
    } else {
        $template = $Perk.SecondaryTemplate
        $roleValue = $Perk.SecondaryRoleValue
        $bonus = $Perk.SecondaryBonus
        $incrementValue = $Perk.SecondaryIncrementValue
        $maskValue = $Perk.SecondaryTroopMaskValue
    }

    [pscustomobject][ordered]@{
        template_raw = $template
        template = Strip-LocPrefix $template
        role = Convert-Role $roleValue
        role_value = $roleValue
        bonus = $bonus
        increment_type = Convert-Increment $incrementValue
        increment_value = $incrementValue
        troop_usage = Convert-TroopMask $maskValue
        troop_usage_value = $maskValue
    }
}

function Convert-PerkToRawObject {
    param($Perk)
    [pscustomobject][ordered]@{
        string_id = $Perk.StringId
        name_raw = $Perk.NameRaw
        name = $Perk.Name
        attribute = Get-SkillAttribute $Perk.Skill
        skill = $Perk.Skill
        level = $Perk.Level
        field = $Perk.Field
        alternative_field = $Perk.AlternativeField
        alternative_string_id = $Perk.AlternativeStringId
        primary_effect = Convert-RawEffectSlot -Perk $Perk -Slot 'primary'
        secondary_effect = Convert-RawEffectSlot -Perk $Perk -Slot 'secondary'
    }
}

function Convert-RowToExportObject {
    param($Row)
    [pscustomobject][ordered]@{
        id = "$($Row.PerkStringId)|$($Row.EffectSlot)"
        project = $Row.Project
        type = $Row.Type
        game_version_target = $Row.GameVersionTarget
        attribute = $Row.Attribute
        skill = $Row.Skill
        level = $Row.Level
        perk = $Row.Perk
        perk_string_id = $Row.PerkStringId
        effect_slot = $Row.EffectSlot
        alternative_perk_string_id = $Row.AlternativePerkStringId
        game = [pscustomobject][ordered]@{
            role = $Row.Role
            role_value = $Row.RoleValue
            bonus = $Row.Bonus
            increment_type = $Row.IncrementType
            increment_value = $Row.IncrementValue
            troop_usage = $Row.TroopUsage
            troop_usage_value = $Row.TroopUsageValue
            effect = $Row.Effect
            effect_template = $Row.EffectTemplate
        }
        classification = [pscustomobject][ordered]@{
            perk_type = $Row.PerkType
            perk_subtype = $Row.PerkSubtype
            trigger_conditions = @($Row.TriggerCondition)
            effect_tags = @($Row.EffectTags)
        }
        review = [pscustomobject][ordered]@{
            needs_review = $Row.NeedsReview
            functioning = $Row.Functioning
            perk_wrong = $Row.PerkWrong
            bug_note = $Row.BugNote
            notes = $Row.Notes
            classification_review = $Row.ClassificationReview
        }
        source = [pscustomobject][ordered]@{
            status = $Row.SourceStatus
            name = $Row.Source
            version = $Row.SourceVersion
        }
    }
}

function New-EffectRow {
    param($Perk, [string]$Slot)
    if ($Slot -eq 'primary') {
        $template = $Perk.PrimaryTemplate
        $roleValue = $Perk.PrimaryRoleValue
        $bonus = $Perk.PrimaryBonus
        $incrementValue = $Perk.PrimaryIncrementValue
        $maskValue = $Perk.PrimaryTroopMaskValue
    } else {
        $template = $Perk.SecondaryTemplate
        $roleValue = $Perk.SecondaryRoleValue
        $bonus = $Perk.SecondaryBonus
        $incrementValue = $Perk.SecondaryIncrementValue
        $maskValue = $Perk.SecondaryTroopMaskValue
    }
    if ([string]::IsNullOrWhiteSpace((Strip-LocPrefix $template))) {
        return $null
    }
    $effect = Render-Effect -Template $template -Bonus $bonus
    $role = Convert-Role $roleValue
    $class = Classify-Effect -Effect $effect -Skill $Perk.Skill -Role $role
    $classificationReview = $class.Review
    $class = Normalize-Classification -Type $class.Type -Subtype $class.Subtype -Skill $Perk.Skill
    $facets = Get-ReadableFacets -Type $class.Type -Subtype $class.Subtype -Effect $effect -Role $role
    $perkWrong = $false
    $notes = ''

    if ($effect -match 'part of an army') {
        $notes = 'Applies only while the party is part of an army; no dedicated army-membership trigger condition exists.'
    } elseif ($effect -match 'village raids') {
        $notes = 'Applies when taking food during village raids; no dedicated raid trigger condition exists.'
    }

    if ($effect -match 'Control skills of infantry.*Vigor skills of archers') {
        $classificationReview = 'Troop skill bonus spans infantry Control and archer Vigor; not hero character growth.'
    } elseif ($effect -match 'wages.*upgrade costs.*mercenary troops') {
        $classificationReview = 'Composite effect spans wages and upgrade costs for mercenary troops; single classification is partial.'
    } elseif ($effect -match 'companion wages.*recruitment fees') {
        $classificationReview = 'Composite effect spans companion wages and recruitment fees; single classification is partial.'
    }
    $row = [pscustomobject]@{
        Project = 'Bannerlord'
        Type = 'bannerlord_perk_effect'
        GameVersionTarget = '1.4.5'
        Attribute = Get-SkillAttribute $Perk.Skill
        Skill = $Perk.Skill
        Level = $Perk.Level
        Perk = $Perk.Name
        PerkStringId = $Perk.StringId
        EffectSlot = $Slot
        Role = $role
        RoleValue = $roleValue
        PerkType = $facets.Type
        PerkSubtype = $facets.Subtype
        TriggerCondition = @($facets.TriggerCondition)
        EffectTags = @($facets.EffectTags)
        Bonus = $bonus
        IncrementType = Convert-Increment $incrementValue
        IncrementValue = $incrementValue
        TroopUsage = Convert-TroopMask $maskValue
        TroopUsageValue = $maskValue
        Effect = $effect
        EffectTemplate = Strip-LocPrefix $template
        AlternativePerkStringId = $Perk.AlternativeStringId
        SourceStatus = 'local_game_assembly'
        Source = 'TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll'
        SourceVersion = '1.4.5'
        NeedsReview = $false
        Functioning = $null
        PerkWrong = $perkWrong
        BugNote = ''
        Notes = $notes
        ClassificationReview = $classificationReview
    }
    $row
}

$campaignAsm = [System.Reflection.Assembly]::LoadFrom($campaignDll)
[void][System.Reflection.Assembly]::LoadFrom($coreDll)
$defaultPerksType = $campaignAsm.GetType('TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultPerks', $true)
$register = $defaultPerksType.GetMethod('RegisterAll', [System.Reflection.BindingFlags]'NonPublic,Instance')
$initialize = $defaultPerksType.GetMethod('InitializeAll', [System.Reflection.BindingFlags]'NonPublic,Instance')

$createMap = Get-PerkCreateMap (Get-Instructions $register)
$perks = Get-PerkDefinitions -Instructions (Get-Instructions $initialize) -CreateMap $createMap
Write-JsonFile -Path $rawPerksPath -Value @($perks | Sort-Object Skill, Level, Name | ForEach-Object { Convert-PerkToRawObject -Perk $_ })

$rows = @()
foreach ($perk in $perks) {
    $primaryRow = New-EffectRow -Perk $perk -Slot 'primary'
    if ($primaryRow) { $rows += $primaryRow }
    $secondaryRow = New-EffectRow -Perk $perk -Slot 'secondary'
    if ($secondaryRow) { $rows += $secondaryRow }
}

Ensure-Directory -Path (Split-Path -Parent $rawPerksPath)
Ensure-Directory -Path (Split-Path -Parent $generatedRowsPath)
$resolvedGeneratedParent = (Resolve-Path -LiteralPath (Split-Path -Parent $generatedRowsPath)).Path
if (-not $generatedRowsPath.StartsWith($workspace, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Generated rows path is outside workspace: $generatedRowsPath"
}
if ($resolvedGeneratedParent -notlike "$workspace*") {
    throw "Generated rows parent is outside workspace: $resolvedGeneratedParent"
}
Write-JsonFile -Path $generatedRowsPath -Value @($rows | Sort-Object Attribute, Skill, Level, Perk, EffectSlot | ForEach-Object { Convert-RowToExportObject -Row $_ })

if (-not (Test-Path -LiteralPath $postprocessScript)) {
    throw "Could not find Python post-processing script: $postprocessScript"
}
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    throw 'Python is required for perk post-processing. Install Python or make python available on PATH.'
}
& $python.Source $postprocessScript --workspace $workspace
if ($LASTEXITCODE -ne 0) {
    throw "Python post-processing failed with exit code $LASTEXITCODE."
}

$reviewRows = $rows | Where-Object { $_.ClassificationReview }
$roleSummary = $rows | Group-Object Role | Sort-Object Name | ForEach-Object { "$($_.Name): $($_.Count)" }
$typeSummary = $rows | Group-Object PerkType | Sort-Object Name | ForEach-Object { "$($_.Name): $($_.Count)" }
Write-Output "Perks extracted: $($perks.Count)"
Write-Output "Generated effect rows: $($rows.Count)"
Write-Output "Generated review flags: $($reviewRows.Count)"
Write-Output 'Generated roles:'
$roleSummary | ForEach-Object { Write-Output "  $_" }
Write-Output 'Generated types:'
$typeSummary | ForEach-Object { Write-Output "  $_" }
