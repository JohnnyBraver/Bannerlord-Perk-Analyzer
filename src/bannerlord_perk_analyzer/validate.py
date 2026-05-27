from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


EXPECTED_WRONG = {
    "BowTrainer|primary",
    "TradeLocalConnection|primary",
    "RogueryArmsDealer|secondary",
    "ThrowingSplinters|primary",
    "TacticsGensdarmes|primary",
    "TwoHandedOnTheEdge|secondary",
    "CrossbowLooseAndMove|secondary",
    "BowBowControl|secondary",
    "BowDeadAim|secondary",
    "BowBodkin|secondary",
    "BowNockingPoint|secondary",
    "BowQuickAdjustments|secondary",
    "BowRapidFire|secondary",
    "BowStrongBows|secondary",
    "BowSkirmishPhaseMaster|secondary",
    "BowBullsEye|primary",
    "EngineeringImprovedTools|secondary",
    "OneHandedWrappedHandles|secondary",
    "OneHandedDeadlyPurpose|secondary",
    "PolearmCavalry|secondary",
    "PolearmSwiftSwing|secondary",
    "PolearmUnstoppableForce|primary",
    "PolearmUnstoppableForce|secondary",
    "PolearmSharpenTheTip|secondary",
    "RogueryCarver|secondary",
    "ThrowingMountedSkirmisher|secondary",
    "ThrowingKnockOff|secondary",
    "ThrowingSaddlebags|secondary",
    "TwoHandedVandal|secondary",
}


def default_workspace() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def yaml_scalar(text: str, name: str) -> str:
    quoted = re.search(rf'(?m)^{re.escape(name)}: "([^"]*)"', text)
    if quoted:
        return quoted.group(1)
    scalar = re.search(rf"(?m)^{re.escape(name)}: ([^\r\n]+)", text)
    if scalar:
        return scalar.group(1).strip()
    return ""


def yaml_list(text: str, name: str) -> list[str]:
    match = re.search(rf'(?ms)^{re.escape(name)}:[ \t]*(?P<body>(?:\r?\n  - "[^"]*")*)', text)
    if not match:
        return []
    return re.findall(r'  - "([^"]*)"', match.group("body"))


def read_markdown_rows(data_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(data_root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        key = f"{yaml_scalar(text, 'perk_string_id')}|{yaml_scalar(text, 'effect_slot')}"
        rows.append(
            {
                "path": path,
                "key": key,
                "perk_string_id": yaml_scalar(text, "perk_string_id"),
                "effect_slot": yaml_scalar(text, "effect_slot"),
                "role": yaml_scalar(text, "role"),
                "perk_type": yaml_scalar(text, "perk_type"),
                "perk_subtype": yaml_scalar(text, "perk_subtype"),
                "trigger_conditions": yaml_list(text, "trigger_condition"),
                "effect_tags": yaml_list(text, "effect_tags"),
                "troop_usage": yaml_scalar(text, "troop_usage"),
                "effect": yaml_scalar(text, "effect"),
                "perk_wrong": yaml_scalar(text, "perk_wrong") == "true",
            }
        )
    return rows


def row_key(row: dict[str, Any]) -> str:
    return str(row["id"])


def override_key(override: dict[str, Any]) -> str:
    return f"{override.get('perk_string_id', '')}|{override.get('effect_slot', '')}"


def validate(workspace: Path) -> None:
    markdown_root = workspace / "Data" / "generated" / "perk-effects"
    override_path = workspace / "Data" / "curated" / "perk-effect-overrides.json"
    raw_perks_path = workspace / "Data" / "raw" / "perks.json"
    generated_path = workspace / "Data" / "generated" / "classified-perk-effects.json"
    postprocessed_path = workspace / "Data" / "generated" / "postprocessed-perk-effects.json"
    export_path = workspace / "Data" / "export" / "perk-effects.json"
    tag_index_export_path = workspace / "Data" / "export" / "tag-index.json"

    errors: list[str] = []
    markdown_rows = read_markdown_rows(markdown_root)
    markdown_by_key: dict[str, dict[str, Any]] = {}
    for row in markdown_rows:
        if row["key"] in markdown_by_key:
            errors.append(f"Duplicate markdown row key: {row['key']}")
        markdown_by_key[row["key"]] = row

    raw_perks = read_json(raw_perks_path)
    generated_rows = read_json(generated_path)
    postprocessed_rows = read_json(postprocessed_path)
    export_rows = read_json(export_path)
    tag_index = read_json(tag_index_export_path)
    overrides = read_json(override_path)

    if not raw_perks:
        errors.append(f"Raw perk export is empty: {raw_perks_path}")

    generated_by_key = {row_key(row): row for row in generated_rows}
    postprocessed_by_key = {row_key(row): row for row in postprocessed_rows}
    export_by_key = {row_key(row): row for row in export_rows}

    if len(generated_by_key) != len(generated_rows):
        errors.append("Generated JSON contains duplicate row keys.")
    if len(postprocessed_by_key) != len(postprocessed_rows):
        errors.append("Postprocessed JSON contains duplicate row keys.")
    if len(export_by_key) != len(export_rows):
        errors.append("Export JSON contains duplicate row keys.")

    if len(postprocessed_rows) != len(generated_rows):
        errors.append(
            f"Postprocessed row count {len(postprocessed_rows)} does not match generated row count {len(generated_rows)}."
        )
    if len(export_rows) != len(generated_rows):
        errors.append(f"Export row count {len(export_rows)} does not match generated row count {len(generated_rows)}.")
    if len(markdown_rows) != len(export_rows):
        errors.append(f"Markdown row count {len(markdown_rows)} does not match export row count {len(export_rows)}.")

    for key in generated_by_key:
        if key not in postprocessed_by_key:
            errors.append(f"Generated row missing from postprocessed JSON: {key}")
        if key not in export_by_key:
            errors.append(f"Generated row missing from final export: {key}")
        if key not in markdown_by_key:
            errors.append(f"Generated row missing from markdown output: {key}")

    for override in overrides:
        key = override_key(override)
        if key not in generated_by_key:
            errors.append(f"Override does not match a generated row: {key}")

    for row in export_rows:
        if "provenance" not in row:
            errors.append(f"Export row is missing provenance: {row_key(row)}")
            continue
        generated = row["provenance"].get("generated", {})
        if "classification" not in generated or "review" not in generated:
            errors.append(f"Export row provenance is missing generated snapshot: {row_key(row)}")

    if not tag_index.get("roles") or not tag_index.get("perk_types") or not tag_index.get("effect_tags"):
        errors.append(f"Tag index JSON export is missing expected sections: {tag_index_export_path}")

    for row in export_rows:
        key = row_key(row)
        effect = row["game"]["effect"].lower()
        classification = row["classification"]
        trigger_conditions = classification.get("trigger_conditions", [])
        perk_type = classification["perk_type"]

        if re.search(r"sent to confront|sent as attackers|sent to sally out", effect) and "simulation" not in trigger_conditions:
            errors.append(f"Missing simulation trigger: {key}")

        if "morale loss" in effect and "morale threshold" in trigger_conditions:
            errors.append(f"Morale-loss text should not create morale threshold: {key}")

        restricted_composition = re.compile(
            r"foot troops|infantry|archers|ranged troops|melee troops|mounted troops|cavalry|"
            r"bandit|mercenary|pack animals|prisoners|tier \d|garrisoned cavalry|"
            r"footmen on horses|composed of|less than \d+ soldiers|equipped with throwing"
        )
        generic_troop_scope = re.compile(
            r"troops? in your (party|formation)|troops? under your formation|units in your (party|formation)"
        )
        if (
            "party composition" in trigger_conditions
            and generic_troop_scope.search(effect)
            and not restricted_composition.search(effect)
        ):
            errors.append(f"Generic troop target scope marked as party composition: {key}")

        mechanic_as_type = {
            "ammo capacity",
            "damage increase",
            "damage resistance",
            "hit points",
            "morale damage",
            "ranged accuracy",
            "reload speed",
        }
        siege_mechanic = re.search(
            r"siege engine|siege engines|ballista|mangonel|trebuchet|ram|siege-tower|walls?|bombardment",
            effect,
        )
        if perk_type in mechanic_as_type and not siege_mechanic:
            errors.append(f"Combat mechanic left as top-level type outside siege context: {key}")

    actual_wrong = {row_key(row) for row in export_rows if row["review"].get("perk_wrong")}
    for key in sorted(EXPECTED_WRONG - actual_wrong):
        errors.append(f"Expected perk_wrong row is missing: {key}")
    for key in sorted(actual_wrong - EXPECTED_WRONG):
        errors.append(f"Unexpected perk_wrong row: {key}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(f"Perk effect validation failed with {len(errors)} issue(s).")

    print(
        "OK: checked "
        f"{len(markdown_rows)} perk effect files, "
        f"{len(generated_rows)} generated rows, "
        f"{len(overrides)} overrides."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate generated and post-processed perk effect data.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    args = parser.parse_args()
    validate(args.workspace.resolve())


if __name__ == "__main__":
    main()
