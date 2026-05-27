$ErrorActionPreference = 'Stop'

$workspace = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$gameRoot = 'E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord'
$bin = Join-Path $gameRoot 'bin\Win64_Shipping_Client'
$campaignDll = Join-Path $bin 'TaleWorlds.CampaignSystem.dll'
$coreDll = Join-Path $bin 'TaleWorlds.Core.dll'
$outRoot = Join-Path $workspace 'Data\Perk Effects'
$reviewPath = Join-Path $workspace 'Perk Classification Review.md'
$tagIndexPath = Join-Path $workspace 'Tag index.md'

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

function Classify-Effect {
    param([string]$Effect, [string]$Skill, [string]$Role)
    $t = $Effect.ToLowerInvariant()
    $type = 'utility'
    $subtype = ''
    $review = ''

    if ($t -match 'ignore.+shield|penetrate shields|javelins ignore shields') { $type = 'unique'; $subtype = 'shield_bypass' }
    elseif ($t -match 'deflect.*projectile|projectile.*deflect') { $type = 'projectile_protection' }
    elseif ($t -match 'all bows on horseback|mount any bow|long bow|longbow') { $type = 'unique'; $subtype = 'mounted_longbow' }
    elseif ($t -match 'old age|survive') { $type = 'death_avoidance' }
    elseif ($t -match 'enemy wounded|enemy troops recover|enemy casualties') { $type = 'unique'; $subtype = 'enemy_medicine' }
    elseif ($t -match 'uninterrupted|interrupt') { $type = 'unique'; $subtype = 'reload_interrupt_resistance' }
    elseif ($t -match 'upgrade bandit|bandits can be converted') { $type = 'unique'; $subtype = 'bandit_conversion' }
    elseif ($t -match 'surrendering bandit parties can be recruited') { $type = 'unique'; $subtype = 'bandit_recruitment' }
    elseif ($t -match 'settlements?.*barter') { $type = 'unique'; $subtype = 'settlement_barter' }
    elseif ($t -match 'trade in towns while in disguise') { $type = 'unique'; $subtype = 'disguise_trading' }
    elseif ($t -match 'ignore .*knockback resistance') { $type = 'stagger_bonus' }
    elseif ($t -match 'ignore .*knockdown resistance') { $type = 'stagger_bonus' }
    elseif ($t -match 'lance staying couched') { $type = 'unique'; $subtype = 'couched_lance' }
    elseif ($t -match 'pick up arrows|pick up items.*mounted|mounted.*pick') { $type = 'utility'; $subtype = 'mounted_pickup' }
    elseif ($t -match 'handling') {
        $type = 'weapon_handling'
        if ($t -match 'one handed') { $subtype = 'one_handed' }
        elseif ($t -match 'two handed') { $subtype = 'two_handed' }
        elseif ($t -match 'polearm') { $subtype = 'polearm' }
        elseif ($t -match 'bow') { $subtype = 'bow' }
        elseif ($t -match 'crossbow') { $subtype = 'crossbow' }
        elseif ($t -match 'weapon') { $subtype = 'weapon' }
    }
    elseif ($t -match 'maneuvering|top speed to your mount|mount speed') {
        $type = 'mount_performance'
        if ($t -match 'charge damage') { $subtype = 'maneuver_charge' }
        elseif ($t -match 'maneuver') { $subtype = 'maneuver' }
        elseif ($t -match 'speed') { $subtype = 'speed' }
    }
    elseif ($t -match 'mount dying|becoming lame|recover a lame horse|recover mounts|mount when traveling|animals in your party reproducing|tier 2 horses') {
        $type = 'mount_management'
        if ($t -match 'dying|lame') { $subtype = 'mount_recovery' }
        elseif ($t -match 'reproducing|tier 2 horses') { $subtype = 'mount_breeding' }
        elseif ($t -match 'find a mount') { $subtype = 'mount_finding' }
    }
    elseif ($t -match 'carrying capacity|carry capacity') {
        $type = 'carrying_capacity'
        if ($t -match 'pack animals') { $subtype = 'pack_animals' }
        elseif ($t -match 'prisoners') { $subtype = 'prisoners' }
        elseif ($t -match 'troops') { $subtype = 'troops' }
        elseif ($t -match 'party') { $subtype = 'party' }
    }
    elseif ($t -match 'prisoner.*escape|escape chance.*prisoner|prisoner lords escaping|prisoner limit|hero prisoners|escape chance when imprisoned') {
        $type = 'prisoner_management'
        if ($t -match 'limit') { $subtype = 'prisoner_limit' }
        elseif ($t -match 'hero|lords') { $subtype = 'hero_prisoners' }
        elseif ($t -match 'imprisoned') { $subtype = 'personal_escape' }
        else { $subtype = 'prisoner_escape' }
    }
    elseif ($t -match 'prisoner recruitment|recruitment rate.*prisoner|recruitment rate for .*prisoners|faster .*prisoner recruitment') {
        $type = 'prisoner_recruitment'
        if ($t -match 'bandit') { $subtype = 'bandits' }
        elseif ($t -match 'non-bandit') { $subtype = 'non_bandits' }
        elseif ($t -match 'tier 4') { $subtype = 'high_tier' }
        elseif ($t -match 'tier 1|tier 2|tier 3') { $subtype = 'low_tier' }
        elseif ($t -match 'infantry') { $subtype = 'infantry' }
        elseif ($t -match 'ranged') { $subtype = 'ranged' }
    }
    elseif ($t -match 'recruitment slot') {
        $type = 'recruitment_slot'
        if ($t -match 'merchant') { $subtype = 'merchant_notables' }
        elseif ($t -match 'artisan') { $subtype = 'artisan_notables' }
        elseif ($t -match 'gang') { $subtype = 'gang_leaders' }
        elseif ($t -match 'rural') { $subtype = 'rural_notables' }
        elseif ($t -match 'urban') { $subtype = 'urban_notables' }
    }
    elseif ($t -match 'volunteering rate|extra troop from village|troop tiers when recruiting') {
        $type = 'recruitment_bonus'
        if ($t -match 'cavalry') { $subtype = 'cavalry' }
        elseif ($t -match 'village') { $subtype = 'village_notables' }
        elseif ($t -match 'tier') { $subtype = 'troop_tier' }
    }
    elseif ($t -match 'influence gain|influence return|influence per day') { $type = 'influence_gain' }
    elseif ($t -match 'influence cost|influence required') { $type = 'influence_cost_reduction' }
    elseif ($t -match 'persuading lords to defect') { $type = 'persuasion_cost_reduction'; $subtype = 'lord_defection' }
    elseif ($t -match 'barter penalty|bartering for safe passage|barter for safe passage') {
        $type = 'barter_penalty_reduction'
        if ($t -match 'same culture') { $subtype = 'same_culture' }
        elseif ($t -match 'different culture') { $subtype = 'different_culture' }
        elseif ($t -match 'items') { $subtype = 'items' }
        elseif ($t -match 'safe passage') { $subtype = 'safe_passage' }
    }
    elseif ($t -match 'profits are marked|prices are marked|trade rumors') {
        $type = 'trade_info'
        if ($t -match 'profits') { $subtype = 'profit_marking' }
        elseif ($t -match 'prices') { $subtype = 'price_marking' }
        elseif ($t -match 'rumors') { $subtype = 'trade_rumors' }
    }
    elseif ($t -match 'hiring costs|recruitment fees|gold required to recruit') { $type = 'recruit_cost_reduction' }
    elseif ($t -match 'trade penalty|price penalty|sell price penalty|better trade deals|gold required|ransom cost|better deals') {
        $type = 'trade_penalty_reduction'
        if ($t -match '\bmount(?:s|ed)?\b|horses?') { $subtype = 'mounts' }
        elseif ($t -match 'pack animals') { $subtype = 'pack_animals' }
        elseif ($t -match 'food') { $subtype = 'food' }
        elseif ($t -match 'villages') { $subtype = 'villages' }
        elseif ($t -match 'weapons|smithing weapons') { $subtype = 'weapons' }
        elseif ($t -match 'mercenary') { $subtype = 'mercenaries' }
        elseif ($t -match 'ransom') { $subtype = 'ransom' }
        elseif ($t -match 'caravans|villagers') { $subtype = 'caravans_villagers' }
    }
    elseif ($t -match 'loot amount for every skill point') { $type = 'loot_bonus'; $subtype = 'skill_scaling' }
    elseif ($t -match 'more loot|remove negative modifiers on looted items') {
        $type = 'loot_bonus'
        if ($t -match 'negative modifiers') { $subtype = 'item_quality' }
    }
    elseif ($t -match 'raid speed') { $type = 'raid_speed' }
    elseif ($t -match 'extra food.*village raids') { $type = 'food_reserve'; $subtype = 'raid_food' }
    elseif ($t -match 'companion limit') { $type = 'companion_limit' }
    elseif ($t -match 'more likely to have children') { $type = 'fertility' }
    elseif ($t -match 'garrison limit|garrison size') { $type = 'garrison_size' }
    elseif ($t -match 'food reserve') { $type = 'food_reserve' }
    elseif ($t -match 'prebuilt catapult|prebuilt ballista') { $type = 'siege_engines'; $subtype = 'prebuilt' }
    elseif ($t -match 'siege camp preparation speed') { $type = 'siege_camp_speed' }
    elseif ($t -match 'chance from siege bombardments|siege attrition') { $type = 'damage_resistance' }
    elseif ($t -match 'chance of troops getting wounded instead of getting killed|lethal wounds|chance to recover from death|cheat death') { $type = 'death_avoidance' }
    elseif ($t -match 'learning rate of new part designs|crafting stamina recovery rate|stamina spent while|greater chance of creating|produce .* iron|refine .* steel|refine .* iron|thamaskene|charcoal|hardwood') {
        $type = 'crafting_bonus'
        if ($t -match 'learning rate') { $subtype = 'crafting_learning' }
        elseif ($t -match 'stamina') { $subtype = 'crafting_stamina' }
        elseif ($t -match 'chance of creating') { $subtype = 'crafting_quality' }
        elseif ($t -match 'produce|refine|thamaskene|steel|iron|charcoal|hardwood') { $subtype = 'crafting_materials' }
    }
    elseif ($t -match 'crime rating|sneaking into towns|bandits.*surrender|convincing bandits') {
        $type = 'crime_bonus'
        if ($t -match 'crime rating') { $subtype = 'crime_rating' }
        elseif ($t -match 'sneaking') { $subtype = 'sneaking' }
        elseif ($t -match 'surrender|convincing') { $subtype = 'bandit_dialog' }
    }
    elseif ($t -match 'morale penalty.*disorganized state|disorganized state.*morale penalty') { $type = 'morale_bonus'; $subtype = 'disorganized_state' }
    elseif ($t -match 'disorganized state|troops left behind|breaking into or out|break into or out') {
        $type = 'battle_escape'
        if ($t -match 'disorganized') { $subtype = 'disorganized_state' }
        elseif ($t -match 'left behind') { $subtype = 'troops_left_behind' }
        elseif ($t -match 'breaking into or out|break into or out') { $subtype = 'siege_breakthrough' }
    }
    elseif ($t -match 'hideout crew') { $type = 'party_size'; $subtype = 'hideout' }
    elseif ($t -match 'hideout detection') { $type = 'party_vision'; $subtype = 'hideout' }
    elseif ($t -match 'advantage against bandits') { $type = 'simulation_bonus'; $subtype = 'bandits' }
    elseif ($t -match 'fortification bonus') { $type = 'simulation_bonus'; $subtype = 'fortification_bonus' }
    elseif ($t -match 'betting allowed') { $type = 'utility'; $subtype = 'tournament_betting' }
    elseif ($t -match 'stun duration|stun your enemies longer') { $type = 'stagger_bonus'; $subtype = 'stun_duration' }
    elseif ($t -match 'staggered while reloading') { $type = 'stagger_bonus'; $subtype = 'reload' }
    elseif ($t -match 'reload any crossbow on horseback') { $type = 'unique'; $subtype = 'mounted_crossbow_reload' }
    elseif ($t -match 'blocking projectiles from behind') { $type = 'projectile_protection'; $subtype = 'rear_shield' }
    elseif ($t -match 'penetrate shields') { $type = 'unique'; $subtype = 'shields' }
    elseif ($t -match 'zoom with (bows|crossbows)') { $type = 'ranged_accuracy'; $subtype = 'zoom' }
    elseif ($t -match 'zoom with throwing') { $type = 'ranged_accuracy'; $subtype = 'zoom' }
    elseif ($t -match 'draw speed with throwing') { $type = 'reload_speed'; $subtype = 'throwing' }
    elseif ($t -match 'accuracy penalty.*throwing weapons while mounted') { $type = 'ranged_accuracy'; $subtype = 'mounted' }
    elseif ($t -match 'travel speed to .*throwing weapons') { $type = 'projectile_speed'; $subtype = 'throwing' }
    elseif ($t -match 'ignore armors? below') { $type = 'damage_increase'; $subtype = 'armor_penetration' }
    elseif ($t -match 'sling weapons can penetrate head armor') { $type = 'damage_increase'; $subtype = 'armor_penetration' }
    elseif ($t -match 'chance to die when you fall unconscious') { $type = 'death_avoidance'; $subtype = 'combat_death_save' }
    elseif ($t -match 'denar return') { $type = 'income_increase'; $subtype = 'compensation' }
    elseif ($t -match 'experience per day|skill experience|experience from battles|donated .*experience') { $type = 'experience_gain' }
    elseif ($t -match 'tax income for each skill point') { $type = 'income_increase'; $subtype = 'skill_scaling' }
    elseif ($t -match 'gold per day') { $type = 'income_increase' }
    elseif ($t -match 'costs of recruiting minor faction clans') { $type = 'recruit_cost_reduction'; $subtype = 'minor_faction_clans' }
    elseif ($t -match 'militias will spawn as veteran') { $type = 'militia_quality'; $subtype = 'veteran_spawn' }
    elseif ($t -match 'clan party limit') { $type = 'clan_party_limit' }
    elseif ($t -match 'siege engine build speed.*militia') { $type = 'project_speed'; $subtype = 'militia_scaling' }
    elseif ($t -match 'equipped (bows|crossbows) do not slow you down') { $type = 'movement_speed'; $subtype = 'weapon_slowdown' }
    elseif ($t -match 'overburden|herding speed penalty') {
        $type = 'party_speed'
        if ($t -match 'overburden') { $subtype = 'overburden' }
        elseif ($t -match 'herding') { $subtype = 'herding' }
    }
    elseif ($t -match 'shield hitpoints|shield hit points') { $type = 'shield_durability' }
    elseif ($t -match 'siege bombardment casualties') { $type = 'siege_engines'; $subtype = 'bombardment' }
    elseif ($t -match 'damage to your shields?|damage to shields of') { $type = 'shield_durability' }
    elseif ($t -match 'shield protection area') { $type = 'projectile_protection' }
    elseif ($t -match 'damage taken|damage to you|less damage|damage reduced|damage reduction|reduced.*damage') {
        $type = 'damage_resistance'
        if ($t -match 'sent to confront') { $subtype = 'auto_resolve' }
        elseif ($t -match 'ranged|projectile|arrow|bolt') { $subtype = 'ranged' }
        elseif ($t -match 'melee') { $subtype = 'melee' }
        elseif ($t -match 'charge') { $subtype = 'charge' }
        elseif ($t -match 'fall') { $subtype = 'fall' }
        else { $subtype = 'all' }
    }
    elseif ($t -match 'charge damage') { $type = 'damage_increase'; $subtype = 'charge' }
    elseif ($t -match 'damage bonus from speed') { $type = 'damage_increase'; $subtype = 'speed_bonus' }
    elseif ($t -match 'armor penetration') { $type = 'damage_increase'; $subtype = 'armor_penetration' }
    elseif ($t -match 'damage') {
        $type = 'damage_increase'
        if ($t -match 'sent to confront') { $subtype = 'auto_resolve' }
        elseif ($t -match 'siege bombardment|during siege bombardment|damage dealt to walls') { $subtype = 'siege_engines' }
        elseif ($t -match 'siege engines') { $subtype = 'siege_engines' }
        elseif ($t -match 'destructible') { $subtype = 'destructible_objects' }
        elseif ($t -match 'without a shield') { $subtype = 'no_shield' }
        elseif ($t -match 'shield') { $subtype = 'shields' }
        elseif ($t -match 'as melee|mounted melee') { $subtype = 'melee' }
        elseif ($t -match 'ranged damage while mounted|mounted archers') { $subtype = 'ranged' }
        elseif ($t -match 'swing damage|thrust damage') { $subtype = 'melee' }
        elseif ($t -match 'while mounted|by mounted troops') {
            if ($t -match 'throwing') { $subtype = 'mounted_throwing' }
            elseif ($t -match 'ranged|bow|crossbow') { $subtype = 'mounted_ranged' }
            elseif ($t -match 'melee') { $subtype = 'mounted_melee' }
            else { $subtype = 'mounted' }
        }
        elseif ($t -match 'mount') { $subtype = 'mounts' }
        elseif ($t -match 'ranged|bow|crossbow|throwing') {
            if ($t -match 'crossbow') { $subtype = 'crossbow' }
            elseif ($t -match 'bow') { $subtype = 'bow' }
            elseif ($t -match 'throwing|javelin') { $subtype = 'throwing' }
            else { $subtype = 'ranged' }
        }
        elseif ($t -match 'one handed') { $subtype = 'one_handed' }
        elseif ($t -match 'two handed') { $subtype = 'two_handed' }
        elseif ($t -match 'polearm') { $subtype = 'polearm' }
        elseif ($t -match 'destructible') { $subtype = 'destructible_objects' }
        elseif ($t -match '\bmelee\b') { $subtype = 'melee' }
        else { $subtype = 'weapon' }
    }
    elseif ($t -match 'movement speed penalty') { $type = 'movement_speed' }
    elseif ($t -match 'swing speed|attack speed') {
        $type = 'attack_speed'
        if ($t -match 'one handed') { $subtype = 'one_handed' }
        elseif ($t -match 'two handed') { $subtype = 'two_handed' }
        elseif ($t -match 'polearm') { $subtype = 'polearm' }
        elseif ($t -match 'melee') { $subtype = 'melee' }
    }
    elseif ($t -match 'reload') {
        $type = 'reload_speed'
        if ($t -match 'crossbow') { $subtype = 'crossbow' }
        elseif ($t -match 'bow') { $subtype = 'bow' }
        elseif ($t -match 'siege') { $subtype = 'siege' }
    }
    elseif ($t -match 'missile speed|projectile speed|throwing weapon speed') {
        $type = 'projectile_speed'
        if ($t -match 'throw') { $subtype = 'throwing' }
        elseif ($t -match 'bow') { $subtype = 'bow' }
        elseif ($t -match 'crossbow') { $subtype = 'crossbow' }
    }
    elseif ($t -match 'movement speed|speed on foot|faster on foot|combat movement') {
        $type = 'movement_speed'
        if ($t -match 'armor') { $subtype = 'armor_weight' }
        elseif ($t -match 'shield') { $subtype = 'shield_penalty' }
        elseif ($t -match 'foot|on foot') { $subtype = 'foot' }
        elseif ($t -match 'combat') { $subtype = 'combat' }
    }
    elseif ($t -match 'party speed|map speed|travel speed') {
        $type = 'party_speed'
        if ($t -match 'forest|desert|snow|steppe|terrain|plains') { $subtype = 'terrain' }
    }
    elseif ($t -match 'hit point regeneration|healing rate|recovery rate') { $type = 'regen_bonus' }
    elseif ($t -match 'hit point|hit points|hp') { $type = 'hit_points' }
    elseif ($t -match 'armor weight') { $type = 'utility' }
    elseif ($t -match 'discarded armors.*experience|donated armors.*experience') { $type = 'experience_gain' }
    elseif ($t -match 'armor') { $type = 'armor_increase' }
    elseif ($t -match 'ammo|ammunition|arrows? per quiver|bolts? per quiver|extra arrows|extra arrow|extra bolts|extra bolt|throwing weapons') { $type = 'ammo_capacity' }
    elseif ($t -match 'accuracy|aim|spread') { $type = 'ranged_accuracy' }
    elseif ($t -match 'skill') { $type = 'skill_increase' }
    elseif ($t -match 'focus point') { $type = 'focus_increase' }
    elseif ($t -match 'attribute point|vigor|control|endurance|cunning|social|intelligence') { $type = 'attribute_increase' }
    elseif ($t -match 'morale loss|morale damage|morale penalty to enemies|battle morale penalty to enemies|morale effect to enemy') { $type = 'morale_damage' }
    elseif ($t -match 'morale') { $type = 'morale_bonus' }
    elseif ($t -match 'renown') { $type = 'renown_bonus' }
    elseif ($t -match 'relation|relationship') { $type = 'relationship_gain' }
    elseif ($t -match 'experience|xp') { $type = 'experience_gain' }
    elseif ($t -match 'wage|wages|upkeep') { $type = 'upkeep_reduction' }
    elseif ($t -match 'recruit.*cost|recruitment cost') { $type = 'recruit_cost_reduction' }
    elseif ($t -match 'upgrade cost') { $type = 'upgrade_cost_reduction' }
    elseif ($t -match 'party size|party limit') { $type = 'party_size' }
    elseif ($t -match 'sight|spotting|track|visual range') { $type = 'party_vision' }
    elseif ($t -match 'food consumption') { $type = 'food_consumption' }
    elseif ($t -match 'hearth') { $type = 'hearth_growth' }
    elseif ($t -match 'loyalty') { $type = 'loyalty_increase' }
    elseif ($t -match 'security') { $type = 'security' }
    elseif ($t -match 'militia') { $type = 'militia_increase' }
    elseif ($t -match 'prosperity') { $type = 'prosperity_bonus' }
    elseif ($t -match 'income|tariff|tax|gold for each') { $type = 'income_increase' }
    elseif ($t -match 'effect from forums|effect from.*marketplaces|effect from.*festivals|effect from boosting projects|project effects|effectiveness to continuous projects|town project effects') { $type = 'project_effect' }
    elseif ($t -match 'construction|project') { $type = 'project_speed' }
    elseif ($t -match 'production') { $type = 'production_output' }
    elseif ($t -match 'healing|wounded|recovery|recover') { $type = 'regen_bonus' }
    elseif ($t -match 'food item.*smuggled') { $type = 'food_reserve'; $subtype = 'smuggling' }
    elseif ($t -match 'siege engine|siege engines|siege equipment') { $type = 'siege_engines' }
    elseif ($t -match 'simulation') { $type = 'simulation_bonus' }
    elseif ($t -match 'stagger') { $type = 'stagger_bonus' }
    elseif ($t -match 'dismount') { $type = 'dismount' }
    elseif ($t -match 'death') { $type = 'death_avoidance' }
    elseif ($t -match 'dialog|persuasion') { $type = 'dialog_checks_bonus' }
    elseif ($t -match 'cohesion') { $type = 'cohesion_bonus' }

    if ($type -eq 'utility' -and $subtype -ne 'tournament_betting' -and $t -match 'ignore|unlock|allow|never|can now') {
        $review = 'Check whether this should be unique instead of utility.'
    }
    if ($type -eq 'utility' -and $t -match '^\s*[+-]?\d') {
        $review = 'Numeric utility effect may deserve a more specific perk_type.'
    }
    if ($type -eq 'damage_increase' -and $subtype -eq '') {
        $review = 'Damage effect needs a useful subtype if the condition/source matters.'
    }
    if ($t -match 'morale and renown|food consumption, wages and .*morale loss') {
        $review = 'Composite effect spans multiple classification categories.'
    }
    if ($t -match 'renown and influence|relationship.*loyalty|companion wages.*recruitment fees|wages.*upgrade costs|damage.*movement speed|fall damage.*kick damage|damage.*stun duration|charge damage.*maneuvering') {
        $review = 'Composite effect spans multiple classification categories.'
    }
    if ($t -match 'outnumbered') {
        $review = 'Outnumbered condition is not represented by current trigger_condition taxonomy.'
    }
    if ($t -match 'ransom cost') {
        $review = 'Ransom-cost reduction is not really a trade penalty; current subtype is a lossy fallback unless a ransom-cost subtype is added.'
    }
    [pscustomobject]@{ Type = $type; Subtype = $subtype; Review = $review }
}

function Normalize-Classification {
    param(
        [string]$Type,
        [string]$Subtype,
        [string]$Skill
    )

    if ([string]::IsNullOrWhiteSpace($Subtype)) {
        return [pscustomobject]@{ Type = $Type; Subtype = '' }
    }

    if ($Type -eq 'unique') {
        $uniqueSubtype = if ($Subtype -eq 'shields') { 'shields' } else { '' }
        return [pscustomobject]@{ Type = $Type; Subtype = $uniqueSubtype }
    }

    $skillSubtypeMap = @{
        'One Handed' = 'one_handed'
        'Two Handed' = 'two_handed'
        'Polearm' = 'polearm'
        'Bow' = 'bow'
        'Crossbow' = 'crossbow'
        'Throwing' = 'throwing'
    }
    if ($skillSubtypeMap.ContainsKey($Skill) -and $skillSubtypeMap[$Skill] -eq $Subtype) {
        return [pscustomobject]@{ Type = $Type; Subtype = '' }
    }

    $reusableSubtypesByType = @{
        'crafting_bonus' = @('crafting_learning', 'crafting_materials', 'crafting_quality', 'crafting_stamina')
        'damage_increase' = @('armor_penetration', 'charge', 'melee', 'mounts', 'ranged', 'shields', 'siege', 'siege_engines', 'speed_bonus')
        'damage_resistance' = @('charge', 'fall', 'ranged')
        'movement_speed' = @('combat', 'shield_penalty')
        'party_speed' = @('overburden', 'terrain')
        'prisoner_management' = @('hero_prisoners', 'prisoner_escape', 'prisoner_limit')
        'prisoner_recruitment' = @('bandits')
        'trade_info' = @('price_marking', 'profit_marking', 'trade_rumors')
        'simulation_bonus' = @('fortification_bonus')
        'trade_penalty_reduction' = @('food', 'mounts', 'ransom', 'weapons')
    }
    if ($reusableSubtypesByType.ContainsKey($Type) -and $reusableSubtypesByType[$Type] -contains $Subtype) {
        return [pscustomobject]@{ Type = $Type; Subtype = $Subtype }
    }

    [pscustomobject]@{ Type = $Type; Subtype = '' }
}

function Convert-ToReadableLabel {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) { return '' }
    ($Value -replace '_', ' ').Trim()
}

function Add-UniqueListValue {
    param(
        [System.Collections.Generic.List[string]]$List,
        [string]$Value
    )
    if ([string]::IsNullOrWhiteSpace($Value)) { return }
    $clean = $Value.Trim()
    if (-not $List.Contains($clean)) {
        [void]$List.Add($clean)
    }
}

function Get-ReadableMechanic {
    param([string]$Type)
    $map = @{
        'attribute_increase' = 'attribute point'
        'barter_penalty_reduction' = 'barter'
        'clan_party_limit' = 'clan party limit'
        'cohesion_bonus' = 'cohesion'
        'companion_limit' = 'companion limit'
        'dialog_checks_bonus' = 'dialog checks'
        'experience_gain' = 'experience gain'
        'focus_increase' = 'focus point'
        'food_consumption' = 'food consumption'
        'food_reserve' = 'food reserve'
        'garrison_size' = 'garrison size'
        'hearth_growth' = 'hearth growth'
        'income_increase' = 'income'
        'influence_cost_reduction' = 'influence cost'
        'influence_gain' = 'influence'
        'loyalty_increase' = 'loyalty'
        'militia_increase' = 'militia gain'
        'militia_quality' = 'militia quality'
        'morale_bonus' = 'morale'
        'party_size' = 'party size'
        'party_speed' = 'party speed'
        'persuasion_cost_reduction' = 'persuasion cost'
        'prisoner_management' = 'prisoners'
        'prisoner_recruitment' = 'prisoner recruitment'
        'project_effect' = 'project effect'
        'project_speed' = 'build speed'
        'prosperity_bonus' = 'prosperity'
        'production_output' = 'production'
        'raid_speed' = 'raid speed'
        'recruit_cost_reduction' = 'recruitment cost'
        'recruitment_bonus' = 'recruitment bonus'
        'recruitment_slot' = 'recruitment slot'
        'relationship_gain' = 'relationship'
        'renown_bonus' = 'renown'
        'siege_camp_speed' = 'siege camp speed'
        'simulation_bonus' = 'simulation bonus'
        'skill_increase' = 'skill bonus'
        'trade_info' = 'trade info'
        'trade_penalty_reduction' = 'trade penalty reduction'
        'upgrade_cost_reduction' = 'upgrade cost'
        'upkeep_reduction' = 'wages'
    }
    if ($map.ContainsKey($Type)) { return $map[$Type] }
    Convert-ToReadableLabel $Type
}

function Get-TriggerConditions {
    param([string]$Effect)
    $t = $Effect.ToLowerInvariant()
    $conditions = New-Object 'System.Collections.Generic.List[string]'

    if ($t -match 'siege|besieging|besieged|bombardment|sally out') { Add-UniqueListValue $conditions 'during siege' }
    if ($t -match 'while waiting|waiting in|resting in settlements?|stationary on campaign map|stationary for at least') { Add-UniqueListValue $conditions 'while waiting' }
    if ($t -match 'while traveling|when traveling|traveling through|when moving|moving on campaign map' -or ($t -match 'travel speed' -and $t -notmatch 'throwing weapons?|projectile|missile|javelins?')) { Add-UniqueListValue $conditions 'while traveling' }
    if ($t -match 'sent to confront|sent as attackers|sent to sally out') { Add-UniqueListValue $conditions 'simulation' }
    if ($t -match 'desert|dunes|forest|forests|steppe|steppes|plains|snowy|terrain') { Add-UniqueListValue $conditions 'terrain' }
    if ($t -match 'after every battle|after a battle|after battle|after battles|from victories|at the end of the battle|battle is over|battles won|winning battles|winning sieges|when an enemy lord is defeated') { Add-UniqueListValue $conditions 'after battle' }
    if ($t -match 'continuous project|while building a project|when a project is finished|project is finished|boosting projects|build speed.*projects?') { Add-UniqueListValue $conditions 'project active' }
    if ($t -match 'same culture|own culture') { Add-UniqueListValue $conditions 'same culture' }
    if ($t -match 'different culture|different cultures') { Add-UniqueListValue $conditions 'different culture' }
    if ($t -match 'own kingdom|your kingdom') { Add-UniqueListValue $conditions 'own kingdom' }
    if ($t -match 'morale .*higher|morale higher|morale .*above') { Add-UniqueListValue $conditions 'morale threshold' }
    if ($t -match 'composed of|less than \d+ soldiers|foot troops|your infantry|footmen on horses|infantry troops|ranged troops|melee troops|mounted troops|cavalry troops|bandit units|bandit troops|garrisoned cavalry|tier \d\+? (?:troops|units|recruits|prisoners|bandits|infantry|cavalry|archers)' -or ($t -match '(?:archers|infantry|cavalry|mounted troops|ranged troops|melee troops|bandits|bandit prisoners|bandit troops|mercenary troops?|troops|units|recruits|prisoners)' -and $t -match '(?:in your party|in your formation|in the formation|under your formation|garrisoned|of your party|of the party)')) { Add-UniqueListValue $conditions 'party composition' }
    if ($t -match 'governed settlement|governed town|governed castle|villages bound|bound villages|governed by your clan') { Add-UniqueListValue $conditions 'governed settlement' }
    if ($t -match 'for every skill point above|for each .*point above|skill point over|above 200|above 250|above 275') { Add-UniqueListValue $conditions 'over skill cap' }
    if ($t -match 'while mounted|when you start a battle mounted|on horseback|horseback') { Add-UniqueListValue $conditions 'while mounted' }
    if ($t -match 'on foot|while on foot') { Add-UniqueListValue $conditions 'on foot' }
    if ($t -match 'more than 90%.*hit points|less than half.*hit points') { Add-UniqueListValue $conditions 'health threshold' }
    if ($t -match 'for each enemy you kill|when you kill|kill an enemy|after a kill|with .* kills|kills? by') { Add-UniqueListValue $conditions 'on kill' }
    if ($t -match 'when attacking|sent as attackers|attacking enemy|offensive battle') { Add-UniqueListValue $conditions 'attacking' }
    if ($t -match 'when defending|defending at|while defending|defending in|being attacked') { Add-UniqueListValue $conditions 'defending' }

    @($conditions.ToArray())
}

function Get-EffectTags {
    param(
        [string]$Effect,
        [string]$OldSubtype,
        [string]$NewType,
        [string]$NewSubtype,
        [object[]]$TriggerConditions
    )
    $t = $Effect.ToLowerInvariant()
    $tags = New-Object 'System.Collections.Generic.List[string]'

    if (-not [string]::IsNullOrWhiteSpace($OldSubtype)) {
        Add-UniqueListValue $tags (Convert-ToReadableLabel $OldSubtype)
    }
    if ($NewType -eq 'settlement defense' -or $t -match 'security|militia|garrison|fortification|besieged governed settlement|governed settlement.*under siege') { Add-UniqueListValue $tags 'defense' }
    if ($t -match 'food|grain|olives|fish|date|starv') { Add-UniqueListValue $tags 'food' }
    if ($t -match 'militia|militias') { Add-UniqueListValue $tags 'militia' }
    if ($t -match 'garrison|garrisoned') { Add-UniqueListValue $tags 'garrison' }
    if ($t -match 'fortifications?|castle|barrack|(?:settlement|town|castle|siege|defensive) walls?') { Add-UniqueListValue $tags 'fortifications' }
    if ($t -match 'build speed|construction speed|build rate|siege engine build speed') { Add-UniqueListValue $tags 'build speed' }
    if ($t -match 'tax') { Add-UniqueListValue $tags 'tax' }
    if ($t -match 'tariff') { Add-UniqueListValue $tags 'tariff' }
    if ($t -match 'workshop|workshops') { Add-UniqueListValue $tags 'workshop' }
    if ($t -match 'caravan|caravans') { Add-UniqueListValue $tags 'caravan' }
    if ($t -match 'village|villages|villager|villagers') { Add-UniqueListValue $tags 'village' }
    if ($t -match 'wages|paid wages') { Add-UniqueListValue $tags 'wages' }
    if ($t -match 'recruitment cost|recruitment fees|hiring costs|costs? of recruiting|gold required to recruit') { Add-UniqueListValue $tags 'recruitment cost' }
    if ($t -match 'upgrade cost|upgrade costs') { Add-UniqueListValue $tags 'upgrade cost' }
    if ($t -match 'ransom') { Add-UniqueListValue $tags 'ransom' }
    if ($t -match 'weapon|weapons|swords?|axes?|maces?|javelins?|polearms?') { Add-UniqueListValue $tags 'weapons' }
    if ($t -match '\bmount(?:s|ed)?\b|horses?|cavalry|pack animals') { Add-UniqueListValue $tags 'mounts' }
    if ($t -match 'prisoner|prisoners|imprisoned') { Add-UniqueListValue $tags 'prisoners' }
    if ($t -match 'escape chance|chance to escape|prisoners? escape') { Add-UniqueListValue $tags 'prisoner escape' }
    if ($t -match 'bandit|bandits') { Add-UniqueListValue $tags 'bandits' }
    if ($t -match 'companion|companions') { Add-UniqueListValue $tags 'companions' }
    if ($t -match 'loot|looted') { Add-UniqueListValue $tags 'loot' }
    if ($t -match 'overburden') { Add-UniqueListValue $tags 'overburden' }
    if ($t -match 'barter') { Add-UniqueListValue $tags 'barter' }
    if ($t -match 'trade|price|profits?|deals') { Add-UniqueListValue $tags 'trade' }
    if ($t -match '\bprojects?\b|while building a project|boosting projects|project is finished') { Add-UniqueListValue $tags 'projects' }
    if ($t -match 'combat movement|in combat') { Add-UniqueListValue $tags 'combat' }

    $clean = New-Object 'System.Collections.Generic.List[string]'
    foreach ($tag in $tags) {
        if ($tag -eq $NewType -or $tag -eq $NewSubtype) { continue }
        if ($TriggerConditions -contains $tag) { continue }
        Add-UniqueListValue $clean $tag
    }
    @($clean.ToArray())
}

function Get-ReadableFacets {
    param(
        [string]$Type,
        [string]$Subtype,
        [string]$Effect,
        [string]$Role
    )

    $t = $Effect.ToLowerInvariant()
    $newType = Convert-ToReadableLabel $Type
    $newSubtype = if ($Type -eq 'unique') { '' } elseif (-not [string]::IsNullOrWhiteSpace($Subtype)) { Convert-ToReadableLabel $Subtype } else { '' }
    $social = @('relationship_gain', 'renown_bonus', 'dialog_checks_bonus', 'fertility')
    $partyManagement = @('clan_party_limit', 'companion_limit', 'carrying_capacity', 'morale_bonus', 'party_size', 'party_speed', 'prisoner_management', 'prisoner_recruitment', 'recruitment_bonus', 'recruitment_slot', 'raid_speed')
    $goldEconomy = @('barter_penalty_reduction', 'loot_bonus', 'persuasion_cost_reduction', 'recruit_cost_reduction', 'trade_info', 'trade_penalty_reduction', 'upgrade_cost_reduction', 'upkeep_reduction')
    $settlementEconomy = @('hearth_growth', 'production_output', 'prosperity_bonus')
    $settlementDefense = @('garrison_size', 'militia_increase', 'militia_quality', 'security')
    $settlementGovernance = @('loyalty_increase', 'project_effect')
    $characterGrowth = @('attribute_increase', 'focus_increase', 'skill_increase')
    $armyManagement = @('cohesion_bonus', 'influence_cost_reduction', 'influence_gain')
    $movement = @('movement_speed', 'mount_performance')
    $siege = @('siege_camp_speed', 'siege_engines')

    if ($social -contains $Type) {
        $newType = 'social'
        $newSubtype = Get-ReadableMechanic $Type
    } elseif ($Type -eq 'experience_gain') {
        if ($t -match 'companions|party member|clan member|hero') {
            $newType = 'character growth'
            $newSubtype = 'experience gain'
        } elseif ($Role -eq 'governor' -and $t -match 'garrison|governed settlement') {
            $newType = 'settlement defense'
            $newSubtype = 'troop xp'
        } else {
            $newType = 'party management'
            $newSubtype = 'troop xp'
        }
    } elseif ($Type -eq 'skill_increase' -and $t -match 'troops?|infantry|archers|cavalry|formation|garrison') {
        $newType = 'troop combat'
        $newSubtype = 'skill bonus'
    } elseif ($characterGrowth -contains $Type) {
        $newType = 'character growth'
        $newSubtype = Get-ReadableMechanic $Type
    } elseif ($armyManagement -contains $Type) {
        $newType = 'army management'
        $newSubtype = Get-ReadableMechanic $Type
    } elseif ($Type -eq 'party_size' -and $Role -eq 'governor' -and $t -match 'villager|village') {
        $newType = 'settlement economy'
        $newSubtype = 'party size'
    } elseif ($partyManagement -contains $Type) {
        $newType = 'party management'
        $newSubtype = Get-ReadableMechanic $Type
    } elseif ($goldEconomy -contains $Type) {
        $newType = 'gold economy'
        $newSubtype = Get-ReadableMechanic $Type
    } elseif ($settlementEconomy -contains $Type) {
        $newType = 'settlement economy'
        $newSubtype = Get-ReadableMechanic $Type
    } elseif ($settlementDefense -contains $Type) {
        $newType = 'settlement defense'
        $newSubtype = Get-ReadableMechanic $Type
    } elseif ($settlementGovernance -contains $Type) {
        $newType = 'settlement governance'
        $newSubtype = Get-ReadableMechanic $Type
    } elseif ($movement -contains $Type) {
        $newType = 'movement'
        $newSubtype = Get-ReadableMechanic $Type
    } elseif ($siege -contains $Type) {
        $newType = 'siege'
        $newSubtype = Get-ReadableMechanic $Type
    } elseif ($Type -eq 'income_increase') {
        if ($Role -eq 'governor') {
            $newType = 'settlement economy'
            $newSubtype = 'settlement income'
        } else {
            $newType = 'gold economy'
            $newSubtype = 'income'
        }
    } elseif ($Type -eq 'food_reserve') {
        if ($Role -eq 'governor') {
            $newType = 'settlement defense'
        } else {
            $newType = 'party management'
        }
        $newSubtype = 'food reserve'
    } elseif ($Type -eq 'food_consumption') {
        if ($Role -eq 'governor' -and $t -match 'town population') {
            $newType = 'settlement economy'
        } elseif ($Role -eq 'governor') {
            $newType = 'settlement defense'
        } else {
            $newType = 'party management'
        }
        $newSubtype = 'food consumption'
    } elseif ($Type -eq 'project_speed') {
        if ($t -match 'fortification|military|castle|siege engine|militia|barrack|walls?') {
            $newType = 'settlement defense'
        } else {
            $newType = 'settlement governance'
        }
        $newSubtype = 'build speed'
    } elseif ($Type -eq 'simulation_bonus' -and $Role -eq 'governor') {
        $newType = 'settlement defense'
        $newSubtype = 'fortification bonus'
    }

    $combatMechanicTypes = @(
        'ammo capacity',
        'armor increase',
        'attack speed',
        'damage increase',
        'damage resistance',
        'dismount',
        'hit points',
        'morale damage',
        'projectile protection',
        'projectile speed',
        'ranged accuracy',
        'reload speed',
        'shield durability',
        'stagger bonus',
        'weapon handling'
    )
    $combatMechanic = ''
    if ($combatMechanicTypes -contains $newType) {
        $combatMechanic = $newType
    } elseif ($newType -eq 'party management' -and $newSubtype -eq 'morale' -and $t -match 'battle morale effect to (friendly|enemy) troops') {
        $combatMechanic = 'morale'
    } elseif ($newType -eq 'movement' -and $newSubtype -eq 'movement speed' -and $t -notmatch 'campaign map|travel speed|party speed') {
        $combatMechanic = 'movement speed'
    } elseif ($newType -eq 'mount management' -and $newSubtype -eq 'mount performance') {
        $combatMechanic = 'mount performance'
    }

    if ($combatMechanic) {
        $combatSubtype = if ([string]::IsNullOrWhiteSpace($newSubtype)) { $combatMechanic } else { $newSubtype }
        $troopCombat = ($Role -eq 'captain') -or
            ($t -match '(?:troops?|infantry|archers|cavalry|mounted troops|ranged troops|melee troops|foot troops|formation|garrison|militia)' -and $t -match '(?:in your party|in your formation|under your formation|in the formation|garrison|governed settlement|friendly troops|enemy troops|by troops|to troops|of troops)')
        $personalCombat = ($Role -in @('personal', 'player')) -or
            ($t -match '\byou\b|your attacks|your .*kills|your throwing weapons|your shields?|with your')

        $personalRoleTroopEffect = $t -match 'battle morale effect to (friendly|enemy) troops'

        if ($troopCombat -and (-not ($Role -in @('personal', 'player')) -or $personalRoleTroopEffect)) {
            $newType = 'troop combat'
            $newSubtype = $combatSubtype
        } elseif ($personalCombat) {
            $newType = 'personal combat'
            $newSubtype = $combatSubtype
        }
    }

    $triggers = @(Get-TriggerConditions -Effect $Effect)
    if ($Role -eq 'governor' -and $newType -match '^settlement ') {
        Add-UniqueListValue $triggers 'governed settlement'
    }
    $tags = @(Get-EffectTags -Effect $Effect -OldSubtype $Subtype -NewType $newType -NewSubtype $newSubtype -TriggerConditions $triggers)

    [pscustomobject]@{
        Type = $newType
        Subtype = $newSubtype
        TriggerCondition = $triggers
        EffectTags = $tags
    }
}

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

    if ($Perk.StringId -eq 'BowTrainer' -and $Slot -eq 'primary') {
        $perkWrong = $true
        $notes = 'Party member wording likely targets hero party members (companions/family/main hero if lowest Bow); game bonus is +6 but description has no numeric placeholder.'
    } elseif ($Perk.StringId -eq 'TradeLocalConnection' -and $Slot -eq 'primary') {
        $perkWrong = $true
        $notes = 'Description says double relationship gain, but game increment_type is add while paired Distributed Goods uses add_factor.'
    } elseif ($Perk.StringId -eq 'RogueryArmsDealer' -and $Slot -eq 'secondary') {
        $perkWrong = $true
        $notes = 'Description renders as 200% militia per day, but game increment_type is add with bonus 2.'
    } elseif ($Perk.StringId -eq 'ThrowingSplinters' -and $Slot -eq 'primary') {
        $perkWrong = $true
        $notes = 'Description says triple shield damage, but bonus 3 with add_factor appears to apply +300% damage, or 4x total, unless this path treats the factor as a direct multiplier.'
    } elseif ($Perk.StringId -eq 'TacticsGensdarmes' -and $Slot -eq 'primary') {
        $perkWrong = $true
        $notes = 'Game troop_usage is ranged, but description says cavalry troops in formation; likely value/description mismatch.'
    } elseif ($Perk.StringId -eq 'TwoHandedOnTheEdge' -and $Slot -eq 'secondary') {
        $perkWrong = $true
        $notes = 'Game troop_usage includes cavalry, but description says swing speed to infantry in your formation.'
    } elseif ($Perk.StringId -eq 'LegendarySmith' -and $Slot -eq 'primary') {
        $notes = 'Bonus stores the base +5% Legendary chance; description also includes +1% per 5 Smithing above 275.'
    } elseif ($effect -match 'part of an army') {
        $notes = 'Applies only while the party is part of an army; no dedicated army-membership trigger condition exists.'
    } elseif ($effect -match 'village raids') {
        $notes = 'Applies when taking food during village raids; no dedicated raid trigger condition exists.'
    }

    if ($Perk.StringId -eq 'TacticsImproviser' -and $Slot -eq 'primary') {
        $classificationReview = 'Effect removes morale penalty from disorganized state; battle escape is only an indirect source of the state.'
    } elseif ($effect -match 'Control skills of infantry.*Vigor skills of archers') {
        $classificationReview = 'Troop skill bonus spans infantry Control and archer Vigor; not hero character growth.'
    } elseif ($effect -match 'wages.*upgrade costs.*mercenary troops') {
        $classificationReview = 'Composite effect spans wages and upgrade costs for mercenary troops; single classification is partial.'
    } elseif ($effect -match 'companion wages.*recruitment fees') {
        $classificationReview = 'Composite effect spans companion wages and recruitment fees; single classification is partial.'
    }
    [pscustomobject]@{
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
}

function Write-EffectNote {
    param($Row, [int]$DuplicateIndex)
    $skillDir = Join-Path $outRoot (Safe-FilePart $Row.Skill)
    if (-not (Test-Path -LiteralPath $skillDir)) {
        New-Item -ItemType Directory -Path $skillDir | Out-Null
    }
    $sub = if ($Row.PerkSubtype) { " - $($Row.PerkSubtype)" } else { '' }
    $dup = if ($DuplicateIndex -gt 1) { " - $DuplicateIndex" } else { '' }
    $fileName = '{0:000} - {1} - {2} - {3}{4}{5}.md' -f $Row.Level, (Safe-FilePart $Row.Perk), $Row.Role, $Row.PerkType, $sub, $dup
    $path = Join-Path $skillDir $fileName
    $lines = @(
        '---'
        "project: $(Escape-Yaml $Row.Project)"
        "type: $(Escape-Yaml $Row.Type)"
        "game_version_target: $(Escape-Yaml $Row.GameVersionTarget)"
        "attribute: $(Escape-Yaml $Row.Attribute)"
        "skill: $(Escape-Yaml $Row.Skill)"
        "level: $($Row.Level)"
        "perk: $(Escape-Yaml $Row.Perk)"
        "perk_string_id: $(Escape-Yaml $Row.PerkStringId)"
        "effect_slot: $(Escape-Yaml $Row.EffectSlot)"
        "role: $(Escape-Yaml $Row.Role)"
        "role_value: $($Row.RoleValue)"
        "perk_type: $(Escape-Yaml $Row.PerkType)"
        "perk_subtype: $(Escape-Yaml $Row.PerkSubtype)"
        (Format-YamlList -Name 'trigger_condition' -Values $Row.TriggerCondition)
        (Format-YamlList -Name 'effect_tags' -Values $Row.EffectTags)
        "bonus: $($Row.Bonus.ToString('0.########', [Globalization.CultureInfo]::InvariantCulture))"
        "increment_type: $(Escape-Yaml $Row.IncrementType)"
        "increment_value: $($Row.IncrementValue)"
        "troop_usage: $(Escape-Yaml $Row.TroopUsage)"
        "troop_usage_value: $($Row.TroopUsageValue)"
        "effect: $(Escape-Yaml $Row.Effect)"
        "effect_template: $(Escape-Yaml $Row.EffectTemplate)"
        "alternative_perk_string_id: $(Escape-Yaml $Row.AlternativePerkStringId)"
        "source_status: $(Escape-Yaml $Row.SourceStatus)"
        "source: $(Escape-Yaml $Row.Source)"
        "source_version: $(Escape-Yaml $Row.SourceVersion)"
        "needs_review: $($Row.NeedsReview.ToString().ToLowerInvariant())"
        "functioning: null"
        "perk_wrong: $($Row.PerkWrong.ToString().ToLowerInvariant())"
        "bug_note: $(Escape-Yaml $Row.BugNote)"
        "notes: $(Escape-Yaml $Row.Notes)"
        "classification_review: $(Escape-Yaml $Row.ClassificationReview)"
        '---'
        ''
        "# $($Row.Perk) - $($Row.Role) - $($Row.PerkType)"
        ''
        $Row.Effect
    )
    [System.IO.File]::WriteAllLines($path, $lines, [System.Text.UTF8Encoding]::new($false))
}

$campaignAsm = [System.Reflection.Assembly]::LoadFrom($campaignDll)
[void][System.Reflection.Assembly]::LoadFrom($coreDll)
$defaultPerksType = $campaignAsm.GetType('TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultPerks', $true)
$register = $defaultPerksType.GetMethod('RegisterAll', [System.Reflection.BindingFlags]'NonPublic,Instance')
$initialize = $defaultPerksType.GetMethod('InitializeAll', [System.Reflection.BindingFlags]'NonPublic,Instance')

$createMap = Get-PerkCreateMap (Get-Instructions $register)
$perks = Get-PerkDefinitions -Instructions (Get-Instructions $initialize) -CreateMap $createMap
$rows = @()
foreach ($perk in $perks) {
    $primaryRow = New-EffectRow -Perk $perk -Slot 'primary'
    if ($primaryRow) { $rows += $primaryRow }
    $secondaryRow = New-EffectRow -Perk $perk -Slot 'secondary'
    if ($secondaryRow) { $rows += $secondaryRow }
}

$resolvedOutParent = (Resolve-Path -LiteralPath (Split-Path -Parent $outRoot)).Path
if (-not $outRoot.StartsWith($workspace, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Output path is outside workspace: $outRoot"
}
if ($resolvedOutParent -notlike "$workspace*") {
    throw "Output parent is outside workspace: $resolvedOutParent"
}
if (Test-Path -LiteralPath $outRoot) {
    [System.IO.Directory]::EnumerateFiles($outRoot, '*.md', [System.IO.SearchOption]::AllDirectories) |
        ForEach-Object {
            $deletePath = $_
            for ($attempt = 1; $attempt -le 10; $attempt++) {
                try {
                    [System.IO.File]::Delete($deletePath)
                    break
                } catch {
                    if ($attempt -eq 10) { throw }
                    Start-Sleep -Milliseconds 250
                }
            }
        }
    Get-ChildItem -LiteralPath $outRoot -Recurse -File | Remove-Item -Force
} else {
    New-Item -ItemType Directory -Path $outRoot | Out-Null
}

$seen = @{}
foreach ($row in $rows) {
    $key = "$($row.Skill)|$($row.Level)|$($row.Perk)|$($row.Role)|$($row.PerkType)|$($row.PerkSubtype)"
    if (-not $seen.ContainsKey($key)) { $seen[$key] = 0 }
    $seen[$key]++
    Write-EffectNote -Row $row -DuplicateIndex $seen[$key]
}

$reviewRows = $rows | Where-Object { $_.ClassificationReview }
$reviewLines = @(
    '# Perk Classification Review'
    ''
    "Generated from local Bannerlord $($rows[0].GameVersionTarget) assembly data. Rows listed here are classification heuristics that look ambiguous and should be hand-checked."
    ''
)
if ($reviewRows.Count -eq 0) {
    $reviewLines += 'No classification review flags were generated.'
} else {
    $reviewLines += '| Skill | Level | Perk | Role | Type | Subtype | Effect | Review |'
    $reviewLines += '|---|---:|---|---|---|---|---|---|'
    foreach ($row in $reviewRows | Sort-Object Skill, Level, Perk, EffectSlot) {
        $reviewLines += '| {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} |' -f `
            ($row.Skill -replace '\|','\|'), $row.Level, ($row.Perk -replace '\|','\|'), $row.Role, $row.PerkType, $row.PerkSubtype, ($row.Effect -replace '\|','\|'), ($row.ClassificationReview -replace '\|','\|')
    }
}
[System.IO.File]::WriteAllLines($reviewPath, $reviewLines, [System.Text.UTF8Encoding]::new($false))

$tagLines = @('role')
$tagLines += $rows | Select-Object -ExpandProperty Role -Unique | Sort-Object
$tagLines += ''
$tagLines += 'perk_type'
$tagLines += $rows | Select-Object -ExpandProperty PerkType -Unique | Sort-Object
$tagLines += ''
$tagLines += 'perk_subtype'
$tagLines += $rows |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_.PerkSubtype) } |
    Select-Object -ExpandProperty PerkSubtype -Unique |
    Sort-Object
$tagLines += ''
$tagLines += 'trigger_condition'
$tagLines += $rows |
    ForEach-Object { $_.TriggerCondition } |
    Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) } |
    Select-Object -Unique |
    Sort-Object
$tagLines += ''
$tagLines += 'effect_tags'
$tagLines += $rows |
    ForEach-Object { $_.EffectTags } |
    Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) } |
    Select-Object -Unique |
    Sort-Object
[System.IO.File]::WriteAllLines($tagIndexPath, $tagLines, [System.Text.UTF8Encoding]::new($false))

$roleSummary = $rows | Group-Object Role | Sort-Object Name | ForEach-Object { "$($_.Name): $($_.Count)" }
$typeSummary = $rows | Group-Object PerkType | Sort-Object Name | ForEach-Object { "$($_.Name): $($_.Count)" }
Write-Output "Perks extracted: $($perks.Count)"
Write-Output "Effect rows written: $($rows.Count)"
Write-Output "Review flags: $($reviewRows.Count)"
Write-Output 'Roles:'
$roleSummary | ForEach-Object { Write-Output "  $_" }
Write-Output 'Types:'
$typeSummary | ForEach-Object { Write-Output "  $_" }
