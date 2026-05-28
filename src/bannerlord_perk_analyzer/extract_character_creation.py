from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from .postprocess import default_workspace
    from .xp_reports import display_path, table_escape
except ImportError:
    from postprocess import default_workspace
    from xp_reports import display_path, table_escape


SCAN_ASSEMBLIES = [
    "TaleWorlds.CampaignSystem",
    "StoryMode",
]

SCAN_QUERIES = [
    "CharacterCreationCampaignBehavior",
    "StoryModeCharacterCreationCampaignBehavior",
    "NarrativeOptionArgs",
    "SetAffectedSkills",
    "SetFocusToSkills",
    "SetLevelToSkills",
    "SetLevelToAttribute",
    "SetAffectedTraits",
    "SetLevelToTraits",
    "SetRenownToAdd",
    "SetUnspentFocusToAdd",
    "SetUnspentAttributeToAdd",
]

STAGE_ORDER = [
    "family",
    "childhood",
    "education",
    "youth",
    "adulthood",
    "age",
    "escape",
    "other",
]

CULTURE_PREFIXES = {
    "Aserai": "Aserai",
    "Battania": "Battania",
    "Empire": "Empire",
    "Khuzait": "Khuzait",
    "Sturgia": "Sturgia",
    "Vlandia": "Vlandia",
}

SKILL_ORDER = [
    "One Handed",
    "Two Handed",
    "Polearm",
    "Bow",
    "Crossbow",
    "Throwing",
    "Riding",
    "Athletics",
    "Smithing",
    "Scouting",
    "Tactics",
    "Roguery",
    "Charm",
    "Leadership",
    "Trade",
    "Steward",
    "Medicine",
    "Engineering",
]

SKILL_NAME_MAP = {
    "OneHanded": "One Handed",
    "TwoHanded": "Two Handed",
    "Polearm": "Polearm",
    "Bow": "Bow",
    "Crossbow": "Crossbow",
    "Throwing": "Throwing",
    "Riding": "Riding",
    "Athletics": "Athletics",
    "Crafting": "Smithing",
    "Scouting": "Scouting",
    "Tactics": "Tactics",
    "Roguery": "Roguery",
    "Charm": "Charm",
    "Leadership": "Leadership",
    "Trade": "Trade",
    "Steward": "Steward",
    "Medicine": "Medicine",
    "Engineering": "Engineering",
}


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def resolve_game_root(game_root: Path | None) -> Path:
    env_game_root = os.environ.get("BANNERLORD_GAME_ROOT")
    if game_root is None and not env_game_root:
        raise SystemExit("Bannerlord game root is required. Pass --game-root or set BANNERLORD_GAME_ROOT.")
    return (game_root or Path(str(env_game_root))).resolve()


def run_find_methods(workspace: Path, game_root: Path, output: Path) -> dict[str, Any]:
    project = workspace / "tools" / "BannerlordExtractor" / "BannerlordExtractor.csproj"
    if not project.exists():
        raise SystemExit(f"Extractor project is missing: {project}")

    command = [
        "dotnet",
        "run",
        "--project",
        str(project),
        "--",
        "find-methods",
        "--game-root",
        str(game_root),
        "--include-il",
        "--output",
        str(output),
    ]
    for assembly in SCAN_ASSEMBLIES:
        command.extend(["--assembly", assembly])
    for query in SCAN_QUERIES:
        command.extend(["--query", query])

    subprocess.run(command, check=True)
    return read_json(output)


def strip_loc_prefix(text: str) -> str:
    return re.sub(r"^\{=[^}]*\}", "", text).strip()


def slugify(text: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", text.lower())).strip("_")


def split_words(text: str) -> str:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    return spaced.replace("_", " ").strip()


def type_short_name(type_name: str) -> str:
    return type_name.split("+")[-1].split(".")[-1]


def short_method_name(method: dict[str, Any]) -> str:
    return f"{type_short_name(str(method.get('type', '')))}.{method.get('method')}"


def referenced_text(method: dict[str, Any]) -> str:
    return "\n".join(str(value) for value in (method.get("referenced_members", []) + method.get("il", [])))


def sort_skills(skills: list[str]) -> list[str]:
    return sorted(set(skills), key=lambda skill: SKILL_ORDER.index(skill) if skill in SKILL_ORDER else 999)


def parse_ldstr(line: str) -> str | None:
    if " ldstr" not in line:
        return None
    return line.split("ldstr", 1)[1].strip()


def parse_ldc_i4(line: str) -> int | None:
    if "ldc.i4.m1" in line:
        return -1
    special = re.search(r"ldc\.i4\.([0-8])\b", line)
    if special:
        return int(special.group(1))
    value = re.search(r"ldc\.i4(?:\.s)?\s+(-?\d+)", line)
    if value:
        return int(value.group(1))
    return None


def parse_field_name(line: str) -> str | None:
    match = re.search(r"\.(_[A-Za-z0-9]+)$", line.strip())
    return match.group(1) if match else None


def constructor_defaults(payload: dict[str, Any]) -> dict[str, int]:
    defaults: dict[str, int] = {}
    for method in payload.get("methods", []):
        if method.get("method") != ".ctor":
            continue
        lines = list(method.get("il", []))
        for index, line in enumerate(lines):
            if " stfld" not in line:
                continue
            field_name = parse_field_name(str(line))
            if not field_name:
                continue
            for previous in reversed(lines[max(0, index - 4) : index]):
                value = parse_ldc_i4(str(previous))
                if value is not None:
                    defaults[field_name] = value
                    break
    return defaults


def value_before_call(il: list[str], call_name: str, field_defaults: dict[str, int]) -> int | None:
    for index, line in enumerate(il):
        if f".{call_name}(" not in line:
            continue
        for previous in reversed(il[max(0, index - 10) : index]):
            field_name = parse_field_name(str(previous))
            if field_name and field_name in field_defaults:
                return field_defaults[field_name]
            value = parse_ldc_i4(str(previous))
            if value is not None:
                return value
    return None


def option_registration_map(payload: dict[str, Any]) -> dict[str, dict[str, str]]:
    registrations: dict[str, dict[str, str]] = {}
    for method in payload.get("methods", []):
        il = [str(line) for line in method.get("il", [])]
        if not il:
            continue
        for index, line in enumerate(il):
            if " ldftn" not in line:
                continue
            match = re.search(r"\.(Get[A-Za-z0-9]+OptionArgs)\(", line)
            if not match:
                continue

            strings: list[str] = []
            for previous in reversed(il[:index]):
                literal = parse_ldstr(previous)
                if literal is None:
                    continue
                strings.append(literal)
                if len(strings) == 3:
                    break
            if len(strings) < 3:
                continue

            option_method = match.group(1)
            registrations[option_method] = {
                "option_id": strings[2],
                "title_raw": strings[1],
                "title": strip_loc_prefix(strings[1]),
                "description_raw": strings[0],
                "description": strip_loc_prefix(strings[0]),
                "registration_method": str(method.get("method", "")),
                "registration_type": str(method.get("type", "")),
            }
    return registrations


def stage_for_method(method: dict[str, Any]) -> str:
    name = str(method.get("method", ""))
    type_name = str(method.get("type", ""))
    if "StoryModeCharacterCreationCampaignBehavior" in type_name:
        return "escape"
    if name.startswith("GetAgeSelection"):
        return "age"
    if name.startswith("GetChildhood"):
        return "childhood"
    if name.startswith("GetEducation"):
        return "education"
    if name.startswith("GetYouth") or name.startswith("GetEnvoys"):
        return "youth"
    if name.startswith("GetAdulthood"):
        return "adulthood"
    if any(name.startswith(f"Get{prefix}") for prefix in CULTURE_PREFIXES):
        return "family"
    return "other"


def culture_for_method(method: dict[str, Any]) -> str:
    name = str(method.get("method", ""))
    for prefix, culture in CULTURE_PREFIXES.items():
        if name.startswith(f"Get{prefix}"):
            return culture
    return ""


def method_choice_name(method_name: str) -> str:
    name = method_name
    name = re.sub(r"^Get", "", name)
    name = re.sub(r"NarrativeOptionArgs$", "", name)
    name = re.sub(r"OptionArgs$", "", name)
    for prefix in [
        *CULTURE_PREFIXES,
        "Childhood",
        "Education",
        "Youth",
        "Adulthood",
        "AgeSelection",
        "Escape",
    ]:
        if name.startswith(prefix):
            name = name[len(prefix) :]
            break
    return split_words(name)


def option_sort_key(option: dict[str, Any]) -> tuple[int, str, str, str]:
    stage = str(option.get("stage", "other"))
    return (
        STAGE_ORDER.index(stage) if stage in STAGE_ORDER else 999,
        str(option.get("culture", "")),
        str(option.get("option_id", "")),
        str(option.get("method", "")),
    )


def extract_skills(text: str) -> list[str]:
    matches = re.findall(r"TaleWorlds\.Core\.DefaultSkills\.get_([A-Za-z0-9_]+)\(", text)
    return sort_skills([SKILL_NAME_MAP.get(match, match) for match in matches])


def extract_attribute(text: str) -> str:
    matches = re.findall(r"TaleWorlds\.Core\.DefaultCharacterAttributes\.get_([A-Za-z0-9_]+)\(", text)
    return matches[0] if matches else ""


def extract_traits(text: str) -> list[str]:
    matches = re.findall(r"TaleWorlds\.CampaignSystem\.CharacterDevelopment\.DefaultTraits\.get_([A-Za-z0-9_]+)\(", text)
    return sorted(set(matches))


def extract_options(payload: dict[str, Any]) -> list[dict[str, Any]]:
    field_defaults = constructor_defaults(payload)
    registrations = option_registration_map(payload)
    options: list[dict[str, Any]] = []

    for method in payload.get("methods", []):
        method_name = str(method.get("method", ""))
        if not (method_name.startswith("Get") and method_name.endswith("OptionArgs")):
            continue
        if "CharacterCreationCampaignBehavior" not in str(method.get("type", "")):
            continue

        il = [str(line) for line in method.get("il", [])]
        text = referenced_text(method)
        registration = registrations.get(method_name, {})
        skills = extract_skills(text)
        skill_focus = value_before_call(il, "SetFocusToSkills", field_defaults) or 0
        skill_levels = value_before_call(il, "SetLevelToSkills", field_defaults) or 0
        attribute = extract_attribute(text)
        attribute_levels = value_before_call(il, "SetLevelToAttribute", field_defaults) or 0
        trait_levels = value_before_call(il, "SetLevelToTraits", field_defaults) or 0

        option_id = registration.get("option_id", slugify(method_choice_name(method_name)))
        choice_name = registration.get("title") or method_choice_name(method_name)
        option = {
            "id": option_id,
            "option_id": option_id,
            "title": choice_name,
            "title_raw": registration.get("title_raw", ""),
            "description": registration.get("description", ""),
            "description_raw": registration.get("description_raw", ""),
            "stage": stage_for_method(method),
            "culture": culture_for_method(method),
            "assembly": method.get("assembly", ""),
            "type": method.get("type", ""),
            "method": method_name,
            "short_method": short_method_name(method),
            "registration_method": registration.get("registration_method", ""),
            "effects": {
                "skills": [
                    {
                        "skill": skill,
                        "focus": skill_focus,
                        "skill_levels": skill_levels,
                    }
                    for skill in skills
                ],
                "attribute": {
                    "attribute": attribute,
                    "levels": attribute_levels,
                }
                if attribute
                else None,
                "traits": [
                    {
                        "trait": trait,
                        "levels": trait_levels,
                    }
                    for trait in extract_traits(text)
                ],
                "renown": value_before_call(il, "SetRenownToAdd", field_defaults) or 0,
                "unspent_focus": value_before_call(il, "SetUnspentFocusToAdd", field_defaults) or 0,
                "unspent_attribute": value_before_call(il, "SetUnspentAttributeToAdd", field_defaults) or 0,
            },
            "numeric_constants": method.get("numeric_constants", []),
        }
        options.append(option)

    return sorted(options, key=option_sort_key)


def effect_summary(option: dict[str, Any]) -> str:
    effects = option.get("effects", {})
    parts: list[str] = []
    attribute = effects.get("attribute")
    if attribute:
        parts.append(f"+{attribute['levels']} {attribute['attribute']}")

    skills = effects.get("skills", [])
    if skills:
        skill_names = ", ".join(skill["skill"] for skill in skills)
        focus = skills[0].get("focus", 0)
        levels = skills[0].get("skill_levels", 0)
        skill_parts = []
        if focus:
            skill_parts.append(f"+{focus} focus")
        if levels:
            skill_parts.append(f"+{levels} skill")
        if skill_parts:
            parts.append(f"{' and '.join(skill_parts)} to {skill_names}")

    traits = effects.get("traits", [])
    for trait in traits:
        parts.append(f"+{trait['levels']} {trait['trait']} trait")

    renown = effects.get("renown", 0)
    if renown:
        parts.append(f"+{renown} renown")

    unspent_focus = effects.get("unspent_focus", 0)
    unspent_attribute = effects.get("unspent_attribute", 0)
    if unspent_focus:
        parts.append(f"+{unspent_focus} unspent focus")
    if unspent_attribute:
        parts.append(f"+{unspent_attribute} unspent attribute")

    return "; ".join(parts) if parts else "No mechanical effect found"


def title_case_stage(stage: str) -> str:
    return stage.replace("_", " ").title()


def write_markdown(payload: dict[str, Any], options: list[dict[str, Any]], path: Path, workspace: Path, json_output: Path) -> None:
    stage_counts = Counter(str(option["stage"]) for option in options)
    skill_counts = Counter(
        skill["skill"]
        for option in options
        for skill in option.get("effects", {}).get("skills", [])
    )
    attribute_counts = Counter(
        option.get("effects", {}).get("attribute", {}).get("attribute")
        for option in options
        if option.get("effects", {}).get("attribute")
    )
    field_defaults = payload.get("character_creation_field_defaults", {})

    lines = [
        "# Bannerlord Character Creation Choices",
        "",
        f"Generated: {payload.get('generated_at', '')}",
        "",
        "This report is extracted from local compiled assemblies. It covers the initial player character creation option effects exposed through `NarrativeMenuOptionArgs`.",
        "",
        "## Reading Notes",
        "",
        "- The standard non-age options use constructor defaults: "
        f"+{field_defaults.get('_focusToAdd', '?')} focus per affected skill, "
        f"+{field_defaults.get('_skillLevelToAdd', '?')} skill levels per affected skill, and "
        f"+{field_defaults.get('_attributeLevelToAdd', '?')} attribute level.",
        "- `Smithing` appears as `Crafting` in the compiled `DefaultSkills` API; this report displays the player-facing skill name.",
        "- Age choices add unspent points rather than assigning them to a specific skill or attribute.",
        "- Story-mode escape choices are included because they use the same character creation option effect path.",
        "",
        "## Stage Summary",
        "",
        "| Stage | Options |",
        "| --- | ---: |",
    ]
    for stage in STAGE_ORDER:
        if stage_counts.get(stage):
            lines.append(f"| {title_case_stage(stage)} | {stage_counts[stage]} |")

    lines += [
        "",
        "## Skill Coverage",
        "",
        "| Skill | Choice count |",
        "| --- | ---: |",
    ]
    for skill in SKILL_ORDER:
        if skill_counts.get(skill):
            lines.append(f"| {skill} | {skill_counts[skill]} |")

    lines += [
        "",
        "## Attribute Coverage",
        "",
        "| Attribute | Choice count |",
        "| --- | ---: |",
    ]
    for attribute, count in sorted(attribute_counts.items()):
        lines.append(f"| {attribute} | {count} |")

    lines += [
        "",
        "## Options",
        "",
    ]
    current_stage = ""
    for option in options:
        stage = str(option["stage"])
        if stage != current_stage:
            if current_stage:
                lines.append("")
            current_stage = stage
            lines += [
                f"### {title_case_stage(stage)}",
                "",
                "| Culture | Choice | Effects | Option id |",
                "| --- | --- | --- | --- |",
            ]
        culture = option.get("culture") or ""
        lines.append(
            "| {culture} | {choice} | {effects} | `{option_id}` |".format(
                culture=table_escape(culture),
                choice=table_escape(option.get("title", "")),
                effects=table_escape(effect_summary(option)),
                option_id=table_escape(option.get("option_id", "")),
            )
        )

    lines += [
        "",
        "## Outputs",
        "",
        f"- JSON: `{display_path(json_output, workspace)}`",
        f"- Report: `{display_path(path, workspace)}`",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def extract_character_creation(
    workspace: Path,
    game_root: Path | None,
    json_output: Path,
    markdown_output: Path,
    skip_scan: bool,
) -> None:
    if skip_scan and json_output.exists():
        payload = read_json(json_output)
    else:
        payload = run_find_methods(workspace, resolve_game_root(game_root), json_output)

    options = extract_options(payload)
    payload["character_creation_field_defaults"] = constructor_defaults(payload)
    payload["character_creation_options"] = options
    payload["character_creation_option_count"] = len(options)
    write_json(json_output, payload)
    write_markdown(payload, options, markdown_output, workspace, json_output)
    print(f"Character creation JSON written: {json_output}")
    print(f"Character creation report written: {markdown_output}")
    print(f"Character creation options: {len(options)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Bannerlord character creation option effects.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--game-root", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    parser.add_argument("--skip-scan", action="store_true", help="Reuse the existing JSON output and regenerate only the markdown.")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    json_output = args.json_output or workspace / "Data" / "generated" / "character-creation-options.json"
    markdown_output = args.markdown_output or workspace / "Data" / "generated" / "reports" / "character-creation-options.md"
    extract_character_creation(
        workspace=workspace,
        game_root=args.game_root,
        json_output=json_output,
        markdown_output=markdown_output,
        skip_scan=args.skip_scan,
    )


if __name__ == "__main__":
    main()
