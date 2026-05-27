from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from .postprocess import MACHINE_FIELDS, default_workspace, read_json, write_json
except ImportError:
    from postprocess import MACHINE_FIELDS, default_workspace, read_json, write_json


def as_strings(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def same_members(left: Any, right: Any) -> bool:
    return set(as_strings(left)) == set(as_strings(right))


def row_key(row: dict[str, Any]) -> str:
    return str(row["id"])


def override_key(override: dict[str, Any]) -> str:
    return f"{override.get('perk_string_id', '')}|{override.get('effect_slot', '')}"


def prune_machine_field(override: dict[str, Any], row: dict[str, Any], field: str) -> bool:
    classification = row.get("classification", {})

    if field == "perk_type":
        return str(classification.get("perk_type", "")) == str(override[field])
    if field == "perk_subtype":
        return str(classification.get("perk_subtype", "")) == str(override[field])

    if field == "trigger_condition":
        return same_members(classification.get("trigger_conditions", []), override[field])
    if field == "effect_tags":
        return same_members(classification.get("effect_tags", []), override[field])

    if field == "add_trigger_condition":
        current = set(as_strings(classification.get("trigger_conditions", [])))
        missing = [value for value in as_strings(override[field]) if value not in current]
        if missing:
            override[field] = missing
            return False
        return True

    if field == "add_effect_tags":
        current = set(as_strings(classification.get("effect_tags", [])))
        missing = [value for value in as_strings(override[field]) if value not in current]
        if missing:
            override[field] = missing
            return False
        return True

    if field == "remove_trigger_condition":
        current = set(as_strings(classification.get("trigger_conditions", [])))
        present = [value for value in as_strings(override[field]) if value in current]
        if present:
            override[field] = present
            return False
        return True

    if field == "remove_effect_tags":
        current = set(as_strings(classification.get("effect_tags", [])))
        present = [value for value in as_strings(override[field]) if value in current]
        if present:
            override[field] = present
            return False
        return True

    return False


def prune_overrides(workspace: Path, dry_run: bool = False) -> tuple[int, int, int]:
    generated_path = workspace / "Data" / "generated" / "classified-perk-effects.json"
    override_path = workspace / "Data" / "curated" / "perk-effect-overrides.json"

    generated_rows = read_json(generated_path)
    rows_by_key = {row_key(row): row for row in generated_rows}
    overrides = read_json(override_path)

    kept: list[dict[str, Any]] = []
    removed_entries = 0
    removed_fields = 0

    for original in overrides:
        override = dict(original)
        key = override_key(override)
        row = rows_by_key.get(key)
        if row is None:
            kept.append(override)
            continue

        for field in list(override):
            if field not in MACHINE_FIELDS:
                continue
            if prune_machine_field(override, row, field):
                del override[field]
                removed_fields += 1

        if set(override) <= {"perk_string_id", "effect_slot"}:
            removed_entries += 1
            continue
        kept.append(override)

    if not dry_run:
        write_json(override_path, kept)

    return len(overrides), len(kept), removed_fields


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove redundant machine override fields already handled by the classifier.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    before, after, removed_fields = prune_overrides(args.workspace.resolve(), dry_run=args.dry_run)
    action = "Would prune" if args.dry_run else "Pruned"
    print(f"{action} {before - after} override entries and {removed_fields} machine fields.")
    print(f"Overrides: {before} -> {after}")


if __name__ == "__main__":
    main()
