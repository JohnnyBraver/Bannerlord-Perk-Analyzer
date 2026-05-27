from __future__ import annotations

import re
from typing import Any


def matches(text: str, pattern: str) -> bool:
    return re.search(pattern, text) is not None


def classify_effect(effect: str, skill: str, role: str) -> dict[str, str]:
    t = effect.lower()
    type_ = "utility"
    subtype = ""
    review = ""

    if matches(t, r"ignore.+shield|penetrate shields|javelins ignore shields"):
        type_, subtype = "unique", "shield_bypass"
    elif matches(t, r"deflect.*projectile|projectile.*deflect"):
        type_ = "projectile_protection"
    elif matches(t, r"all bows on horseback|mount any bow|long bow|longbow"):
        type_, subtype = "unique", "mounted_longbow"
    elif matches(t, r"old age|survive"):
        type_ = "death_avoidance"
    elif matches(t, r"enemy wounded|enemy troops recover|enemy casualties"):
        type_, subtype = "unique", "enemy_medicine"
    elif matches(t, r"uninterrupted|interrupt"):
        type_, subtype = "unique", "reload_interrupt_resistance"
    elif matches(t, r"upgrade bandit|bandits can be converted"):
        type_, subtype = "unique", "bandit_conversion"
    elif matches(t, r"surrendering bandit parties can be recruited"):
        type_, subtype = "unique", "bandit_recruitment"
    elif matches(t, r"settlements?.*barter"):
        type_, subtype = "unique", "settlement_barter"
    elif matches(t, r"trade in towns while in disguise"):
        type_, subtype = "unique", "disguise_trading"
    elif matches(t, r"ignore .*knockback resistance"):
        type_ = "stagger_bonus"
    elif matches(t, r"ignore .*knockdown resistance"):
        type_ = "stagger_bonus"
    elif matches(t, r"lance staying couched"):
        type_, subtype = "unique", "couched_lance"
    elif matches(t, r"pick up arrows|pick up items.*mounted|mounted.*pick"):
        type_, subtype = "utility", "mounted_pickup"
    elif matches(t, r"handling"):
        type_ = "weapon_handling"
        if matches(t, r"one handed"):
            subtype = "one_handed"
        elif matches(t, r"two handed"):
            subtype = "two_handed"
        elif matches(t, r"polearm"):
            subtype = "polearm"
        elif matches(t, r"bow"):
            subtype = "bow"
        elif matches(t, r"crossbow"):
            subtype = "crossbow"
        elif matches(t, r"weapon"):
            subtype = "weapon"
    elif matches(t, r"maneuvering|top speed to your mount|mount speed"):
        type_ = "mount_performance"
        if matches(t, r"charge damage"):
            subtype = "maneuver_charge"
        elif matches(t, r"maneuver"):
            subtype = "maneuver"
        elif matches(t, r"speed"):
            subtype = "speed"
    elif matches(
        t,
        r"mount dying|becoming lame|recover a lame horse|recover mounts|mount when traveling|"
        r"animals in your party reproducing|tier 2 horses",
    ):
        type_ = "mount_management"
        if matches(t, r"dying|lame"):
            subtype = "mount_recovery"
        elif matches(t, r"reproducing|tier 2 horses"):
            subtype = "mount_breeding"
        elif matches(t, r"find a mount"):
            subtype = "mount_finding"
    elif matches(t, r"carrying capacity|carry capacity"):
        type_ = "carrying_capacity"
        if matches(t, r"pack animals"):
            subtype = "pack_animals"
        elif matches(t, r"prisoners"):
            subtype = "prisoners"
        elif matches(t, r"troops"):
            subtype = "troops"
        elif matches(t, r"party"):
            subtype = "party"
    elif matches(
        t,
        r"prisoner.*escape|escape chance.*prisoner|prisoner lords escaping|prisoner limit|"
        r"hero prisoners|escape chance when imprisoned",
    ):
        type_ = "prisoner_management"
        if matches(t, r"limit"):
            subtype = "prisoner_limit"
        elif matches(t, r"hero|lords"):
            subtype = "hero_prisoners"
        elif matches(t, r"imprisoned"):
            subtype = "personal_escape"
        else:
            subtype = "prisoner_escape"
    elif matches(t, r"prisoner recruitment|recruitment rate.*prisoner|recruitment rate for .*prisoners|faster .*prisoner recruitment"):
        type_ = "prisoner_recruitment"
        if matches(t, r"bandit"):
            subtype = "bandits"
        elif matches(t, r"non-bandit"):
            subtype = "non_bandits"
        elif matches(t, r"tier 4"):
            subtype = "high_tier"
        elif matches(t, r"tier 1|tier 2|tier 3"):
            subtype = "low_tier"
        elif matches(t, r"infantry"):
            subtype = "infantry"
        elif matches(t, r"ranged"):
            subtype = "ranged"
    elif matches(t, r"recruitment slot"):
        type_ = "recruitment_slot"
        if matches(t, r"merchant"):
            subtype = "merchant_notables"
        elif matches(t, r"artisan"):
            subtype = "artisan_notables"
        elif matches(t, r"gang"):
            subtype = "gang_leaders"
        elif matches(t, r"rural"):
            subtype = "rural_notables"
        elif matches(t, r"urban"):
            subtype = "urban_notables"
    elif matches(t, r"volunteering rate|extra troop from village|troop tiers when recruiting"):
        type_ = "recruitment_bonus"
        if matches(t, r"cavalry"):
            subtype = "cavalry"
        elif matches(t, r"village"):
            subtype = "village_notables"
        elif matches(t, r"tier"):
            subtype = "troop_tier"
    elif matches(t, r"influence gain|influence return|influence per day"):
        type_ = "influence_gain"
    elif matches(t, r"influence cost|influence required"):
        type_ = "influence_cost_reduction"
    elif matches(t, r"persuading lords to defect"):
        type_, subtype = "persuasion_cost_reduction", "lord_defection"
    elif matches(t, r"barter penalty|bartering for safe passage|barter for safe passage"):
        type_ = "barter_penalty_reduction"
        if matches(t, r"same culture"):
            subtype = "same_culture"
        elif matches(t, r"different culture"):
            subtype = "different_culture"
        elif matches(t, r"items"):
            subtype = "items"
        elif matches(t, r"safe passage"):
            subtype = "safe_passage"
    elif matches(t, r"profits are marked|prices are marked|trade rumors"):
        type_ = "trade_info"
        if matches(t, r"profits"):
            subtype = "profit_marking"
        elif matches(t, r"prices"):
            subtype = "price_marking"
        elif matches(t, r"rumors"):
            subtype = "trade_rumors"
    elif matches(t, r"hiring costs|recruitment fees|gold required to recruit"):
        type_ = "recruit_cost_reduction"
    elif matches(t, r"trade penalty|price penalty|sell price penalty|better trade deals|gold required|ransom cost|better deals"):
        type_ = "trade_penalty_reduction"
        if matches(t, r"\bmount(?:s|ed)?\b|horses?"):
            subtype = "mounts"
        elif matches(t, r"pack animals"):
            subtype = "pack_animals"
        elif matches(t, r"food"):
            subtype = "food"
        elif matches(t, r"villages"):
            subtype = "villages"
        elif matches(t, r"weapons|smithing weapons"):
            subtype = "weapons"
        elif matches(t, r"mercenary"):
            subtype = "mercenaries"
        elif matches(t, r"ransom"):
            subtype = "ransom"
        elif matches(t, r"caravans|villagers"):
            subtype = "caravans_villagers"
    elif matches(t, r"loot amount for every skill point"):
        type_, subtype = "loot_bonus", "skill_scaling"
    elif matches(t, r"more loot|remove negative modifiers on looted items"):
        type_ = "loot_bonus"
        if matches(t, r"negative modifiers"):
            subtype = "item_quality"
    elif matches(t, r"raid speed"):
        type_ = "raid_speed"
    elif matches(t, r"extra food.*village raids"):
        type_, subtype = "food_reserve", "raid_food"
    elif matches(t, r"companion limit"):
        type_ = "companion_limit"
    elif matches(t, r"more likely to have children"):
        type_ = "fertility"
    elif matches(t, r"garrison limit|garrison size"):
        type_ = "garrison_size"
    elif matches(t, r"food reserve"):
        type_ = "food_reserve"
    elif matches(t, r"prebuilt catapult|prebuilt ballista"):
        type_, subtype = "siege_engines", "prebuilt"
    elif matches(t, r"siege camp preparation speed"):
        type_ = "siege_camp_speed"
    elif matches(t, r"chance from siege bombardments|siege attrition|getting hit while under bombardment"):
        type_ = "damage_resistance"
    elif matches(t, r"chance of troops getting wounded instead of getting killed|lethal wounds|chance to recover from death|cheat death"):
        type_ = "death_avoidance"
    elif matches(
        t,
        r"learning rate of new part designs|crafting stamina recovery rate|stamina spent while|"
        r"greater chance of creating|produce .* iron|refine .* steel|refine .* iron|thamaskene|charcoal|hardwood",
    ):
        type_ = "crafting_bonus"
        if matches(t, r"learning rate"):
            subtype = "crafting_learning"
        elif matches(t, r"stamina"):
            subtype = "crafting_stamina"
        elif matches(t, r"chance of creating"):
            subtype = "crafting_quality"
        elif matches(t, r"produce|refine|thamaskene|steel|iron|charcoal|hardwood"):
            subtype = "crafting_materials"
    elif matches(t, r"crime rating|sneaking into towns|bandits.*surrender|convincing bandits"):
        type_ = "crime_bonus"
        if matches(t, r"crime rating"):
            subtype = "crime_rating"
        elif matches(t, r"sneaking"):
            subtype = "sneaking"
        elif matches(t, r"surrender|convincing"):
            subtype = "bandit_dialog"
    elif matches(t, r"morale penalty.*disorganized state|disorganized state.*morale penalty"):
        type_, subtype = "morale_bonus", "disorganized_state"
    elif matches(t, r"disorganized state|troops left behind|breaking into or out|break into or out"):
        type_ = "battle_escape"
        if matches(t, r"disorganized"):
            subtype = "disorganized_state"
        elif matches(t, r"left behind"):
            subtype = "troops_left_behind"
        elif matches(t, r"breaking into or out|break into or out"):
            subtype = "siege_breakthrough"
    elif matches(t, r"hideout crew"):
        type_, subtype = "party_size", "hideout"
    elif matches(t, r"hideout detection"):
        type_, subtype = "party_vision", "hideout"
    elif matches(t, r"advantage against bandits"):
        type_, subtype = "simulation_bonus", "bandits"
    elif matches(t, r"fortification bonus"):
        type_, subtype = "simulation_bonus", "fortification_bonus"
    elif matches(t, r"betting allowed"):
        type_, subtype = "utility", "tournament_betting"
    elif matches(t, r"stun duration|stun your enemies longer"):
        type_, subtype = "stagger_bonus", "stun_duration"
    elif matches(t, r"staggered while reloading"):
        type_, subtype = "stagger_bonus", "reload"
    elif matches(t, r"reload any crossbow on horseback"):
        type_, subtype = "unique", "mounted_crossbow_reload"
    elif matches(t, r"blocking projectiles from behind"):
        type_, subtype = "projectile_protection", "rear_shield"
    elif matches(t, r"penetrate shields"):
        type_, subtype = "unique", "shields"
    elif matches(t, r"zoom with (bows|crossbows)"):
        type_, subtype = "ranged_accuracy", "zoom"
    elif matches(t, r"zoom with throwing"):
        type_, subtype = "ranged_accuracy", "zoom"
    elif matches(t, r"draw speed with throwing"):
        type_, subtype = "reload_speed", "throwing"
    elif matches(t, r"accuracy penalty.*throwing weapons while mounted"):
        type_, subtype = "ranged_accuracy", "mounted"
    elif matches(t, r"travel speed to .*throwing weapons"):
        type_, subtype = "projectile_speed", "throwing"
    elif matches(t, r"ignore armors? below"):
        type_, subtype = "damage_increase", "armor_penetration"
    elif matches(t, r"sling weapons can penetrate head armor"):
        type_, subtype = "damage_increase", "armor_penetration"
    elif matches(t, r"chance to die when you fall unconscious"):
        type_, subtype = "death_avoidance", "combat_death_save"
    elif matches(t, r"denar return"):
        type_, subtype = "income_increase", "compensation"
    elif matches(t, r"experience per day|skill experience|experience from battles|donated .*experience"):
        type_ = "experience_gain"
    elif matches(t, r"tax income for each skill point"):
        type_, subtype = "income_increase", "skill_scaling"
    elif matches(t, r"gold per day"):
        type_ = "income_increase"
    elif matches(t, r"costs of recruiting minor faction clans"):
        type_, subtype = "recruit_cost_reduction", "minor_faction_clans"
    elif matches(t, r"militias will spawn as veteran"):
        type_, subtype = "militia_quality", "veteran_spawn"
    elif matches(t, r"clan party limit"):
        type_ = "clan_party_limit"
    elif matches(t, r"siege engine build speed.*militia"):
        type_, subtype = "project_speed", "militia_scaling"
    elif matches(t, r"equipped (bows|crossbows) do not slow you down"):
        type_, subtype = "movement_speed", "weapon_slowdown"
    elif matches(t, r"overburden|herding speed penalty"):
        type_ = "party_speed"
        if matches(t, r"overburden"):
            subtype = "overburden"
        elif matches(t, r"herding"):
            subtype = "herding"
    elif matches(t, r"shield hitpoints|shield hit points"):
        type_ = "shield_durability"
    elif matches(t, r"siege bombardment casualties"):
        type_, subtype = "siege_engines", "bombardment"
    elif matches(t, r"damage to your shields?|damage to shields of"):
        type_ = "shield_durability"
    elif matches(t, r"shield protection area"):
        type_ = "projectile_protection"
    elif matches(t, r"damage taken|damage to you|less damage|damage reduced|damage reduction|reduced.*damage"):
        type_ = "damage_resistance"
        if matches(t, r"sent to confront"):
            subtype = "auto_resolve"
        elif matches(t, r"ranged|projectile|arrow|bolt"):
            subtype = "ranged"
        elif matches(t, r"melee"):
            subtype = "melee"
        elif matches(t, r"charge"):
            subtype = "charge"
        elif matches(t, r"fall"):
            subtype = "fall"
        else:
            subtype = "all"
    elif matches(t, r"charge damage"):
        type_, subtype = "damage_increase", "charge"
    elif matches(t, r"damage bonus from speed"):
        type_, subtype = "damage_increase", "speed_bonus"
    elif matches(t, r"armor penetration"):
        type_, subtype = "damage_increase", "armor_penetration"
    elif matches(t, r"damage"):
        type_ = "damage_increase"
        if matches(t, r"sent to confront"):
            subtype = "auto_resolve"
        elif matches(t, r"siege bombardment|during siege bombardment|damage dealt to walls"):
            subtype = "siege_engines"
        elif matches(t, r"siege engines"):
            subtype = "siege_engines"
        elif matches(t, r"destructible"):
            subtype = "destructible_objects"
        elif matches(t, r"without a shield"):
            subtype = "no_shield"
        elif matches(t, r"shield"):
            subtype = "shields"
        elif matches(t, r"as melee|mounted melee"):
            subtype = "melee"
        elif matches(t, r"ranged damage while mounted|mounted archers"):
            subtype = "ranged"
        elif matches(t, r"swing damage|thrust damage"):
            subtype = "melee"
        elif matches(t, r"while mounted|by mounted troops"):
            if matches(t, r"throwing"):
                subtype = "mounted_throwing"
            elif matches(t, r"ranged|bow|crossbow"):
                subtype = "mounted_ranged"
            elif matches(t, r"melee"):
                subtype = "mounted_melee"
            else:
                subtype = "mounted"
        elif matches(t, r"mount"):
            subtype = "mounts"
        elif matches(t, r"ranged|bow|crossbow|throwing"):
            if matches(t, r"crossbow"):
                subtype = "crossbow"
            elif matches(t, r"bow"):
                subtype = "bow"
            elif matches(t, r"throwing|javelin"):
                subtype = "throwing"
            else:
                subtype = "ranged"
        elif matches(t, r"one handed"):
            subtype = "one_handed"
        elif matches(t, r"two handed"):
            subtype = "two_handed"
        elif matches(t, r"polearm"):
            subtype = "polearm"
        elif matches(t, r"destructible"):
            subtype = "destructible_objects"
        elif matches(t, r"\bmelee\b"):
            subtype = "melee"
        else:
            subtype = "weapon"
    elif matches(t, r"movement speed penalty"):
        type_ = "movement_speed"
    elif matches(t, r"swing speed|attack speed"):
        type_ = "attack_speed"
        if matches(t, r"one handed"):
            subtype = "one_handed"
        elif matches(t, r"two handed"):
            subtype = "two_handed"
        elif matches(t, r"polearm"):
            subtype = "polearm"
        elif matches(t, r"melee"):
            subtype = "melee"
    elif matches(t, r"reload"):
        type_ = "reload_speed"
        if matches(t, r"crossbow"):
            subtype = "crossbow"
        elif matches(t, r"bow"):
            subtype = "bow"
        elif matches(t, r"siege"):
            subtype = "siege"
    elif matches(t, r"missile speed|projectile speed|throwing weapon speed"):
        type_ = "projectile_speed"
        if matches(t, r"throw"):
            subtype = "throwing"
        elif matches(t, r"bow"):
            subtype = "bow"
        elif matches(t, r"crossbow"):
            subtype = "crossbow"
    elif matches(t, r"movement speed|speed on foot|faster on foot|combat movement"):
        type_ = "movement_speed"
        if matches(t, r"armor"):
            subtype = "armor_weight"
        elif matches(t, r"shield"):
            subtype = "shield_penalty"
        elif matches(t, r"foot|on foot"):
            subtype = "foot"
        elif matches(t, r"combat"):
            subtype = "combat"
    elif matches(t, r"party speed|map speed|travel speed"):
        type_ = "party_speed"
        if matches(t, r"forest|desert|snow|steppe|terrain|plains"):
            subtype = "terrain"
    elif matches(t, r"hit point regeneration|healing rate|recovery rate"):
        type_ = "regen_bonus"
    elif matches(t, r"hit point|hit points|hp"):
        type_ = "hit_points"
    elif matches(t, r"armor weight"):
        type_ = "utility"
    elif matches(t, r"discarded armors.*experience|donated armors.*experience"):
        type_ = "experience_gain"
    elif matches(t, r"armor"):
        type_ = "armor_increase"
    elif matches(t, r"ammo|ammunition|arrows? per quiver|bolts? per quiver|extra arrows|extra arrow|extra bolts|extra bolt|throwing weapons"):
        type_ = "ammo_capacity"
    elif matches(t, r"accuracy|aim|spread"):
        type_ = "ranged_accuracy"
    elif matches(t, r"skill"):
        type_ = "skill_increase"
    elif matches(t, r"focus point"):
        type_ = "focus_increase"
    elif matches(t, r"party size|party limit"):
        type_ = "party_size"
    elif matches(t, r"attribute point|vigor|endurance|cunning|social|intelligence") or (
        matches(t, r"\bcontrol\b") and not matches(t, r"you control|controlled")
    ):
        type_ = "attribute_increase"
    elif matches(t, r"no morale loss|morale loss from converting|morale loss to troops|morale penalty when troops"):
        type_ = "morale_bonus"
    elif matches(t, r"morale loss|morale damage|morale penalty to enemies|battle morale penalty to enemies|morale effect to enemy"):
        type_ = "morale_damage"
    elif matches(t, r"morale"):
        type_ = "morale_bonus"
    elif matches(t, r"renown"):
        type_ = "renown_bonus"
    elif matches(t, r"relation|relationship"):
        type_ = "relationship_gain"
    elif matches(t, r"experience|xp"):
        type_ = "experience_gain"
    elif matches(t, r"wage|wages|upkeep"):
        type_ = "upkeep_reduction"
    elif matches(t, r"recruit.*cost|recruitment cost"):
        type_ = "recruit_cost_reduction"
    elif matches(t, r"upgrade cost"):
        type_ = "upgrade_cost_reduction"
    elif matches(t, r"sight|spotting|track|visual range"):
        type_ = "party_vision"
    elif matches(t, r"food consumption"):
        type_ = "food_consumption"
    elif matches(t, r"hearth"):
        type_ = "hearth_growth"
    elif matches(t, r"loyalty"):
        type_ = "loyalty_increase"
    elif matches(t, r"security"):
        type_ = "security"
    elif matches(t, r"militia"):
        type_ = "militia_increase"
    elif matches(t, r"prosperity"):
        type_ = "prosperity_bonus"
    elif matches(t, r"income|tariff|tax|gold for each"):
        type_ = "income_increase"
    elif matches(t, r"effect from forums|effect from.*marketplaces|effect from.*festivals|effect from boosting projects|project effects|effectiveness to continuous projects|town project effects"):
        type_ = "project_effect"
    elif matches(t, r"construction|project"):
        type_ = "project_speed"
    elif matches(t, r"production"):
        type_ = "production_output"
    elif matches(t, r"healing|wounded|recovery|recover"):
        type_ = "regen_bonus"
    elif matches(t, r"food item.*smuggled"):
        type_, subtype = "food_reserve", "smuggling"
    elif matches(t, r"siege engine|siege engines|siege equipment"):
        type_ = "siege_engines"
    elif matches(t, r"simulation"):
        type_ = "simulation_bonus"
    elif matches(t, r"stagger"):
        type_ = "stagger_bonus"
    elif matches(t, r"dismount"):
        type_ = "dismount"
    elif matches(t, r"death"):
        type_ = "death_avoidance"
    elif matches(t, r"dialog|persuasion"):
        type_ = "dialog_checks_bonus"
    elif matches(t, r"cohesion"):
        type_ = "cohesion_bonus"

    if type_ == "utility" and subtype != "tournament_betting" and matches(t, r"ignore|unlock|allow|never|can now"):
        review = "Check whether this should be unique instead of utility."
    if type_ == "utility" and matches(t, r"^\s*[+-]?\d"):
        review = "Numeric utility effect may deserve a more specific perk_type."
    if type_ == "damage_increase" and subtype == "":
        review = "Damage effect needs a useful subtype if the condition/source matters."
    if matches(t, r"morale and renown|food consumption, wages and .*morale loss"):
        review = "Composite effect spans multiple classification categories."
    if matches(t, r"renown and influence|relationship.*loyalty|companion wages.*recruitment fees|wages.*upgrade costs|damage.*movement speed|fall damage.*kick damage|damage.*stun duration|charge damage.*maneuvering"):
        review = "Composite effect spans multiple classification categories."
    if matches(t, r"outnumbered"):
        review = "Outnumbered condition is not represented by current trigger_condition taxonomy."
    if matches(t, r"ransom cost"):
        review = "Ransom-cost reduction is not really a trade penalty; current subtype is a lossy fallback unless a ransom-cost subtype is added."

    return {"type": type_, "subtype": subtype, "review": review}


def normalize_classification(type_: str, subtype: str, skill: str) -> dict[str, str]:
    if not subtype.strip():
        return {"type": type_, "subtype": ""}
    if type_ == "unique":
        unique_subtype = "shields" if subtype in {"shields", "shield_bypass"} else ""
        return {"type": type_, "subtype": unique_subtype}

    skill_subtype_map = {
        "One Handed": "one_handed",
        "Two Handed": "two_handed",
        "Polearm": "polearm",
        "Bow": "bow",
        "Crossbow": "crossbow",
        "Throwing": "throwing",
    }
    if skill_subtype_map.get(skill) == subtype:
        return {"type": type_, "subtype": ""}

    reusable_subtypes_by_type = {
        "crafting_bonus": {"crafting_learning", "crafting_materials", "crafting_quality", "crafting_stamina"},
        "damage_increase": {"armor_penetration", "charge", "melee", "mounts", "ranged", "shields", "siege", "siege_engines", "speed_bonus"},
        "damage_resistance": {"charge", "fall", "ranged"},
        "movement_speed": {"combat", "shield_penalty"},
        "party_speed": {"overburden", "terrain"},
        "prisoner_management": {"hero_prisoners", "prisoner_escape", "prisoner_limit"},
        "prisoner_recruitment": {"bandits"},
        "trade_info": {"price_marking", "profit_marking", "trade_rumors"},
        "simulation_bonus": {"fortification_bonus"},
        "trade_penalty_reduction": {"food", "mounts", "ransom", "weapons"},
    }
    if subtype in reusable_subtypes_by_type.get(type_, set()):
        return {"type": type_, "subtype": subtype}
    return {"type": type_, "subtype": ""}


def readable_label(value: str) -> str:
    return value.replace("_", " ").strip() if value.strip() else ""


def add_unique(values: list[str], value: str) -> None:
    clean = value.strip()
    if clean and clean not in values:
        values.append(clean)


def readable_mechanic(type_: str) -> str:
    labels = {
        "attribute_increase": "attribute point",
        "barter_penalty_reduction": "barter",
        "clan_party_limit": "clan party limit",
        "cohesion_bonus": "cohesion",
        "companion_limit": "companion limit",
        "dialog_checks_bonus": "dialog checks",
        "experience_gain": "experience gain",
        "focus_increase": "focus point",
        "food_consumption": "food consumption",
        "food_reserve": "food reserve",
        "garrison_size": "garrison size",
        "hearth_growth": "hearth growth",
        "income_increase": "income",
        "influence_cost_reduction": "influence cost",
        "influence_gain": "influence",
        "loyalty_increase": "loyalty",
        "militia_increase": "militia gain",
        "militia_quality": "militia quality",
        "morale_bonus": "morale",
        "party_size": "party size",
        "party_speed": "party speed",
        "persuasion_cost_reduction": "persuasion cost",
        "prisoner_management": "prisoners",
        "prisoner_recruitment": "prisoner recruitment",
        "project_effect": "project effect",
        "project_speed": "build speed",
        "prosperity_bonus": "prosperity",
        "production_output": "production",
        "raid_speed": "raid speed",
        "recruit_cost_reduction": "recruitment cost",
        "recruitment_bonus": "recruitment bonus",
        "recruitment_slot": "recruitment slot",
        "relationship_gain": "relationship",
        "renown_bonus": "renown",
        "siege_camp_speed": "siege camp speed",
        "simulation_bonus": "simulation bonus",
        "skill_increase": "skill bonus",
        "trade_info": "trade info",
        "trade_penalty_reduction": "trade penalty reduction",
        "upgrade_cost_reduction": "upgrade cost",
        "upkeep_reduction": "wages",
    }
    return labels.get(type_, readable_label(type_))


def get_trigger_conditions(effect: str) -> list[str]:
    t = effect.lower()
    conditions: list[str] = []
    if matches(t, r"siege|besieging|besieged|bombardment|sally out"):
        add_unique(conditions, "during siege")
    if matches(t, r"while waiting|waiting in|resting in settlements?|stationary on (?:the )?campaign map|stationary for at least"):
        add_unique(conditions, "while waiting")
    if matches(t, r"while traveling|when traveling|traveling through|traveling in|when moving|moving on campaign map") or (
        matches(t, r"travel speed") and not matches(t, r"throwing weapons?|projectile|missile|javelins?")
    ):
        add_unique(conditions, "while traveling")
    if matches(t, r"sent to confront|sent as attackers|sent to sally out"):
        add_unique(conditions, "simulation")
    if matches(t, r"desert|dunes|forest|forests|steppe|steppes|plains|snowy|terrain"):
        add_unique(conditions, "terrain")
    if matches(t, r"after every battle|after a battle|after battle|after each battle|after each offensive battle|after battles|from battles|from victories|at the end of the battle|battle is over|battles won|winning battles|winning sieges|when an enemy lord is defeated|helping lords in battle|recover .* in battles"):
        add_unique(conditions, "after battle")
    if matches(t, r"continuous project|while building a project|when a project is finished|project is finished|boosting projects|build speed.*projects?|effect from forums|effect from.*marketplaces|effect from.*festivals|town project effects|civilian projects|construction speed.*prisoners?|projects in the governed"):
        add_unique(conditions, "project active")
    if matches(t, r"same culture|own culture"):
        add_unique(conditions, "same culture")
    if matches(t, r"different culture|different cultures"):
        add_unique(conditions, "different culture")
    if matches(t, r"own kingdom|your kingdom"):
        add_unique(conditions, "own kingdom")
    if not matches(t, r"morale loss") and matches(t, r"morale .*higher|morale higher|morale .*above"):
        add_unique(conditions, "morale threshold")
    tier_band_pattern = r"tier \d(?:\+|(?:, \d)*(?: and \d)?| to \d)? (?:troops?|units?|recruits?|prisoners?|bandits?|infantry|cavalry|archers)"
    party_composition_pattern = (
        r"composed of|foot troops|your infantry|\binfantry\b|\barchers\b|\bcavalry\b|footmen on horses|"
        r"infantry prisoners|ranged prisoners|cavalry prisoners|infantry troops?|ranged troops?|melee troops?|"
        r"mounted troops?|cavalry troops?|bandit units|bandit troops?|bandit prisoners?|non-bandit prisoners?|"
        r"mercenary troops?|pack animals|garrisoned cavalry|hero prisoners|equipped with throwing weapons|"
        + tier_band_pattern
        + r"|(?:archers|infantry|cavalry|mounted troops|ranged troops|melee troops|bandits|bandit prisoners|bandit troops|mercenary troops?|pack animals) "
        r"(?:in your party|in your formation|in the formation|under your formation|garrisoned|of your party|of the party|in the governed settlement)"
    )
    if matches(t, party_composition_pattern):
        add_unique(conditions, "party composition")
    if matches(t, r"governed settlement|governed town|governed castle|governing settlement|villages bound|bound villages|governed by your clan"):
        add_unique(conditions, "governed settlement")
    if matches(t, r"for every skill point above|for each .*point above|skill point over|above 200|above 250|above 275"):
        add_unique(conditions, "over skill cap")
    if matches(t, r"while mounted|when you start a battle mounted|on horseback|horseback|mounted melee|mounted ranged|mounted throwing"):
        add_unique(conditions, "while mounted")
    if matches(t, r"on foot|while on foot"):
        add_unique(conditions, "on foot")
    if matches(t, r"more than 90%.*hit points|less than half.*hit points"):
        add_unique(conditions, "health threshold")
    if matches(t, r"for each enemy you kill|when you kill|kill an enemy|after a kill|with .* kills|kills? by"):
        add_unique(conditions, "on kill")
    if matches(t, r"when attacking|sent as attackers|offensive battle"):
        add_unique(conditions, "attacking")
    if matches(t, r"when defending|defending at|while defending|defending in|being attacked|confront the attacking enemy|sent to sally out|sally out"):
        add_unique(conditions, "defending")
    return conditions


def get_effect_tags(effect: str, old_subtype: str, new_type: str, new_subtype: str, trigger_conditions: list[str]) -> list[str]:
    t = effect.lower()
    tags: list[str] = []
    if old_subtype.strip():
        add_unique(tags, readable_label(old_subtype))
    defense_text = matches(t, r"security|militia|fortification|besieged governed settlement|besieged settlement|governed settlement.*under siege")
    if new_type == "settlement defense" or defense_text or (new_type != "gold economy" and matches(t, r"garrison")):
        add_unique(tags, "defense")
    if matches(t, r"food|grain|olives|fish|date|starv"):
        add_unique(tags, "food")
    if matches(t, r"militia|militias"):
        add_unique(tags, "militia")
    if matches(t, r"garrison|garrisoned"):
        add_unique(tags, "garrison")
    if matches(t, r"fortifications?|barrack|(?:settlement|town|castle|siege|defensive) walls?|\bwall hit points"):
        add_unique(tags, "fortifications")
    if matches(t, r"build speed|construction speed|build rate|siege engine build speed"):
        add_unique(tags, "build speed")
    if matches(t, r"movement speed penalty.*shields?|wielding shields"):
        add_unique(tags, "shield penalty")
    if matches(t, r"tax"):
        add_unique(tags, "tax")
    if matches(t, r"tariff"):
        add_unique(tags, "tariff")
    if matches(t, r"workshop|workshops"):
        add_unique(tags, "workshop")
    if matches(t, r"caravan|caravans"):
        add_unique(tags, "caravan")
    if matches(t, r"village|villages|villager|villagers"):
        add_unique(tags, "village")
    if matches(t, r"wages|paid wages"):
        add_unique(tags, "wages")
    if matches(t, r"recruitment cost|recruitment fees|hiring costs|costs? of recruiting|gold required to recruit"):
        add_unique(tags, "recruitment cost")
    if matches(t, r"upgrade cost|upgrade costs"):
        add_unique(tags, "upgrade cost")
    if matches(t, r"ransom"):
        add_unique(tags, "ransom")
    if matches(t, r"weapon|weapons|swords?|axes?|maces?|javelins?|polearms?|lances?|couched lance|bows?|crossbows?|throwing"):
        add_unique(tags, "weapons")
    if matches(t, r"\bmount(?:s|ed)?\b|horses?|horseback|steed|cavalry|pack animals|animals in your party|maneuvering|couched lance|couch lance|lance staying couched"):
        add_unique(tags, "mounts")
    if matches(t, r"prisoner|prisoners|imprisoned"):
        add_unique(tags, "prisoners")
    if matches(t, r"escape chance|chance to escape|prisoners? escape|prisoner lords escaping"):
        add_unique(tags, "prisoner escape")
    if matches(t, r"bandit|bandits"):
        add_unique(tags, "bandits")
    if matches(t, r"companion|companions"):
        add_unique(tags, "companions")
    if matches(t, r"loot|looted"):
        add_unique(tags, "loot")
    if matches(t, r"overburden"):
        add_unique(tags, "overburden")
    if matches(t, r"barter"):
        add_unique(tags, "barter")
    if matches(t, r"trade|price|profits?|deals"):
        add_unique(tags, "trade")
    if matches(t, r"\bprojects?\b|while building a project|boosting projects|project is finished|forums|marketplaces|festivals"):
        add_unique(tags, "projects")
    if matches(t, r"combat movement|in combat"):
        add_unique(tags, "combat")

    clean: list[str] = []
    for tag in tags:
        if tag == new_type or (tag == new_subtype and tag != "mounts"):
            continue
        if tag in trigger_conditions:
            continue
        add_unique(clean, tag)
    return clean


def get_readable_facets(type_: str, subtype: str, effect: str, role: str) -> dict[str, Any]:
    t = effect.lower()
    new_type = readable_label(type_)
    if type_ == "unique" and subtype == "shields":
        new_subtype = "shields"
    elif type_ == "unique":
        new_subtype = ""
    elif subtype.strip():
        new_subtype = readable_label(subtype)
    else:
        new_subtype = ""

    social = {"relationship_gain", "renown_bonus", "dialog_checks_bonus", "fertility"}
    party_management = {
        "clan_party_limit",
        "companion_limit",
        "carrying_capacity",
        "morale_bonus",
        "party_size",
        "party_speed",
        "prisoner_management",
        "prisoner_recruitment",
        "recruitment_bonus",
        "recruitment_slot",
        "raid_speed",
    }
    gold_economy = {
        "barter_penalty_reduction",
        "loot_bonus",
        "persuasion_cost_reduction",
        "recruit_cost_reduction",
        "trade_info",
        "trade_penalty_reduction",
        "upgrade_cost_reduction",
        "upkeep_reduction",
    }
    settlement_economy = {"hearth_growth", "production_output", "prosperity_bonus"}
    settlement_defense = {"garrison_size", "militia_increase", "militia_quality", "security"}
    settlement_governance = {"loyalty_increase", "project_effect"}
    character_growth = {"attribute_increase", "focus_increase", "skill_increase"}
    army_management = {"cohesion_bonus", "influence_cost_reduction", "influence_gain"}
    movement = {"movement_speed", "mount_performance"}
    siege = {"siege_camp_speed", "siege_engines"}

    if type_ in social:
        new_type, new_subtype = "social", readable_mechanic(type_)
    elif type_ == "experience_gain":
        if matches(t, r"companions|party member|clan member|hero"):
            new_type, new_subtype = "character growth", "experience gain"
        elif role == "governor" and matches(t, r"garrison|governed settlement"):
            new_type, new_subtype = "settlement defense", "troop xp"
        else:
            new_type, new_subtype = "party management", "troop xp"
    elif type_ == "skill_increase" and matches(t, r"troops?|units?|infantry|archers|cavalry|bandit|formation|garrison"):
        new_type, new_subtype = "troop combat", "skill bonus"
    elif type_ in character_growth:
        new_type, new_subtype = "character growth", readable_mechanic(type_)
    elif type_ in army_management:
        new_type, new_subtype = "army management", readable_mechanic(type_)
    elif type_ == "party_size" and role == "governor" and matches(t, r"villager|village"):
        new_type, new_subtype = "settlement economy", "party size"
    elif type_ == "prisoner_management" and matches(t, r"imprisoned by mobile parties|escape chance when imprisoned"):
        new_type, new_subtype = "utility", "prisoners"
    elif type_ == "prisoner_management" and role == "governor" and matches(t, r"dungeons?|governed settlements?"):
        new_type, new_subtype = "settlement governance", "prisoners"
    elif type_ in party_management:
        new_type, new_subtype = "party management", readable_mechanic(type_)
    elif type_ in gold_economy:
        new_type, new_subtype = "gold economy", readable_mechanic(type_)
    elif type_ in settlement_economy:
        new_type, new_subtype = "settlement economy", readable_mechanic(type_)
    elif type_ in settlement_defense:
        new_type, new_subtype = "settlement defense", readable_mechanic(type_)
    elif type_ in settlement_governance:
        new_type, new_subtype = "settlement governance", readable_mechanic(type_)
    elif type_ == "mount_management" and role == "governor" and matches(t, r"villages bound|bound villages|producing tier 2 horses"):
        new_type, new_subtype = "settlement economy", "production"
    elif type_ in movement:
        new_type, new_subtype = "movement", readable_mechanic(type_)
    elif type_ in siege:
        new_type, new_subtype = "siege", readable_mechanic(type_)
    elif type_ == "income_increase":
        if role == "governor":
            new_type, new_subtype = "settlement economy", "settlement income"
        else:
            new_type, new_subtype = "gold economy", "income"
    elif type_ == "food_reserve":
        if role == "governor" and matches(t, r"maximum food reserve limits"):
            new_type = "settlement economy"
        elif role == "governor":
            new_type = "settlement defense"
        else:
            new_type = "party management"
        new_subtype = "food reserve"
    elif type_ == "food_consumption":
        if role == "governor" and matches(t, r"town population"):
            new_type = "settlement economy"
        elif role == "governor":
            new_type = "settlement defense"
        else:
            new_type = "party management"
        new_subtype = "food consumption"
    elif type_ == "regen_bonus" and role == "governor" and matches(t, r"recovery rate from raids in villages bound"):
        new_type, new_subtype = "settlement economy", ""
    elif type_ == "project_speed":
        if matches(t, r"fortification|military|castle|siege engine|militia|barrack|walls?"):
            new_type = "settlement defense"
        else:
            new_type = "settlement governance"
        new_subtype = "build speed"
    elif type_ == "simulation_bonus" and role == "governor":
        new_type, new_subtype = "settlement defense", "fortification bonus"

    combat_mechanic_types = {
        "ammo capacity",
        "armor increase",
        "attack speed",
        "damage increase",
        "damage resistance",
        "dismount",
        "hit points",
        "morale damage",
        "projectile protection",
        "projectile speed",
        "ranged accuracy",
        "reload speed",
        "shield durability",
        "stagger bonus",
        "weapon handling",
    }
    combat_mechanic = ""
    if new_type in combat_mechanic_types:
        combat_mechanic = new_type
    elif new_type == "party management" and new_subtype == "morale" and matches(
        t,
        r"battle morale|starting battle morale|morale effect to (friendly|enemy) troops|morale loss to troops|"
        r"morale penalty when troops|wounded troops.*morale in battles|retreat due to low morale",
    ):
        combat_mechanic = "morale"
    elif new_type == "movement" and new_subtype == "movement speed" and not matches(t, r"campaign map|travel speed|party speed"):
        combat_mechanic = "movement speed"
    elif new_type == "mount management" and new_subtype == "mount performance":
        combat_mechanic = "mount performance"

    siege_engine_pattern = r"siege engines?|siege equipment|ballistas?|mangonels?|trebuchets?|rams?|siege-?towers?|bombardments?"
    if combat_mechanic and not new_subtype.strip() and matches(t, siege_engine_pattern):
        new_subtype = "siege engines"
    if role == "governor" and combat_mechanic:
        if new_type == "ranged accuracy" and matches(t, r"ballistas? in the governed settlement"):
            new_type, new_subtype, combat_mechanic = "settlement defense", "ranged accuracy", ""
        elif new_type == "damage resistance" and matches(t, r"siege attrition"):
            new_type, new_subtype, combat_mechanic = "settlement defense", "damage resistance", ""
        elif new_type == "hit points" and matches(t, r"wall hit points"):
            new_type, new_subtype, combat_mechanic = "settlement defense", "hit points", ""
        elif new_type == "damage increase" and matches(t, r"besieging siege engines|besieging troops in siege bombardment"):
            new_type, new_subtype, combat_mechanic = "settlement defense", "siege engines", ""

    if combat_mechanic:
        combat_subtype = combat_mechanic if not new_subtype.strip() else new_subtype
        troop_target_pattern = r"(?:troops?|units?|infantry|archers|cavalry|mounts?|mounted troops|ranged troops|melee troops|foot troops|formation|garrison|militia)"
        troop_scope_pattern = (
            r"(?:in your party|in the party|in your formation|under your formation|in the formation|garrison|"
            r"governed settlement|friendly troops|enemy troops|by troops|by your troops|to troops|"
            r"to (?:tier \d(?:\+| to \d)? )?(?:ranged|melee|mounted|cavalry|infantry|foot|bandit)? ?troops|"
            r"of troops|troops are sent|for troops|to mounts)"
        )
        battle_morale_target = combat_mechanic == "morale" and matches(
            t,
            r"battle morale|starting battle morale|morale loss to troops|morale penalty when troops|"
            r"wounded troops.*morale in battles|retreat due to low morale",
        )
        troop_combat = (
            role == "captain"
            or matches(t, r"sent to confront|sent as attackers|sent to sally out")
            or battle_morale_target
            or (matches(t, troop_target_pattern) and matches(t, troop_scope_pattern))
        )
        personal_combat = role in {"personal", "player"} or matches(
            t, r"\byou\b|your attacks|your .*kills|your throwing weapons|your shields?|with your|other heroes in your party"
        )
        personal_role_troop_effect = matches(t, r"battle morale (?:effect )?to troops|battle morale effect to (friendly|enemy) troops") or (
            role in {"personal", "player"}
            and matches(t, troop_target_pattern)
            and matches(t, r"(?:in your party|to troops|to (?:tier \d(?:\+| to \d)? )?(?:ranged|melee|mounted|cavalry|infantry|foot|bandit)? ?troops|for troops)")
        )

        if troop_combat and (role not in {"personal", "player"} or personal_role_troop_effect):
            new_type, new_subtype = "troop combat", combat_subtype
        elif personal_combat:
            new_type, new_subtype = "personal combat", combat_subtype

    triggers: list[str] = []
    for trigger in get_trigger_conditions(effect):
        add_unique(triggers, trigger)
    if role == "governor" and re.search(r"^settlement ", new_type):
        add_unique(triggers, "governed settlement")
    tags = get_effect_tags(effect, subtype, new_type, new_subtype, triggers)
    return {
        "type": new_type,
        "subtype": new_subtype,
        "trigger_condition": triggers,
        "effect_tags": tags,
    }
