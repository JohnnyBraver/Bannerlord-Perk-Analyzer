from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


MACHINE_FIELDS = {
    "perk_type",
    "perk_subtype",
    "trigger_condition",
    "add_trigger_condition",
    "remove_trigger_condition",
    "effect_tags",
    "add_effect_tags",
    "remove_effect_tags",
}

CURATED_FIELDS = {
    "perk_wrong",
    "needs_review",
    "functioning",
    "bug_note",
    "notes",
    "classification_review",
}

OVERRIDE_KEY_FIELDS = {"perk_string_id", "effect_slot"}


def default_workspace() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def add_unique(current: list[Any], values: Any) -> list[str]:
    result: list[str] = []
    for item in [*current, *as_list(values)]:
        text = str(item)
        if text not in result:
            result.append(text)
    return result


def remove_values(current: list[Any], values: Any) -> list[str]:
    removed = {str(item) for item in as_list(values)}
    return [str(item) for item in current if str(item) not in removed]


def override_key(item: dict[str, Any]) -> str:
    return f"{item.get('perk_string_id', '')}|{item.get('effect_slot', '')}"


def row_key(row: dict[str, Any]) -> str:
    return str(row["id"])


def sort_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            row.get("attribute") or "",
            row.get("skill") or "",
            int(row.get("level") or 0),
            row.get("perk") or "",
            row.get("effect_slot") or "",
        ),
    )


def load_overrides(path: Path) -> dict[str, dict[str, Any]]:
    items = read_json(path) if path.exists() else []
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        if not all(field in item for field in OVERRIDE_KEY_FIELDS):
            raise ValueError(f"Override entry is missing perk_string_id or effect_slot: {item!r}")
        key = override_key(item)
        if key in result:
            raise ValueError(f"Duplicate override key: {key}")
        result[key] = item
    return result


def ensure_review(row: dict[str, Any]) -> dict[str, Any]:
    review = row.setdefault("review", {})
    review.setdefault("needs_review", False)
    review.setdefault("functioning", None)
    review.setdefault("perk_wrong", False)
    review.setdefault("bug_note", "")
    review.setdefault("notes", "")
    review.setdefault("classification_review", "")
    return review


def ensure_provenance(row: dict[str, Any]) -> dict[str, Any]:
    provenance = row.setdefault(
        "provenance",
        {
            "generated": {
                "classification": copy.deepcopy(row.get("classification", {})),
                "review": copy.deepcopy(ensure_review(row)),
            },
            "postprocessed": {
                "override_fields": [],
                "changes": [],
            },
            "curated": {
                "override_fields": [],
                "changes": [],
            },
        },
    )
    return provenance


def append_change(
    row: dict[str, Any],
    stage: str,
    field: str,
    before: Any,
    after: Any,
    operation: str,
) -> None:
    if before == after:
        return
    stage_info = ensure_provenance(row)[stage]
    if field not in stage_info["override_fields"]:
        stage_info["override_fields"].append(field)
    stage_info["changes"].append(
        {
            "field": field,
            "operation": operation,
            "from": before,
            "to": after,
        }
    )


def apply_machine_field(row: dict[str, Any], name: str, value: Any) -> None:
    classification = row.setdefault("classification", {})
    if name == "perk_type":
        before = classification.get("perk_type", "")
        classification["perk_type"] = str(value)
        append_change(row, "postprocessed", "classification.perk_type", before, classification["perk_type"], "replace")
    elif name == "perk_subtype":
        before = classification.get("perk_subtype", "")
        classification["perk_subtype"] = str(value)
        append_change(row, "postprocessed", "classification.perk_subtype", before, classification["perk_subtype"], "replace")
    elif name == "trigger_condition":
        before = list(classification.get("trigger_conditions", []))
        classification["trigger_conditions"] = [str(item) for item in as_list(value)]
        append_change(row, "postprocessed", "classification.trigger_conditions", before, classification["trigger_conditions"], "replace")
    elif name == "add_trigger_condition":
        before = list(classification.get("trigger_conditions", []))
        classification["trigger_conditions"] = add_unique(before, value)
        append_change(row, "postprocessed", "classification.trigger_conditions", before, classification["trigger_conditions"], "add")
    elif name == "remove_trigger_condition":
        before = list(classification.get("trigger_conditions", []))
        classification["trigger_conditions"] = remove_values(before, value)
        append_change(row, "postprocessed", "classification.trigger_conditions", before, classification["trigger_conditions"], "remove")
    elif name == "effect_tags":
        before = list(classification.get("effect_tags", []))
        classification["effect_tags"] = [str(item) for item in as_list(value)]
        append_change(row, "postprocessed", "classification.effect_tags", before, classification["effect_tags"], "replace")
    elif name == "add_effect_tags":
        before = list(classification.get("effect_tags", []))
        classification["effect_tags"] = add_unique(before, value)
        append_change(row, "postprocessed", "classification.effect_tags", before, classification["effect_tags"], "add")
    elif name == "remove_effect_tags":
        before = list(classification.get("effect_tags", []))
        classification["effect_tags"] = remove_values(before, value)
        append_change(row, "postprocessed", "classification.effect_tags", before, classification["effect_tags"], "remove")


def apply_curated_field(row: dict[str, Any], name: str, value: Any) -> None:
    review = ensure_review(row)
    field = f"review.{name}"
    before = review.get(name)
    if name in {"perk_wrong", "needs_review"}:
        review[name] = bool(value)
    elif name == "functioning":
        review[name] = value
    else:
        review[name] = "" if value is None else str(value)
    append_change(row, "curated", field, before, review[name], "replace")


def apply_overrides(
    generated_rows: list[dict[str, Any]],
    overrides_by_key: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], Counter[str]]:
    generated_keys = {row_key(row) for row in generated_rows}
    missing = sorted(set(overrides_by_key) - generated_keys)
    if missing:
        raise ValueError("Override does not match a generated row: " + ", ".join(missing[:20]))

    stats: Counter[str] = Counter()
    postprocessed_rows: list[dict[str, Any]] = []
    final_rows: list[dict[str, Any]] = []

    for generated in sort_rows(generated_rows):
        key = row_key(generated)
        override = overrides_by_key.get(key, {})

        postprocessed = copy.deepcopy(generated)
        ensure_review(postprocessed)
        ensure_provenance(postprocessed)
        for name in sorted(MACHINE_FIELDS):
            if name in override:
                apply_machine_field(postprocessed, name, override[name])
                stats["machine_override_rows"] += 1
        postprocessed_rows.append(postprocessed)

        final = copy.deepcopy(postprocessed)
        for name in sorted(CURATED_FIELDS):
            if name in override:
                apply_curated_field(final, name, override[name])
                stats["curated_override_rows"] += 1
        final_rows.append(final)

    return postprocessed_rows, final_rows, stats


def safe_file_part(text: Any) -> str:
    safe = re.sub(r'[<>:"/\\|?*]', "-", str(text))
    safe = re.sub(r"\s+", " ", safe)
    return safe.strip()


def yaml_escape(value: Any) -> str:
    if value is None:
        return '""'
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def format_yaml_list(name: str, values: Any) -> list[str]:
    items: list[str] = []
    for value in as_list(values):
        text = str(value)
        if text.strip() and text not in items:
            items.append(text)
    if not items:
        return [f"{name}: []"]
    return [f"{name}:"] + [f"  - {yaml_escape(item)}" for item in items]


def format_number(value: Any) -> str:
    if isinstance(value, (int, float)):
        text = f"{float(value):.8f}".rstrip("0").rstrip(".")
        return text or "0"
    return str(value)


def format_nullable(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    return yaml_escape(value)


def write_markdown_rows(rows: list[dict[str, Any]], output_root: Path) -> int:
    output_root = output_root.resolve()
    workspace = output_root.parents[2]
    if workspace not in output_root.parents:
        raise ValueError(f"Refusing to write outside workspace: {output_root}")
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)

    seen: defaultdict[str, int] = defaultdict(int)
    count = 0
    for row in sort_rows(rows):
        game = row["game"]
        classification = row["classification"]
        review = ensure_review(row)
        duplicate_key = "|".join(
            [
                str(row["skill"]),
                str(row["level"]),
                str(row["perk"]),
                str(game["role"]),
                str(classification["perk_type"]),
                str(classification.get("perk_subtype") or ""),
            ]
        )
        seen[duplicate_key] += 1
        duplicate_suffix = f" - {seen[duplicate_key]}" if seen[duplicate_key] > 1 else ""
        subtype = f" - {classification['perk_subtype']}" if classification.get("perk_subtype") else ""
        skill_dir = output_root / safe_file_part(row["skill"])
        skill_dir.mkdir(parents=True, exist_ok=True)
        filename = (
            f"{int(row['level']):03d} - {safe_file_part(row['perk'])} - "
            f"{game['role']} - {classification['perk_type']}{subtype}{duplicate_suffix}.md"
        )
        path = skill_dir / filename
        lines = [
            "---",
            f"project: {yaml_escape(row['project'])}",
            f"type: {yaml_escape(row['type'])}",
            f"game_version_target: {yaml_escape(row['game_version_target'])}",
            f"attribute: {yaml_escape(row['attribute'])}",
            f"skill: {yaml_escape(row['skill'])}",
            f"level: {row['level']}",
            f"perk: {yaml_escape(row['perk'])}",
            f"perk_string_id: {yaml_escape(row['perk_string_id'])}",
            f"effect_slot: {yaml_escape(row['effect_slot'])}",
            f"role: {yaml_escape(game['role'])}",
            f"role_value: {game['role_value']}",
            f"perk_type: {yaml_escape(classification['perk_type'])}",
            f"perk_subtype: {yaml_escape(classification.get('perk_subtype') or '')}",
            *format_yaml_list("trigger_condition", classification.get("trigger_conditions", [])),
            *format_yaml_list("effect_tags", classification.get("effect_tags", [])),
            f"bonus: {format_number(game['bonus'])}",
            f"increment_type: {yaml_escape(game['increment_type'])}",
            f"increment_value: {game['increment_value']}",
            f"troop_usage: {yaml_escape(game['troop_usage'])}",
            f"troop_usage_value: {game['troop_usage_value']}",
            f"effect: {yaml_escape(game['effect'])}",
            f"effect_template: {yaml_escape(game['effect_template'])}",
            f"alternative_perk_string_id: {yaml_escape(row.get('alternative_perk_string_id') or '')}",
            f"source_status: {yaml_escape(row['source']['status'])}",
            f"source: {yaml_escape(row['source']['name'])}",
            f"source_version: {yaml_escape(row['source']['version'])}",
            f"needs_review: {str(review['needs_review']).lower()}",
            f"functioning: {format_nullable(review['functioning'])}",
            f"perk_wrong: {str(review['perk_wrong']).lower()}",
            f"bug_note: {yaml_escape(review['bug_note'])}",
            f"notes: {yaml_escape(review['notes'])}",
            f"classification_review: {yaml_escape(review['classification_review'])}",
            "---",
            "",
            f"# {row['perk']} - {game['role']} - {classification['perk_type']}",
            "",
            str(game["effect"]),
            "",
        ]
        path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
        count += 1
    return count


def table_escape(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def write_review_report(rows: list[dict[str, Any]], path: Path) -> int:
    review_rows = [row for row in rows if ensure_review(row).get("classification_review")]
    lines = [
        "# Perk Classification Review",
        "",
        "Generated from local Bannerlord assembly data. Rows listed here are classification heuristics that look ambiguous and should be hand-checked.",
        "",
    ]
    if not review_rows:
        lines.append("No classification review flags were generated.")
    else:
        lines += [
            "| Skill | Level | Perk | Role | Type | Subtype | Effect | Review |",
            "|---|---:|---|---|---|---|---|---|",
        ]
        for row in sort_rows(review_rows):
            game = row["game"]
            classification = row["classification"]
            review = ensure_review(row)
            lines.append(
                "| {skill} | {level} | {perk} | {role} | {ptype} | {subtype} | {effect} | {review} |".format(
                    skill=table_escape(row["skill"]),
                    level=row["level"],
                    perk=table_escape(row["perk"]),
                    role=table_escape(game["role"]),
                    ptype=table_escape(classification["perk_type"]),
                    subtype=table_escape(classification.get("perk_subtype") or ""),
                    effect=table_escape(game["effect"]),
                    review=table_escape(review["classification_review"]),
                )
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return len(review_rows)


def collect_tag_index(rows: list[dict[str, Any]]) -> dict[str, list[str]]:
    def unique_sorted(values: list[Any]) -> list[str]:
        return sorted({str(value) for value in values if str(value).strip()})

    return {
        "roles": unique_sorted([row["game"]["role"] for row in rows]),
        "perk_types": unique_sorted([row["classification"]["perk_type"] for row in rows]),
        "perk_subtypes": unique_sorted([row["classification"].get("perk_subtype", "") for row in rows]),
        "trigger_conditions": unique_sorted(
            [
                condition
                for row in rows
                for condition in row["classification"].get("trigger_conditions", [])
            ]
        ),
        "effect_tags": unique_sorted(
            [tag for row in rows for tag in row["classification"].get("effect_tags", [])]
        ),
    }


def write_tag_report(tag_index: dict[str, list[str]], path: Path) -> None:
    section_names = [
        ("roles", "role"),
        ("perk_types", "perk_type"),
        ("perk_subtypes", "perk_subtype"),
        ("trigger_conditions", "trigger_condition"),
        ("effect_tags", "effect_tags"),
    ]
    lines: list[str] = []
    for index, (json_name, title) in enumerate(section_names):
        if index:
            lines.append("")
        lines.append(title)
        lines.extend(tag_index[json_name])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def summarize_overrides(overrides_by_key: dict[str, dict[str, Any]]) -> dict[str, int]:
    summary = Counter()
    for override in overrides_by_key.values():
        fields = set(override) - OVERRIDE_KEY_FIELDS
        has_machine = bool(fields & MACHINE_FIELDS)
        has_curated = bool(fields & CURATED_FIELDS)
        summary["override_entries"] += 1
        if has_machine:
            summary["entries_with_machine_fields"] += 1
        if has_curated:
            summary["entries_with_curated_fields"] += 1
        if has_machine and has_curated:
            summary["entries_with_mixed_fields"] += 1
    return dict(summary)


def postprocess(workspace: Path) -> None:
    generated_path = workspace / "Data" / "generated" / "classified-perk-effects.json"
    postprocessed_path = workspace / "Data" / "generated" / "postprocessed-perk-effects.json"
    overrides_path = workspace / "Data" / "curated" / "perk-effect-overrides.json"
    export_path = workspace / "Data" / "export" / "perk-effects.json"
    tag_index_export_path = workspace / "Data" / "export" / "tag-index.json"
    markdown_root = workspace / "Data" / "generated" / "perk-effects"
    reports_root = workspace / "Data" / "generated" / "reports"

    generated_rows = read_json(generated_path)
    overrides_by_key = load_overrides(overrides_path)
    postprocessed_rows, final_rows, apply_stats = apply_overrides(generated_rows, overrides_by_key)
    final_rows = sort_rows(final_rows)
    postprocessed_rows = sort_rows(postprocessed_rows)

    write_json(postprocessed_path, postprocessed_rows)
    write_json(export_path, final_rows)
    tag_index = collect_tag_index(final_rows)
    write_json(tag_index_export_path, tag_index)
    markdown_count = write_markdown_rows(final_rows, markdown_root)
    review_count = write_review_report(final_rows, reports_root / "perk-classification-review.md")
    write_tag_report(tag_index, reports_root / "tag-index.md")

    override_summary = summarize_overrides(overrides_by_key)
    print(f"Generated rows read: {len(generated_rows)}")
    print(f"Postprocessed rows written: {len(postprocessed_rows)}")
    print(f"Final export rows written: {len(final_rows)}")
    print(f"Markdown files written: {markdown_count}")
    print(f"Review flags: {review_count}")
    print(f"Overrides: {override_summary.get('override_entries', 0)} entries")
    print(f"  machine entries: {override_summary.get('entries_with_machine_fields', 0)}")
    print(f"  curated entries: {override_summary.get('entries_with_curated_fields', 0)}")
    print(f"  mixed entries: {override_summary.get('entries_with_mixed_fields', 0)}")
    print(f"  machine field applications: {apply_stats.get('machine_override_rows', 0)}")
    print(f"  curated field applications: {apply_stats.get('curated_override_rows', 0)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply perk-effect post-processing and curated review data.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    args = parser.parse_args()
    postprocess(args.workspace.resolve())


if __name__ == "__main__":
    main()
