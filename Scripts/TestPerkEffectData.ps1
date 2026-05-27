$ErrorActionPreference = 'Stop'

$workspace = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$dataRoot = Join-Path $workspace 'Data\Perk Effects'
$overridePath = Join-Path $workspace 'Data\PerkEffectOverrides.json'

function Get-YamlScalar {
    param([string]$Text, [string]$Name)
    $match = [regex]::Match($Text, "(?m)^$([regex]::Escape($Name)): ""([^""]*)""")
    if ($match.Success) { return $match.Groups[1].Value }
    $match = [regex]::Match($Text, "(?m)^$([regex]::Escape($Name)): ([^`r`n]+)")
    if ($match.Success) { return $match.Groups[1].Value.Trim() }
    ''
}

function Get-YamlList {
    param([string]$Text, [string]$Name)
    $match = [regex]::Match($Text, "(?ms)^$([regex]::Escape($Name)):[ \t]*(?<body>(?:`r?`n  - ""[^""]*"")*)")
    if (-not $match.Success) { return @() }
    @([regex]::Matches($match.Groups['body'].Value, '  - "([^"]*)"') | ForEach-Object { $_.Groups[1].Value })
}

function Read-EffectRows {
    Get-ChildItem -LiteralPath $dataRoot -Recurse -File -Filter '*.md' | ForEach-Object {
        $text = Get-Content -LiteralPath $_.FullName -Raw
        [pscustomobject]@{
            Path = $_.FullName
            Key = "$(Get-YamlScalar -Text $text -Name 'perk_string_id')|$(Get-YamlScalar -Text $text -Name 'effect_slot')"
            PerkStringId = Get-YamlScalar -Text $text -Name 'perk_string_id'
            EffectSlot = Get-YamlScalar -Text $text -Name 'effect_slot'
            Role = Get-YamlScalar -Text $text -Name 'role'
            PerkType = Get-YamlScalar -Text $text -Name 'perk_type'
            PerkSubtype = Get-YamlScalar -Text $text -Name 'perk_subtype'
            TriggerCondition = @(Get-YamlList -Text $text -Name 'trigger_condition')
            EffectTags = @(Get-YamlList -Text $text -Name 'effect_tags')
            TroopUsage = Get-YamlScalar -Text $text -Name 'troop_usage'
            Effect = Get-YamlScalar -Text $text -Name 'effect'
            PerkWrong = (Get-YamlScalar -Text $text -Name 'perk_wrong') -eq 'true'
        }
    }
}

$rows = @(Read-EffectRows)
$errors = New-Object 'System.Collections.Generic.List[string]'
$rowByKey = @{}
foreach ($row in $rows) {
    if ($rowByKey.ContainsKey($row.Key)) {
        $errors.Add("Duplicate generated row key: $($row.Key)")
    } else {
        $rowByKey[$row.Key] = $row
    }
}

$overrides = Get-Content -LiteralPath $overridePath -Raw | ConvertFrom-Json
foreach ($override in $overrides) {
    $key = "$($override.perk_string_id)|$($override.effect_slot)"
    if (-not $rowByKey.ContainsKey($key)) {
        $errors.Add("Override does not match a generated row: $key")
    }
}

foreach ($row in $rows) {
    $effect = $row.Effect.ToLowerInvariant()

    if ($effect -match 'sent to confront|sent as attackers|sent to sally out' -and $row.TriggerCondition -notcontains 'simulation') {
        $errors.Add("Missing simulation trigger: $($row.Path)")
    }

    if ($effect -match 'morale loss' -and $row.TriggerCondition -contains 'morale threshold') {
        $errors.Add("Morale-loss text should not create morale threshold: $($row.Path)")
    }

    $restrictedComposition = 'foot troops|infantry|archers|ranged troops|melee troops|mounted troops|cavalry|bandit|mercenary|pack animals|prisoners|tier \d|garrisoned cavalry|footmen on horses|composed of|less than \d+ soldiers|equipped with throwing'
    $genericTroopScope = 'troops? in your (party|formation)|troops? under your formation|units in your (party|formation)'
    if ($row.TriggerCondition -contains 'party composition' -and $effect -match $genericTroopScope -and $effect -notmatch $restrictedComposition) {
        $errors.Add("Generic troop target scope marked as party composition: $($row.Path)")
    }

    $mechanicAsType = @('ammo capacity', 'damage increase', 'damage resistance', 'hit points', 'morale damage', 'ranged accuracy', 'reload speed')
    $siegeMechanic = $effect -match 'siege engine|siege engines|ballista|mangonel|trebuchet|ram|siege-tower|walls?|bombardment'
    if ($mechanicAsType -contains $row.PerkType -and -not $siegeMechanic) {
        $errors.Add("Combat mechanic left as top-level type outside siege context: $($row.Path)")
    }
}

$expectedWrong = @(
    'BowTrainer|primary',
    'TradeLocalConnection|primary',
    'RogueryArmsDealer|secondary',
    'ThrowingSplinters|primary',
    'TacticsGensdarmes|primary',
    'TwoHandedOnTheEdge|secondary',
    'CrossbowLooseAndMove|secondary',
    'BowBowControl|secondary',
    'BowDeadAim|secondary',
    'BowBodkin|secondary',
    'BowNockingPoint|secondary',
    'BowQuickAdjustments|secondary',
    'BowRapidFire|secondary',
    'BowStrongBows|secondary',
    'BowSkirmishPhaseMaster|secondary',
    'BowBullsEye|primary',
    'EngineeringImprovedTools|secondary',
    'OneHandedWrappedHandles|secondary',
    'OneHandedDeadlyPurpose|secondary',
    'PolearmCavalry|secondary',
    'PolearmSwiftSwing|secondary',
    'PolearmUnstoppableForce|primary',
    'PolearmUnstoppableForce|secondary',
    'PolearmSharpenTheTip|secondary',
    'RogueryCarver|secondary',
    'ThrowingMountedSkirmisher|secondary',
    'ThrowingKnockOff|secondary',
    'ThrowingSaddlebags|secondary',
    'TwoHandedVandal|secondary'
)
$actualWrong = @($rows | Where-Object { $_.PerkWrong } | ForEach-Object { $_.Key })
foreach ($key in $expectedWrong) {
    if ($actualWrong -notcontains $key) {
        $errors.Add("Expected perk_wrong row is missing: $key")
    }
}
foreach ($key in $actualWrong) {
    if ($expectedWrong -notcontains $key) {
        $errors.Add("Unexpected perk_wrong row: $key")
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Output "ERROR: $_" }
    throw "Perk effect validation failed with $($errors.Count) issue(s)."
}

Write-Output "OK: checked $($rows.Count) perk effect files and $($overrides.Count) overrides."
