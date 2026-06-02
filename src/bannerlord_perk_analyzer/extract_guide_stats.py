from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
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


def load_plugins() -> list[Any]:
    plugins_dir = Path(__file__).resolve().parent / "guide_extractors"
    plugins = []
    if not plugins_dir.exists():
        return plugins
    for p in sorted(plugins_dir.glob("*.py")):
        if p.name == "__init__.py":
            continue
        module_name = f"guide_extractors.{p.stem}"
        spec = importlib.util.spec_from_file_location(module_name, p)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            plugins.append(module)
    return plugins


def build_payload(workspace: Path, perk_export_path: Path) -> dict[str, Any]:
    rows = read_json(perk_export_path)
    index = {row_key(row): row for row in rows}

    plugins = load_plugins()

    direct_weapon_effects = []
    ai_behavior_formulas = []
    survival_formulas = []
    smithing_formulas = []
    guide_buckets_list = []
    
    stacks_def = {
        "ai_skill": [],
        "hit_points": [],
        "armor": [],
        "damage_reduction": [],
    }

    for plugin in plugins:
        if hasattr(plugin, "get_weapon_effects"):
            direct_weapon_effects.extend(plugin.get_weapon_effects())
        if hasattr(plugin, "get_behavior_formulas"):
            ai_behavior_formulas.extend(plugin.get_behavior_formulas())
        if hasattr(plugin, "get_survival_formulas"):
            survival_formulas.extend(plugin.get_survival_formulas())
        if hasattr(plugin, "get_smithing_formulas"):
            smithing_formulas.extend(plugin.get_smithing_formulas())
        if hasattr(plugin, "get_buckets"):
            guide_buckets_list.extend(plugin.get_buckets())
        if hasattr(plugin, "get_stacks"):
            plugin_stacks = plugin.get_stacks()
            for key, val in plugin_stacks.items():
                if key in stacks_def:
                    stacks_def[key].extend(val)

    buckets: dict[str, Any] = {}
    for bucket in guide_buckets_list:
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
        "direct_weapon_effects": direct_weapon_effects,
        "ai_behavior_formulas": ai_behavior_formulas,
        "survival_formulas": survival_formulas,
        "smithing_formulas": smithing_formulas,
        "buckets": buckets,
        "stacks": {
            "ai_skill": [build_stack(index, definition) for definition in stacks_def["ai_skill"]],
            "hit_points": [build_stack(index, definition) for definition in stacks_def["hit_points"]],
            "armor": [build_stack(index, definition) for definition in stacks_def["armor"]],
            "damage_reduction": [build_stack(index, definition) for definition in stacks_def["damage_reduction"]],
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
    json_output = args.json_output or workspace / "Data" / "export" / "guide-stat-extracts.json"
    markdown_output = args.markdown_output or workspace / "Docs" / "reports" / "guide-stat-extracts.md"
    extract_guide_stats(
        workspace=workspace,
        perk_export_path=perk_export_path.resolve(),
        json_output=json_output,
        markdown_output=markdown_output,
    )


if __name__ == "__main__":
    main()
