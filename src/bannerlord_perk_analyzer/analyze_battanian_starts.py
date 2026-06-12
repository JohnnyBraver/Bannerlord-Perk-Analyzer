from __future__ import annotations

import argparse
import math
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from .postprocess import default_workspace, read_json, write_json
except ImportError:
    from postprocess import default_workspace, read_json, write_json


STAGES = ("family", "childhood", "education", "youth", "adulthood", "escape")
ATTRIBUTES = ("Vigor", "Control", "Endurance", "Cunning", "Social", "Intelligence")
BASE_ATTRIBUTES = {attribute: 2 for attribute in ATTRIBUTES}
URBAN_PARENT_OCCUPATIONS = {
    "artisan_urban",
    "bard_urban",
    "healer_urban",
    "merchant_urban",
    "mercenary_urban",
    "physician_urban",
    "retainer_urban",
    "vagabond_urban",
}
EDUCATION_URBAN_OPTIONS = {
    "education_docker_option",
    "education_ganger_option",
    "education_horser_option",
    "education_marketer_option",
    "education_tutor_option",
    "education_watcher_option",
}
EDUCATION_NON_URBAN_OPTIONS = {
    "education_doctor_option",
    "education_engineer_option",
    "education_herder_option",
    "education_hunter_option",
    "education_merchant_option",
    "education_smith_option",
}
YOUTH_CULTURE_OPTIONS = {
    "youth_camp_option": {"Vlandia", "Sturgia"},
    "youth_cavalry_option": {"Vlandia"},
    "youth_envoys_guard_first_option": {"Empire", "Khuzait"},
    "youth_envoys_guard_second_option": {"Aserai", "Battania"},
    "youth_groom_option": {"Vlandia"},
    "youth_guard_empire_register_option": {"Empire"},
    "youth_guard_garrisons_register_option": {"Aserai", "Battania", "Khuzait"},
    "youth_guard_high_register_option": {"Vlandia"},
    "youth_guard_low_register_option": {"Sturgia"},
    "youth_hearth_option": {"Battania", "Sturgia"},
    "youth_infantry_option": {"Aserai", "Battania", "Empire", "Khuzait", "Sturgia", "Vlandia"},
    "youth_kern_option": {"Battania"},
    "youth_rider_high_register_option": {"Empire", "Khuzait"},
    "youth_rider_low_register_option": {"Aserai", "Sturgia"},
    "youth_servant_first_option": {"Khuzait"},
    "youth_servant_second_option": {"Battania"},
    "youth_skirmisher_option": {"Aserai", "Empire", "Khuzait", "Sturgia", "Vlandia"},
    "youth_staff_first_option": {"Empire"},
    "youth_staff_second_option": {"Aserai"},
}
ADULTHOOD_URBAN_OPTIONS = {
    "adulthood_escapade_low_register_option",
    "adulthood_siege_survivor_option",
    "adulthood_workshop_option",
}
ADULTHOOD_NON_URBAN_OPTIONS = {
    "adulthood_escapade_high_register_option",
    "adulthood_hunter_option",
    "adulthood_investor_option",
}
ADULTHOOD_CULTURE_OCCUPATION_OPTIONS = {
    "adulthood_caravan_leader_option": ({"Aserai", "Empire", "Khuzait", "Sturgia", "Vlandia"}, "urban"),
    "adulthood_manhunt_option": ({"Aserai", "Battania", "Empire", "Khuzait", "Vlandia"}, "non_urban"),
    "adulthood_saved_city_option": ({"Battania"}, "urban"),
    "adulthood_saved_village_option": ({"Sturgia"}, "non_urban"),
}
ADULTHOOD_ALWAYS_OPTIONS = {
    "adulthood_defeated_enemy_option",
    "adulthood_nice_person_option",
}
DEFAULT_TARGET_ATTRIBUTES = {
    "Vigor": 3,
    "Control": 2,
    "Endurance": 3,
    "Cunning": 7,
    "Social": 2,
    "Intelligence": 7,
}

FOCUS_POLICY: dict[str, dict[str, Any]] = {
    "Scouting": {"bucket": "core", "cap": 5, "read": "Core 275 engagement-control target."},
    "Medicine": {"bucket": "core", "cap": 5, "read": "Core 275 troop-survival target."},
    "Steward": {"bucket": "core", "cap": 5, "read": "Core party-scaling target if the player is quartermaster."},
    "Athletics": {"bucket": "core", "cap": 5, "read": "Physical attribute and foot-party enabler."},
    "Smithing": {"bucket": "core", "cap": 5, "read": "Attribute/focus engine and money engine."},
    "One Handed": {"bucket": "core", "cap": 5, "read": "Core Vigor infantry package."},
    "Polearm": {"bucket": "core", "cap": 5, "read": "Core Vigor infantry package."},
    "Two Handed": {"bucket": "core", "cap": 3, "read": "Default stop is 175; later focus is optional."},
    "Riding": {"bucket": "core", "cap": 1, "read": "Only needs one focus for Riding 100 in infantry doctrine."},
    "Bow": {"bucket": "side_plan", "cap": 0, "read": "Ranged-side plan only; Bow 100 Merry Men costs two focus under assisted Control 4 and is too thin for default infantry."},
    "Throwing": {"bucket": "core", "cap": 2, "read": "Throwing 125 Skirmisher under assisted Control 4."},
    "Leadership": {"bucket": "optional", "cap": 5, "read": "Useful party-size stretch; Social still stays at 2."},
    "Charm": {"bucket": "optional", "cap": 1, "read": "One-focus QoL or renown pickup."},
    "Trade": {"bucket": "optional", "cap": 1, "read": "One-focus price-marking QoL pickup."},
    "Tactics": {"bucket": "soft", "cap": 5, "read": "Soft leak unless Tactics 200 is planned."},
    "Engineering": {"bucket": "side_plan", "cap": 0, "read": "Convertible hard leak: delegate by default, but Engineering 225 Metallurgy can justify a late player-engineer stretch."},
    "Roguery": {"bucket": "side_plan", "cap": 0, "read": "Side plan only; loot/crime build."},
    "Crossbow": {"bucket": "side_plan", "cap": 0, "read": "Side plan only; crossbow formations."},
}


def table_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def format_counter(counter: dict[str, int] | Counter[str]) -> str:
    items = [(key, value) for key, value in counter.items() if value]
    if not items:
        return "none"
    return ", ".join(f"{key} {value}" for key, value in sorted(items))


def option_attribute(option: dict[str, Any]) -> str | None:
    attribute = option.get("effects", {}).get("attribute")
    if not attribute:
        return None
    return str(attribute.get("attribute") or "") or None


def option_skills(option: dict[str, Any]) -> list[str]:
    return [str(item.get("skill", "")) for item in option.get("effects", {}).get("skills", []) if item.get("skill")]


def is_urban_parent(parent_occupation: str | None) -> bool:
    return bool(parent_occupation in URBAN_PARENT_OCCUPATIONS)


def method_to_on_select(method_name: str) -> str:
    if method_name.startswith("Get") and method_name.endswith("OptionArgs"):
        return method_name[3:-len("OptionArgs")] + "OptionOnSelect"
    return ""


def family_parent_occupations(payload: dict[str, Any]) -> dict[str, str]:
    methods = {str(method.get("method", "")): method for method in payload.get("methods", [])}
    occupations: dict[str, str] = {}
    for option in payload.get("character_creation_options", []):
        if option.get("stage") != "family":
            continue
        on_select = methods.get(method_to_on_select(str(option.get("method", ""))))
        if not on_select:
            continue
        il = [str(line) for line in on_select.get("il", [])]
        for index, line in enumerate(il):
            if "SetParentOccupation" not in line:
                continue
            for previous in reversed(il[:index]):
                occupation = parse_ldstr_value(previous)
                if occupation:
                    occupations[str(option.get("id", ""))] = occupation
                    break
            break
    return occupations


def parse_ldstr_value(line: str) -> str | None:
    marker = "ldstr"
    if marker not in line:
        return None
    return line.split(marker, 1)[1].strip() or None


def option_allowed(option: dict[str, Any], culture: str, parent_occupation: str | None) -> bool:
    option_id = str(option.get("id", ""))
    stage = str(option.get("stage", ""))
    urban = is_urban_parent(parent_occupation)
    if stage == "education":
        if option_id in EDUCATION_URBAN_OPTIONS:
            return urban
        if option_id in EDUCATION_NON_URBAN_OPTIONS:
            return not urban
    elif stage == "youth":
        cultures = YOUTH_CULTURE_OPTIONS.get(option_id)
        if cultures is not None:
            return culture in cultures
    elif stage == "adulthood":
        if option_id in ADULTHOOD_ALWAYS_OPTIONS:
            return True
        if option_id in ADULTHOOD_URBAN_OPTIONS:
            return urban
        if option_id in ADULTHOOD_NON_URBAN_OPTIONS:
            return not urban
        gated = ADULTHOOD_CULTURE_OCCUPATION_OPTIONS.get(option_id)
        if gated:
            cultures, occupation_gate = gated
            if culture not in cultures:
                return False
            return urban if occupation_gate == "urban" else not urban
    return True


def option_summary(option: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": option.get("id", ""),
        "stage": option.get("stage", ""),
        "culture": option.get("culture", ""),
        "title": option.get("title", ""),
        "attribute": option_attribute(option),
        "skills": option_skills(option),
    }


def load_stage_options(workspace: Path, culture: str) -> dict[str, list[dict[str, Any]]]:
    payload = read_json(workspace / "Data" / "raw" / "character-creation-options.json")
    options = payload.get("character_creation_options", [])
    parent_occupations = family_parent_occupations(payload)
    result: dict[str, list[dict[str, Any]]] = {stage: [] for stage in STAGES}
    for option in options:
        stage = str(option.get("stage", ""))
        if stage not in result:
            continue
        option_culture = option.get("culture")
        if stage == "family":
            if option_culture != culture:
                continue
        elif option_culture not in ("", None):
            continue
        if "campaign" not in option.get("availability", []):
            continue
        if stage == "family":
            option = {**option, "parent_occupation": parent_occupations.get(str(option.get("id", "")), "")}
        result[stage].append(option)
    missing = [stage for stage, values in result.items() if not values]
    if missing:
        raise ValueError(f"No campaign character creation options found for stages: {', '.join(missing)}")
    return result


def list_family_cultures(workspace: Path) -> list[str]:
    payload = read_json(workspace / "Data" / "raw" / "character-creation-options.json")
    return sorted(
        {
            str(option.get("culture"))
            for option in payload.get("character_creation_options", [])
            if option.get("stage") == "family" and option.get("culture")
        }
    )


def classify_focus(focus: Counter[str]) -> dict[str, dict[str, int]]:
    buckets = {
        "core": {},
        "optional": {},
        "soft": {},
        "side_plan": {},
        "overflow": {},
    }
    for skill, count in sorted(focus.items()):
        policy = FOCUS_POLICY.get(skill, {"bucket": "side_plan", "cap": 0})
        bucket = str(policy["bucket"])
        cap = int(policy["cap"])
        if bucket != "side_plan" and count > cap:
            buckets["overflow"][skill] = count - cap
        if bucket == "side_plan" and count:
            buckets["side_plan"][skill] = count
        elif bucket in buckets and count:
            buckets[bucket][skill] = count
        else:
            buckets["side_plan"][skill] = count
    return buckets


def path_record(
    choices: list[dict[str, Any]],
    attributes: Counter[str],
    target_attributes: dict[str, int],
) -> dict[str, Any]:
    focus: Counter[str] = Counter()
    for choice in choices:
        focus.update(option_skills(choice))
    starting_attributes = {
        attribute: BASE_ATTRIBUTES[attribute] + attributes.get(attribute, 0)
        for attribute in ATTRIBUTES
    }
    level_up_attributes = {
        attribute: target_attributes[attribute] - starting_attributes[attribute]
        for attribute in ATTRIBUTES
        if target_attributes[attribute] != starting_attributes[attribute]
    }
    buckets = classify_focus(focus)
    hard_focus = sum(buckets["side_plan"].values()) + sum(buckets["overflow"].values())
    soft_focus = sum(buckets["soft"].values())
    optional_focus = sum(buckets["optional"].values())
    core_focus = sum(buckets["core"].values())
    default_focus_leaks = hard_focus + soft_focus
    return {
        "choices": [option_summary(choice) for choice in choices],
        "starting_attributes": starting_attributes,
        "level_up_attributes": level_up_attributes,
        "focus": dict(sorted(focus.items())),
        "focus_buckets": buckets,
        "score": {
            "hard_focus": hard_focus,
            "soft_focus": soft_focus,
            "default_focus_leaks": default_focus_leaks,
            "optional_focus": optional_focus,
            "core_focus": core_focus,
        },
    }


def enumerate_paths(
    stage_options: dict[str, list[dict[str, Any]]],
    target_attributes: dict[str, int],
    culture: str,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    valid: list[dict[str, Any]] = []
    pruned: Counter[str] = Counter()

    def walk(
        stage_index: int,
        choices: list[dict[str, Any]],
        attributes: Counter[str],
        parent_occupation: str | None,
    ) -> None:
        if stage_index >= len(STAGES):
            valid.append(path_record(choices, attributes, target_attributes))
            return
        stage = STAGES[stage_index]
        for option in stage_options[stage]:
            if not option_allowed(option, culture, parent_occupation):
                pruned[f"{stage}_condition"] += 1
                continue
            attribute = option_attribute(option)
            next_attributes = Counter(attributes)
            if attribute:
                next_attributes[attribute] += 1
            overflow = {
                name: BASE_ATTRIBUTES[name] + next_attributes.get(name, 0) - target_attributes[name]
                for name in ATTRIBUTES
                if BASE_ATTRIBUTES[name] + next_attributes.get(name, 0) > target_attributes[name]
            }
            if overflow:
                if overflow.get("Control", 0) > 0:
                    pruned["control_attribute"] += 1
                elif overflow.get("Social", 0) > 0:
                    pruned["social_attribute"] += 1
                else:
                    pruned["other_attribute_overflow"] += 1
                continue
            next_parent_occupation = parent_occupation
            if stage == "family":
                next_parent_occupation = str(option.get("parent_occupation") or "")
            walk(stage_index + 1, [*choices, option], next_attributes, next_parent_occupation)

    walk(0, [], Counter(), None)
    return valid, dict(sorted(pruned.items()))


def path_sort_key(path: dict[str, Any]) -> tuple[int, int, int, int, int, int, str]:
    score = path["score"]
    first_title = str(path["choices"][0]["title"]) if path["choices"] else ""
    return (
        int(score["default_focus_leaks"]),
        int(score["hard_focus"]),
        int(path["focus_buckets"]["soft"].get("Tactics", 0)),
        int(score["optional_focus"]),
        -int(score["core_focus"]),
        sum(path["level_up_attributes"].values()),
        first_title,
    )


def profile_key(path: dict[str, Any]) -> str:
    side = format_counter(path["focus_buckets"]["side_plan"])
    overflow = format_counter(path["focus_buckets"]["overflow"])
    tactics = path["focus_buckets"]["soft"].get("Tactics", 0)
    optional = format_counter(path["focus_buckets"]["optional"])
    return f"side={side}; overflow={overflow}; tactics={tactics}; optional={optional}"


def summarize_paths(paths: list[dict[str, Any]], top: int) -> dict[str, Any]:
    profile_counts: Counter[str] = Counter(profile_key(path) for path in paths)
    side_sources: Counter[tuple[str, str, str]] = Counter()
    overflow_counts: Counter[str] = Counter()
    hard_skill_path_counts: Counter[str] = Counter()
    no_hard_paths: list[dict[str, Any]] = []
    for path in paths:
        side_plan = path["focus_buckets"]["side_plan"]
        overflow = path["focus_buckets"]["overflow"]
        if not side_plan and not overflow:
            no_hard_paths.append(path)
        for skill in side_plan:
            hard_skill_path_counts[skill] += 1
            for choice in path["choices"]:
                if skill in choice["skills"]:
                    side_sources[(skill, str(choice["stage"]), str(choice["title"]))] += 1
        for skill in overflow:
            overflow_counts[skill] += 1

    tactics_distribution = Counter(
        str(path["focus_buckets"]["soft"].get("Tactics", 0))
        for path in no_hard_paths
    )
    best_paths = sorted(paths, key=path_sort_key)[:top]
    best_no_hard = sorted(no_hard_paths, key=path_sort_key)[:top]
    leak_distribution: Counter[str] = Counter(str(path["score"]["default_focus_leaks"]) for path in paths)
    min_default_focus_leaks = min((int(path["score"]["default_focus_leaks"]) for path in paths), default=0)
    paths_at_min_default_leaks = [
        path for path in paths if int(path["score"]["default_focus_leaks"]) == min_default_focus_leaks
    ]
    best_min_leak_paths = sorted(paths_at_min_default_leaks, key=path_sort_key)[:top]
    return {
        "attribute_valid_paths": len(paths),
        "minimum_default_focus_leaks": min_default_focus_leaks,
        "paths_at_minimum_default_focus_leaks": len(paths_at_min_default_leaks),
        "zero_default_focus_leak_paths": sum(
            1 for path in paths if int(path["score"]["default_focus_leaks"]) == 0
        ),
        "no_hard_focus_leak_paths": len(no_hard_paths),
        "no_hard_no_tactics_paths": sum(
            1 for path in no_hard_paths if path["focus_buckets"]["soft"].get("Tactics", 0) == 0
        ),
        "no_hard_tactics_at_most_2_paths": sum(
            1 for path in no_hard_paths if path["focus_buckets"]["soft"].get("Tactics", 0) <= 2
        ),
        "hard_skill_path_counts": dict(sorted(hard_skill_path_counts.items())),
        "overflow_path_counts": dict(sorted(overflow_counts.items())),
        "default_focus_leak_distribution": dict(sorted(leak_distribution.items(), key=lambda item: int(item[0]))),
        "tactics_distribution_no_hard": dict(sorted(tactics_distribution.items(), key=lambda item: int(item[0]))),
        "top_profiles": [
            {"profile": profile, "paths": count}
            for profile, count in profile_counts.most_common(top)
        ],
        "side_plan_sources": [
            {"skill": skill, "stage": stage, "choice": title, "paths": count}
            for (skill, stage, title), count in side_sources.most_common(top)
        ],
        "best_paths": best_paths,
        "best_min_leak_paths": best_min_leak_paths,
        "best_no_hard_paths": best_no_hard,
    }


def render_choice_path(path: dict[str, Any]) -> str:
    return " -> ".join(str(choice["title"]) for choice in path["choices"])


def render_attributes(attributes: dict[str, int]) -> str:
    return " - ".join(str(attributes[attribute]) for attribute in ATTRIBUTES)


def render_report(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    culture = str(payload["culture"])
    lines: list[str] = [
        f"# {culture} Start Focus Leak Analysis",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        f"This report brute-forces {culture} story-campaign character creation choices, applies the game's parent-occupation and culture option gates, prunes starts that exceed the current commander attribute target, and classifies where unavoidable focus leaks land.",
        "",
        "## Assumptions",
        "",
        f"- Culture: {payload['culture']}",
        f"- Stage order: {', '.join(STAGES)}",
        f"- Base attributes: {format_counter(BASE_ATTRIBUTES)}",
        f"- Target attributes: {format_counter(payload['target_attributes'])}",
        f"- Total combinations before pruning: {payload['total_combinations']}",
        "",
        "## Focus Buckets",
        "",
        "| Skill | Bucket | Cap | Read |",
        "| --- | --- | ---: | --- |",
    ]
    for skill, policy in sorted(FOCUS_POLICY.items(), key=lambda item: (item[1]["bucket"], item[0])):
        lines.append(
            f"| {table_escape(skill)} | {table_escape(policy['bucket'])} | {policy['cap']} | {table_escape(policy['read'])} |"
        )

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Attribute-valid paths after pruning: {summary['attribute_valid_paths']}",
            f"- Minimum default focus leaks: {summary['minimum_default_focus_leaks']} across {summary['paths_at_minimum_default_focus_leaks']} paths",
            f"- Zero default focus leak paths: {summary['zero_default_focus_leak_paths']}",
            f"- Paths with no side-plan focus and no cap overflow: {summary['no_hard_focus_leak_paths']}",
            f"- Paths with no hard focus leak and no Tactics focus: {summary['no_hard_no_tactics_paths']}",
            f"- Paths with no hard focus leak and at most 2 Tactics focus: {summary['no_hard_tactics_at_most_2_paths']}",
            f"- Attribute branches pruned while walking: {format_counter(payload['pruned_branches'])}",
            "",
            "Default focus leaks count side-plan focus, focus cap overflow, and Tactics soft focus. Optional one-focus QoL sinks such as Trade and Charm, plus planned Leadership, are not counted as leaks.",
            "",
            f"Main read: after dropping purchased Control, {culture} campaign starts can avoid hard side-plan focus leaks, but they may or may not avoid Tactics focus depending on the culture-specific family choices. Treat Tactics as a soft leak unless Tactics 200 is deliberately part of the commander plan.",
            "",
            "## Default Focus Leak Distribution",
            "",
            "| Default Focus Leaks | Paths |",
            "| ---: | ---: |",
        ]
    )
    for leaks, count in summary["default_focus_leak_distribution"].items():
        lines.append(f"| {leaks} | {count} |")

    lines.extend(
        [
            "",
            "## No-Hard-Leak Tactics Distribution",
            "",
            "| Tactics Focus | Paths |",
            "| ---: | ---: |",
        ]
    )
    for tactics, count in summary["tactics_distribution_no_hard"].items():
        lines.append(f"| {tactics} | {count} |")

    lines.extend(
        [
            "",
            "## Side-Plan Leak Sources",
            "",
            "These choices push focus into skills that are not part of the default shock-infantry commander plan.",
            "",
            "| Skill | Stage | Choice | Attribute-valid Paths Affected |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for item in summary["side_plan_sources"]:
        lines.append(
            f"| {table_escape(item['skill'])} | {table_escape(item['stage'])} | {table_escape(item['choice'])} | {item['paths']} |"
        )
    if not summary["side_plan_sources"]:
        lines.append("| none | none | none | 0 |")

    lines.extend(
        [
            "",
            "## Focus Overflow",
            "",
            "Overflow means the start grants more focus than the default plan can use before a skill becomes a variant choice.",
            "",
            f"- Overflow path counts: {format_counter(summary['overflow_path_counts'])}",
            "",
            "## Best Minimum-Leak Paths",
            "",
            "| Leaks | Start Attributes | Level-Up Attributes | Side-Plan Leaks | Overflow | Soft Leaks | Optional Sinks | Core Sinks | Path |",
            "| ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for path in summary["best_min_leak_paths"]:
        lines.append(
            "| {leaks} | {attrs} | {levelups} | {side} | {overflow} | {soft} | {optional} | {core} | {path} |".format(
                leaks=path["score"]["default_focus_leaks"],
                attrs=table_escape(render_attributes(path["starting_attributes"])),
                levelups=table_escape(format_counter(path["level_up_attributes"])),
                side=table_escape(format_counter(path["focus_buckets"]["side_plan"])),
                overflow=table_escape(format_counter(path["focus_buckets"]["overflow"])),
                soft=table_escape(format_counter(path["focus_buckets"]["soft"])),
                optional=table_escape(format_counter(path["focus_buckets"]["optional"])),
                core=table_escape(format_counter(path["focus_buckets"]["core"])),
                path=table_escape(render_choice_path(path)),
            )
        )

    lines.extend(
        [
            "",
            "## Best No-Hard-Leak Paths",
            "",
            "| Start Attributes | Level-Up Attributes | Soft Leaks | Optional Sinks | Core Sinks | Path |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for path in summary["best_no_hard_paths"]:
        lines.append(
            "| {attrs} | {levelups} | {soft} | {optional} | {core} | {path} |".format(
                attrs=table_escape(render_attributes(path["starting_attributes"])),
                levelups=table_escape(format_counter(path["level_up_attributes"])),
                soft=table_escape(format_counter(path["focus_buckets"]["soft"])),
                optional=table_escape(format_counter(path["focus_buckets"]["optional"])),
                core=table_escape(format_counter(path["focus_buckets"]["core"])),
                path=table_escape(render_choice_path(path)),
            )
        )

    lines.extend(
        [
            "",
            "## Common Leak Profiles",
            "",
            "| Paths | Profile |",
            "| ---: | --- |",
        ]
    )
    for item in summary["top_profiles"]:
        lines.append(f"| {item['paths']} | {table_escape(item['profile'])} |")

    return "\n".join(lines) + "\n"


def best_no_hard_read(summary: dict[str, Any]) -> tuple[str, str, str]:
    paths = summary.get("best_no_hard_paths", [])
    if not paths:
        return "none", "none", "none"
    best = paths[0]
    return (
        render_attributes(best["starting_attributes"]),
        format_counter(best["focus_buckets"]["soft"]),
        render_choice_path(best),
    )


def best_min_leak_read(summary: dict[str, Any]) -> tuple[str, str, str]:
    paths = summary.get("best_min_leak_paths", [])
    if not paths:
        return "none", "none", "none"
    best = paths[0]
    leak_profile = (
        f"side {format_counter(best['focus_buckets']['side_plan'])}; "
        f"overflow {format_counter(best['focus_buckets']['overflow'])}; "
        f"soft {format_counter(best['focus_buckets']['soft'])}"
    )
    return (
        render_attributes(best["starting_attributes"]),
        leak_profile,
        render_choice_path(best),
    )


def render_culture_comparison_report(payload: dict[str, Any]) -> str:
    cultures = sorted(
        payload["cultures"],
        key=lambda item: (
            int(item["summary"]["minimum_default_focus_leaks"]),
            -int(item["summary"]["paths_at_minimum_default_focus_leaks"]),
            -int(item["summary"]["zero_default_focus_leak_paths"]),
            -int(item["summary"]["no_hard_focus_leak_paths"]),
            item["culture"],
        ),
    )
    leak_groups: dict[int, list[str]] = {}
    for item in cultures:
        leak_count = int(item["summary"]["minimum_default_focus_leaks"])
        leak_groups.setdefault(leak_count, []).append(str(item["culture"]))

    lines: list[str] = [
        "# Culture Start Focus Leak Comparison",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This report compares story-campaign character creation paths across cultures for the current commander attribute target, after applying the game's parent-occupation and culture option gates.",
        "",
        "## Assumptions",
        "",
        f"- Target attributes: {format_counter(payload['target_attributes'])}",
        "- Default focus leaks count side-plan focus, focus cap overflow, and Tactics soft focus.",
        "- Optional one-focus QoL sinks such as Trade and Charm, plus planned Leadership, are not treated as leaks.",
        "- Attribute leaks are pruned before scoring. The table is only comparing focus leaks among starts that can still hit the target attribute line.",
        "",
        "## Culture Summary",
        "",
        "| Culture | Minimum Default Leaks | Paths At Minimum | Zero-Leak Paths | Attribute-Valid Paths | No Hard Leak | No-Hard <=2 Tactics | Best Minimum-Leak Start | Best Minimum-Leak Profile | Best Minimum-Leak Path |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for item in cultures:
        summary = item["summary"]
        attrs, leak_profile, path = best_min_leak_read(summary)
        lines.append(
            "| {culture} | {min_leaks} | {paths_at_min} | {zero_leak} | {valid} | {no_hard} | {low_tactics} | {attrs} | {leak_profile} | {path} |".format(
                culture=table_escape(item["culture"]),
                min_leaks=summary["minimum_default_focus_leaks"],
                paths_at_min=summary["paths_at_minimum_default_focus_leaks"],
                zero_leak=summary["zero_default_focus_leak_paths"],
                valid=summary["attribute_valid_paths"],
                no_hard=summary["no_hard_focus_leak_paths"],
                low_tactics=summary["no_hard_tactics_at_most_2_paths"],
                attrs=table_escape(attrs),
                leak_profile=table_escape(leak_profile),
                path=table_escape(path),
            )
        )

    zero_leak_cultures = [
        item["culture"]
        for item in cultures
        if int(item["summary"]["zero_default_focus_leak_paths"]) > 0
    ]
    best_leak_count = min(leak_groups) if leak_groups else 0
    lines.extend(
        [
            "",
            "## Leak Count Groups",
            "",
            "| Minimum Default Focus Leaks | Cultures |",
            "| ---: | --- |",
        ]
    )
    for leak_count, culture_names in sorted(leak_groups.items()):
        lines.append(f"| {leak_count} | {table_escape(', '.join(sorted(culture_names)))} |")

    lines.extend(
        [
            "",
            "## Verdict",
            "",
        ]
    )
    if zero_leak_cultures:
        lines.append(
            "Cultures with at least one zero-default-leak path: "
            + ", ".join(zero_leak_cultures)
            + "."
        )
    else:
        lines.append("No culture has a zero-default-leak path under this target and focus policy.")
    if leak_groups:
        lines.append(
            f"Lowest minimum default focus leak count: {best_leak_count} in "
            + ", ".join(sorted(leak_groups[best_leak_count]))
            + "."
        )
    lines.extend(
        [
            "",
            "## Hard Leak Counts",
            "",
            "| Culture | Crossbow | Engineering | Roguery | Focus Overflow |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )
    for item in cultures:
        hard = item["summary"]["hard_skill_path_counts"]
        overflow = item["summary"]["overflow_path_counts"]
        lines.append(
            "| {culture} | {crossbow} | {engineering} | {roguery} | {overflow} |".format(
                culture=table_escape(item["culture"]),
                crossbow=hard.get("Crossbow", 0),
                engineering=hard.get("Engineering", 0),
                roguery=hard.get("Roguery", 0),
                overflow=table_escape(format_counter(overflow)),
            )
        )

    lines.extend(
        [
            "",
            "## Tactics Distribution Among No-Hard-Leak Paths",
            "",
            "| Culture | Tactics 0 | Tactics 1 | Tactics 2 | Tactics 3 | Tactics 4 | Tactics 5 |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for item in cultures:
        dist = item["summary"]["tactics_distribution_no_hard"]
        lines.append(
            "| {culture} | {t0} | {t1} | {t2} | {t3} | {t4} | {t5} |".format(
                culture=table_escape(item["culture"]),
                t0=dist.get("0", 0),
                t1=dist.get("1", 0),
                t2=dist.get("2", 0),
                t3=dist.get("3", 0),
                t4=dist.get("4", 0),
                t5=dist.get("5", 0),
            )
        )

    return "\n".join(lines) + "\n"


def analyze_battanian_starts(
    workspace: Path,
    culture: str = "Battania",
    json_output: Path | None = None,
    markdown_output: Path | None = None,
    top: int = 20,
) -> dict[str, Any]:
    workspace = workspace.resolve()
    stage_options = load_stage_options(workspace, culture)
    total_combinations = math.prod(len(stage_options[stage]) for stage in STAGES)
    paths, pruned = enumerate_paths(stage_options, DEFAULT_TARGET_ATTRIBUTES, culture)
    summary = summarize_paths(paths, top=top)
    payload = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "culture": culture,
        "stages": STAGES,
        "target_attributes": DEFAULT_TARGET_ATTRIBUTES,
        "focus_policy": FOCUS_POLICY,
        "stage_option_counts": {stage: len(stage_options[stage]) for stage in STAGES},
        "total_combinations": total_combinations,
        "pruned_branches": pruned,
        "summary": summary,
    }
    if json_output is not None:
        write_json(json_output, payload)
    if markdown_output is not None:
        markdown_output.parent.mkdir(parents=True, exist_ok=True)
        markdown_output.write_text(render_report(payload), encoding="utf-8", newline="\n")
    return payload


def analyze_culture_start_leaks(
    workspace: Path,
    cultures: list[str] | None = None,
    json_output: Path | None = None,
    markdown_output: Path | None = None,
    top: int = 20,
) -> dict[str, Any]:
    workspace = workspace.resolve()
    selected_cultures = cultures or list_family_cultures(workspace)
    culture_payloads = [
        analyze_battanian_starts(
            workspace=workspace,
            culture=culture,
            json_output=None,
            markdown_output=None,
            top=top,
        )
        for culture in selected_cultures
    ]
    payload = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "target_attributes": DEFAULT_TARGET_ATTRIBUTES,
        "focus_policy": FOCUS_POLICY,
        "cultures": culture_payloads,
    }
    if json_output is not None:
        write_json(json_output, payload)
    if markdown_output is not None:
        markdown_output.parent.mkdir(parents=True, exist_ok=True)
        markdown_output.write_text(render_culture_comparison_report(payload), encoding="utf-8", newline="\n")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze character creation focus leaks.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--culture", default="Battania")
    parser.add_argument("--all-cultures", action="store_true")
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    if args.all_cultures:
        json_output = args.json_output or workspace / "Data" / "intermediate" / "culture_start_leaks.json"
        markdown_output = args.markdown_output or workspace / "Docs" / "reports" / "culture-start-leaks.md"
        payload = analyze_culture_start_leaks(
            workspace=workspace,
            cultures=None,
            json_output=json_output,
            markdown_output=markdown_output,
            top=args.top,
        )
        print(f"Culture start leak JSON written: {json_output}")
        print(f"Culture start leak report written: {markdown_output}")
        for item in payload["cultures"]:
            summary = item["summary"]
            print(
                "  {culture}: valid {valid}, no-hard {no_hard}, perfect {perfect}".format(
                    culture=item["culture"],
                    valid=summary["attribute_valid_paths"],
                    no_hard=summary["no_hard_focus_leak_paths"],
                    perfect=summary["no_hard_no_tactics_paths"],
                )
            )
        return

    json_output = args.json_output or workspace / "Data" / "intermediate" / "battanian_start_leaks.json"
    markdown_output = args.markdown_output or workspace / "Docs" / "reports" / "battanian-start-leaks.md"
    payload = analyze_battanian_starts(
        workspace=workspace,
        culture=args.culture,
        json_output=json_output,
        markdown_output=markdown_output,
        top=args.top,
    )
    summary = payload["summary"]
    print(f"Battanian start leak JSON written: {json_output}")
    print(f"Battanian start leak report written: {markdown_output}")
    print(f"  attribute-valid paths: {summary['attribute_valid_paths']}")
    print(f"  no-hard-leak paths: {summary['no_hard_focus_leak_paths']}")
    print(f"  no-hard/no-tactics paths: {summary['no_hard_no_tactics_paths']}")


if __name__ == "__main__":
    main()
