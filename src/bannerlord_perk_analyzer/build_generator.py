from __future__ import annotations

import argparse
import itertools
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from .perk_limits import (
        MAX_ATTRIBUTE,
        MAX_FOCUS,
        MIN_ATTRIBUTE,
        minimum_focus_for_level,
        peak_learning_range,
        skill_limit,
    )
    from .postprocess import default_workspace, read_json
except ImportError:
    from perk_limits import MAX_ATTRIBUTE, MAX_FOCUS, MIN_ATTRIBUTE, minimum_focus_for_level, peak_learning_range, skill_limit
    from postprocess import default_workspace, read_json


ATTRIBUTES = ("Vigor", "Control", "Endurance", "Cunning", "Social", "Intelligence")
ENDURANCE_SKILLS = {"Athletics", "Riding", "Smithing"}


@dataclass
class SkillInfo:
    name: str
    attribute: str
    perks_by_level: dict[int, list[str]] = field(default_factory=dict)
    perk_lookup: dict[str, tuple[str, int]] = field(default_factory=dict)


@dataclass
class TargetDetail:
    level: int
    reasons: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BonusPlan:
    name: str
    required_targets: tuple[tuple[str, int], ...]
    bonuses: tuple[tuple[str, int], ...]
    source_bonuses: tuple[tuple[str, tuple[tuple[str, int], ...]], ...]
    notes: tuple[str, ...]

    def bonus_counter(self) -> Counter[str]:
        return Counter(dict(self.bonuses))

    def source_bonus_counter(self, source: str) -> Counter[str]:
        for name, items in self.source_bonuses:
            if name == source:
                return Counter(dict(items))
        return Counter()

    def has_source(self, source: str) -> bool:
        return any(name == source for name, _items in self.source_bonuses)


@dataclass
class SkillPlan:
    skill: str
    attribute: str
    target_level: int
    focus: int
    effective_attribute: int
    peak_learning_range: int
    limit: int
    requested: bool
    perks: list[str]


@dataclass
class BuildPlan:
    requested_targets: dict[str, TargetDetail]
    final_targets: dict[str, TargetDetail]
    purchased_attributes: dict[str, int]
    base_attributes: dict[str, int]
    base_focus: dict[str, int]
    creation_choices: list[dict[str, Any]]
    starting_skill_levels: dict[str, int]
    skill_plans: list[SkillPlan]
    bonus_plan: BonusPlan
    free_focus_points: int
    free_attribute_points: int
    free_focus_points_used: int
    free_attribute_points_used: int
    focus_points_spent: int
    attribute_points_spent: int
    level_ups_needed: int
    unused_focus_points: int
    unused_attribute_points: int


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def merge_counter(left: Counter[str], right: Counter[str]) -> Counter[str]:
    result = Counter(left)
    result.update(right)
    return +result


def subtract_counter(left: Counter[str], right: Counter[str]) -> Counter[str]:
    result = Counter(left)
    result.subtract(right)
    return +result


def load_skill_info(workspace: Path) -> dict[str, SkillInfo]:
    raw_perks = read_json(workspace / "Data" / "raw" / "perks.json")
    skills: dict[str, SkillInfo] = {}
    for perk in raw_perks:
        skill = str(perk["skill"])
        attribute = str(perk["attribute"])
        info = skills.setdefault(skill, SkillInfo(name=skill, attribute=attribute))
        level = int(perk["level"])
        name = str(perk["name"])
        string_id = str(perk["string_id"])
        info.perks_by_level.setdefault(level, [])
        if name not in info.perks_by_level[level]:
            info.perks_by_level[level].append(name)
        info.perk_lookup[normalize(name)] = (name, level)
        info.perk_lookup[normalize(string_id)] = (name, level)
    for info in skills.values():
        info.perks_by_level = {level: sorted(names) for level, names in sorted(info.perks_by_level.items())}
    return dict(sorted(skills.items()))


def load_character_creation_options(workspace: Path) -> list[dict[str, Any]]:
    path = workspace / "Data" / "generated" / "character-creation-options.json"
    if not path.exists():
        raise ValueError(
            "Character creation options are not generated yet. "
            "Run extract_character_creation.py with --game-root first."
        )
    payload = read_json(path)
    return list(payload.get("character_creation_options", []))


def resolve_named(value: str, choices: list[str], kind: str) -> str:
    key = normalize(value)
    exact = [choice for choice in choices if normalize(choice) == key]
    if len(exact) == 1:
        return exact[0]
    contains = [choice for choice in choices if key and key in normalize(choice)]
    if len(contains) == 1:
        return contains[0]
    if not exact and not contains:
        raise ValueError(f"Unknown {kind}: {value}")
    matches = ", ".join(sorted(exact or contains)[:8])
    raise ValueError(f"Ambiguous {kind} {value!r}: {matches}")


def resolve_creation_choice(value: str, options: list[dict[str, Any]]) -> dict[str, Any]:
    key = normalize(value)
    matches: list[dict[str, Any]] = []
    for option in options:
        candidates = [
            str(option.get("id", "")),
            str(option.get("option_id", "")),
            str(option.get("title", "")),
            str(option.get("method", "")),
            str(option.get("short_method", "")),
        ]
        if any(normalize(candidate) == key for candidate in candidates):
            matches.append(option)

    if not matches:
        for option in options:
            candidates = [
                str(option.get("id", "")),
                str(option.get("option_id", "")),
                str(option.get("title", "")),
                str(option.get("method", "")),
                str(option.get("short_method", "")),
            ]
            if any(key and key in normalize(candidate) for candidate in candidates):
                matches.append(option)

    unique: dict[str, dict[str, Any]] = {str(option.get("id", "")): option for option in matches}
    if len(unique) == 1:
        return next(iter(unique.values()))
    if not unique:
        raise ValueError(f"Unknown character creation choice: {value}")
    rendered = ", ".join(f"{option.get('title')} ({option.get('id')})" for option in unique.values())
    raise ValueError(f"Ambiguous character creation choice {value!r}: {rendered}")


def resolve_perk(value: str, skills: dict[str, SkillInfo], skill_hint: str | None = None) -> tuple[str, str, int]:
    key = normalize(value)
    matches: list[tuple[str, str, int]] = []
    search_skills = [skill_hint] if skill_hint else list(skills)
    for skill in search_skills:
        info = skills[skill]
        if key in info.perk_lookup:
            perk_name, level = info.perk_lookup[key]
            matches.append((skill, perk_name, level))
            continue
        for perk_key, (perk_name, level) in info.perk_lookup.items():
            if key and key in perk_key:
                matches.append((skill, perk_name, level))
    unique = sorted(set(matches))
    if len(unique) == 1:
        return unique[0]
    if not unique:
        location = f" in {skill_hint}" if skill_hint else ""
        raise ValueError(f"Unknown perk{location}: {value}")
    rendered = ", ".join(f"{skill}:{perk} ({level})" for skill, perk, level in unique[:8])
    raise ValueError(f"Ambiguous perk {value!r}: {rendered}")


def split_target_spec(spec: str) -> tuple[str | None, str]:
    for separator in ("=", ":"):
        if separator in spec:
            left, right = spec.split(separator, 1)
            return left.strip(), right.strip()
    match = re.match(r"^(?P<left>.+?)\s+(?P<right>\d+)$", spec.strip())
    if match:
        return match.group("left").strip(), match.group("right").strip()
    return None, spec.strip()


def add_target(targets: dict[str, TargetDetail], skill: str, level: int, reason: str) -> None:
    detail = targets.setdefault(skill, TargetDetail(level=0))
    if level > detail.level:
        detail.level = level
    if reason not in detail.reasons:
        detail.reasons.append(reason)


def parse_target(spec: str, skills: dict[str, SkillInfo]) -> tuple[str, int, str]:
    left, right = split_target_spec(spec)
    if left is not None:
        skill = resolve_named(left, list(skills), "skill")
        if right.isdigit():
            return skill, int(right), f"target {skill} {right}"
        resolved_skill, perk, level = resolve_perk(right, skills, skill_hint=skill)
        return resolved_skill, level, f"perk {perk}"

    if right.isdigit():
        raise ValueError(f"Target {spec!r} needs a skill, for example Bow:{right}.")

    try:
        skill = resolve_named(right, list(skills), "skill")
        level = max(skills[skill].perks_by_level)
        return skill, level, f"all {skill} perks"
    except ValueError:
        skill, perk, level = resolve_perk(right, skills)
        return skill, level, f"perk {perk}"


def parse_assignment(spec: str, valid_names: list[str], kind: str, minimum: int, maximum: int) -> tuple[str, int]:
    if "=" in spec:
        left, right = spec.split("=", 1)
    elif ":" in spec:
        left, right = spec.split(":", 1)
    else:
        match = re.match(r"^(?P<left>.+?)\s+(?P<right>\d+)$", spec.strip())
        if not match:
            raise ValueError(f"{kind} assignment must look like Name=Value: {spec}")
        left, right = match.group("left"), match.group("right")
    name = resolve_named(left.strip(), valid_names, kind)
    value = int(right.strip())
    if value < minimum or value > maximum:
        raise ValueError(f"{kind} {name} must be between {minimum} and {maximum}: {value}")
    return name, value


def counter_items(counter: Counter[str]) -> tuple[tuple[str, int], ...]:
    return tuple(sorted((key, value) for key, value in counter.items() if value))


def make_bonus_plan(
    name: str,
    required_targets: dict[str, int],
    source_bonuses: dict[str, Counter[str]],
    notes: list[str],
) -> BonusPlan:
    total = Counter()
    for bonus in source_bonuses.values():
        total.update(bonus)
    return BonusPlan(
        name=name,
        required_targets=tuple(sorted(required_targets.items())),
        bonuses=counter_items(total),
        source_bonuses=tuple(sorted((source, counter_items(bonus)) for source, bonus in source_bonuses.items())),
        notes=tuple(notes),
    )


def athletics_variants(milestone: int, mode: str) -> list[tuple[str, dict[str, int], dict[str, Counter[str]], list[str]]]:
    if milestone == 0:
        return [("no Athletics attribute perk", {}, {}, [])]
    if milestone == 175:
        return [
            (
                "Athletics 175",
                {"Athletics": 175},
                {"athletics_175": Counter({"Endurance": 1})},
                ["Athletics 175 Durable: +1 Endurance."],
            )
        ]
    if mode == "stretch":
        return [
            (
                "Athletics 200 stretch",
                {"Athletics": 200},
                {
                    "athletics_175": Counter({"Endurance": 1}),
                    "athletics_200": Counter({"Vigor": 1, "Control": 1}),
                },
                ["Athletics 175 Durable: +1 Endurance.", "Athletics 200 respec stretch: +1 Vigor and +1 Control."],
            )
        ]
    return [
        (
            "Athletics 200 Strong",
            {"Athletics": 200},
            {"athletics_175": Counter({"Endurance": 1}), "athletics_200": Counter({"Vigor": 1})},
            ["Athletics 175 Durable: +1 Endurance.", "Athletics 200 Strong: +1 Vigor."],
        ),
        (
            "Athletics 200 Steady",
            {"Athletics": 200},
            {"athletics_175": Counter({"Endurance": 1}), "athletics_200": Counter({"Control": 1})},
            ["Athletics 175 Durable: +1 Endurance.", "Athletics 200 Steady: +1 Control."],
        ),
    ]


def smithing_variants(milestone: int, mode: str) -> list[tuple[str, dict[str, int], dict[str, Counter[str]], list[str]]]:
    if milestone == 0:
        return [("no Smithing attribute perk", {}, {}, [])]
    if mode == "stretch":
        required = {"Smithing": milestone}
        source_bonuses = {"smithing_150": Counter({"Vigor": 1, "Control": 1})}
        notes = ["Smithing 150 respec stretch: +1 Vigor and +1 Control."]
        if milestone == 225:
            source_bonuses["smithing_225"] = Counter({"Endurance": 1})
            notes.append("Smithing 225 Enduring Smith: +1 Endurance.")
        return [(f"Smithing {milestone} stretch", required, source_bonuses, notes)]

    variants = []
    for attribute, perk in (("Vigor", "Vigorous Smith"), ("Control", "Controlled Smith")):
        required = {"Smithing": milestone}
        source_bonuses = {"smithing_150": Counter({attribute: 1})}
        notes = [f"Smithing 150 {perk}: +1 {attribute}."]
        if milestone == 225:
            source_bonuses["smithing_225"] = Counter({"Endurance": 1})
            notes.append("Smithing 225 Enduring Smith: +1 Endurance.")
        variants.append((f"Smithing {milestone} {attribute}", required, source_bonuses, notes))
    return variants


def allowed_milestones(skill: str, current_targets: dict[str, TargetDetail], auto_endurance: bool) -> list[int]:
    if auto_endurance:
        return [0, 175, 200] if skill == "Athletics" else [0, 150, 225]
    target = current_targets.get(skill, TargetDetail(0)).level
    if skill == "Athletics":
        return [milestone for milestone in (0, 175, 200) if milestone == 0 or target >= milestone]
    return [milestone for milestone in (0, 150, 225) if milestone == 0 or target >= milestone]


def enumerate_bonus_plans(
    mode: str,
    current_targets: dict[str, TargetDetail],
    auto_endurance: bool,
) -> list[BonusPlan]:
    if mode == "none":
        return [make_bonus_plan("no endurance bonuses", {}, {}, [])]

    plans: dict[tuple[Any, ...], BonusPlan] = {}
    for athletics_milestone in allowed_milestones("Athletics", current_targets, auto_endurance):
        for smithing_milestone in allowed_milestones("Smithing", current_targets, auto_endurance):
            for athletics_name, athletics_required, athletics_sources, athletics_notes in athletics_variants(
                athletics_milestone, mode
            ):
                for smithing_name, smithing_required, smithing_sources, smithing_notes in smithing_variants(
                    smithing_milestone, mode
                ):
                    required = dict(athletics_required)
                    for skill, level in smithing_required.items():
                        required[skill] = max(required.get(skill, 0), level)
                    sources = dict(athletics_sources)
                    sources.update(smithing_sources)
                    notes = [*athletics_notes, *smithing_notes]
                    name = " + ".join(part for part in (athletics_name, smithing_name) if not part.startswith("no "))
                    if not name:
                        name = "no endurance bonuses"
                    plan = make_bonus_plan(name, required, sources, notes)
                    key = (plan.required_targets, plan.bonuses, plan.source_bonuses)
                    plans[key] = plan
    return sorted(plans.values(), key=lambda item: (sum(dict(item.required_targets).values()), item.name))


def cap_with_bonuses(
    skill: str,
    purchased_attributes: dict[str, int],
    focus_by_skill: dict[str, int],
    bonus: Counter[str],
    skills: dict[str, SkillInfo],
) -> int:
    attribute = skills[skill].attribute
    effective_attribute = min(MAX_ATTRIBUTE, purchased_attributes[attribute] + bonus.get(attribute, 0))
    return skill_limit(effective_attribute, focus_by_skill[skill])


def valid_bonus_timing(
    plan: BonusPlan,
    purchased_attributes: dict[str, int],
    focus_by_skill: dict[str, int],
    skills: dict[str, SkillInfo],
) -> bool:
    bonuses = plan.bonus_counter()

    if plan.has_source("athletics_175"):
        before = subtract_counter(bonuses, plan.source_bonus_counter("athletics_175"))
        before = subtract_counter(before, plan.source_bonus_counter("athletics_200"))
        before = subtract_counter(before, plan.source_bonus_counter("smithing_225"))
        if cap_with_bonuses("Athletics", purchased_attributes, focus_by_skill, before, skills) < 175:
            return False

    if plan.has_source("athletics_200"):
        before = subtract_counter(bonuses, plan.source_bonus_counter("athletics_200"))
        before = subtract_counter(before, plan.source_bonus_counter("smithing_225"))
        if cap_with_bonuses("Athletics", purchased_attributes, focus_by_skill, before, skills) < 200:
            return False

    if plan.has_source("smithing_150"):
        before = subtract_counter(bonuses, plan.source_bonus_counter("smithing_150"))
        if cap_with_bonuses("Smithing", purchased_attributes, focus_by_skill, before, skills) < 150:
            return False

    if plan.has_source("smithing_225"):
        before = subtract_counter(bonuses, plan.source_bonus_counter("smithing_225"))
        if cap_with_bonuses("Smithing", purchased_attributes, focus_by_skill, before, skills) < 225:
            return False

    return True


def merge_targets(requested: dict[str, TargetDetail], plan: BonusPlan) -> dict[str, TargetDetail]:
    targets = {skill: TargetDetail(detail.level, list(detail.reasons)) for skill, detail in requested.items()}
    for skill, level in plan.required_targets:
        add_target(targets, skill, level, "endurance attribute enabler")
    return targets


def solve_for_bonus_plan(
    requested: dict[str, TargetDetail],
    plan: BonusPlan,
    skills: dict[str, SkillInfo],
    base_attributes: dict[str, int],
    base_focus: dict[str, int],
    creation_choices: list[dict[str, Any]],
    starting_skill_levels: dict[str, int],
    free_focus_points: int,
    free_attribute_points: int,
) -> BuildPlan | None:
    targets = merge_targets(requested, plan)
    used_attributes = sorted({skills[skill].attribute for skill in targets}, key=ATTRIBUTES.index)
    ranges = [range(base_attributes[attribute], MAX_ATTRIBUTE + 1) for attribute in used_attributes]
    bonuses = plan.bonus_counter()
    best: tuple[tuple[int, int, int, int, int], BuildPlan] | None = None

    for values in itertools.product(*ranges):
        purchased = dict(base_attributes)
        purchased.update(dict(zip(used_attributes, values)))

        skill_plans: list[SkillPlan] = []
        focus_by_skill: dict[str, int] = {}
        possible = True
        for skill, detail in sorted(targets.items()):
            info = skills[skill]
            effective_attribute = min(MAX_ATTRIBUTE, purchased[info.attribute] + bonuses.get(info.attribute, 0))
            focus = minimum_focus_for_level(detail.level, effective_attribute, base_focus.get(skill, 0))
            if focus is None:
                possible = False
                break
            focus_by_skill[skill] = focus
            skill_plans.append(
                SkillPlan(
                    skill=skill,
                    attribute=info.attribute,
                    target_level=detail.level,
                    focus=focus,
                    effective_attribute=effective_attribute,
                    peak_learning_range=peak_learning_range(effective_attribute, focus),
                    limit=skill_limit(effective_attribute, focus),
                    requested=skill in requested,
                    perks=skills[skill].perks_by_level.get(detail.level, []),
                )
            )
        if not possible:
            continue

        if not valid_bonus_timing(plan, purchased, focus_by_skill, skills):
            continue

        raw_focus_points = sum(max(0, focus_by_skill[skill] - base_focus.get(skill, 0)) for skill in targets)
        raw_attribute_points = sum(max(0, purchased[attribute] - base_attributes[attribute]) for attribute in ATTRIBUTES)
        free_focus_used = min(free_focus_points, raw_focus_points)
        free_attribute_used = min(free_attribute_points, raw_attribute_points)
        focus_points = raw_focus_points - free_focus_used
        attribute_points = raw_attribute_points - free_attribute_used
        level_ups = max(focus_points, attribute_points * 4)
        enabler_levels = sum(
            max(0, detail.level - requested.get(skill, TargetDetail(0)).level)
            for skill, detail in targets.items()
        )
        score = (level_ups, attribute_points + focus_points, attribute_points, focus_points, enabler_levels)

        build_plan = BuildPlan(
            requested_targets=requested,
            final_targets=targets,
            purchased_attributes=purchased,
            base_attributes=base_attributes,
            base_focus=base_focus,
            creation_choices=creation_choices,
            starting_skill_levels=starting_skill_levels,
            skill_plans=sorted(skill_plans, key=lambda item: (ATTRIBUTES.index(item.attribute), item.skill)),
            bonus_plan=plan,
            free_focus_points=free_focus_points,
            free_attribute_points=free_attribute_points,
            free_focus_points_used=free_focus_used,
            free_attribute_points_used=free_attribute_used,
            focus_points_spent=focus_points,
            attribute_points_spent=attribute_points,
            level_ups_needed=level_ups,
            unused_focus_points=max(0, level_ups - focus_points),
            unused_attribute_points=max(0, (level_ups // 4) - attribute_points),
        )
        if best is None or score < best[0]:
            best = (score, build_plan)

    return None if best is None else best[1]


def optimize_build(
    requested: dict[str, TargetDetail],
    skills: dict[str, SkillInfo],
    base_attributes: dict[str, int],
    base_focus: dict[str, int],
    creation_choices: list[dict[str, Any]],
    starting_skill_levels: dict[str, int],
    free_focus_points: int,
    free_attribute_points: int,
    bonus_mode: str,
    auto_endurance: bool,
) -> BuildPlan:
    candidates: list[BuildPlan] = []
    for plan in enumerate_bonus_plans(bonus_mode, requested, auto_endurance):
        solved = solve_for_bonus_plan(
            requested,
            plan,
            skills,
            base_attributes,
            base_focus,
            creation_choices,
            starting_skill_levels,
            free_focus_points,
            free_attribute_points,
        )
        if solved is not None:
            candidates.append(solved)
    if not candidates:
        raise ValueError("No valid attribute/focus plan can reach those targets.")
    return sorted(
        candidates,
        key=lambda item: (
            item.level_ups_needed,
            item.attribute_points_spent + item.focus_points_spent,
            item.attribute_points_spent,
            item.focus_points_spent,
            sum(max(0, item.final_targets[skill].level - requested.get(skill, TargetDetail(0)).level) for skill in item.final_targets),
        ),
    )[0]


def target_to_json(detail: TargetDetail) -> dict[str, Any]:
    return {"level": detail.level, "reasons": detail.reasons}


def plan_to_json(plan: BuildPlan) -> dict[str, Any]:
    bonuses = dict(plan.bonus_plan.bonuses)
    return {
        "level_ups_needed": plan.level_ups_needed,
        "focus_points_spent": plan.focus_points_spent,
        "attribute_points_spent": plan.attribute_points_spent,
        "unused_focus_points": plan.unused_focus_points,
        "unused_attribute_points": plan.unused_attribute_points,
        "creation_choices": plan.creation_choices,
        "starting_skill_levels": {skill: value for skill, value in plan.starting_skill_levels.items() if value},
        "free_focus_points": plan.free_focus_points,
        "free_attribute_points": plan.free_attribute_points,
        "free_focus_points_used": plan.free_focus_points_used,
        "free_attribute_points_used": plan.free_attribute_points_used,
        "requested_targets": {skill: target_to_json(detail) for skill, detail in plan.requested_targets.items()},
        "final_targets": {skill: target_to_json(detail) for skill, detail in plan.final_targets.items()},
        "purchased_attributes": plan.purchased_attributes,
        "bonus_attributes": bonuses,
        "skill_plans": [skill_plan.__dict__ for skill_plan in plan.skill_plans],
        "bonus_plan": {
            "name": plan.bonus_plan.name,
            "required_targets": dict(plan.bonus_plan.required_targets),
            "bonuses": bonuses,
            "notes": list(plan.bonus_plan.notes),
        },
    }


def format_target_reason(detail: TargetDetail) -> str:
    return "; ".join(detail.reasons)


def render_text(plan: BuildPlan) -> str:
    bonuses = plan.bonus_plan.bonus_counter()
    lines: list[str] = []
    lines.append("Build Point Plan")
    lines.append("================")
    lines.append("")
    lines.append(
        f"Minimum level-ups worth of points after creation bonuses: {plan.level_ups_needed} "
        f"(focus {plan.focus_points_spent}, attributes {plan.attribute_points_spent} x 4)"
    )
    if plan.free_focus_points or plan.free_attribute_points:
        lines.append(
            "Flexible creation points used: "
            f"{plan.free_focus_points_used}/{plan.free_focus_points} focus, "
            f"{plan.free_attribute_points_used}/{plan.free_attribute_points} attribute."
        )
    if plan.unused_focus_points or plan.unused_attribute_points:
        lines.append(
            f"Point slack at that level: {plan.unused_focus_points} focus, "
            f"{plan.unused_attribute_points} attribute."
        )
    lines.append("Attribute points apply to every skill in their attribute group, not just the skill that forced the purchase.")
    lines.append("")

    if plan.creation_choices:
        lines.append("Character Creation")
        lines.append("| Stage | Culture | Choice | Option id |")
        lines.append("|---|---|---|---|")
        for choice in plan.creation_choices:
            lines.append(
                f"| {choice.get('stage', '')} | {choice.get('culture', '')} | "
                f"{choice.get('title', '')} | `{choice.get('id', '')}` |"
            )
        starting_levels = {skill: value for skill, value in plan.starting_skill_levels.items() if value}
        if starting_levels:
            rendered = ", ".join(f"{skill} +{value}" for skill, value in sorted(starting_levels.items()))
            lines.append("")
            lines.append(f"Starting skill levels from creation: {rendered}.")
            lines.append("These help the XP grind, but the cap plan still targets the actual perk level.")
        lines.append("")

    lines.append("Targets")
    lines.append("| Skill | Attribute | Level | Source | Perks at level |")
    lines.append("|---|---|---:|---|---|")
    skill_by_name = {skill_plan.skill: skill_plan for skill_plan in plan.skill_plans}
    for skill in sorted(plan.final_targets, key=lambda name: (ATTRIBUTES.index(skill_by_name[name].attribute), name)):
        detail = plan.final_targets[skill]
        skill_plan = skill_by_name[skill]
        source = format_target_reason(detail)
        perks = ", ".join(skill_plan.perks) if skill_plan.perks else ""
        lines.append(f"| {skill} | {skill_plan.attribute} | {detail.level} | {source} | {perks} |")

    lines.append("")
    lines.append("Attribute Targets")
    lines.append("| Attribute | Base | Buy to | Bonus | Effective | Planned skills using it |")
    lines.append("|---|---:|---:|---:|---:|---|")
    used_attributes = {
        skill_plan.attribute
        for skill_plan in plan.skill_plans
    } | {attribute for attribute, value in bonuses.items() if value}
    skills_by_attribute: dict[str, list[str]] = {}
    for skill_plan in plan.skill_plans:
        skills_by_attribute.setdefault(skill_plan.attribute, []).append(skill_plan.skill)
    for attribute in ATTRIBUTES:
        if attribute not in used_attributes and plan.purchased_attributes[attribute] == plan.base_attributes[attribute]:
            continue
        bonus = bonuses.get(attribute, 0)
        effective = min(MAX_ATTRIBUTE, plan.purchased_attributes[attribute] + bonus)
        planned_skills = ", ".join(sorted(skills_by_attribute.get(attribute, [])))
        lines.append(
            f"| {attribute} | {plan.base_attributes[attribute]} | "
            f"{plan.purchased_attributes[attribute]} | +{bonus} | {effective} | {planned_skills} |"
        )

    lines.append("")
    lines.append("Skill Investment")
    lines.append("| Skill | Level | Attribute Used | Focus | Peak Range | Limit | Requested |")
    lines.append("|---|---:|---:|---:|---:|---:|---|")
    for skill_plan in plan.skill_plans:
        requested = "yes" if skill_plan.requested else "enabler"
        lines.append(
            f"| {skill_plan.skill} | {skill_plan.target_level} | {skill_plan.effective_attribute} | "
            f"{skill_plan.focus} | {skill_plan.peak_learning_range} | {skill_plan.limit} | {requested} |"
        )

    if plan.bonus_plan.notes:
        lines.append("")
        lines.append("Endurance Attribute Bonuses")
        lines.append(f"Selected plan: {plan.bonus_plan.name}")
        for note in plan.bonus_plan.notes:
            lines.append(f"- {note}")
        lines.append(
            "Stretch mode assumes permanent attribute gains can be banked by later changing the perk choice "
            "after the relevant Endurance skill is high enough."
        )

    return "\n".join(lines) + "\n"


def build_targets(args: argparse.Namespace, skills: dict[str, SkillInfo]) -> dict[str, TargetDetail]:
    targets: dict[str, TargetDetail] = {}
    for spec in args.target:
        skill, level, reason = parse_target(spec, skills)
        add_target(targets, skill, level, reason)
    for spec in args.perk:
        skill, perk, level = resolve_perk(spec, skills)
        add_target(targets, skill, level, f"perk {perk}")
    if not targets:
        raise ValueError("Add at least one --target or --perk.")
    for skill, detail in targets.items():
        if detail.level < 0 or detail.level > 330:
            raise ValueError(f"Target level for {skill} looks invalid: {detail.level}")
    return targets


def build_base_attributes(args: argparse.Namespace) -> dict[str, int]:
    attributes = {attribute: MIN_ATTRIBUTE for attribute in ATTRIBUTES}
    for spec in args.base_attribute:
        attribute, value = parse_assignment(spec, list(ATTRIBUTES), "attribute", 1, MAX_ATTRIBUTE)
        attributes[attribute] = value
    return attributes


def build_base_focus(args: argparse.Namespace, skills: dict[str, SkillInfo]) -> dict[str, int]:
    focus = {skill: 0 for skill in skills}
    for spec in args.base_focus:
        skill, value = parse_assignment(spec, list(skills), "skill focus", 0, MAX_FOCUS)
        focus[skill] = value
    return focus


def selected_creation_choices(args: argparse.Namespace, workspace: Path) -> list[dict[str, Any]]:
    if not args.creation_choice:
        return []
    options = load_character_creation_options(workspace)
    return [resolve_creation_choice(spec, options) for spec in args.creation_choice]


def apply_creation_choices(
    choices: list[dict[str, Any]],
    base_attributes: dict[str, int],
    base_focus: dict[str, int],
    skills: dict[str, SkillInfo],
) -> tuple[dict[str, int], dict[str, int], dict[str, int], int, int]:
    attributes = dict(base_attributes)
    focus = dict(base_focus)
    starting_skill_levels = {skill: 0 for skill in skills}
    free_focus_points = 0
    free_attribute_points = 0

    for choice in choices:
        effects = choice.get("effects", {})
        attribute = effects.get("attribute")
        if attribute:
            name = str(attribute.get("attribute", ""))
            if name in attributes:
                attributes[name] = min(MAX_ATTRIBUTE, attributes[name] + int(attribute.get("levels", 0)))

        for skill_effect in effects.get("skills", []):
            skill = str(skill_effect.get("skill", ""))
            if skill not in focus:
                continue
            focus[skill] = min(MAX_FOCUS, focus[skill] + int(skill_effect.get("focus", 0)))
            starting_skill_levels[skill] += int(skill_effect.get("skill_levels", 0))

        free_focus_points += int(effects.get("unspent_focus", 0))
        free_attribute_points += int(effects.get("unspent_attribute", 0))

    return attributes, focus, starting_skill_levels, free_focus_points, free_attribute_points


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Bannerlord terminal build point plan.",
        epilog=(
            'Examples:\n'
            '  python src/bannerlord_perk_analyzer/build_generator.py --target "Bow:275" --target "Riding:225"\n'
            '  python src/bannerlord_perk_analyzer/build_generator.py --target "Medicine:Minister of Health" --perk "Deadshot"\n'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--target", action="append", default=[], help="Skill:level, Skill:perk, or a perk/skill name.")
    parser.add_argument("--perk", action="append", default=[], help="Perk name or Skill:perk to include as a target.")
    parser.add_argument("--base-attribute", action="append", default=[], help="Starting attribute, e.g. Control=4.")
    parser.add_argument("--base-focus", action="append", default=[], help="Starting focus, e.g. Bow=2.")
    parser.add_argument(
        "--creation-choice",
        action="append",
        default=[],
        help="Character creation option id/title to apply, e.g. vlandia_blacksmith_option or age_selection_adult_option.",
    )
    parser.add_argument(
        "--bonus-mode",
        choices=("none", "permanent", "stretch"),
        default="stretch",
        help="How to model Endurance attribute perks.",
    )
    parser.add_argument(
        "--no-auto-endurance",
        action="store_true",
        help="Only use Endurance bonuses from Athletics/Smithing targets already in the build.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    try:
        workspace = args.workspace.resolve()
        skills = load_skill_info(workspace)
        creation_choices = selected_creation_choices(args, workspace)
        targets = build_targets(args, skills)
        base_attributes = build_base_attributes(args)
        base_focus = build_base_focus(args, skills)
        base_attributes, base_focus, starting_skill_levels, free_focus_points, free_attribute_points = apply_creation_choices(
            creation_choices,
            base_attributes,
            base_focus,
            skills,
        )
        plan = optimize_build(
            requested=targets,
            skills=skills,
            base_attributes=base_attributes,
            base_focus=base_focus,
            creation_choices=creation_choices,
            starting_skill_levels=starting_skill_levels,
            free_focus_points=free_focus_points,
            free_attribute_points=free_attribute_points,
            bonus_mode=args.bonus_mode,
            auto_endurance=not args.no_auto_endurance,
        )
    except ValueError as error:
        raise SystemExit(f"ERROR: {error}")

    if args.format == "json":
        print(json.dumps(plan_to_json(plan), indent=2))
    else:
        print(render_text(plan), end="")


if __name__ == "__main__":
    main()
