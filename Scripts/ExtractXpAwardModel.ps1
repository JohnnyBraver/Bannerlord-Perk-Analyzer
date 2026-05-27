param(
    [string]$GameRoot = $env:BANNERLORD_GAME_ROOT,
    [string[]]$AssemblyNames = @(
        'TaleWorlds.Core',
        'TaleWorlds.CampaignSystem'
    ),
    [string]$JsonOutputPath,
    [string]$MarkdownOutputPath,
    [string]$IlOutputPath,
    [switch]$DeepScanCallers,
    [switch]$IncludeContracts,
    [switch]$IncludeIl
)

$ErrorActionPreference = 'Stop'

$workspace = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
if ([string]::IsNullOrWhiteSpace($GameRoot)) {
    throw 'Bannerlord game root is required. Pass -GameRoot or set BANNERLORD_GAME_ROOT.'
}

$GameRoot = (Resolve-Path -LiteralPath $GameRoot).Path
$bin = Join-Path $GameRoot 'bin\Win64_Shipping_Client'
if (-not (Test-Path -LiteralPath $bin)) {
    throw "Could not find Bannerlord binary directory under '$GameRoot'. Check -GameRoot."
}

if ([string]::IsNullOrWhiteSpace($JsonOutputPath)) {
    $JsonOutputPath = Join-Path $workspace 'Data\generated\xp-award-methods.json'
}
if ([string]::IsNullOrWhiteSpace($MarkdownOutputPath)) {
    $MarkdownOutputPath = Join-Path $workspace 'Data\generated\reports\xp-awards.md'
}
if ([string]::IsNullOrWhiteSpace($IlOutputPath)) {
    $IlOutputPath = Join-Path $workspace 'Data\generated\reports\xp-award-il.md'
}

foreach ($path in @($JsonOutputPath, $MarkdownOutputPath, $IlOutputPath)) {
    $directory = Split-Path -Parent $path
    if (-not (Test-Path -LiteralPath $directory)) {
        New-Item -ItemType Directory -Path $directory | Out-Null
    }
}

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
        if ($value -le 0xff) {
            $single[$value] = $op
        } else {
            $double[$value -band 0xff] = $op
        }
    }

    @{
        Single = $single
        Double = $double
    }
}

function Get-TypeDisplayName {
    param($Type)
    if ($null -eq $Type) { return 'void' }
    if ($Type.IsGenericType) {
        $baseName = $Type.FullName
        if ([string]::IsNullOrWhiteSpace($baseName)) { $baseName = $Type.Name }
        $tick = $baseName.IndexOf('`')
        if ($tick -ge 0) { $baseName = $baseName.Substring(0, $tick) }
        $args = @($Type.GetGenericArguments() | ForEach-Object { Get-TypeDisplayName $_ })
        return ('{0}<{1}>' -f $baseName, ($args -join ', '))
    }
    if (-not [string]::IsNullOrWhiteSpace($Type.FullName)) { return $Type.FullName }
    return $Type.Name
}

function Get-MemberDisplayName {
    param($Member)
    if ($null -eq $Member) { return $null }
    try {
        if ($Member -is [System.Reflection.MethodBase]) {
            $parameters = @($Member.GetParameters() | ForEach-Object { Get-TypeDisplayName $_.ParameterType })
            $declaringType = Get-TypeDisplayName $Member.DeclaringType
            return ('{0}.{1}({2})' -f $declaringType, $Member.Name, ($parameters -join ', '))
        }
        if ($Member -is [System.Reflection.FieldInfo]) {
            return ('{0}.{1}' -f (Get-TypeDisplayName $Member.DeclaringType), $Member.Name)
        }
        if ($Member -is [System.Type]) {
            return Get-TypeDisplayName $Member
        }
        return $Member.ToString()
    } catch {
        return $Member.ToString()
    }
}

function Resolve-IlMember {
    param(
        [System.Reflection.MethodBase]$Method,
        [int]$Token,
        [string]$Kind
    )

    $module = $Method.Module
    $typeArgs = $null
    $methodArgs = $null
    if ($Method.DeclaringType -and $Method.DeclaringType.IsGenericType) {
        $typeArgs = $Method.DeclaringType.GetGenericArguments()
    }
    if ($Method.IsGenericMethod) {
        $methodArgs = $Method.GetGenericArguments()
    }

    try {
        switch ($Kind) {
            'Field' { return $module.ResolveField($Token, $typeArgs, $methodArgs) }
            'Method' { return $module.ResolveMethod($Token, $typeArgs, $methodArgs) }
            'Type' { return $module.ResolveType($Token, $typeArgs, $methodArgs) }
            'Member' { return $module.ResolveMember($Token, $typeArgs, $methodArgs) }
        }
    } catch {
        return ('unresolved:{0}:0x{1:x8}' -f $Kind, $Token)
    }
}

function Convert-ToSignedByte {
    param([byte]$Value)
    if ($Value -gt 127) { return ([int]$Value - 256) }
    return [int]$Value
}

function Read-Operand {
    param(
        [System.Reflection.MethodBase]$Method,
        $OpCode,
        [byte[]]$Bytes,
        [ref]$Index
    )

    switch ($OpCode.OperandType.ToString()) {
        'InlineNone' { return $null }
        'ShortInlineI' { $v = Convert-ToSignedByte $Bytes[$Index.Value]; $Index.Value += 1; return $v }
        'InlineI' { $v = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4; return $v }
        'InlineI8' { $v = [BitConverter]::ToInt64($Bytes, $Index.Value); $Index.Value += 8; return $v }
        'ShortInlineR' { $v = [BitConverter]::ToSingle($Bytes, $Index.Value); $Index.Value += 4; return $v }
        'InlineR' { $v = [BitConverter]::ToDouble($Bytes, $Index.Value); $Index.Value += 8; return $v }
        'ShortInlineBrTarget' { $v = Convert-ToSignedByte $Bytes[$Index.Value]; $Index.Value += 1; return $v }
        'InlineBrTarget' { $v = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4; return $v }
        'InlineSwitch' {
            $count = [BitConverter]::ToInt32($Bytes, $Index.Value)
            $Index.Value += 4
            $targets = @()
            for ($n = 0; $n -lt $count; $n++) {
                $targets += [BitConverter]::ToInt32($Bytes, $Index.Value)
                $Index.Value += 4
            }
            return $targets
        }
        'InlineString' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value)
            $Index.Value += 4
            try { return $Method.Module.ResolveString($token) } catch { return ('unresolved:String:0x{0:x8}' -f $token) }
        }
        'InlineField' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value)
            $Index.Value += 4
            return Resolve-IlMember -Method $Method -Token $token -Kind Field
        }
        'InlineMethod' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value)
            $Index.Value += 4
            return Resolve-IlMember -Method $Method -Token $token -Kind Method
        }
        'InlineType' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value)
            $Index.Value += 4
            return Resolve-IlMember -Method $Method -Token $token -Kind Type
        }
        'InlineTok' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value)
            $Index.Value += 4
            return Resolve-IlMember -Method $Method -Token $token -Kind Member
        }
        'InlineSig' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value)
            $Index.Value += 4
            return ('sig:0x{0:x8}' -f $token)
        }
        'ShortInlineVar' { $v = $Bytes[$Index.Value]; $Index.Value += 1; return $v }
        'InlineVar' { $v = [BitConverter]::ToUInt16($Bytes, $Index.Value); $Index.Value += 2; return $v }
        default { return $null }
    }
}

function Get-LdcNumber {
    param($OpCode, $Operand)
    switch ($OpCode.Name) {
        'ldc.i4.m1' { return -1 }
        'ldc.i4.0' { return 0 }
        'ldc.i4.1' { return 1 }
        'ldc.i4.2' { return 2 }
        'ldc.i4.3' { return 3 }
        'ldc.i4.4' { return 4 }
        'ldc.i4.5' { return 5 }
        'ldc.i4.6' { return 6 }
        'ldc.i4.7' { return 7 }
        'ldc.i4.8' { return 8 }
        'ldc.i4.s' { return $Operand }
        'ldc.i4' { return $Operand }
        'ldc.i8' { return $Operand }
        'ldc.r4' { return $Operand }
        'ldc.r8' { return $Operand }
        default { return $null }
    }
}

function Read-MethodIl {
    param(
        [System.Reflection.MethodBase]$Method,
        $OpcodeMaps,
        [switch]$KeepInstructions
    )

    $info = [ordered]@{
        il_bytes = 0
        numbers = @()
        strings = @()
        members = @()
        instructions = @()
        errors = @()
    }

    try {
        $body = $Method.GetMethodBody()
    } catch {
        $info.errors += $_.Exception.Message
        return $info
    }
    if ($null -eq $body) { return $info }

    $bytes = $body.GetILAsByteArray()
    $info.il_bytes = $bytes.Length
    $i = 0

    while ($i -lt $bytes.Length) {
        $offset = $i
        $b = $bytes[$i]
        $i++
        if ($b -eq 0xfe) {
            $op = $OpcodeMaps.Double[[int]$bytes[$i]]
            $i++
        } else {
            $op = $OpcodeMaps.Single[[int]$b]
        }
        if ($null -eq $op) {
            $info.errors += ('Unknown opcode 0x{0:x2} at IL_{1:x4}' -f $b, $offset)
            continue
        }

        $refIndex = [ref]$i
        $operand = Read-Operand -Method $Method -OpCode $op -Bytes $bytes -Index $refIndex
        $i = $refIndex.Value

        $number = Get-LdcNumber -OpCode $op -Operand $operand
        if ($null -ne $number) {
            $info.numbers += $number
        }
        if ($op.OperandType.ToString() -eq 'InlineString' -and $null -ne $operand) {
            $info.strings += [string]$operand
        }
        if ($operand -is [System.Reflection.MemberInfo] -or $operand -is [System.Type]) {
            $memberText = Get-MemberDisplayName $operand
            if (-not [string]::IsNullOrWhiteSpace($memberText)) {
                $info.members += $memberText
            }
        } elseif ($operand -is [string] -and $operand.StartsWith('unresolved:')) {
            $info.members += $operand
        }

        if ($KeepInstructions) {
            $operandText = ''
            if ($null -ne $operand) {
                if ($operand -is [System.Reflection.MemberInfo] -or $operand -is [System.Type]) {
                    $operandText = Get-MemberDisplayName $operand
                } elseif ($operand -is [array]) {
                    $operandText = $operand -join ', '
                } else {
                    $operandText = [string]$operand
                }
            }
            $info.instructions += ('IL_{0:x4}: {1,-14} {2}' -f $offset, $op.Name, $operandText).TrimEnd()
        }
    }

    $info.numbers = @($info.numbers | Sort-Object -Unique)
    $info.strings = @($info.strings | Sort-Object -Unique)
    $info.members = @($info.members | Sort-Object -Unique)
    return $info
}

function Get-MethodVisibility {
    param([System.Reflection.MethodBase]$Method)
    if ($Method.IsPublic) { return 'public' }
    if ($Method.IsFamily) { return 'protected' }
    if ($Method.IsAssembly) { return 'internal' }
    if ($Method.IsFamilyOrAssembly) { return 'protected internal' }
    if ($Method.IsPrivate) { return 'private' }
    return 'non-public'
}

function Get-MethodSignature {
    param([System.Reflection.MethodBase]$Method)
    $returnType = 'void'
    if ($Method -is [System.Reflection.MethodInfo]) {
        $returnType = Get-TypeDisplayName $Method.ReturnType
    }
    $parameters = @($Method.GetParameters() | ForEach-Object {
        '{0} {1}' -f (Get-TypeDisplayName $_.ParameterType), $_.Name
    })
    return ('{0} {1}.{2}({3})' -f $returnType, (Get-TypeDisplayName $Method.DeclaringType), $Method.Name, ($parameters -join ', '))
}

function Get-XpCategory {
    param([System.Reflection.MethodBase]$Method)
    $text = ('{0}.{1}' -f (Get-TypeDisplayName $Method.DeclaringType), $Method.Name)

    if ($text -match 'DefaultCombatXpModel|CombatXp|GetXpFromHit|MapEvent.*CommitXp|SkillLevelingManager.OnBattleEnded') { return 'combat xp' }
    if ($text -match 'PartyTraining|TroopRoster|FlattenedTroop|PartyAddSharedXp|CanTroopGainXp|GenerateSharedXp|TroopUpgrade|DailyTroopXpBonus|PartyBase.OnXpChanged|CampaignBattleRecoveryBehavior.GiveTroopXp|GarrisonRecruitment|ItemDiscard|InventoryLogic.*Xp|GetUpgradeXpCost|AddTroopsXp|AddPrisonersXp|GetMaximumXpAmountPartyCanGet') { return 'troop xp' }
    if ($text -match 'Healing|Medicine|PartyHealing') { return 'healing xp' }
    if ($text -match 'Smithing|Crafting|CraftingOrder') { return 'crafting xp' }
    if ($text -match 'Diplomacy|Charm|Persuasion|Tournament|Workshop|Alley|Hideout|IncidentEffect|Issue') { return 'activity xp' }
    if ($text -match 'GenericXp|Multiplier') { return 'xp multiplier' }
    if ($text -match 'HeroDeveloper|CharacterDevelopment|Learning|SkillLevel|SkillXp|GainRawXp|AddSkillXp|XpRequiredForLevel|TraitXp') { return 'hero progression' }
    return 'other xp'
}

function Test-NameCandidate {
    param([System.Reflection.MethodBase]$Method)
    $text = ('{0}.{1}' -f (Get-TypeDisplayName $Method.DeclaringType), $Method.Name)
    return ($text -cmatch '(Xp|XP|Xpf|Experience(?!d)|LearningLimit|LearningRate|SkillLevelChange|SkillsRequiredForLevel|MaxSkillPoint|PartyAddSharedXp|CanTroopGainXp|AddSkillXp|GainRawXp|AddXpToTroop)')
}

function Get-XpMemberReferences {
    param([string[]]$Members)
    @($Members | Where-Object {
        $_ -cmatch '(Xp|XP|Xpf|Experience(?!d)|Learning|SkillLevel|AddSkill|GainRaw|AddXpToTroop|PartyAddSharedXp|GenerateSharedXp|OnTroopGainXp|TroopRoster|HeroDeveloper)'
    } | Sort-Object -Unique)
}

function ConvertTo-JsonFile {
    param($Value, [string]$Path)
    $json = $Value | ConvertTo-Json -Depth 12
    [System.IO.File]::WriteAllText($Path, $json + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
}

function Write-Utf8File {
    param([string]$Path, [string[]]$Lines)
    [System.IO.File]::WriteAllLines($Path, $Lines, [System.Text.UTF8Encoding]::new($false))
}

function Escape-MarkdownCell {
    param([string]$Text)
    if ([string]::IsNullOrWhiteSpace($Text)) { return '' }
    return (($Text -replace '\|', '\|') -replace "`r?`n", ' ')
}

function Get-DisplayPath {
    param([string]$Path)
    $fullPath = [System.IO.Path]::GetFullPath($Path)
    if ($fullPath.StartsWith($workspace, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $fullPath.Substring($workspace.Length).TrimStart('\', '/')
    }
    return '<local path>'
}

function Get-SafeTypes {
    param([System.Reflection.Assembly]$Assembly)
    try {
        return @($Assembly.GetTypes())
    } catch [System.Reflection.ReflectionTypeLoadException] {
        return @($_.Exception.Types | Where-Object { $null -ne $_ })
    }
}

$opcodeMaps = New-OpcodeMaps
$loadedAssemblies = @()
$loadErrors = @()

foreach ($assemblyName in $AssemblyNames) {
    $dll = Join-Path $bin ($assemblyName + '.dll')
    if (-not (Test-Path -LiteralPath $dll)) {
        $loadErrors += "Missing assembly: $dll"
        continue
    }
    try {
        $loadedAssemblies += [System.Reflection.Assembly]::LoadFrom($dll)
    } catch {
        $loadErrors += "Could not load $dll`: $($_.Exception.Message)"
    }
}

if ($loadedAssemblies.Count -eq 0) {
    throw 'No Bannerlord assemblies were loaded.'
}

$bindingFlags = [System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly'
$methodsScanned = 0
$candidates = @()

foreach ($assembly in $loadedAssemblies) {
    $types = Get-SafeTypes -Assembly $assembly
    foreach ($type in $types) {
        $methods = @()
        try {
            $methods += $type.GetMethods($bindingFlags)
            $methods += $type.GetConstructors($bindingFlags)
        } catch {
            continue
        }

        foreach ($method in $methods) {
            $methodsScanned++
            $declaringTypeName = Get-TypeDisplayName $method.DeclaringType
            if ($method.IsConstructor) {
                continue
            }
            if ($declaringTypeName -eq 'TaleWorlds.CampaignSystem.GameModels' -and $method.Name -cmatch '(Xp|XP|Experience)') {
                continue
            }
            if ($method.Name -like 'AutoGeneratedGetMemberValue_*') {
                continue
            }
            $nameCandidate = Test-NameCandidate -Method $method
            if (-not $nameCandidate -and -not $DeepScanCallers) {
                continue
            }
            $ilInfo = Read-MethodIl -Method $method -OpcodeMaps $opcodeMaps -KeepInstructions:$IncludeIl
            if (-not $IncludeContracts -and $ilInfo.il_bytes -eq 0) {
                continue
            }
            $xpRefs = Get-XpMemberReferences -Members $ilInfo.members
            $callCandidate = $xpRefs.Count -gt 0
            if ($method.IsConstructor -and -not $callCandidate) {
                continue
            }
            if (-not $nameCandidate -and -not $callCandidate) {
                continue
            }

            $reasons = @()
            if ($nameCandidate) { $reasons += 'name' }
            if ($callCandidate) { $reasons += 'references-xp-member' }

            $parameters = @($method.GetParameters() | ForEach-Object {
                [ordered]@{
                    name = $_.Name
                    type = Get-TypeDisplayName $_.ParameterType
                }
            })

            $returnType = 'void'
            if ($method -is [System.Reflection.MethodInfo]) {
                $returnType = Get-TypeDisplayName $method.ReturnType
            }

            $candidates += [ordered]@{
                category = Get-XpCategory -Method $method
                assembly = $assembly.GetName().Name
                type = Get-TypeDisplayName $method.DeclaringType
                method = $method.Name
                signature = Get-MethodSignature -Method $method
                visibility = Get-MethodVisibility -Method $method
                is_static = $method.IsStatic
                return_type = $returnType
                parameters = $parameters
                il_bytes = $ilInfo.il_bytes
                match_reasons = $reasons
                numeric_constants = @($ilInfo.numbers)
                string_literals = @($ilInfo.strings)
                xp_references = @($xpRefs)
                referenced_members = @($ilInfo.members)
                il = @($ilInfo.instructions)
                errors = @($ilInfo.errors)
            }
        }
    }
}

$candidates = @($candidates | Sort-Object category, type, method)
$generatedAt = (Get-Date).ToString('o')
$payload = [ordered]@{
    generated_at = $generatedAt
    game_root = '<local path omitted>'
    bin = '<local path omitted>\bin\Win64_Shipping_Client'
    assemblies_requested = @($AssemblyNames)
    assemblies_loaded = @($loadedAssemblies | ForEach-Object { $_.GetName().Name })
    load_errors = @($loadErrors)
    deep_scan_callers = [bool]$DeepScanCallers
    include_contracts = [bool]$IncludeContracts
    methods_scanned = $methodsScanned
    methods_matched = $candidates.Count
    methods = $candidates
}

ConvertTo-JsonFile -Value $payload -Path $JsonOutputPath

$categoryOrder = @(
    'hero progression',
    'combat xp',
    'troop xp',
    'healing xp',
    'crafting xp',
    'activity xp',
    'xp multiplier',
    'other xp'
)

$markdown = New-Object System.Collections.Generic.List[string]
$markdown.Add('# Bannerlord XP Award Extraction') | Out-Null
$markdown.Add('') | Out-Null
$markdown.Add("Generated: $generatedAt") | Out-Null
$markdown.Add('') | Out-Null
$markdown.Add('This report is extracted from local compiled assemblies. It is a map of XP-related model methods, constants, and XP-relevant references, not source comments or decompiled C#.') | Out-Null
$markdown.Add('') | Out-Null
$markdown.Add('## Inputs') | Out-Null
$markdown.Add('') | Out-Null
$loadedAssemblyNames = (@($loadedAssemblies | ForEach-Object { '`' + $_.GetName().Name + '`' })) -join ', '
$markdown.Add('- Game root: local path omitted; provided by `-GameRoot` or `BANNERLORD_GAME_ROOT`') | Out-Null
$markdown.Add('- Assemblies loaded: ' + $loadedAssemblyNames) | Out-Null
$markdown.Add("- Methods scanned: $methodsScanned") | Out-Null
$markdown.Add("- XP-related methods matched: $($candidates.Count)") | Out-Null
$markdown.Add("- Deep caller scan: $([bool]$DeepScanCallers)") | Out-Null
$markdown.Add("- Include abstract contracts: $([bool]$IncludeContracts)") | Out-Null
if ($loadErrors.Count -gt 0) {
    $markdown.Add("- Load warnings: $($loadErrors.Count)") | Out-Null
}
$markdown.Add('') | Out-Null
$markdown.Add('## Reading Notes') | Out-Null
$markdown.Add('') | Out-Null
$markdown.Add('- `hero progression` is where hero skill XP is accepted, scaled, and converted into skill levels and character levels.') | Out-Null
$markdown.Add('- `combat xp` covers hit/kill XP and perk bonuses applied to battle XP.') | Out-Null
$markdown.Add('- `troop xp` covers shared party XP, daily training XP, troop roster XP, and upgrade-related XP.') | Out-Null
$markdown.Add('- `activity xp` covers non-combat sources such as charm, persuasion, tournaments, workshops, alleys, and hideouts.') | Out-Null
$markdown.Add('- Numeric constants are raw IL constants. Some are formula values; some are indexes, enum values, or branch helpers, so they need review before becoming prose.') | Out-Null
$markdown.Add('- Run with `-DeepScanCallers` to inspect every method body for calls into XP sinks. That is slower, especially if extra assemblies are included.') | Out-Null
$markdown.Add('') | Out-Null

$anchorMethods = @(
    'TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.AddSkillXp',
    'TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GainRawXp',
    'TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.CalculateLearningRate',
    'TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetXpFromHit',
    'TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetBattleXpBonusFromPerks',
    'TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GetEffectiveDailyExperience',
    'TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GenerateSharedXp',
    'Helpers.MobilePartyHelper.CanTroopGainXp',
    'Helpers.MobilePartyHelper.PartyAddSharedXp',
    'TaleWorlds.CampaignSystem.MapEvents.MapEventParty.CommitXpGain',
    'TaleWorlds.CampaignSystem.CampaignBehaviors.CampaignBattleRecoveryBehavior.GiveTroopXp',
    'TaleWorlds.CampaignSystem.Roster.TroopRoster.AddXpToTroop'
)
$anchorsFound = @()
foreach ($anchor in $anchorMethods) {
    $match = @($candidates | Where-Object { ($_.type + '.' + $_.method) -eq $anchor } | Select-Object -First 1)
    if ($match.Count -gt 0) { $anchorsFound += $match[0] }
}
if ($anchorsFound.Count -gt 0) {
    $markdown.Add('## High-Signal Entry Points') | Out-Null
    $markdown.Add('') | Out-Null
    foreach ($row in $anchorsFound) {
        $markdown.Add('- `' + $row.type + '.' + $row.method + '` (' + $row.category + ', IL bytes: ' + $row.il_bytes + ')') | Out-Null
    }
    $markdown.Add('') | Out-Null
}

foreach ($category in $categoryOrder) {
    $rows = @($candidates | Where-Object { $_.category -eq $category })
    if ($rows.Count -eq 0) { continue }
    $markdown.Add("## $($category.Substring(0, 1).ToUpper() + $category.Substring(1))") | Out-Null
    $markdown.Add('') | Out-Null
    $markdown.Add('| Method | IL bytes | Constants | XP references |') | Out-Null
    $markdown.Add('| --- | ---: | --- | --- |') | Out-Null
    foreach ($row in $rows) {
        $constants = ''
        if ($row.numeric_constants.Count -gt 0) {
            $constants = (($row.numeric_constants | Select-Object -First 12) -join ', ')
            if ($row.numeric_constants.Count -gt 12) { $constants += ', ...' }
        }
        $refs = ''
        if ($row.xp_references.Count -gt 0) {
            $refs = (($row.xp_references | Select-Object -First 5) -join '<br>')
            if ($row.xp_references.Count -gt 5) { $refs += '<br>...' }
        }
        $methodText = '`' + $row.type + '.' + $row.method + '`'
        $methodCell = Escape-MarkdownCell $methodText
        $constantsCell = Escape-MarkdownCell $constants
        $refsCell = Escape-MarkdownCell $refs
        $line = '| {0} | {1} | {2} | {3} |' -f $methodCell, $row.il_bytes, $constantsCell, $refsCell
        $markdown.Add($line) | Out-Null
    }
    $markdown.Add('') | Out-Null
}

if ($loadErrors.Count -gt 0) {
    $markdown.Add('## Load Warnings') | Out-Null
    $markdown.Add('') | Out-Null
    foreach ($warning in $loadErrors) {
        $markdown.Add("- $warning") | Out-Null
    }
    $markdown.Add('') | Out-Null
}

$markdown.Add('## Outputs') | Out-Null
$markdown.Add('') | Out-Null
$markdown.Add('- JSON index: `' + (Get-DisplayPath $JsonOutputPath) + '`') | Out-Null
if ($IncludeIl) {
    $markdown.Add('- IL dump: `' + (Get-DisplayPath $IlOutputPath) + '`') | Out-Null
}

Write-Utf8File -Path $MarkdownOutputPath -Lines $markdown

if ($IncludeIl) {
    $ilLines = New-Object System.Collections.Generic.List[string]
    $ilLines.Add('# Bannerlord XP Award IL Dump') | Out-Null
    $ilLines.Add('') | Out-Null
    $ilLines.Add("Generated: $generatedAt") | Out-Null
    $ilLines.Add('') | Out-Null
    foreach ($row in $candidates) {
        if ($row.il.Count -eq 0) { continue }
        $ilLines.Add("## $($row.type).$($row.method)") | Out-Null
        $ilLines.Add('') | Out-Null
        $ilLines.Add('```text') | Out-Null
        foreach ($line in $row.il) {
            $ilLines.Add($line) | Out-Null
        }
        $ilLines.Add('```') | Out-Null
        $ilLines.Add('') | Out-Null
    }
    Write-Utf8File -Path $IlOutputPath -Lines $ilLines
}

Write-Output "XP methods scanned: $methodsScanned"
Write-Output "XP methods matched: $($candidates.Count)"
Write-Output "JSON written: $JsonOutputPath"
Write-Output "Report written: $MarkdownOutputPath"
if ($IncludeIl) {
    Write-Output "IL written: $IlOutputPath"
}
