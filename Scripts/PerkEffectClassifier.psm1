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
    if ($t -notmatch 'morale loss' -and $t -match 'morale .*higher|morale higher|morale .*above') { Add-UniqueListValue $conditions 'morale threshold' }
    $partyCompositionPattern = 'composed of|less than \d+ soldiers|foot troops|your infantry|footmen on horses|infantry troops|ranged troops|melee troops|mounted troops|cavalry troops|bandit units|bandit troops|bandit prisoners|non-bandit prisoners|mercenary troops?|pack animals|garrisoned cavalry|hero prisoners|tier \d\+? (?:troops|units|recruits|prisoners|bandits|infantry|cavalry|archers)|(?:archers|infantry|cavalry|mounted troops|ranged troops|melee troops|bandits|bandit prisoners|bandit troops|mercenary troops?|pack animals) (?:in your party|in your formation|in the formation|under your formation|garrisoned|of your party|of the party|in the governed settlement)'
    if ($t -match $partyCompositionPattern) { Add-UniqueListValue $conditions 'party composition' }
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
    if ($t -match 'fortifications?|barrack|(?:settlement|town|castle|siege|defensive) walls?') { Add-UniqueListValue $tags 'fortifications' }
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
    if ($t -match 'weapon|weapons|swords?|axes?|maces?|javelins?|polearms?|lances?|couched lance|bows?|crossbows?|throwing') { Add-UniqueListValue $tags 'weapons' }
    if ($t -match '\bmount(?:s|ed)?\b|horses?|horseback|steed|cavalry|pack animals') { Add-UniqueListValue $tags 'mounts' }
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
    } elseif ($newType -eq 'party management' -and $newSubtype -eq 'morale' -and $t -match 'battle morale|starting battle morale|morale effect to (friendly|enemy) troops') {
        $combatMechanic = 'morale'
    } elseif ($newType -eq 'movement' -and $newSubtype -eq 'movement speed' -and $t -notmatch 'campaign map|travel speed|party speed') {
        $combatMechanic = 'movement speed'
    } elseif ($newType -eq 'mount management' -and $newSubtype -eq 'mount performance') {
        $combatMechanic = 'mount performance'
    }

    if ($combatMechanic) {
        $combatSubtype = if ([string]::IsNullOrWhiteSpace($newSubtype)) { $combatMechanic } else { $newSubtype }
        $troopCombat = ($Role -eq 'captain') -or
            ($t -match 'sent to confront|sent as attackers|sent to sally out') -or
            ($t -match '(?:troops?|infantry|archers|cavalry|mounted troops|ranged troops|melee troops|foot troops|formation|garrison|militia)' -and $t -match '(?:in your party|in your formation|under your formation|in the formation|garrison|governed settlement|friendly troops|enemy troops|by troops|to troops|of troops|troops are sent)')
        $personalCombat = ($Role -in @('personal', 'player')) -or
            ($t -match '\byou\b|your attacks|your .*kills|your throwing weapons|your shields?|with your')

        $personalRoleTroopEffect = ($t -match 'battle morale effect to (friendly|enemy) troops') -or
            ($Role -in @('personal', 'player') -and $t -match '(?:troops?|infantry|archers|cavalry|mounted troops|ranged troops|melee troops|foot troops) in your party')

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

function Test-JsonProperty {
    param($Object, [string]$Name)
    $null -ne $Object -and $null -ne $Object.PSObject.Properties[$Name]
}

function Convert-OverrideList {
    param($Value)
    if ($null -eq $Value) { return @() }
    if ($Value -is [System.Array]) { return @($Value) }
    @($Value)
}

function Add-OverrideListValues {
    param([object[]]$Current, $Values)
    $list = New-Object 'System.Collections.Generic.List[string]'
    foreach ($item in @($Current)) { Add-UniqueListValue $list ([string]$item) }
    foreach ($item in @(Convert-OverrideList $Values)) { Add-UniqueListValue $list ([string]$item) }
    @($list.ToArray())
}

function Remove-OverrideListValues {
    param([object[]]$Current, $Values)
    $remove = @(Convert-OverrideList $Values)
    @($Current | Where-Object { $remove -notcontains [string]$_ })
}

function Load-PerkEffectOverrides {
    param([string]$Path)
    $overrides = @{}
    if (-not (Test-Path -LiteralPath $Path)) { return $overrides }

    $items = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    foreach ($item in @($items)) {
        if (-not (Test-JsonProperty -Object $item -Name 'perk_string_id') -or -not (Test-JsonProperty -Object $item -Name 'effect_slot')) {
            throw "Override entry is missing perk_string_id or effect_slot."
        }
        $key = "$($item.perk_string_id)|$($item.effect_slot)"
        if ($overrides.ContainsKey($key)) {
            throw "Duplicate override key: $key"
        }
        $overrides[$key] = $item
    }
    $overrides
}

function Apply-PerkEffectOverride {
    param($Row, [hashtable]$Overrides)
    if ($null -eq $Row -or $null -eq $Overrides) { return $Row }

    $key = "$($Row.PerkStringId)|$($Row.EffectSlot)"
    if (-not $Overrides.ContainsKey($key)) { return $Row }

    $override = $Overrides[$key]
    if (Test-JsonProperty -Object $override -Name 'perk_type') { $Row.PerkType = [string]$override.perk_type }
    if (Test-JsonProperty -Object $override -Name 'perk_subtype') { $Row.PerkSubtype = [string]$override.perk_subtype }
    if (Test-JsonProperty -Object $override -Name 'trigger_condition') { $Row.TriggerCondition = @(Convert-OverrideList $override.trigger_condition) }
    if (Test-JsonProperty -Object $override -Name 'add_trigger_condition') { $Row.TriggerCondition = @(Add-OverrideListValues -Current $Row.TriggerCondition -Values $override.add_trigger_condition) }
    if (Test-JsonProperty -Object $override -Name 'remove_trigger_condition') { $Row.TriggerCondition = @(Remove-OverrideListValues -Current $Row.TriggerCondition -Values $override.remove_trigger_condition) }
    if (Test-JsonProperty -Object $override -Name 'effect_tags') { $Row.EffectTags = @(Convert-OverrideList $override.effect_tags) }
    if (Test-JsonProperty -Object $override -Name 'add_effect_tags') { $Row.EffectTags = @(Add-OverrideListValues -Current $Row.EffectTags -Values $override.add_effect_tags) }
    if (Test-JsonProperty -Object $override -Name 'remove_effect_tags') { $Row.EffectTags = @(Remove-OverrideListValues -Current $Row.EffectTags -Values $override.remove_effect_tags) }
    if (Test-JsonProperty -Object $override -Name 'perk_wrong') { $Row.PerkWrong = [bool]$override.perk_wrong }
    if (Test-JsonProperty -Object $override -Name 'notes') { $Row.Notes = [string]$override.notes }
    if (Test-JsonProperty -Object $override -Name 'classification_review') { $Row.ClassificationReview = [string]$override.classification_review }
    $Row
}

Export-ModuleMember -Function Classify-Effect, Normalize-Classification, Get-ReadableFacets, Load-PerkEffectOverrides, Apply-PerkEffectOverride
