from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from .postprocess import default_workspace
    from .xp_reports import display_path, table_escape
except ImportError:
    from postprocess import default_workspace
    from xp_reports import display_path, table_escape


CATEGORY_META = {
    "core_troop_lethality": {
        "title": "Core Troop Lethality",
        "description": (
            "Direct live-battle power per soldier: damage, combat skill, attack cadence, accuracy, "
            "melee pressure, and troop combat movement. For shock infantry, movement speed is treated "
            "as a lethality multiplier because it shortens arrow exposure and helps force melee contact."
        ),
    },
    "combat_staying_power": {
        "title": "Combat Staying Power",
        "description": (
            "Live-battle durability for elite troops: hit points, armor, damage reduction, shield coverage, "
            "stagger resistance, and survival-facing combat effects."
        ),
    },
    "engagement_control": {
        "title": "Engagement Control",
        "description": (
            "Campaign movement and pursuit tools that let the party choose fights, avoid bad ones, and later "
            "run down parties of equal or smaller size."
        ),
    },
    "party_scaling": {
        "title": "Party Scaling",
        "description": (
            "Party size and logistics that scale the elite stack. These are valuable, but they come after "
            "per-troop dominance and enough map speed to pick engagements."
        ),
    },
    "low_priority_misleading": {
        "title": "Low Priority or Misleading for This Doctrine",
        "description": (
            "Personal-only, governor-only, siege-only, simulation-only, projectile-speed, and weapon-handling "
            "rows that can look relevant in a keyword report but do not provide core one-party shock-infantry value."
        ),
    },
}

CATEGORY_ORDER = tuple(CATEGORY_META)
RATING_ORDER = {"high": 0, "medium": 1, "low": 2}

COMMANDER_ROLES = {
    "captain",
    "party leader",
    "quartermaster",
    "scout",
    "surgeon",
    "clan leader",
    "army leader",
}

SPEED_KIND_DESCRIPTIONS = {
    "campaign_party_speed": "Strategic party or army movement on the campaign map.",
    "troop_combat_movement": "Live battle movement speed for troops or formations.",
    "personal_combat_movement": "Live battle movement speed for the player hero only.",
    "weapon_handling_speed": "Reload, draw, aiming, swing, attack, or loadout movement handling.",
    "projectile_speed": "Projectile travel speed for arrows, bolts, or thrown weapons.",
    "siege_speed": "Siege engine build, preparation, bombardment, or reload speed.",
}

BANNER_COMPARISON_EFFECTS = {
    "infantry_speed": {
        "effect": "IncreasedTroopMovementSpeed",
        "role": "Speed-minded shock infantry",
        "summary": "Best default banner when the main problem is reaching melee contact under fire.",
    },
    "mounted_speed": {
        "effect": "IncreasedMountMovementSpeed",
        "role": "Mounted mobility",
        "summary": "Mounted version of the speed plan; useful for cavalry or horse archer formations, but much smaller.",
    },
    "ranged_resistance": {
        "effect": "DecreasedRangedAttackDamage",
        "role": "Anti-arrow staying power",
        "summary": "Best defensive rival to the infantry speed banner when the formation must trade under ranged fire.",
    },
    "archer_accuracy": {
        "effect": "DecreasedRangedAccuracyPenalty",
        "role": "Archer-heavy specialist",
        "summary": "Specialist banner for dense archer formations; not a shock-infantry survival tool.",
    },
    "melee_damage": {
        "effect": "IncreasedMeleeDamage",
        "role": "Melee damage breakpoint test",
        "summary": "Strong on paper, but may be wasted when elite troops already overkill common targets.",
    },
}

PACKAGE_METRIC_KEYS = (
    "infantry_movement_percent",
    "ranged_movement_percent",
    "mounted_movement_percent",
    "campaign_speed_percent",
    "melee_damage_percent",
    "ranged_damage_percent",
    "ranged_armor_penetration_percent",
    "ranged_accuracy_penalty_reduction_percent",
    "weapon_inaccuracy_reduction_percent",
    "melee_skill_bonus",
    "ranged_skill_bonus",
    "hit_points",
    "armor",
    "ranged_damage_taken_reduction_percent",
    "shield_damage_reduction_percent",
    "party_size",
    "troop_xp_percent",
)

PACKAGE_DEFINITIONS = {
    "shock_speed": {
        "title": "Shock Speed",
        "banner_key": "infantry_speed",
        "doctrine": "Elite shock infantry reaching melee alive and fast.",
        "weights": {
            "infantry_movement_percent": 3.5,
            "melee_damage_percent": 1.7,
            "melee_skill_bonus": 0.25,
            "hit_points": 0.35,
            "armor": 0.8,
            "ranged_damage_taken_reduction_percent": 1.2,
            "shield_damage_reduction_percent": 0.6,
            "campaign_speed_percent": 1.0,
            "party_size": 0.5,
        },
    },
    "anti_arrow": {
        "title": "Anti-Arrow Durability",
        "banner_key": "ranged_resistance",
        "doctrine": "Infantry that expects to trade under ranged fire before contact.",
        "weights": {
            "hit_points": 1.2,
            "armor": 2.0,
            "ranged_damage_taken_reduction_percent": 4.0,
            "shield_damage_reduction_percent": 1.5,
            "infantry_movement_percent": 1.4,
            "melee_damage_percent": 1.0,
            "melee_skill_bonus": 0.18,
            "campaign_speed_percent": 0.8,
            "party_size": 0.5,
        },
    },
    "archer_accuracy": {
        "title": "Archer Accuracy",
        "banner_key": "archer_accuracy",
        "doctrine": "Ranged-heavy formation where hit rate is the bottleneck.",
        "weights": {
            "weapon_inaccuracy_reduction_percent": 4.0,
            "ranged_accuracy_penalty_reduction_percent": 4.0,
            "ranged_damage_percent": 2.2,
            "ranged_armor_penetration_percent": 2.2,
            "ranged_skill_bonus": 0.3,
            "ranged_movement_percent": 1.0,
            "hit_points": 0.35,
            "campaign_speed_percent": 0.8,
            "party_size": 0.5,
        },
    },
    "melee_damage": {
        "title": "Melee Damage",
        "banner_key": "melee_damage",
        "doctrine": "Shock infantry damage breakpoints and fast cleanup.",
        "weights": {
            "melee_damage_percent": 5.0,
            "melee_skill_bonus": 0.32,
            "infantry_movement_percent": 2.0,
            "hit_points": 0.4,
            "armor": 0.8,
            "ranged_damage_taken_reduction_percent": 0.8,
            "shield_damage_reduction_percent": 0.5,
            "campaign_speed_percent": 0.8,
            "party_size": 0.5,
        },
    },
}


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def row_effect(row: dict[str, Any]) -> str:
    return str(row.get("game", {}).get("effect", ""))


def row_effect_lower(row: dict[str, Any]) -> str:
    return row_effect(row).lower()


def row_role(row: dict[str, Any]) -> str:
    return str(row.get("game", {}).get("role", ""))


def row_type(row: dict[str, Any]) -> str:
    return str(row.get("classification", {}).get("perk_type", ""))


def row_subtype(row: dict[str, Any]) -> str:
    return str(row.get("classification", {}).get("perk_subtype", ""))


def row_triggers(row: dict[str, Any]) -> set[str]:
    return {str(item) for item in row.get("classification", {}).get("trigger_conditions", [])}


def row_tags(row: dict[str, Any]) -> set[str]:
    return {str(item) for item in row.get("classification", {}).get("effect_tags", [])}


def matches(text: str, pattern: str) -> bool:
    return bool(re.search(pattern, text))


def is_siege_text(text: str) -> bool:
    return matches(text, r"siege|ballista|mangonel|trebuchet|bombardment|ram|siege camp|engine")


def classify_speed_kind(row: dict[str, Any]) -> str | None:
    text = row_effect_lower(row)
    subtype = row_subtype(row)
    role = row_role(row)

    has_speed_text = "speed" in text or "faster" in text or subtype in {
        "party speed",
        "movement speed",
        "projectile speed",
        "reload speed",
        "attack speed",
    }
    if not has_speed_text:
        return None

    if is_siege_text(text) and matches(text, r"speed|faster|reload|build|preparation"):
        return "siege_speed"

    if subtype == "projectile speed" or matches(text, r"travel speed to .*weapons?|throwing weapons"):
        return "projectile_speed"

    if subtype == "party speed" or matches(
        text,
        r"\bparty speed\b|travel speed (?:during|on|when|while|from|penalty)|"
        r"speed penalty from (?:forests?|wounded|herding|overburdened)|"
        r"movement speed to parties called",
    ):
        return "campaign_party_speed"

    if matches(
        text,
        r"reload speed|draw speed|aiming speed|attack speed|swing speed|weapon handling|ready speed|"
        r"movement speed penalty while reloading|wielding shields",
    ):
        return "weapon_handling_speed"

    if subtype == "movement speed" or "movement speed" in text or "combat movement" in text:
        if role == "captain" or matches(
            text,
            r"troops?|infantry|archers?|ranged|mounted|cavalry|formation|tier \d|foot",
        ):
            return "troop_combat_movement"
        return "personal_combat_movement"

    return None


def troop_classes(row: dict[str, Any]) -> list[str]:
    text = f"{row_effect_lower(row)} {row.get('game', {}).get('troop_usage', '')}".lower()
    classes: set[str] = set()
    restricted_scope = matches(
        text,
        r"infantry|foot troops?|footmen|on_foot|melee troops|archers?|ranged troops?|bow_user|"
        r"crossbow|thrown_user|throwing|cavalry|mounted troops?|mounted melee|horse archers?",
    )

    if "all troops" in text or (
        not restricted_scope
        and matches(text, r"\btroops in your formation\b|\btroops in your party\b|\btroops under your formation\b")
    ):
        classes.add("all_troops")
    if matches(text, r"infantry|foot troops?|footmen|on_foot|melee troops"):
        classes.add("infantry_or_foot")
    if "melee troops" in text:
        classes.add("melee")
    if matches(text, r"archers?|bow_user"):
        classes.update({"ranged", "archers"})
    if matches(text, r"ranged troops?|crossbow|bow|thrown_user|throwing weapons"):
        classes.add("ranged")
    if matches(text, r"crossbow"):
        classes.add("crossbow")
    if matches(text, r"throwing|thrown_user"):
        classes.add("throwing")
    if matches(text, r"cavalry|mounted troops?|mounted melee|mounts? of troops"):
        classes.update({"mounted", "cavalry"})
    if matches(text, r"horse archers?|mounted archers"):
        classes.update({"mounted", "ranged", "horse_archers"})
    if "garrison" in text:
        classes.add("garrison")
    if is_siege_text(text):
        classes.add("siege")

    return sorted(classes)


def troop_facing(row: dict[str, Any], classes: list[str]) -> bool:
    if classes:
        return True
    text = row_effect_lower(row)
    return row_role(row) == "captain" or matches(
        text,
        r"troops?|formation|infantry|archers?|ranged|mounted|cavalry|party|garrison|units?",
    )


def default_force_fit(row: dict[str, Any], classes: list[str], speed_kind: str | None) -> str:
    role = row_role(row)
    if role == "personal":
        return "personal only"
    if role == "governor" or "governed settlement" in row_triggers(row):
        return "governor/settlement only"
    if role == "army leader":
        return "army-only support"
    if "simulation" in row_triggers(row):
        return "simulation only"
    if "all_troops" in classes:
        return "all troops"
    if "infantry_or_foot" in classes or "melee" in classes:
        return "shock-infantry fit"
    if speed_kind == "campaign_party_speed":
        return "one-party mobility"
    if "ranged" in classes:
        return "ranged-specific"
    if "mounted" in classes or "cavalry" in classes:
        return "mounted-specific"
    if row_subtype(row) == "party size":
        return "one-party scaling"
    return "situational"


CORE_SUBTYPES = {
    "damage increase",
    "skill bonus",
    "attack speed",
    "reload speed",
    "ranged accuracy",
    "armor penetration",
    "shield damage",
    "morale damage",
    "ammo capacity",
}

STAYING_SUBTYPES = {
    "hit points",
    "armor",
    "damage resistance",
    "survival chance",
    "shield protection",
    "shield durability",
    "stagger resistance",
    "morale",
}

SCALING_SUBTYPES = {
    "party size",
    "wages",
    "recruitment",
    "prisoner recruitment",
    "food",
    "carrying capacity",
    "morale",
    "troop xp",
}


def doctrine_category(row: dict[str, Any], speed_kind: str | None, classes: list[str]) -> str:
    role = row_role(row)
    subtype = row_subtype(row)
    ptype = row_type(row)
    text = row_effect_lower(row)
    triggers = row_triggers(row)

    if role == "governor" or "governed settlement" in triggers or "simulation" in triggers:
        return "low_priority_misleading"
    if speed_kind in {"projectile_speed", "siege_speed", "personal_combat_movement", "weapon_handling_speed"}:
        return "low_priority_misleading"
    if role == "personal" and not classes:
        return "low_priority_misleading"
    if speed_kind == "troop_combat_movement":
        return "core_troop_lethality"
    if ptype == "troop combat" and subtype in STAYING_SUBTYPES:
        return "combat_staying_power"
    if ptype == "troop combat" and subtype in CORE_SUBTYPES:
        return "core_troop_lethality"
    if ptype == "troop combat" and matches(text, r"damage|skill|accuracy|armor penetration|shield"):
        return "core_troop_lethality"
    if subtype in STAYING_SUBTYPES and troop_facing(row, classes):
        return "combat_staying_power"
    if speed_kind == "campaign_party_speed":
        return "engagement_control"
    if subtype == "party size" or "party size" in text:
        return "party_scaling"
    if role in COMMANDER_ROLES and (subtype in SCALING_SUBTYPES or matches(text, r"food|wage|recruit|prisoner|carry|morale")):
        return "party_scaling"
    return "low_priority_misleading"


def value_rating(row: dict[str, Any], category: str, speed_kind: str | None, fit: str) -> str:
    subtype = row_subtype(row)
    role = row_role(row)
    text = row_effect_lower(row)

    if category == "low_priority_misleading":
        return "low"
    if category == "core_troop_lethality":
        if speed_kind == "troop_combat_movement" and fit in {"all troops", "shock-infantry fit"}:
            return "high"
        if fit in {"all troops", "shock-infantry fit"}:
            return "high"
        return "medium"
    if category == "combat_staying_power":
        if subtype in {"damage resistance", "armor", "shield protection"}:
            return "high"
        return "medium"
    if category == "engagement_control":
        if role in {"party leader", "scout", "surgeon"} and not matches(text, r"army|raid"):
            return "high"
        return "medium"
    if category == "party_scaling":
        if subtype == "party size" or "party size" in text:
            return "high"
        return "medium"
    return "low"


def comparison_note(
    row: dict[str, Any],
    speed_kind: str | None,
    alternatives_by_perk: dict[str, list[dict[str, Any]]],
) -> str:
    alt_id = str(row.get("alternative_perk_string_id", ""))
    if not alt_id:
        return ""

    alternatives = alternatives_by_perk.get(alt_id, [])
    alt_has_troop_hp = any(row_subtype(alt) == "hit points" and troop_facing(alt, troop_classes(alt)) for alt in alternatives)
    alt_has_troop_speed = any(classify_speed_kind(alt) == "troop_combat_movement" for alt in alternatives)

    if speed_kind == "troop_combat_movement" and alt_has_troop_hp:
        return (
            "Speed competes with a troop HP alternative here. For shock infantry, speed can be the scarcer "
            "multiplier because Medicine and resistance stacks already add a lot of survivability."
        )
    if row_subtype(row) == "hit points" and troop_facing(row, troop_classes(row)) and alt_has_troop_speed:
        return (
            "HP competes with a troop speed alternative here. Take HP when the formation already reaches contact "
            "reliably; otherwise speed may prevent more arrow exposure than the flat HP absorbs."
        )
    return ""


def record_notes(
    row: dict[str, Any],
    category: str,
    speed_kind: str | None,
    fit: str,
    comparison: str,
) -> list[str]:
    notes: list[str] = []
    subtype = row_subtype(row)
    role = row_role(row)

    if speed_kind == "troop_combat_movement":
        if fit in {"all troops", "shock-infantry fit"}:
            notes.append(
                "Shock-infantry multiplier: closes under fire faster, keeps melee pressure, and improves formation responsiveness."
            )
        else:
            notes.append(
                "Troop movement speed for this troop class; useful tactically, but not an infantry-wide mobility buff."
            )
    elif speed_kind == "campaign_party_speed":
        notes.append("Engagement-control perk: helps choose, refuse, or chase fights on the campaign map.")
    elif speed_kind == "projectile_speed":
        notes.append("Projectile travel speed, not party mobility or troop foot speed.")
    elif speed_kind == "weapon_handling_speed":
        notes.append("Weapon handling or personal reload/loadout movement; do not count as party mobility.")
    elif speed_kind == "siege_speed":
        notes.append("Siege-speed effect; useful in sieges but outside the default one-party shock-infantry doctrine.")

    if subtype == "hit points" and category == "combat_staying_power":
        notes.append("HP is useful, but it is easier to stack through Medicine than troop combat speed is.")
    if subtype == "party size":
        notes.append("Party size is always welcome, but larger parties are naturally slower, so it ranks after combat power and mobility.")
    if role == "army leader":
        notes.append("Army-leader effect; weaker fit for a single-party commander.")
    if "simulation" in row_triggers(row):
        notes.append("Simulation/autoresolve row, not live tactical combat.")
    if fit in {"ranged-specific", "mounted-specific"}:
        notes.append(f"{fit}; do not assume it buffs infantry.")
    if comparison:
        notes.append(comparison)

    return notes


def commander_candidate(row: dict[str, Any]) -> bool:
    role = row_role(row)
    subtype = row_subtype(row)
    ptype = row_type(row)
    text = row_effect_lower(row)
    speed_kind = classify_speed_kind(row)

    if role in COMMANDER_ROLES and (
        speed_kind
        or ptype in {"troop combat", "party management", "troop management"}
        or subtype in CORE_SUBTYPES
        or subtype in STAYING_SUBTYPES
        or subtype in SCALING_SUBTYPES
        or matches(text, r"party size|travel speed|party speed|recruit|wage|food|prisoner")
    ):
        return True

    if speed_kind in {
        "troop_combat_movement",
        "campaign_party_speed",
        "weapon_handling_speed",
        "projectile_speed",
        "siege_speed",
        "personal_combat_movement",
    }:
        return True

    if matches(text, r"damage bonus from speed|movement speed"):
        return True

    return False


def compact_record(row: dict[str, Any], alternatives_by_perk: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    speed_kind = classify_speed_kind(row)
    classes = troop_classes(row)
    fit = default_force_fit(row, classes, speed_kind)
    category = doctrine_category(row, speed_kind, classes)
    rating = value_rating(row, category, speed_kind, fit)
    comparison = comparison_note(row, speed_kind, alternatives_by_perk)
    game = row.get("game", {})
    classification = row.get("classification", {})

    return {
        "id": row.get("id", f"{row.get('perk_string_id', '')}|{row.get('effect_slot', '')}"),
        "skill": row.get("skill", ""),
        "level": row.get("level", 0),
        "perk": row.get("perk", ""),
        "perk_string_id": row.get("perk_string_id", ""),
        "effect_slot": row.get("effect_slot", ""),
        "alternative_perk_string_id": row.get("alternative_perk_string_id", ""),
        "role": game.get("role", ""),
        "bonus": game.get("bonus", 0),
        "increment_type": game.get("increment_type", ""),
        "troop_usage": game.get("troop_usage", ""),
        "perk_type": classification.get("perk_type", ""),
        "perk_subtype": classification.get("perk_subtype", ""),
        "trigger_conditions": classification.get("trigger_conditions", []),
        "effect_tags": classification.get("effect_tags", []),
        "effect": game.get("effect", ""),
        "speed_kind": speed_kind,
        "troop_classes": classes,
        "default_force_fit": fit,
        "doctrine_category": category,
        "value_rating": rating,
        "comparison_note": comparison,
        "notes": record_notes(row, category, speed_kind, fit, comparison),
    }


def record_sort_key(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        CATEGORY_ORDER.index(record["doctrine_category"]),
        RATING_ORDER.get(record["value_rating"], 9),
        0 if record["default_force_fit"] in {"all troops", "shock-infantry fit", "one-party mobility"} else 1,
        int(record.get("level", 0)),
        str(record.get("skill", "")),
        str(record.get("perk", "")),
        str(record.get("effect_slot", "")),
    )


def build_commander_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    alternatives_by_perk: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        alternatives_by_perk[str(row.get("perk_string_id", ""))].append(row)

    records = [compact_record(row, alternatives_by_perk) for row in rows if commander_candidate(row)]
    return sorted(records, key=record_sort_key)


def format_percent_from_factor(value: Any, force_plus: bool = False) -> str:
    try:
        percent = float(value) * 100.0
    except (TypeError, ValueError):
        return str(value)

    if abs(percent - round(percent)) < 1e-6:
        text = f"{round(percent):.0f}%"
    else:
        text = f"{percent:.4f}".rstrip("0").rstrip(".") + "%"
    if force_plus and not text.startswith("-"):
        return "+" + text
    return text


def add_factor_percent(record: dict[str, Any]) -> float:
    if record.get("increment_type") != "add_factor":
        return 0.0
    try:
        return float(record.get("bonus", 0)) * 100.0
    except (TypeError, ValueError):
        return 0.0


def add_value(record: dict[str, Any]) -> float:
    if record.get("increment_type") != "add":
        return 0.0
    try:
        return float(record.get("bonus", 0))
    except (TypeError, ValueError):
        return 0.0


def rounded(value: float, digits: int = 4) -> float:
    return round(value, digits)


def record_choice(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record.get("id", ""),
        "skill": record.get("skill", ""),
        "level": record.get("level", 0),
        "perk": record.get("perk", ""),
        "perk_string_id": record.get("perk_string_id", ""),
        "effect_slot": record.get("effect_slot", ""),
        "value": format_bonus(record),
        "bonus": record.get("bonus", 0),
        "increment_type": record.get("increment_type", ""),
        "perk_subtype": record.get("perk_subtype", ""),
        "doctrine_category": record.get("doctrine_category", ""),
        "fit": record.get("default_force_fit", ""),
        "speed_kind": record.get("speed_kind"),
        "effect": record.get("effect", ""),
    }


def useful_alternative_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ignored_fits = {"personal only", "governor/settlement only", "simulation only"}
    useful = [record for record in records if record.get("default_force_fit") not in ignored_fits]
    return useful or records


def banner_choice(banner_payload: dict[str, Any] | None, key: str) -> dict[str, Any]:
    meta = BANNER_COMPARISON_EFFECTS[key]
    choice = {
        "key": key,
        "effect": meta["effect"],
        "role": meta["role"],
        "summary": meta["summary"],
        "available": False,
    }
    if not banner_payload:
        return choice

    groups = {str(group.get("effect", "")): group for group in banner_payload.get("groups", [])}
    group = groups.get(meta["effect"])
    if not group:
        return choice

    tiers = sorted(group.get("tiers", []), key=lambda tier: int(tier.get("level", 0)))
    if not tiers:
        return choice
    top_tier = tiers[-1]
    top_level = int(top_tier.get("level", 0))
    top_items = [
        item
        for item in banner_payload.get("items", [])
        if item.get("effect") == meta["effect"] and int(item.get("banner_level", 0)) == top_level
    ]
    choice.update(
        {
            "available": True,
            "effect_name": group.get("effect_name", meta["effect"]),
            "tier": top_level,
            "bonus": top_tier.get("bonus", 0),
            "bonus_percent": rounded(float(top_tier.get("bonus", 0)) * 100.0),
            "display_bonus": top_tier.get("display_bonus", format_percent_from_factor(top_tier.get("bonus", 0))),
            "items": [str(item.get("name", item.get("id", ""))) for item in top_items],
        }
    )
    return choice


def banner_bonus_percent(choice: dict[str, Any]) -> float:
    if not choice.get("available"):
        return 0.0
    try:
        return float(choice.get("bonus", 0)) * 100.0
    except (TypeError, ValueError):
        return 0.0


def empty_metrics() -> dict[str, float]:
    return {key: 0.0 for key in PACKAGE_METRIC_KEYS}


def merge_metrics(target: dict[str, float], source: dict[str, float]) -> None:
    for key in PACKAGE_METRIC_KEYS:
        target[key] = target.get(key, 0.0) + source.get(key, 0.0)


def clean_metrics(metrics: dict[str, float]) -> dict[str, float]:
    return {key: rounded(value, 3) for key, value in metrics.items() if abs(value) > 1e-9}


def record_scope(record: dict[str, Any]) -> str:
    classes = set(record.get("troop_classes", []))
    fit = str(record.get("default_force_fit", ""))
    if "ranged" in classes and "infantry_or_foot" not in classes and "all_troops" not in classes:
        return "ranged"
    if "mounted" in classes and "all_troops" not in classes:
        return "mounted"
    if fit in {"all troops", "shock-infantry fit"} or classes & {"all_troops", "infantry_or_foot", "melee"}:
        return "infantry"
    return "other"


def record_package_metrics(record: dict[str, Any]) -> dict[str, float]:
    metrics = empty_metrics()
    subtype = str(record.get("perk_subtype", ""))
    text = str(record.get("effect", "")).lower()
    scope = record_scope(record)
    factor = add_factor_percent(record)
    value = add_value(record)

    if record.get("speed_kind") == "troop_combat_movement":
        if scope == "ranged":
            metrics["ranged_movement_percent"] += factor
        elif scope == "mounted":
            metrics["mounted_movement_percent"] += factor
        elif scope == "infantry":
            metrics["infantry_movement_percent"] += factor
    elif record.get("speed_kind") == "campaign_party_speed":
        metrics["campaign_speed_percent"] += abs(factor)

    if subtype == "hit points" and "mount" not in text:
        metrics["hit_points"] += value
    elif subtype == "armor":
        metrics["armor"] += value
    elif subtype == "party size":
        metrics["party_size"] += value
    elif subtype == "troop xp":
        metrics["troop_xp_percent"] += factor or value

    if subtype in {"damage resistance", "projectile protection"} or matches(text, r"damage taken from projectiles|ranged .*damage taken|damage from projectiles"):
        metrics["ranged_damage_taken_reduction_percent"] += abs(factor)
    if subtype in {"shield protection", "shield durability"} or matches(text, r"damage to shields?|shield damage"):
        if "damage" in text:
            metrics["shield_damage_reduction_percent"] += abs(factor)

    if subtype in {"damage increase", "melee", "shield damage", "armor penetration"}:
        if matches(text, r"bow|crossbow|ranged|projectile|arrow"):
            if subtype == "armor penetration":
                metrics["ranged_armor_penetration_percent"] += abs(factor)
            else:
                metrics["ranged_damage_percent"] += factor
        elif scope != "mounted":
            metrics["melee_damage_percent"] += factor
    if "damage and movement speed" in text and scope == "infantry" and subtype != "damage increase":
        metrics["melee_damage_percent"] += factor

    if subtype == "skill bonus":
        if matches(text, r"bow|crossbow|ranged|archers?"):
            metrics["ranged_skill_bonus"] += value
        elif matches(text, r"one handed|two handed|polearm|melee|infantry|troops"):
            metrics["melee_skill_bonus"] += value

    if subtype == "ranged accuracy" and factor < 0:
        metrics["ranged_accuracy_penalty_reduction_percent"] += abs(factor)

    return metrics


def banner_package_metrics(choice: dict[str, Any]) -> dict[str, float]:
    metrics = empty_metrics()
    if not choice.get("available"):
        return metrics
    percent = banner_bonus_percent(choice)
    effect = str(choice.get("effect", ""))
    if effect == "IncreasedTroopMovementSpeed":
        metrics["infantry_movement_percent"] += max(0.0, percent)
    elif effect == "IncreasedMountMovementSpeed":
        metrics["mounted_movement_percent"] += max(0.0, percent)
    elif effect == "DecreasedRangedAttackDamage":
        metrics["ranged_damage_taken_reduction_percent"] += abs(min(0.0, percent))
    elif effect == "DecreasedRangedAccuracyPenalty":
        metrics["weapon_inaccuracy_reduction_percent"] += abs(min(0.0, percent))
    elif effect == "IncreasedMeleeDamage":
        metrics["melee_damage_percent"] += max(0.0, percent)
    return metrics


def metrics_for_records(records: list[dict[str, Any]]) -> dict[str, float]:
    totals = empty_metrics()
    for record in records:
        merge_metrics(totals, record_package_metrics(record))
    return totals


def score_metrics(metrics: dict[str, float], weights: dict[str, float]) -> float:
    return sum(metrics.get(key, 0.0) * weight for key, weight in weights.items())


def score_records(records: list[dict[str, Any]], weights: dict[str, float]) -> float:
    return score_metrics(metrics_for_records(records), weights)


def choice_label(records: list[dict[str, Any]]) -> str:
    if not records:
        return ""
    first = records[0]
    return f"{first.get('skill', '')} {first.get('level', '')} - {first.get('perk', '')}"


def build_alternative_pair_sides(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records_by_perk: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        records_by_perk[str(record.get("perk_string_id", ""))].append(record)

    pairs = []
    seen: set[tuple[str, str]] = set()
    for record in records:
        alt_id = str(record.get("alternative_perk_string_id", ""))
        perk_id = str(record.get("perk_string_id", ""))
        if not alt_id or alt_id not in records_by_perk or not perk_id:
            continue
        pair_key = tuple(sorted([perk_id, alt_id]))
        if pair_key in seen:
            continue
        seen.add(pair_key)
        left = useful_alternative_records(records_by_perk.get(pair_key[0], []))
        right = useful_alternative_records(records_by_perk.get(pair_key[1], []))
        if not left or not right:
            continue
        pairs.append(
            {
                "key": "|".join(pair_key),
                "left_perk_string_id": pair_key[0],
                "right_perk_string_id": pair_key[1],
                "left_label": choice_label(left),
                "right_label": choice_label(right),
                "left_records": left,
                "right_records": right,
            }
        )
    return sorted(
        pairs,
        key=lambda pair: (
            int((pair["left_records"] or pair["right_records"])[0].get("level", 0)),
            str((pair["left_records"] or pair["right_records"])[0].get("skill", "")),
            pair["key"],
        ),
    )


def describe_metric_differences(chosen: dict[str, float], other: dict[str, float]) -> str:
    deltas = []
    labels = {
        "infantry_movement_percent": "infantry movement",
        "ranged_movement_percent": "ranged movement",
        "mounted_movement_percent": "mounted movement",
        "melee_damage_percent": "melee damage",
        "ranged_damage_percent": "ranged damage",
        "ranged_armor_penetration_percent": "ranged armor penetration",
        "ranged_accuracy_penalty_reduction_percent": "accuracy penalty reduction",
        "melee_skill_bonus": "melee skill",
        "ranged_skill_bonus": "ranged skill",
        "hit_points": "HP",
        "armor": "armor",
        "ranged_damage_taken_reduction_percent": "ranged damage reduction",
        "shield_damage_reduction_percent": "shield damage reduction",
        "party_size": "party size",
    }
    for key, label in labels.items():
        delta = chosen.get(key, 0.0) - other.get(key, 0.0)
        if abs(delta) < 1e-9:
            continue
        sign = "+" if delta > 0 else ""
        suffix = "" if key in {"hit_points", "armor", "party_size", "melee_skill_bonus", "ranged_skill_bonus"} else "%"
        deltas.append(f"{sign}{rounded(delta, 2):g}{suffix} {label}")
    return "; ".join(deltas[:4])


def build_banner_package_simulation(
    records: list[dict[str, Any]],
    banner_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    pairs = build_alternative_pair_sides(records)
    packages: dict[str, Any] = {}

    for package_key, definition in PACKAGE_DEFINITIONS.items():
        weights = definition["weights"]
        banner = banner_choice(banner_payload, definition["banner_key"])
        totals = banner_package_metrics(banner)
        choices = []

        for pair in pairs:
            left_records = pair["left_records"]
            right_records = pair["right_records"]
            left_metrics = metrics_for_records(left_records)
            right_metrics = metrics_for_records(right_records)
            left_score = score_metrics(left_metrics, weights)
            right_score = score_metrics(right_metrics, weights)
            if right_score > left_score:
                chosen_side = "right"
                chosen_records = right_records
                other_records = left_records
                chosen_metrics = right_metrics
                other_metrics = left_metrics
                chosen_score = right_score
                other_score = left_score
            else:
                chosen_side = "left"
                chosen_records = left_records
                other_records = right_records
                chosen_metrics = left_metrics
                other_metrics = right_metrics
                chosen_score = left_score
                other_score = right_score

            merge_metrics(totals, chosen_metrics)
            choices.append(
                {
                    "pair_key": pair["key"],
                    "chosen_side": chosen_side,
                    "chosen_label": choice_label(chosen_records),
                    "other_label": choice_label(other_records),
                    "chosen_perk_string_id": str(chosen_records[0].get("perk_string_id", "")),
                    "other_perk_string_id": str(other_records[0].get("perk_string_id", "")),
                    "score_delta": rounded(chosen_score - other_score, 3),
                    "chosen_metrics": clean_metrics(chosen_metrics),
                    "other_metrics": clean_metrics(other_metrics),
                    "summary": describe_metric_differences(chosen_metrics, other_metrics),
                    "chosen_records": [record_choice(record) for record in chosen_records],
                    "other_records": [record_choice(record) for record in other_records],
                }
            )

        packages[package_key] = {
            "key": package_key,
            "title": definition["title"],
            "doctrine": definition["doctrine"],
            "banner": banner,
            "banner_application": accuracy_banner_application() if definition["banner_key"] == "archer_accuracy" else None,
            "metrics": clean_metrics(totals),
            "choices": choices,
        }

    speed_choices = {
        choice["pair_key"]: choice["chosen_perk_string_id"]
        for choice in packages["shock_speed"]["choices"]
    }
    speed_metrics = packages["shock_speed"]["metrics"]
    for package_key, package in packages.items():
        differences = []
        for choice in package["choices"]:
            speed_pick = speed_choices.get(choice["pair_key"])
            if speed_pick and speed_pick != choice["chosen_perk_string_id"]:
                differences.append(choice)
        package["differences_from_shock_speed"] = differences
        package["delta_vs_shock_speed"] = clean_metrics(
            {
                key: float(package["metrics"].get(key, 0.0)) - float(speed_metrics.get(key, 0.0))
                for key in PACKAGE_METRIC_KEYS
            }
        )

    return {
        "assumptions": [
            "This is a deterministic scoring model over extracted commander-relevant perk alternatives, not a battle simulator.",
            "The full chosen perk set is stored in JSON. The markdown focuses on package totals and choices that differ from the shock-speed package.",
            "Banner bonuses are added as package metrics: infantry speed, ranged damage reduction, weapon inaccuracy reduction, or melee damage.",
            "The archer accuracy banner applies to WeaponInaccuracy, so the model treats it as base inaccuracy reduction rather than direct hit chance.",
        ],
        "accuracy_banner_application": accuracy_banner_application(),
        "packages": packages,
    }


def accuracy_banner_application() -> dict[str, Any]:
    return {
        "effect": "DecreasedRangedAccuracyPenalty",
        "method": "SandBox.GameComponents.SandboxAgentStatCalculateModel.SetPerkAndBannerEffectsOnAgent",
        "applied_to": "AgentDrivenProperties.WeaponInaccuracy",
        "mechanical_read": (
            "The banner bonus is added to the WeaponInaccuracy ExplainedNumber and then written back with "
            "set_WeaponInaccuracy. Tier 3 is -8%, so it should multiply the base inaccuracy/spread component by about 0.92."
        ),
        "not_applied_to": [
            "WeaponMaxMovementAccuracyPenalty",
            "WeaponMaxUnsteadyAccuracyPenalty",
            "WeaponRotationalAccuracyPenaltyInRadians",
            "direct hit chance",
        ],
        "evidence": [
            "IL calls DefaultBannerEffects.get_DecreasedRangedAccuracyPenalty().",
            "The banner is added to local WeaponInaccuracy explained number.",
            "The result is assigned through AgentDrivenProperties.set_WeaponInaccuracy().",
        ],
        "practical_read": (
            "Helpful when raw spread is the limiting factor for many ranged troops firing often, but weaker than it looks "
            "if misses are mostly movement, rotation, target motion, range, projectile travel, line of sight, or AI timing."
        ),
    }


def build_payload(workspace: Path, perk_export_path: Path) -> dict[str, Any]:
    rows = read_json(perk_export_path)
    records = build_commander_records(rows)
    banner_path = workspace / "Data" / "raw" / "banner-items.json"
    banner_payload = read_json(banner_path) if banner_path.exists() else None
    category_counts = Counter(record["doctrine_category"] for record in records)
    rating_counts = Counter(record["value_rating"] for record in records)
    inputs = {"perk_export": display_path(perk_export_path, workspace)}
    if banner_path.exists():
        inputs["banner_items"] = display_path(banner_path, workspace)

    return {
        "generated_at": datetime.now().astimezone().isoformat(),
        "inputs": inputs,
        "doctrine": {
            "target": "Elite shock-infantry-heavy one-party army.",
            "priority_order": [
                "Maximize live combat power per troop, including lethal output and enough staying power to keep elites alive.",
                "Preserve engagement control so the party can choose fights.",
                "Scale party size after the force can still catch worthwhile targets.",
            ],
            "speed_note": (
                "Troop combat movement speed is a core combat stat for shock infantry, not generic mobility: "
                "it reduces ranged exposure, forces contact, and improves battlefield responsiveness."
            ),
        },
        "category_meta": CATEGORY_META,
        "speed_kind_descriptions": SPEED_KIND_DESCRIPTIONS,
        "summary": {
            "total_records": len(records),
            "category_counts": dict(category_counts),
            "rating_counts": dict(rating_counts),
        },
        "banner_package_simulation": build_banner_package_simulation(records, banner_payload),
        "records": records,
    }


def format_bonus(record: dict[str, Any]) -> str:
    bonus = record.get("bonus")
    try:
        value = float(bonus)
    except (TypeError, ValueError):
        return str(bonus)

    if record.get("increment_type") == "add_factor":
        value *= 100
        text = f"{value:.4f}".rstrip("0").rstrip(".")
        return f"{text}%"

    if value.is_integer():
        return str(int(value))
    return f"{value:.4f}".rstrip("0").rstrip(".")


def write_record_table(lines: list[str], records: list[dict[str, Any]]) -> None:
    lines.extend(
        [
            "| Rating | Skill | Level | Perk | Role | Fit | Speed kind | Bonus | Effect | Notes |",
            "| --- | --- | ---: | --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for record in records:
        notes = " ".join(record.get("notes", []))
        speed_kind = record.get("speed_kind") or ""
        lines.append(
            "| {rating} | {skill} | {level} | {perk} | {role} | {fit} | {speed} | {bonus} | {effect} | {notes} |".format(
                rating=table_escape(record["value_rating"]),
                skill=table_escape(record["skill"]),
                level=record["level"],
                perk=table_escape(record["perk"]),
                role=table_escape(record["role"]),
                fit=table_escape(record["default_force_fit"]),
                speed=table_escape(speed_kind),
                bonus=table_escape(format_bonus(record)),
                effect=table_escape(record["effect"]),
                notes=table_escape(notes),
            )
        )
    lines.append("")


def format_banner_cell(choice: dict[str, Any]) -> str:
    if not choice.get("available"):
        return f"{choice.get('effect', '')} (run extract-banners)"
    items = ", ".join(choice.get("items", []))
    return "{effect} T{tier} ({bonus}) - {items}".format(
        effect=choice.get("effect_name", choice.get("effect", "")),
        tier=choice.get("tier", ""),
        bonus=choice.get("display_bonus", ""),
        items=items,
    )


def display_metric(metrics: dict[str, Any], key: str, suffix: str = "%") -> str:
    value = float(metrics.get(key, 0) or 0)
    if abs(value) < 1e-9:
        return ""
    return f"{value:g}{suffix}"


def display_signed_metric(metrics: dict[str, Any], key: str, suffix: str = "%") -> str:
    value = float(metrics.get(key, 0) or 0)
    if abs(value) < 1e-9:
        return ""
    sign = "+" if value > 0 else ""
    return f"{sign}{value:g}{suffix}"


def package_read(package_key: str, package: dict[str, Any]) -> str:
    delta = package.get("delta_vs_shock_speed", {})
    if package_key == "shock_speed":
        return "Baseline package for this comparison."
    if package_key == "anti_arrow":
        return (
            "Trades speed and some damage for a much larger ranged-damage, HP, and shield package."
        )
    if package_key == "archer_accuracy":
        return (
            "Real but specialized: adds base inaccuracy reduction and ranged accuracy perks, while giving up most shock-infantry priorities."
        )
    if package_key == "melee_damage":
        movement_loss = abs(float(delta.get("infantry_movement_percent", 0)))
        damage_gain = float(delta.get("melee_damage_percent", 0))
        return (
            f"Mostly the same perk package as shock speed, but swaps about {movement_loss:g}% infantry movement for {damage_gain:g}% melee damage."
        )
    return ""


def write_package_simulation_markdown(payload: dict[str, Any], path: Path, workspace: Path, json_output: Path) -> None:
    simulation = payload["banner_package_simulation"]
    packages = simulation["packages"]
    accuracy = simulation["accuracy_banner_application"]

    lines = [
        "# Commander Banner Package Comparison",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This report scores full commander-relevant perk alternative sets around each major banner option. It is a package model over extracted perk rows, not a battle simulator.",
        "",
        "Banner mechanics are confirmed in the generated [banner effects reference](banner-effects.md); use that as the source of truth for what each banner modifies before interpreting these package totals.",
        "",
        "## Inputs",
        "",
        f"- Commander JSON: `{display_path(json_output, workspace)}`",
    ]
    for label, input_path in payload.get("inputs", {}).items():
        lines.append(f"- {label}: `{input_path}`")

    lines.extend(
        [
            "",
            "## Package Totals",
            "",
            "| Package | Banner | Infantry movement | Melee damage | Ranged damage taken | Weapon inaccuracy | Accuracy penalty | HP | Shield damage | Differing picks vs speed |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for package_key in PACKAGE_DEFINITIONS:
        package = packages[package_key]
        metrics = package["metrics"]
        lines.append(
            "| {title} | {banner} | {move} | {melee} | {ranged_resist} | {inaccuracy} | {accuracy} | {hp} | {shield} | {diffs} |".format(
                title=table_escape(package["title"]),
                banner=table_escape(format_banner_cell(package["banner"])),
                move=table_escape(display_metric(metrics, "infantry_movement_percent")),
                melee=table_escape(display_metric(metrics, "melee_damage_percent")),
                ranged_resist=table_escape(display_metric(metrics, "ranged_damage_taken_reduction_percent")),
                inaccuracy=table_escape(display_metric(metrics, "weapon_inaccuracy_reduction_percent")),
                accuracy=table_escape(display_metric(metrics, "ranged_accuracy_penalty_reduction_percent")),
                hp=table_escape(display_metric(metrics, "hit_points", "")),
                shield=table_escape(display_metric(metrics, "shield_damage_reduction_percent")),
                diffs=len(package.get("differences_from_shock_speed", [])),
            )
        )

    lines.extend(
        [
            "",
            "## Delta vs Shock Speed",
            "",
            "| Package | Infantry movement | Melee damage | Ranged damage taken | Weapon inaccuracy | Accuracy penalty | HP | Shield damage | Read |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for package_key in PACKAGE_DEFINITIONS:
        if package_key == "shock_speed":
            continue
        package = packages[package_key]
        delta = package.get("delta_vs_shock_speed", {})
        lines.append(
            "| {title} | {move} | {melee} | {ranged_resist} | {inaccuracy} | {accuracy} | {hp} | {shield} | {read} |".format(
                title=table_escape(package["title"]),
                move=table_escape(display_signed_metric(delta, "infantry_movement_percent")),
                melee=table_escape(display_signed_metric(delta, "melee_damage_percent")),
                ranged_resist=table_escape(display_signed_metric(delta, "ranged_damage_taken_reduction_percent")),
                inaccuracy=table_escape(display_signed_metric(delta, "weapon_inaccuracy_reduction_percent")),
                accuracy=table_escape(display_signed_metric(delta, "ranged_accuracy_penalty_reduction_percent")),
                hp=table_escape(display_signed_metric(delta, "hit_points", "")),
                shield=table_escape(display_signed_metric(delta, "shield_damage_reduction_percent")),
                read=table_escape(package_read(package_key, package)),
            )
        )

    lines.extend(
        [
            "",
            "## Accuracy Banner Mechanics",
            "",
            f"- Effect: `{accuracy['effect']}`",
            f"- Applied in: `{accuracy['method']}`",
            f"- Applied to: `{accuracy['applied_to']}`",
            f"- Mechanical read: {accuracy['mechanical_read']}",
            f"- Practical read: {accuracy['practical_read']}",
            "- Not applied to: " + ", ".join(f"`{item}`" for item in accuracy["not_applied_to"]),
            "",
            "That makes the tier 3 accuracy banner real, but narrow: it reduces base weapon inaccuracy/spread by 8%. It does not directly grant 8% hit chance, and it does not reduce the movement, unsteady, or rotational penalty properties that several personal/captain perks touch.",
            "",
            "## Pick Differences vs Shock Speed",
            "",
            "Only choices that differ from the shock-speed package are shown here. The full selected side for every commander-relevant alternative pair is in the JSON output.",
            "",
        ]
    )

    for package_key in PACKAGE_DEFINITIONS:
        if package_key == "shock_speed":
            continue
        package = packages[package_key]
        lines.extend(
            [
                f"### {package['title']}",
                "",
                package["doctrine"],
                "",
            ]
        )
        differences = package.get("differences_from_shock_speed", [])
        if not differences:
            lines.extend(["No perk alternative changes from the shock-speed package.", ""])
            continue
        lines.extend(
            [
                "| Package pick | Shock-speed pick | Why the package flips it |",
                "| --- | --- | --- |",
            ]
        )
        for choice in differences:
            lines.append(
                "| {chosen} | {other} | {summary} |".format(
                    chosen=table_escape(choice.get("chosen_label", "")),
                    other=table_escape(choice.get("other_label", "")),
                    summary=table_escape(choice.get("summary", "")),
                )
            )
        lines.append("")

    lines.extend(["## Assumptions", ""])
    for assumption in simulation.get("assumptions", []):
        lines.append(f"- {assumption}")
    lines.append("- Non-alternative perks common to every package are not re-listed in the markdown comparison.")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_markdown(payload: dict[str, Any], path: Path, workspace: Path, json_output: Path) -> None:
    lines = [
        "# Commander Perks Report",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This generated report is tuned for an elite one-party commander build: first make every troop as lethal as possible, then keep enough campaign speed to choose fights, then add party size once the force can still catch worthwhile targets.",
        "",
        "> [!NOTE]",
        "> Troop combat movement speed is ranked as core combat power for shock infantry. Closing faster means less arrow exposure, better melee contact, better formation response, and faster cleanup. Small HP gains remain useful, but Medicine and resistance stacking make HP easier to find than movement speed.",
        "",
        "## Speed Kind Legend",
        "",
        "| Speed kind | Meaning |",
        "| --- | --- |",
    ]
    for key, description in SPEED_KIND_DESCRIPTIONS.items():
        lines.append(f"| `{key}` | {table_escape(description)} |")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Records: {payload['summary']['total_records']}",
            "- Doctrine order: core troop lethality, combat staying power, engagement control, party scaling.",
            "- Low-priority rows are retained when they are common keyword traps, such as projectile travel speed or personal reload movement.",
            "",
            "| Category | Rows | Purpose |",
            "| --- | ---: | --- |",
        ]
    )
    category_counts = payload["summary"]["category_counts"]
    for key in CATEGORY_ORDER:
        meta = CATEGORY_META[key]
        lines.append(f"| {meta['title']} | {category_counts.get(key, 0)} | {table_escape(meta['description'])} |")

    records_by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in payload["records"]:
        records_by_category[record["doctrine_category"]].append(record)

    for key in CATEGORY_ORDER:
        meta = CATEGORY_META[key]
        lines.extend(["", f"## {meta['title']}", "", meta["description"], ""])
        write_record_table(lines, records_by_category.get(key, []))

    lines.extend(
        [
            "## Outputs",
            "",
            f"- JSON: `{display_path(json_output, workspace)}`",
            f"- Report: `{display_path(path, workspace)}`",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def extract_commander_perks(
    workspace: Path,
    perk_export_path: Path,
    json_output: Path,
    markdown_output: Path,
    package_output: Path | None = None,
) -> None:
    if package_output is None:
        package_output = workspace / "Docs" / "reports" / "commander-banner-package-comparison.md"
    payload = build_payload(workspace, perk_export_path)
    write_json(json_output, payload)
    write_markdown(payload, markdown_output, workspace, json_output)
    write_package_simulation_markdown(payload, package_output, workspace, json_output)
    print(f"Commander perk JSON written: {json_output}")
    print(f"Commander perk report written: {markdown_output}")
    print(f"Commander banner package comparison written: {package_output}")
    for key in CATEGORY_ORDER:
        print(f"  {key}: {payload['summary']['category_counts'].get(key, 0)} rows")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract doctrine-ranked commander perk reports.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--perk-export", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    parser.add_argument("--package-output", type=Path, default=None)
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    perk_export_path = args.perk_export or workspace / "Data" / "export" / "perk-effects.json"
    json_output = args.json_output or workspace / "Data" / "intermediate" / "commander_perks_extracted.json"
    markdown_output = args.markdown_output or workspace / "Data" / "intermediate" / "commander_perks_report.txt"
    package_output = args.package_output or workspace / "Docs" / "reports" / "commander-banner-package-comparison.md"
    extract_commander_perks(
        workspace=workspace,
        perk_export_path=perk_export_path.resolve(),
        json_output=json_output,
        markdown_output=markdown_output,
        package_output=package_output,
    )


if __name__ == "__main__":
    main()
