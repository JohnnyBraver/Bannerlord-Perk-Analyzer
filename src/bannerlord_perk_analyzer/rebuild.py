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
    from .classifier import classify_effect, get_readable_facets, matches, normalize_classification
    from .postprocess import postprocess
except ImportError:
    from classifier import classify_effect, get_readable_facets, matches, normalize_classification
    from postprocess import postprocess


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


def strip_loc_prefix(text: Any) -> str:
    if text is None:
        return ""
    return re.sub(r"^\{=[^}]+\}", "", str(text)).strip()


def format_number(value: float) -> str:
    if abs(value - round(value)) < 0.0001:
        return str(int(round(value)))
    return f"{value:.6f}".rstrip("0").rstrip(".")


def render_effect(template: str, bonus: float) -> str:
    text = strip_loc_prefix(template)
    value = format_number(float(bonus) * 100.0 if "{VALUE}%" in text else float(bonus))
    return text.replace("{VALUE}", value)


def effect_slot(perk: dict[str, Any], slot: str) -> dict[str, Any]:
    return perk[f"{slot}_effect"]


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


def build_effect_row(perk: dict[str, Any], slot: str) -> dict[str, Any] | None:
    raw_effect = effect_slot(perk, slot)
    template = strip_loc_prefix(raw_effect.get("template", raw_effect.get("template_raw", "")))
    if not template.strip():
        return None

    effect = render_effect(template, float(raw_effect["bonus"]))
    role = str(raw_effect["role"])
    base = classify_effect(effect, str(perk["skill"]), role)
    classification_review = base["review"]
    normalized = normalize_classification(base["type"], base["subtype"], str(perk["skill"]))
    facets = get_readable_facets(normalized["type"], normalized["subtype"], effect, role)

    notes = ""
    if matches(effect.lower(), r"part of an army"):
        notes = "Applies only while the party is part of an army; no dedicated army-membership trigger condition exists."
    elif matches(effect.lower(), r"village raids"):
        notes = "Applies when taking food during village raids; no dedicated raid trigger condition exists."

    if matches(effect.lower(), r"control skills of infantry.*vigor skills of archers"):
        classification_review = "Troop skill bonus spans infantry Control and archer Vigor; not hero character growth."
    elif matches(effect.lower(), r"wages.*upgrade costs.*mercenary troops"):
        classification_review = "Composite effect spans wages and upgrade costs for mercenary troops; single classification is partial."
    elif matches(effect.lower(), r"companion wages.*recruitment fees"):
        classification_review = "Composite effect spans companion wages and recruitment fees; single classification is partial."

    return {
        "id": f"{perk['string_id']}|{slot}",
        "project": "Bannerlord",
        "type": "bannerlord_perk_effect",
        "game_version_target": "1.4.5",
        "attribute": perk["attribute"],
        "skill": perk["skill"],
        "level": perk["level"],
        "perk": perk["name"],
        "perk_string_id": perk["string_id"],
        "effect_slot": slot,
        "alternative_perk_string_id": perk.get("alternative_string_id", ""),
        "game": {
            "role": role,
            "role_value": raw_effect["role_value"],
            "bonus": raw_effect["bonus"],
            "increment_type": raw_effect["increment_type"],
            "increment_value": raw_effect["increment_value"],
            "troop_usage": raw_effect["troop_usage"],
            "troop_usage_value": raw_effect["troop_usage_value"],
            "effect": effect,
            "effect_template": template,
        },
        "classification": {
            "perk_type": facets["type"],
            "perk_subtype": facets["subtype"],
            "trigger_conditions": facets["trigger_condition"],
            "effect_tags": facets["effect_tags"],
        },
        "review": {
            "needs_review": False,
            "functioning": None,
            "perk_wrong": False,
            "bug_note": "",
            "notes": notes,
            "classification_review": classification_review,
        },
        "source": {
            "status": "local_game_assembly",
            "name": "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll",
            "version": "1.4.5",
        },
    }


def classify_perks(raw_perks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for perk in raw_perks:
        for slot in ("primary", "secondary"):
            row = build_effect_row(perk, slot)
            if row is not None:
                rows.append(row)
    return sort_rows(rows)


def run_extractor(workspace: Path, game_root: Path, raw_output: Path) -> None:
    project = workspace / "tools" / "BannerlordExtractor" / "BannerlordExtractor.csproj"
    if not project.exists():
        raise SystemExit(f"Extractor project is missing: {project}")
    command = [
        "dotnet",
        "run",
        "--project",
        str(project),
        "--",
        "perks",
        "--game-root",
        str(game_root),
        "--output",
        str(raw_output),
    ]
    subprocess.run(command, check=True)


def rebuild(workspace: Path, game_root: Path | None, skip_extract: bool = False) -> None:
    raw_path = workspace / "Data" / "raw" / "perks.json"
    generated_path = workspace / "Data" / "generated" / "classified-perk-effects.json"

    if not skip_extract:
        env_game_root = os.environ.get("BANNERLORD_GAME_ROOT")
        if game_root is None and not env_game_root:
            raise SystemExit("Bannerlord game root is required. Pass --game-root, set BANNERLORD_GAME_ROOT, or use --skip-extract.")
        resolved_game_root = game_root or Path(str(env_game_root))
        run_extractor(workspace, resolved_game_root.resolve(), raw_path)

    raw_perks = read_json(raw_path)
    rows = classify_perks(raw_perks)
    write_json(generated_path, rows)
    postprocess(workspace)

    review_rows = [row for row in rows if row["review"].get("classification_review")]
    role_summary = Counter(row["game"]["role"] for row in rows)
    type_summary = Counter(row["classification"]["perk_type"] for row in rows)
    print(f"Perks read: {len(raw_perks)}")
    print(f"Generated effect rows: {len(rows)}")
    print(f"Generated review flags: {len(review_rows)}")
    print("Generated roles:")
    for role in sorted(role_summary):
        print(f"  {role}: {role_summary[role]}")
    print("Generated types:")
    for type_name in sorted(type_summary):
        print(f"  {type_name}: {type_summary[type_name]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract, classify, and post-process Bannerlord perk effects.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--game-root", type=Path, default=None)
    parser.add_argument("--skip-extract", action="store_true", help="Use the existing Data/raw/perks.json instead of reading game assemblies.")
    args = parser.parse_args()
    rebuild(args.workspace.resolve(), args.game_root, skip_extract=args.skip_extract)


if __name__ == "__main__":
    main()
