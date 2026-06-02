from __future__ import annotations

import argparse
import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from .postprocess import default_workspace
    from .xp_reports import display_path, table_escape
except ImportError:
    from postprocess import default_workspace
    from xp_reports import display_path, table_escape


NORMAL_AI_FACTOR = 0.96 / 300.0


DIRECT_WEAPON_EFFECTS = [
    {
        "skill": "One Handed",
        "effects": "weapon speed, weapon damage",
        "per_skill": {"speed_pct": 0.07, "damage_pct": 0.15},
    },
    {
        "skill": "Two Handed",
        "effects": "weapon speed, weapon damage",
        "per_skill": {"speed_pct": 0.06, "damage_pct": 0.16},
    },
    {
        "skill": "Polearm",
        "effects": "weapon speed, weapon damage",
        "per_skill": {"speed_pct": 0.06, "damage_pct": 0.07},
    },
    {
        "skill": "Bow",
        "effects": "damage, accuracy",
        "per_skill": {"damage_pct": 0.11, "accuracy_effect_pct": 0.09},
    },
    {
        "skill": "Crossbow",
        "effects": "reload speed, accuracy",
        "per_skill": {"reload_pct": 0.07, "accuracy_effect_pct": 0.05},
    },
    {
        "skill": "Throwing",
        "effects": "ready speed, damage, accuracy",
        "per_skill": {"ready_speed_pct": 0.07, "damage_pct": 0.06, "accuracy_effect_pct": 0.06},
    },
]


AI_BEHAVIOR_FORMULAS = [
    {
        "key": "ai_level",
        "track": "base",
        "formula": "clamp(effectiveSkill / 300 * difficultyFactor * AILevelMultiplier, 0, 1)",
        "normal_high_difficulty": "difficultyFactor = 0.96",
    },
    {"key": "AiShootFreq", "track": "ranged", "formula": "0.3 + 0.7 * currentAI", "shape": "linear"},
    {
        "key": "AiWaitBeforeShootFactor",
        "track": "ranged",
        "formula": "1 - 0.5 * currentAI",
        "shape": "linear reduction",
    },
    {
        "key": "AIBlockOnDecideAbility",
        "track": "melee",
        "formula": "lerp(0.5, 0.99, sqrt(meleeAI))",
        "shape": "diminishing",
    },
    {
        "key": "AIParryOnDecideAbility",
        "track": "melee",
        "formula": "lerp(0.5, 0.95, meleeAI)",
        "shape": "linear",
    },
    {
        "key": "AIDecideOnRealizeEnemyBlockingAttackAbility",
        "track": "melee",
        "formula": "clamp(meleeAI^2.5 - 0.1, 0, 1)",
        "shape": "high-skill weighted",
    },
    {
        "key": "AIRealizeBlockingFromIncorrectSideAbility",
        "track": "melee",
        "formula": "clamp(meleeAI^2.5 - 0.01, 0, 1)",
        "shape": "high-skill weighted",
    },
    {
        "key": "AiRandomizedDefendDirectionChance",
        "track": "melee",
        "formula": "1 - meleeAI^3",
        "shape": "high-skill mistake reduction",
    },
    {
        "key": "AiUseShieldAgainstEnemyMissileProbability",
        "track": "shield",
        "formula": "0.1 + 0.6 * meleeAI + 0.2 * (meleeAI + defensiveness)",
        "shape": "linear plus defensiveness",
    },
]


SMITHING_FORMULAS = [
    {"key": "refining_xp", "formula": "round(0.3 * outputMaterialValue * outputCount)"},
    {"key": "smelting_xp", "formula": "round(0.02 * itemValue)"},
    {"key": "crafting_order_xp", "formula": "round(0.1 * itemValue)"},
    {"key": "free_build_xp", "formula": "round(0.02 * itemValue)"},
    {"key": "crafting_order_base_experience", "formula": "0.25 * theoreticalMaxItemMarketValue(requestedDesignItem)"},
]


SURVIVAL_FORMULAS = [
    {
        "key": "regular_troop_death_chance",
        "formula": "deathChance = 1 / ((1 + medicine * 0.01 * eventMultiplier + troopLevel * 0.02 + additiveBonuses) * (1 + factorBonuses))",
        "notes": [
            "Player map event eventMultiplier is 1.0.",
            "Non-player map event eventMultiplier is 0.25.",
            "Medicine is capped at 330 for player-facing skill.",
        ],
    },
    {
        "key": "minister_of_health_max_hp",
        "formula": "maxBonus = max(0, medicineSkill - 250), capped by max skill 330 => +80 HP",
    },
]


@dataclass(frozen=True)
class PerkRef:
    perk_string_id: str
    effect_slot: str
    effective_bonus: float | None = None
    note: str = ""


@dataclass(frozen=True)
class GuideStack:
    key: str
    title: str
    metric: str
    components: tuple[PerkRef, ...]
    note: str


@dataclass(frozen=True)
class GuideBucket:
    key: str
    title: str
    description: str
    predicate: Callable[[dict[str, Any]], bool]


AI_SKILL_STACKS = [
    GuideStack(
        key="foot_polearm_shield_wall",
        title="Foot Polearm Shield Wall",
        metric="Polearm skill",
        components=(
            PerkRef("PolearmCleanThrust", "secondary"),
            PerkRef("PolearmCounterweight", "secondary"),
            PerkRef("PolearmPhalanx", "primary"),
        ),
        note="Strongest clean melee-AI skill stack found so far.",
    ),
    GuideStack(
        key="foot_one_handed_shield_wall",
        title="Foot One-Handed Shield Wall",
        metric="One Handed skill",
        components=(PerkRef("OneHandedWrappedHandles", "secondary"), PerkRef("PolearmPhalanx", "primary")),
        note="Feeds melee reactions and shield AI.",
    ),
    GuideStack(
        key="foot_two_handed_shield_wall",
        title="Foot Two-Handed Shield Wall",
        metric="Two Handed skill",
        components=(PerkRef("TwoHandedStrongGrip", "secondary"), PerkRef("PolearmPhalanx", "primary")),
        note="Offensive melee-AI stack; no shield-specific defensive payoff.",
    ),
    GuideStack(
        key="horse_archers",
        title="Horse Archers",
        metric="Bow skill",
        components=(PerkRef("BowDeadAim", "secondary"), PerkRef("BowHorseMaster", "secondary")),
        note="Improves ranged AI plus bow damage and accuracy.",
    ),
    GuideStack(
        key="throwing_infantry",
        title="Throwing Infantry",
        metric="Throwing skill",
        components=(
            PerkRef("ThrowingFlexibleFighter", "secondary"),
            PerkRef("AthleticsStrongArms", "secondary"),
            PerkRef("ThrowingRunningThrow", "secondary"),
        ),
        note="Strong javelin-infantry stack; Flexible Fighter is category-sensitive.",
    ),
]


HP_STACKS = [
    GuideStack(
        key="any_regular_troop_hp",
        title="Any Regular Troop HP",
        metric="flat HP",
        components=(
            PerkRef("MedicineMinisterOfHealth", "primary", effective_bonus=80, note="Medicine 330"),
            PerkRef("PolearmHardyFrontline", "primary"),
            PerkRef("TwoHandedThickHides", "secondary"),
        ),
        note="Baseline broad troop HP stack.",
    ),
    GuideStack(
        key="foot_infantry_hp",
        title="Foot Infantry HP",
        metric="flat HP",
        components=(
            PerkRef("MedicineMinisterOfHealth", "primary", effective_bonus=80, note="Medicine 330"),
            PerkRef("PolearmHardyFrontline", "primary"),
            PerkRef("TwoHandedThickHides", "secondary"),
            PerkRef("AthleticsWellBuilt", "secondary"),
            PerkRef("OneHandedUnwaveringDefense", "secondary"),
            PerkRef("PolearmHardKnock", "secondary"),
        ),
        note="Largest flat regular troop HP stack from the current guide set.",
    ),
    GuideStack(
        key="foot_ranged_hp",
        title="Foot Ranged HP",
        metric="flat HP",
        components=(
            PerkRef("MedicineMinisterOfHealth", "primary", effective_bonus=80, note="Medicine 330"),
            PerkRef("PolearmHardyFrontline", "primary"),
            PerkRef("TwoHandedThickHides", "secondary"),
            PerkRef("AthleticsWellBuilt", "secondary"),
            PerkRef("CrossbowBoltenGuard", "secondary"),
        ),
        note="Uses Picked Shots, whose string id is CrossbowBoltenGuard in the extracted data.",
    ),
    GuideStack(
        key="troop_mount_hp",
        title="Troop Mount HP",
        metric="mixed mount HP",
        components=(PerkRef("MedicineSledges", "secondary"), PerkRef("RidingVeterinary", "secondary")),
        note="Flat mount HP and percentage mount HP are kept as separate component types.",
    ),
]


ARMOR_STACKS = [
    GuideStack(
        key="any_troop_armor",
        title="Any Troop Armor",
        metric="armor per equipped armor piece",
        components=(PerkRef("EngineeringMetallurgy", "secondary"),),
        note="Broad captain armor layer.",
    ),
    GuideStack(
        key="foot_troop_armor",
        title="Foot Troop Armor",
        metric="armor per equipped armor piece",
        components=(PerkRef("EngineeringMetallurgy", "secondary"), PerkRef("AthleticsIgnorePain", "secondary")),
        note="Best foot-troop armor stack in the current guide set.",
    ),
    GuideStack(
        key="mounted_rider_armor",
        title="Mounted Rider Armor",
        metric="armor per equipped armor piece",
        components=(PerkRef("EngineeringMetallurgy", "secondary"), PerkRef("RidingDauntlessSteed", "secondary")),
        note="Best rider armor stack for mounted troops.",
    ),
    GuideStack(
        key="troop_mount_armor",
        title="Troop Mount Armor",
        metric="mount armor",
        components=(PerkRef("RidingToughSteed", "secondary"),),
        note="Mount armor, not rider armor.",
    ),
]


RESISTANCE_STACKS = [
    GuideStack(
        key="melee_infantry_vs_projectiles",
        title="Melee Infantry Vs Projectiles",
        metric="listed damage taken factors",
        components=(PerkRef("ThrowingSkirmisher", "secondary"), PerkRef("TacticsEliteReserves", "secondary")),
        note="Does not include Skirmish Phase Master because that is ranged-troop scoped.",
    ),
    GuideStack(
        key="bow_ranged_vs_projectiles",
        title="Bow Ranged Troops Vs Projectiles",
        metric="listed damage taken factors",
        components=(
            PerkRef("BowSkirmishPhaseMaster", "secondary"),
            PerkRef("ThrowingSkirmisher", "secondary"),
            PerkRef("TacticsEliteReserves", "secondary"),
        ),
        note="Counter Fire is not included because the live damage code is crossbow-current-weapon gated.",
    ),
    GuideStack(
        key="crossbow_vs_projectiles",
        title="Crossbow Troops Vs Projectiles",
        metric="listed damage taken factors",
        components=(
            PerkRef("BowSkirmishPhaseMaster", "secondary"),
            PerkRef("CrossbowCounterFire", "secondary"),
            PerkRef("ThrowingSkirmisher", "secondary"),
            PerkRef("TacticsEliteReserves", "secondary"),
        ),
        note="Assumes the victim is holding a crossbow for Counter Fire.",
    ),
    GuideStack(
        key="charge_damage_to_formation",
        title="Charge Damage To Formation",
        metric="listed charge damage factors",
        components=(PerkRef("AthleticsBraced", "secondary"), PerkRef("PolearmSureFooted", "secondary")),
        note="Charge-specific layer.",
    ),
]


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def row_key(row: dict[str, Any]) -> str:
    return f"{row.get('perk_string_id', '')}|{row.get('effect_slot', '')}"


def row_effect(row: dict[str, Any]) -> str:
    return str(row.get("game", {}).get("effect", ""))


def row_subtype(row: dict[str, Any]) -> str:
    return str(row.get("classification", {}).get("perk_subtype", ""))


def row_type(row: dict[str, Any]) -> str:
    return str(row.get("classification", {}).get("perk_type", ""))


def has_troop_scope(row: dict[str, Any]) -> bool:
    text = f"{row_effect(row)} {row.get('game', {}).get('troop_usage', '')}".lower()
    return bool(
        re.search(
            r"troops?|infantry|archers?|ranged|mounted|cavalry|formation|party|mounts?|units?|tier \d|garrison",
            text,
        )
    )


def is_troop_facing(row: dict[str, Any]) -> bool:
    text = row_effect(row).lower()
    if re.search(r"\byour mount\b", text) and not re.search(r"troops?|party|formation", text):
        return False
    return bool(
        re.search(
            r"troops?|infantry|archers?|ranged troops?|mounted troops?|cavalry|formation|units?|tier \d|garrison|"
            r"mounts? (?:of troops|in your party)",
            text,
        )
    )


def is_defensive_survival_effect(row: dict[str, Any]) -> bool:
    text = row_effect(row).lower()
    if re.search(r"damage dealt|damage by|charge damage dealt|morale", text):
        return False
    return bool(
        re.search(
            r"damage taken|less damage|damage to shields?|shield protection|charge damage taken|projectiles?|"
            r"ranged attacks?|sent to confront",
            text,
        )
    )


def compact_perk_row(row: dict[str, Any]) -> dict[str, Any]:
    game = row.get("game", {})
    classification = row.get("classification", {})
    return {
        "id": row_key(row),
        "skill": row.get("skill", ""),
        "level": row.get("level", 0),
        "perk": row.get("perk", ""),
        "effect_slot": row.get("effect_slot", ""),
        "role": game.get("role", ""),
        "bonus": game.get("bonus", 0),
        "increment_type": game.get("increment_type", ""),
        "troop_usage": game.get("troop_usage", ""),
        "perk_type": classification.get("perk_type", ""),
        "perk_subtype": classification.get("perk_subtype", ""),
        "trigger_conditions": classification.get("trigger_conditions", []),
        "effect_tags": classification.get("effect_tags", []),
        "effect": game.get("effect", ""),
    }


def guide_buckets() -> list[GuideBucket]:
    return [
        GuideBucket(
            key="troop_ai_skill_bonuses",
            title="Troop AI Skill Bonus Perks",
            description="Perks that add effective skills to troops and can feed AI formulas when the troop uses that skill.",
            predicate=lambda row: row_subtype(row) == "skill bonus" and has_troop_scope(row),
        ),
        GuideBucket(
            key="troop_survival_hit_points",
            title="Troop Hit Point Perks",
            description="Troop- or mount-facing hit point perks used by the survivability guide.",
            predicate=lambda row: row_subtype(row) == "hit points" and is_troop_facing(row),
        ),
        GuideBucket(
            key="troop_survival_armor",
            title="Troop Armor Perks",
            description="Troop- or mount-facing armor perks used by the survivability guide.",
            predicate=lambda row: row_subtype(row) == "armor increase" and is_troop_facing(row),
        ),
        GuideBucket(
            key="troop_survival_damage_reduction",
            title="Troop Damage Reduction And Shield Perks",
            description="Damage-taken, charge, projectile-protection, and shield durability perks.",
            predicate=lambda row: (
                row_subtype(row)
                in {
                    "damage resistance",
                    "ranged",
                    "charge",
                    "projectile protection",
                    "shield durability",
                }
                and is_troop_facing(row)
                and is_defensive_survival_effect(row)
            ),
        ),
        GuideBucket(
            key="troop_xp",
            title="Troop XP Perks",
            description="Perks that directly mention troop XP or experience gains.",
            predicate=lambda row: row_subtype(row) == "troop xp",
        ),
        GuideBucket(
            key="smithing",
            title="Smithing And Crafting Perks",
            description="Smithing perk effects and crafting-bonus rows.",
            predicate=lambda row: row.get("skill") == "Smithing" or row_type(row) == "crafting bonus",
        ),
    ]


def sort_perk_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            str(row.get("skill", "")),
            int(row.get("level", 0)),
            str(row.get("perk", "")),
            str(row.get("effect_slot", "")),
        ),
    )


def stack_component(index: dict[str, dict[str, Any]], ref: PerkRef) -> dict[str, Any]:
    key = f"{ref.perk_string_id}|{ref.effect_slot}"
    row = index.get(key)
    if row is None:
        return {"id": key, "missing": True, "effective_bonus": 0, "note": ref.note or "Missing from perk export."}
    compact = compact_perk_row(row)
    compact["missing"] = False
    compact["effective_bonus"] = ref.effective_bonus if ref.effective_bonus is not None else row.get("game", {}).get("bonus", 0)
    if ref.note:
        compact["note"] = ref.note
    return compact


def build_stack(index: dict[str, dict[str, Any]], definition: GuideStack) -> dict[str, Any]:
    components = [stack_component(index, ref) for ref in definition.components]
    total = sum(float(component.get("effective_bonus", 0)) for component in components)
    if definition.metric.startswith("mixed"):
        total_value: float | None = None
    else:
        total_value = total
    return {
        "key": definition.key,
        "title": definition.title,
        "metric": definition.metric,
        "total": total_value,
        "normal_high_ai_level_gain": total * NORMAL_AI_FACTOR if "skill" in definition.metric.lower() else None,
        "components": components,
        "note": definition.note,
    }


def format_number(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        rounded = round(value, 6)
        if abs(value - rounded) <= max(1e-8, abs(value) * 1e-7):
            return f"{rounded:.6f}".rstrip("0").rstrip(".")
    return str(value)


def format_factor_percent(value: Any) -> str:
    if value is None:
        return ""
    try:
        return f"{format_number(round(float(value) * 100, 4))}%"
    except (TypeError, ValueError):
        return format_number(value)


def direct_effect_delta_text(effect: dict[str, Any], skill_bonus: int) -> str:
    parts = []
    for key, value in effect["per_skill"].items():
        label = key.removesuffix("_pct").replace("_", " ")
        parts.append(f"{label} +{format_number(float(value) * skill_bonus)}%")
    return ", ".join(parts)


def build_payload(workspace: Path, perk_export_path: Path) -> dict[str, Any]:
    rows = read_json(perk_export_path)
    index = {row_key(row): row for row in rows}

    buckets: dict[str, Any] = {}
    for bucket in guide_buckets():
        bucket_rows = [compact_perk_row(row) for row in rows if bucket.predicate(row)]
        buckets[bucket.key] = {
            "title": bucket.title,
            "description": bucket.description,
            "count": len(bucket_rows),
            "rows": sort_perk_rows(bucket_rows),
        }

    return {
        "generated_at": datetime.now().astimezone().isoformat(),
        "inputs": {"perk_export": display_path(perk_export_path, workspace)},
        "direct_weapon_effects": DIRECT_WEAPON_EFFECTS,
        "ai_behavior_formulas": AI_BEHAVIOR_FORMULAS,
        "survival_formulas": SURVIVAL_FORMULAS,
        "smithing_formulas": SMITHING_FORMULAS,
        "buckets": buckets,
        "stacks": {
            "ai_skill": [build_stack(index, definition) for definition in AI_SKILL_STACKS],
            "hit_points": [build_stack(index, definition) for definition in HP_STACKS],
            "armor": [build_stack(index, definition) for definition in ARMOR_STACKS],
            "damage_reduction": [build_stack(index, definition) for definition in RESISTANCE_STACKS],
        },
    }


def stack_component_names(
    stack: dict[str, Any], bonus_formatter: Callable[[Any], str] = format_number
) -> str:
    names = []
    for component in stack.get("components", []):
        if component.get("missing"):
            names.append(f"{component.get('id')} (missing)")
        else:
            bonus = bonus_formatter(component.get("effective_bonus", ""))
            suffix = f" ({bonus})" if bonus else ""
            names.append(f"{component.get('perk', component.get('id', ''))}{suffix}")
    return ", ".join(names)


def write_stack_table(
    lines: list[str],
    stacks: list[dict[str, Any]],
    include_ai_gain: bool = False,
    total_formatter: Callable[[Any], str] = format_number,
    component_bonus_formatter: Callable[[Any], str] = format_number,
) -> None:
    if include_ai_gain:
        lines.extend(["| Stack | Total | AI level gain | Components | Note |", "| --- | ---: | ---: | --- | --- |"])
    else:
        lines.extend(["| Stack | Total | Components | Note |", "| --- | ---: | --- | --- |"])
    for stack in stacks:
        total = total_formatter(stack.get("total"))
        components = table_escape(stack_component_names(stack, component_bonus_formatter))
        note = table_escape(stack.get("note", ""))
        if include_ai_gain:
            gain = stack.get("normal_high_ai_level_gain")
            gain_text = "" if gain is None else format_number(gain)
            lines.append(f"| {table_escape(stack['title'])} | {total} | {gain_text} | {components} | {note} |")
        else:
            lines.append(f"| {table_escape(stack['title'])} | {total} | {components} | {note} |")
    lines.append("")


def write_bucket_table(lines: list[str], bucket: dict[str, Any]) -> None:
    lines.extend(
        [
            f"### {bucket['title']}",
            "",
            bucket["description"],
            "",
            f"Rows: {bucket['count']}",
            "",
            "| Skill | Level | Perk | Role | Bonus | Scope | Effect |",
            "| --- | ---: | --- | --- | ---: | --- | --- |",
        ]
    )
    for row in bucket["rows"]:
        lines.append(
            "| {skill} | {level} | {perk} | {role} | {bonus} | {scope} | {effect} |".format(
                skill=table_escape(row["skill"]),
                level=row["level"],
                perk=table_escape(row["perk"]),
                role=table_escape(row["role"]),
                bonus=table_escape(format_number(row["bonus"])),
                scope=table_escape(row["troop_usage"]),
                effect=table_escape(row["effect"]),
            )
        )
    lines.append("")


def write_markdown(payload: dict[str, Any], path: Path, workspace: Path, json_output: Path) -> None:
    lines = [
        "# Bannerlord Guide Stat Extracts",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This report collects the perk rows, formulas, and stack definitions behind the manual guide notes. It is meant to make guide updates repeatable: refresh the perk export, re-run this script, and compare the generated stat tables before editing prose.",
        "",
        "## Inputs",
        "",
        f"- Perk export: `{payload['inputs']['perk_export']}`",
        "",
        "## Direct Weapon Skill Effects",
        "",
        "| Skill | Effects | Per skill point | +30 skill | +80 skill |",
        "| --- | --- | --- | --- | --- |",
    ]
    for effect in payload["direct_weapon_effects"]:
        per_skill = ", ".join(
            f"{key.removesuffix('_pct').replace('_', ' ')} +{format_number(value)}%"
            for key, value in effect["per_skill"].items()
        )
        lines.append(
            f"| {effect['skill']} | {effect['effects']} | {per_skill} | "
            f"{direct_effect_delta_text(effect, 30)} | {direct_effect_delta_text(effect, 80)} |"
        )
    lines.extend(
        [
            "",
            "Accuracy effects are stored as negative factors in code because they reduce inaccuracy or penalty; this report displays the player-facing positive effect.",
            "",
            "## AI Behavior Formulas",
            "",
            "| Key | Track | Shape | Formula |",
            "| --- | --- | --- | --- |",
        ]
    )
    for formula in payload["ai_behavior_formulas"]:
        lines.append(
            "| {key} | {track} | {shape} | `{formula}` |".format(
                key=table_escape(formula["key"]),
                track=table_escape(formula["track"]),
                shape=table_escape(formula.get("shape", formula.get("normal_high_difficulty", ""))),
                formula=table_escape(formula["formula"]),
            )
        )

    lines.extend(["", "## AI Skill Stacks", ""])
    write_stack_table(lines, payload["stacks"]["ai_skill"], include_ai_gain=True)

    lines.extend(["## Survivability Stacks", "", "### Hit Points", ""])
    write_stack_table(lines, payload["stacks"]["hit_points"])
    lines.extend(["### Armor", ""])
    write_stack_table(lines, payload["stacks"]["armor"])
    lines.extend(["### Damage Reduction", ""])
    write_stack_table(
        lines,
        payload["stacks"]["damage_reduction"],
        total_formatter=format_factor_percent,
        component_bonus_formatter=format_factor_percent,
    )

    lines.extend(["## Survival Formulas", "", "| Key | Formula | Notes |", "| --- | --- | --- |"])
    for formula in payload["survival_formulas"]:
        notes = " ".join(formula.get("notes", []))
        lines.append(f"| {formula['key']} | `{table_escape(formula['formula'])}` | {table_escape(notes)} |")

    lines.extend(["", "## Smithing Formulas", "", "| Key | Formula |", "| --- | --- |"])
    for formula in payload["smithing_formulas"]:
        lines.append(f"| {formula['key']} | `{formula['formula']}` |")

    lines.extend(["", "## Extracted Perk Buckets", ""])
    for key in sorted(payload["buckets"]):
        write_bucket_table(lines, payload["buckets"][key])

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


def extract_guide_stats(
    workspace: Path,
    perk_export_path: Path,
    json_output: Path,
    markdown_output: Path,
) -> None:
    payload = build_payload(workspace, perk_export_path)
    write_json(json_output, payload)
    write_markdown(payload, markdown_output, workspace, json_output)
    print(f"Guide stat JSON written: {json_output}")
    print(f"Guide stat report written: {markdown_output}")
    for key, bucket in payload["buckets"].items():
        print(f"  {key}: {bucket['count']} rows")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract guide-facing stat tables from generated Bannerlord data.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--perk-export", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    perk_export_path = args.perk_export or workspace / "Data" / "export" / "perk-effects.json"
    json_output = args.json_output or workspace / "Data" / "generated" / "guide-stat-extracts.json"
    markdown_output = args.markdown_output or workspace / "Data" / "generated" / "reports" / "guide-stat-extracts.md"
    extract_guide_stats(
        workspace=workspace,
        perk_export_path=perk_export_path.resolve(),
        json_output=json_output,
        markdown_output=markdown_output,
    )


if __name__ == "__main__":
    main()
