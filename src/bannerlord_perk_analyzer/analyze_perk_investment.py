from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from .build_generator import (
        ATTRIBUTES,
        SkillInfo,
        TargetDetail,
        enumerate_bonus_plans,
        load_skill_info,
        solve_for_bonus_plan,
    )
    from .perk_limits import (
        MAX_ATTRIBUTE,
        MAX_FOCUS,
        MIN_ATTRIBUTE,
        peak_learning_range,
        skill_limit,
    )
    from .postprocess import default_workspace, read_json
    from .xp_reports import display_path, table_escape
except ImportError:
    from build_generator import (
        ATTRIBUTES,
        SkillInfo,
        TargetDetail,
        enumerate_bonus_plans,
        load_skill_info,
        solve_for_bonus_plan,
    )
    from perk_limits import MAX_ATTRIBUTE, MAX_FOCUS, MIN_ATTRIBUTE, peak_learning_range, skill_limit
    from postprocess import default_workspace, read_json
    from xp_reports import display_path, table_escape


FOCUS_ONLY_ATTRIBUTE = MIN_ATTRIBUTE
FOCUS_ONLY_FOCUS = MAX_FOCUS
FOCUS_ONLY_LIMIT = skill_limit(FOCUS_ONLY_ATTRIBUTE, FOCUS_ONLY_FOCUS)
MAX_SKILL_LEVEL = skill_limit(MAX_ATTRIBUTE, MAX_FOCUS)


@dataclass(frozen=True)
class InvestmentSplit:
    attribute: int
    focus: int
    limit: int
    peak_learning_range: int
    purchased_attributes: int
    focus_points: int
    allocation_points: int
    weighted_allocation_cost: int
    level_gate_cost: int


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def row_key(row: dict[str, Any]) -> str:
    return f"{row.get('perk_string_id', '')}|{row.get('effect_slot', '')}"


def perk_key(skill: str, perk_string_id: str) -> str:
    return f"{skill}|{perk_string_id}"


def format_number(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def format_split(split: dict[str, Any] | InvestmentSplit | None) -> str:
    if split is None:
        return ""
    if isinstance(split, InvestmentSplit):
        attribute = split.attribute
        focus = split.focus
    else:
        attribute = int(split["attribute"])
        focus = int(split["focus"])
    return f"{attribute} attr / {focus} focus"


def format_allocation(split: dict[str, Any]) -> str:
    return f"{split['purchased_attributes']} attr + {split['focus_points']} focus"


def investment_category(split: InvestmentSplit) -> str:
    if split.attribute <= FOCUS_ONLY_ATTRIBUTE:
        return "low"
    if split.attribute <= 5:
        return "medium"
    return "high"


def investment_pressure(split: InvestmentSplit) -> str:
    if split.attribute <= FOCUS_ONLY_ATTRIBUTE:
        return "focus-only"
    if split.attribute <= 5:
        return "attribute-gated"
    return "specialist"


def split_to_json(split: InvestmentSplit) -> dict[str, Any]:
    return {
        "attribute": split.attribute,
        "focus": split.focus,
        "limit": split.limit,
        "peak_learning_range": split.peak_learning_range,
        "purchased_attributes": split.purchased_attributes,
        "focus_points": split.focus_points,
        "allocation_points": split.allocation_points,
        "weighted_allocation_cost": split.weighted_allocation_cost,
        "level_gate_cost": split.level_gate_cost,
        "category": investment_category(split),
        "pressure": investment_pressure(split),
    }


def cheapest_split_for_level(level: int) -> InvestmentSplit:
    candidates: list[InvestmentSplit] = []
    for attribute in range(MIN_ATTRIBUTE, MAX_ATTRIBUTE + 1):
        for focus in range(0, MAX_FOCUS + 1):
            limit = skill_limit(attribute, focus)
            if limit < level:
                continue
            purchased_attributes = max(0, attribute - MIN_ATTRIBUTE)
            focus_points = focus
            allocation_points = purchased_attributes + focus_points
            weighted_allocation_cost = focus_points + purchased_attributes * 4
            candidates.append(
                InvestmentSplit(
                    attribute=attribute,
                    focus=focus,
                    limit=limit,
                    peak_learning_range=peak_learning_range(attribute, focus),
                    purchased_attributes=purchased_attributes,
                    focus_points=focus_points,
                    allocation_points=allocation_points,
                    weighted_allocation_cost=weighted_allocation_cost,
                    level_gate_cost=max(focus_points, purchased_attributes * 4),
                )
            )
    if not candidates:
        raise ValueError(f"Cannot reach level {level} with legal attributes/focus.")
    return sorted(
        candidates,
        key=lambda item: (
            item.weighted_allocation_cost,
            item.allocation_points,
            item.level_gate_cost,
            item.purchased_attributes + item.focus_points,
            item.purchased_attributes,
            item.focus_points,
            item.attribute,
        ),
    )[0]


def plan_allocation_points(plan: Any) -> int:
    return plan.focus_points_spent + plan.attribute_points_spent


def plan_weighted_allocation_cost(plan: Any) -> int:
    return plan.focus_points_spent + plan.attribute_points_spent * 4


def optimize_build_for_allocation(
    requested: dict[str, TargetDetail],
    skills: dict[str, SkillInfo],
    base_attributes: dict[str, int],
    base_focus: dict[str, int],
    bonus_mode: str,
    auto_endurance: bool,
) -> Any:
    candidates = []
    for plan in enumerate_bonus_plans(bonus_mode, requested, auto_endurance):
        solved = solve_for_bonus_plan(
            requested=requested,
            plan=plan,
            skills=skills,
            base_attributes=base_attributes,
            base_focus=base_focus,
            creation_choices=[],
            starting_skill_levels={},
            free_focus_points=0,
            free_attribute_points=0,
        )
        if solved is not None:
            candidates.append(solved)
    if not candidates:
        raise ValueError("No valid attribute/focus plan can reach those targets.")
    return sorted(
        candidates,
        key=lambda item: (
            plan_weighted_allocation_cost(item),
            plan_allocation_points(item),
            item.attribute_points_spent,
            item.focus_points_spent,
            item.level_ups_needed,
        ),
    )[0]


def endurance_assisted_plan(skill: str, level: int, skills: dict[str, SkillInfo]) -> dict[str, Any]:
    base_attributes = {attribute: MIN_ATTRIBUTE for attribute in ATTRIBUTES}
    base_focus = {skill_name: 0 for skill_name in skills}
    requested = {skill: TargetDetail(level=level, reasons=[f"{skill} {level}"])}
    no_bonus = optimize_build_for_allocation(
        requested=requested,
        skills=skills,
        base_attributes=base_attributes,
        base_focus=base_focus,
        bonus_mode="none",
        auto_endurance=False,
    )
    assisted = optimize_build_for_allocation(
        requested=requested,
        skills=skills,
        base_attributes=base_attributes,
        base_focus=base_focus,
        bonus_mode="stretch",
        auto_endurance=True,
    )
    return {
        "without_endurance": {
            "weighted_allocation_cost": plan_weighted_allocation_cost(no_bonus),
            "allocation_points": plan_allocation_points(no_bonus),
            "level_ups_needed": no_bonus.level_ups_needed,
            "focus_points_spent": no_bonus.focus_points_spent,
            "attribute_points_spent": no_bonus.attribute_points_spent,
            "skill_plans": [item.__dict__ for item in no_bonus.skill_plans],
            "bonus_plan": no_bonus.bonus_plan.name,
        },
        "with_endurance_stretch": {
            "weighted_allocation_cost": plan_weighted_allocation_cost(assisted),
            "allocation_points": plan_allocation_points(assisted),
            "level_ups_needed": assisted.level_ups_needed,
            "focus_points_spent": assisted.focus_points_spent,
            "attribute_points_spent": assisted.attribute_points_spent,
            "skill_plans": [item.__dict__ for item in assisted.skill_plans],
            "bonus_plan": assisted.bonus_plan.name,
            "bonus_attributes": dict(assisted.bonus_plan.bonuses),
            "notes": list(assisted.bonus_plan.notes),
        },
        "weighted_allocation_delta": plan_weighted_allocation_cost(assisted) - plan_weighted_allocation_cost(no_bonus),
        "allocation_points_delta": plan_allocation_points(assisted) - plan_allocation_points(no_bonus),
        "level_gate_delta": assisted.level_ups_needed - no_bonus.level_ups_needed,
    }


def compact_effect(row: dict[str, Any]) -> dict[str, Any]:
    game = row.get("game", {})
    classification = row.get("classification", {})
    return {
        "id": row_key(row),
        "effect_slot": row.get("effect_slot", ""),
        "role": game.get("role", ""),
        "bonus": game.get("bonus", 0),
        "increment_type": game.get("increment_type", ""),
        "troop_usage": game.get("troop_usage", ""),
        "perk_type": classification.get("perk_type", ""),
        "perk_subtype": classification.get("perk_subtype", ""),
        "effect_tags": classification.get("effect_tags", []),
        "effect": game.get("effect", ""),
    }


def load_effect_index(perk_export_path: Path) -> dict[str, list[dict[str, Any]]]:
    effects: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in read_json(perk_export_path):
        key = perk_key(str(row["skill"]), str(row["perk_string_id"]))
        effects[key].append(compact_effect(row))
    return dict(effects)


def bonus_percent(effect: dict[str, Any]) -> float | None:
    bonus = effect.get("bonus")
    if not isinstance(bonus, (int, float)):
        return None
    if abs(float(bonus)) < 1e-9:
        return None
    increment_type = str(effect.get("increment_type", ""))
    text = str(effect.get("effect", "")).lower()
    if increment_type in {"add_factor", "add_factor_100"} or "%" in text:
        return round(float(bonus) * 100, 4)
    return None


def effect_math_note(effect: dict[str, Any], split: InvestmentSplit) -> str:
    percent = bonus_percent(effect)
    if percent is None:
        return ""
    per_cost = abs(percent) / max(1, split.weighted_allocation_cost)
    if split.attribute > 5 and abs(percent) <= 5:
        return f"small high-tier numeric effect ({format_number(percent)}%, {format_number(per_cost)}% per weighted cost)"
    if split.attribute > FOCUS_ONLY_ATTRIBUTE and abs(percent) <= 2:
        return f"small attribute-gated numeric effect ({format_number(percent)}%, {format_number(per_cost)}% per weighted cost)"
    return f"{format_number(percent)}% over {split.weighted_allocation_cost} weighted cost ({format_number(per_cost)}% per cost)"


def build_perk_rows(
    raw_perks_path: Path,
    effect_index: dict[str, list[dict[str, Any]]],
    split_by_level: dict[int, InvestmentSplit],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for perk in read_json(raw_perks_path):
        level = int(perk["level"])
        split = split_by_level[level]
        key = perk_key(str(perk["skill"]), str(perk["string_id"]))
        effects = effect_index.get(key, [])
        rows.append(
            {
                "id": key,
                "skill": perk["skill"],
                "attribute": perk["attribute"],
                "level": level,
                "perk": perk["name"],
                "perk_string_id": perk["string_id"],
                "alternative_perk_string_id": perk.get("alternative_string_id", ""),
                "cost": split_to_json(split),
                "effects": effects,
                "math_notes": [note for effect in effects if (note := effect_math_note(effect, split))],
            }
        )
    return sorted(rows, key=lambda item: (str(item["attribute"]), str(item["skill"]), int(item["level"]), str(item["perk"])))


def group_counts(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_category = Counter(row["cost"]["category"] for row in rows)
    by_level = Counter(int(row["level"]) for row in rows)
    by_attribute_category: dict[str, Counter[str]] = defaultdict(Counter)
    by_skill_category: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        category = row["cost"]["category"]
        by_attribute_category[str(row["attribute"])][category] += 1
        by_skill_category[str(row["skill"])][category] += 1
    return {
        "by_category": dict(sorted(by_category.items())),
        "by_level": {str(level): count for level, count in sorted(by_level.items())},
        "by_attribute_category": {
            attribute: dict(counter) for attribute, counter in sorted(by_attribute_category.items(), key=lambda item: ATTRIBUTES.index(item[0]))
        },
        "by_skill_category": dict(sorted((skill, dict(counter)) for skill, counter in by_skill_category.items())),
    }


def skill_threshold_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_skill: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if int(row["level"]) > 200:
            by_skill[str(row["skill"])].append(row)

    summaries: list[dict[str, Any]] = []
    for skill, skill_rows in sorted(by_skill.items()):
        attribute = str(skill_rows[0]["attribute"])
        levels = sorted({int(row["level"]) for row in skill_rows})
        effects = Counter()
        roles = Counter()
        for row in skill_rows:
            for effect in row["effects"]:
                effects[str(effect.get("perk_subtype") or effect.get("perk_type") or "unknown")] += 1
                roles[str(effect.get("role", ""))] += 1
        summaries.append(
            {
                "skill": skill,
                "attribute": attribute,
                "levels": levels,
                "perk_count": len(skill_rows),
                "effect_subtypes": dict(effects.most_common(6)),
                "roles": dict(roles),
            }
        )
    return summaries


def tier_reference(split_by_level: dict[int, InvestmentSplit]) -> list[dict[str, Any]]:
    levels = sorted(split_by_level)
    rows = []
    for level in levels:
        split = split_by_level[level]
        rows.append(
            {
                "target_level": level,
                "split": split_to_json(split),
                "above_focus_only": level > FOCUS_ONLY_LIMIT,
            }
        )
    max_split = cheapest_split_for_level(MAX_SKILL_LEVEL)
    rows.append(
        {
            "target_level": MAX_SKILL_LEVEL,
            "label": "max skill",
            "split": split_to_json(max_split),
            "above_focus_only": True,
        }
    )
    return rows


def shared_attribute_examples(skills: dict[str, SkillInfo], levels: list[int]) -> list[dict[str, Any]]:
    skills_by_attribute: dict[str, list[str]] = defaultdict(list)
    for skill, info in skills.items():
        skills_by_attribute[info.attribute].append(skill)

    rows = []
    for attribute in ATTRIBUTES:
        attribute_skills = sorted(skills_by_attribute.get(attribute, []))
        if not attribute_skills:
            continue
        for level in levels:
            split = cheapest_split_for_level(level)
            skill_count = len(attribute_skills)
            isolated_weighted = split.weighted_allocation_cost * skill_count
            shared_focus = split.focus_points * skill_count
            shared_weighted = shared_focus + split.purchased_attributes * 4
            rows.append(
                {
                    "attribute": attribute,
                    "skills": attribute_skills,
                    "target_level": level,
                    "skill_count": skill_count,
                    "shared_attribute_points": split.purchased_attributes,
                    "shared_focus_points": shared_focus,
                    "shared_allocation_points": split.purchased_attributes + shared_focus,
                    "shared_weighted_allocation_cost": shared_weighted,
                    "isolated_weighted_allocation_cost": isolated_weighted,
                    "weighted_savings": isolated_weighted - shared_weighted,
                    "weighted_cost_per_skill": shared_weighted / skill_count,
                }
            )
    return rows


def build_payload(workspace: Path, raw_perks_path: Path, perk_export_path: Path) -> dict[str, Any]:
    skills = load_skill_info(workspace)
    raw_perks = read_json(raw_perks_path)
    effect_index = load_effect_index(perk_export_path)
    raw_levels = sorted({int(perk["level"]) for perk in raw_perks})
    split_by_level = {level: cheapest_split_for_level(level) for level in raw_levels}
    perk_rows = build_perk_rows(raw_perks_path, effect_index, split_by_level)
    above_focus_only = [row for row in perk_rows if int(row["level"]) > FOCUS_ONLY_LIMIT]
    levels_by_skill: dict[str, set[int]] = defaultdict(set)
    for perk in raw_perks:
        levels_by_skill[str(perk["skill"])].add(int(perk["level"]))
    assisted_targets = {}
    for skill, info in skills.items():
        if info.attribute not in {"Vigor", "Control", "Endurance"}:
            continue
        for level in sorted(levels_by_skill.get(skill, set())):
            if level > FOCUS_ONLY_LIMIT:
                assisted_targets[f"{skill}:{level}"] = endurance_assisted_plan(skill, level, skills)
    return {
        "generated_at": datetime.now().astimezone().isoformat(),
        "inputs": {
            "raw_perks": display_path(raw_perks_path, workspace),
            "perk_export": display_path(perk_export_path, workspace),
        },
        "assumptions": {
            "base_attribute": MIN_ATTRIBUTE,
            "max_focus": MAX_FOCUS,
            "focus_only_limit": FOCUS_ONLY_LIMIT,
            "max_skill_level": MAX_SKILL_LEVEL,
            "weighted_allocation_formula": "focus_points_spent + purchased_attribute_points * 4",
            "allocation_points_formula": "focus_points_spent + purchased_attribute_points",
            "level_gate_formula": "max(focus_points_spent, purchased_attribute_points * 4)",
            "categories": {
                "low": "cheapest split uses 2 attribute or less; focus-only from the default practical floor",
                "medium": "cheapest split uses 3-5 attribute",
                "high": "cheapest split uses more than 5 attribute",
            },
        },
        "tier_reference": tier_reference(split_by_level),
        "shared_attribute_examples": shared_attribute_examples(skills, [225, 250, 275]),
        "counts": group_counts(perk_rows),
        "skill_threshold_summary": skill_threshold_rows(perk_rows),
        "above_focus_only_perks": above_focus_only,
        "endurance_assisted_targets": assisted_targets,
    }


def effect_summary(effects: list[dict[str, Any]], max_items: int = 2) -> str:
    parts = []
    for effect in effects[:max_items]:
        role = str(effect.get("role", ""))
        text = str(effect.get("effect", ""))
        parts.append(f"{role}: {text}" if role else text)
    if len(effects) > max_items:
        parts.append(f"+{len(effects) - max_items} more")
    return " / ".join(parts)


def write_markdown(payload: dict[str, Any], path: Path, workspace: Path, json_output: Path) -> None:
    lines = [
        "# Perk Investment Costs",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This report assigns a point-budget cost to every perk tier and starts the pragmatic review of perks above the focus-only line.",
        "",
        "## Assumptions",
        "",
        f"- Baseline is `{payload['assumptions']['base_attribute']}` attribute and `0` focus in every skill.",
        f"- Focus-only means up to `{payload['assumptions']['max_focus']}` focus with no purchased attribute points; that reaches skill `{payload['assumptions']['focus_only_limit']}`.",
        "- Main cost is additive opportunity cost: `focus points spent + purchased attribute points * 4`.",
        "- Raw allocation is also kept as `focus points spent + purchased attribute points`, because `3 attr / 5 focus` really means `1 attr + 5 focus` above the baseline.",
        "- Level gate is still reported separately as `max(focus points spent, purchased attribute points * 4)`, but it is no longer the rating cost.",
        "- Attribute points are broader than focus points. A Vigor point helps One Handed, Two Handed, and Polearm together, so build-level cost should count that attribute point once and share it across the pushed skills.",
        "- Endurance-assisted rows use the planner's stretch mode for Athletics/Smithing permanent attribute perks. Treat them as build-context hints, not a default recommendation.",
        "",
        "## Investment Categories",
        "",
        "| Category | Meaning |",
        "| --- | --- |",
        "| Low | Focus-only from the practical 2-attribute floor. Covers every perk at or below level 200. |",
        "| Medium | Requires attribute points, but the cheapest split stays at 3-5 attribute. Covers levels 225 and 250. |",
        "| High | Requires pushing beyond 5 attribute. Covers level 275 perks and max-skill planning. |",
        "",
        "## Tier Cost Reference",
        "",
        "| Target | Category | Cheapest Split | Raw Allocation | Weighted Cost | Level Gate | Limit | Peak Learning Range |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["tier_reference"]:
        split = row["split"]
        target = str(row.get("label") or row["target_level"])
        lines.append(
            "| {target} | {category} | {split} | {allocation} | {weighted} | {gate} | {limit} | {peak} |".format(
                target=table_escape(target),
                category=split["category"],
                split=format_split(split),
                allocation=format_allocation(split),
                weighted=split["weighted_allocation_cost"],
                gate=split["level_gate_cost"],
                limit=split["limit"],
                peak=split["peak_learning_range"],
            )
        )

    lines.extend(
        [
            "",
            "## Shared Attribute Examples",
            "",
            "If several skills under the same attribute are pushed together, the attribute cost is paid once and the focus costs remain per skill.",
            "",
            "| Attribute | Target | Skills | Shared Raw Allocation | Shared Weighted Cost | Isolated Weighted Cost | Savings | Per-Skill Weighted Cost |",
            "| --- | ---: | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in payload["shared_attribute_examples"]:
        lines.append(
            "| {attribute} | {target} | {skills} | {allocation} | {shared} | {isolated} | {savings} | {per_skill} |".format(
                attribute=table_escape(row["attribute"]),
                target=row["target_level"],
                skills=table_escape(", ".join(row["skills"])),
                allocation=f"{row['shared_attribute_points']} attr + {row['shared_focus_points']} focus",
                shared=row["shared_weighted_allocation_cost"],
                isolated=row["isolated_weighted_allocation_cost"],
                savings=row["weighted_savings"],
                per_skill=format_number(row["weighted_cost_per_skill"]),
            )
        )

    counts = payload["counts"]["by_category"]
    total = sum(counts.values())
    lines.extend(
        [
            "",
            "## Distribution",
            "",
            "| Category | Perks | Share |",
            "| --- | ---: | ---: |",
        ]
    )
    for category in ("low", "medium", "high"):
        count = int(counts.get(category, 0))
        share = 0 if not total else count / total * 100
        lines.append(f"| {category} | {count} | {format_number(round(share, 1))}% |")

    lines.extend(
        [
            "",
            "## Skills Above Focus-Only",
            "",
            "These are the perk bands that require attribute investment under the baseline model.",
            "",
            "| Attribute | Skill | Perks Above 200 | Main Extracted Effect Buckets |",
            "| --- | --- | ---: | --- |",
        ]
    )
    for row in payload["skill_threshold_summary"]:
        buckets = ", ".join(f"{key} ({value})" for key, value in row["effect_subtypes"].items())
        lines.append(
            "| {attribute} | {skill} | {count} | {buckets} |".format(
                attribute=row["attribute"],
                skill=row["skill"],
                count=row["perk_count"],
                buckets=table_escape(buckets),
            )
        )

    lines.extend(
        [
            "",
            "## Endurance Stretch Snapshot",
            "",
            "Single-skill targets rarely justify Endurance detours on additive cost alone. The value is mostly build-wide: free Vigor/Control/Endurance points get much better when several skills in those attributes are being pushed together.",
            "",
            "| Target | No Endurance Weighted Cost | Stretch Weighted Cost | Delta | Level Gate Delta | Stretch Plan |",
            "| --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    interesting = []
    for target, plan in payload["endurance_assisted_targets"].items():
        no_cost = int(plan["without_endurance"]["weighted_allocation_cost"])
        stretch_cost = int(plan["with_endurance_stretch"]["weighted_allocation_cost"])
        delta = int(plan["weighted_allocation_delta"])
        gate_delta = int(plan["level_gate_delta"])
        if delta <= 0 or target.endswith(":275"):
            interesting.append(
                (target, no_cost, stretch_cost, delta, gate_delta, plan["with_endurance_stretch"]["bonus_plan"])
            )
    for target, no_cost, stretch_cost, delta, gate_delta, plan_name in sorted(
        interesting, key=lambda item: (item[1], item[0])
    ):
        lines.append(
            f"| {table_escape(target)} | {no_cost} | {stretch_cost} | {delta:+d} | {gate_delta:+d} | {table_escape(plan_name)} |"
        )

    lines.extend(
        [
            "",
            "## Above Focus-Only Perks",
            "",
            "| Attribute | Skill | Level | Category | Raw Allocation | Weighted Cost | Level Gate | Perk | Effects | Math Notes |",
            "| --- | --- | ---: | --- | --- | ---: | ---: | --- | --- | --- |",
        ]
    )
    for row in payload["above_focus_only_perks"]:
        notes = " / ".join(row.get("math_notes", []))
        lines.append(
            "| {attribute} | {skill} | {level} | {category} | {allocation} | {weighted} | {gate} | {perk} | {effects} | {notes} |".format(
                attribute=table_escape(str(row["attribute"])),
                skill=table_escape(str(row["skill"])),
                level=row["level"],
                category=row["cost"]["category"],
                allocation=format_allocation(row["cost"]),
                weighted=row["cost"]["weighted_allocation_cost"],
                gate=row["cost"]["level_gate_cost"],
                perk=table_escape(str(row["perk"])),
                effects=table_escape(effect_summary(row["effects"])),
                notes=table_escape(notes),
            )
        )

    lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- JSON: `{display_path(json_output, workspace)}`",
            f"- Report: `{display_path(path, workspace)}`",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def analyze_perk_investment(
    workspace: Path,
    raw_perks_path: Path,
    perk_export_path: Path,
    json_output: Path,
    markdown_output: Path,
) -> None:
    payload = build_payload(workspace, raw_perks_path, perk_export_path)
    write_json(json_output, payload)
    write_markdown(payload, markdown_output, workspace, json_output)
    print(f"Perk investment JSON written: {json_output}")
    print(f"Perk investment report written: {markdown_output}")
    for category, count in payload["counts"]["by_category"].items():
        print(f"  {category}: {count} perks")


def main() -> None:
    parser = argparse.ArgumentParser(description="Assign point-budget investment costs to Bannerlord perk tiers.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--raw-perks", type=Path, default=None)
    parser.add_argument("--perk-export", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    raw_perks_path = args.raw_perks or workspace / "Data" / "raw" / "perks.json"
    perk_export_path = args.perk_export or workspace / "Data" / "export" / "perk-effects.json"
    json_output = args.json_output or workspace / "Data" / "intermediate" / "perk-investment-costs.json"
    markdown_output = args.markdown_output or workspace / "Docs" / "reports" / "perk-investment-costs.md"
    analyze_perk_investment(
        workspace=workspace,
        raw_perks_path=raw_perks_path.resolve(),
        perk_export_path=perk_export_path.resolve(),
        json_output=json_output,
        markdown_output=markdown_output,
    )


if __name__ == "__main__":
    main()
