from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from .extract_commander_perks import build_commander_records, build_investment_bars
    from .perk_limits import check_perk_filters
except ImportError:
    from extract_commander_perks import build_commander_records, build_investment_bars
    from perk_limits import check_perk_filters


EXPECTED_WRONG = {
    "BowTrainer|primary",
    "TradeLocalConnection|primary",
    "RogueryArmsDealer|secondary",
    "ThrowingSplinters|primary",
    "BowRapidFire|secondary",
    "CrossbowCounterFire|secondary",
    "OneHandedWrappedHandles|secondary",
    "PolearmUnstoppableForce|primary",
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
        if path.name == "master-perk-effects.md":
            continue
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("|"):
                continue
            parts = [cell.strip() for cell in line.split("|")]
            if len(parts) < 14:
                continue
            if parts[1] == "Level" or parts[1].startswith("---"):
                continue
            
            # parts structure: ['', Level, Perk, Slot, Role, Effect, Type, Subtype, Triggers, Tags, Target Version, Curation/Status, ID, '']
            effect_slot = parts[3]
            role = parts[4]
            effect = parts[5]
            perk_type = parts[6]
            perk_subtype = parts[7]
            triggers_str = parts[8]
            tags_str = parts[9]
            curation = parts[11]
            perk_string_id = parts[12]
            
            key = f"{perk_string_id}|{effect_slot}"
            rows.append(
                {
                    "path": path,
                    "key": key,
                    "perk_string_id": perk_string_id,
                    "effect_slot": effect_slot,
                    "role": role,
                    "perk_type": perk_type,
                    "perk_subtype": perk_subtype,
                    "trigger_conditions": [t.strip() for t in triggers_str.split(",") if t.strip()] if triggers_str else [],
                    "effect_tags": [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else [],
                    "troop_usage": "",
                    "effect": effect,
                    "perk_wrong": "Wrong" in curation,
                }
            )
    return rows


def row_key(row: dict[str, Any]) -> str:
    return str(row["id"])


def override_key(override: dict[str, Any]) -> str:
    return f"{override.get('perk_string_id', '')}|{override.get('effect_slot', '')}"


def validate_commander_report_classification(
    export_rows: list[dict[str, Any]],
    banner_payload: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    records = build_commander_records(export_rows)
    by_key = {str(record["id"]): record for record in records}

    def require_record(key: str) -> dict[str, Any] | None:
        record = by_key.get(key)
        if record is None:
            errors.append(f"Commander report missing expected row: {key}")
        return record

    nocking_point = require_record("BowNockingPoint|primary")
    if nocking_point and nocking_point.get("speed_kind") != "weapon_handling_speed":
        errors.append("Commander report should classify BowNockingPoint|primary as weapon_handling_speed.")
    if nocking_point and nocking_point.get("doctrine_category") != "low_priority_misleading":
        errors.append("Commander report should keep BowNockingPoint|primary out of mobility/lethality buckets.")

    throwing_primary = require_record("ThrowingPerfectTechnique|primary")
    throwing_secondary = require_record("ThrowingPerfectTechnique|secondary")
    for record in [throwing_primary, throwing_secondary]:
        if record and record.get("speed_kind") != "projectile_speed":
            errors.append(f"Commander report should classify {record['id']} as projectile_speed.")
        if record and record.get("doctrine_category") == "engagement_control":
            errors.append(f"Commander report should not classify projectile speed as engagement control: {record['id']}")

    morning_exercise = require_record("AthleticsMorningExercise|secondary")
    if morning_exercise and morning_exercise.get("speed_kind") != "troop_combat_movement":
        errors.append("Commander report should classify AthleticsMorningExercise|secondary as troop_combat_movement.")
    if morning_exercise and morning_exercise.get("doctrine_category") != "core_troop_lethality":
        errors.append("Commander report should rank AthleticsMorningExercise|secondary as core troop lethality.")
    if morning_exercise and not morning_exercise.get("comparison_note"):
        errors.append("Commander report should explain the Athletics speed-vs-HP tradeoff.")

    well_built = require_record("AthleticsWellBuilt|secondary")
    if well_built and not well_built.get("comparison_note"):
        errors.append("Commander report should explain the Athletics HP-vs-speed tradeoff.")

    ignore_pain = require_record("AthleticsIgnorePain|secondary")
    if ignore_pain and ignore_pain.get("doctrine_category") != "combat_staying_power":
        errors.append("Commander report should classify troop-facing Ignore Pain armor as combat staying power.")
    if ignore_pain and ignore_pain.get("value_rating") != "high":
        errors.append("Commander report should rate troop-facing Ignore Pain armor as high value.")

    metallurgy = require_record("EngineeringMetallurgy|secondary")
    if metallurgy and metallurgy.get("doctrine_category") != "combat_staying_power":
        errors.append("Commander report should classify troop-facing Metallurgy armor as combat staying power.")

    shield_bearer = require_record("OneHandedShieldBearer|secondary")
    if shield_bearer and "all_troops" in shield_bearer.get("troop_classes", []):
        errors.append("Commander report should not mark infantry-only Shield Bearer as all_troops.")
    if shield_bearer and "infantry_or_foot" not in shield_bearer.get("troop_classes", []):
        errors.append("Commander report should mark Shield Bearer as infantry_or_foot.")

    loose_and_move = require_record("CrossbowLooseAndMove|secondary")
    if loose_and_move and "infantry_or_foot" in loose_and_move.get("troop_classes", []):
        errors.append("Commander report should not mark ranged-only Loose and Move as infantry_or_foot.")
    if loose_and_move and "all_troops" in loose_and_move.get("troop_classes", []):
        errors.append("Commander report should not mark ranged-only Loose and Move as all_troops.")
    if loose_and_move and "ranged" not in loose_and_move.get("troop_classes", []):
        errors.append("Commander report should mark Loose and Move as ranged-specific.")

    sweeping_wind = require_record("RidingSweepingWind|secondary")
    if sweeping_wind and sweeping_wind.get("speed_kind") != "campaign_party_speed":
        errors.append("Commander report should classify RidingSweepingWind|secondary as campaign_party_speed.")
    if sweeping_wind and sweeping_wind.get("doctrine_category") != "engagement_control":
        errors.append("Commander report should rank RidingSweepingWind|secondary as engagement control.")

    minister = require_record("MedicineMinisterOfHealth|primary")
    if minister and minister.get("doctrine_category") != "combat_staying_power":
        errors.append("Commander report should include troop-facing MedicineMinisterOfHealth as combat staying power.")
    if minister and "all_troops" not in minister.get("troop_classes", []):
        errors.append("Commander report should mark MedicineMinisterOfHealth as troop-facing despite its game role.")

    physician = require_record("MedicinePhysicianOfPeople|secondary")
    if physician and physician.get("doctrine_category") != "combat_staying_power":
        errors.append("Commander report should classify troop-facing Physician of People death avoidance as combat staying power.")

    bars = build_investment_bars(export_rows, records)
    details = {(row["skill"], int(row["level"])): row for row in bars.get("details", [])}
    one_handed_225 = details.get(("One Handed", 225), {})
    if one_handed_225:
        neutral = one_handed_225.get("cost", {}).get("weighted_allocation_cost")
        assisted = one_handed_225.get("assisted_cost", {}).get("weighted_allocation_cost")
        if neutral != 9 or assisted != 5:
            errors.append("Commander investment bars should price One Handed 225 as neutral 9 / assisted 5 weighted cost.")
    athletics_250 = details.get(("Athletics", 250), {})
    if athletics_250:
        neutral = athletics_250.get("cost", {}).get("weighted_allocation_cost")
        assisted = athletics_250.get("assisted_cost", {}).get("weighted_allocation_cost")
        if neutral != 17 or assisted != 9:
            errors.append("Commander investment bars should price Athletics 250 as neutral 17 / assisted 9 weighted cost.")

    return errors


def validate_banner_extraction(workspace: Path) -> list[str]:
    errors: list[str] = []
    banner_path = workspace / "Data" / "raw" / "banner-items.json"
    if not banner_path.exists():
        return errors

    payload = read_json(banner_path)
    effects = payload.get("effect_definitions", [])
    items = payload.get("items", [])
    groups = {str(group.get("effect", "")): group for group in payload.get("groups", [])}

    if len(effects) != 13:
        errors.append(f"Banner extraction expected 13 banner effects, found {len(effects)}.")
    if len(items) != 45:
        errors.append(f"Banner extraction expected 45 singleplayer banner items, found {len(items)}.")

    item_ids = [str(item.get("id", "")) for item in items]
    duplicates = sorted({item_id for item_id in item_ids if item_ids.count(item_id) > 1})
    for item_id in duplicates:
        errors.append(f"Banner extraction contains duplicate item id: {item_id}")

    expected_tier3 = {
        "IncreasedTroopMovementSpeed": 0.30000001192092896,
        "IncreasedMountMovementSpeed": 0.10000000149011612,
        "DecreasedRangedAttackDamage": -0.15000000596046448,
        "DecreasedRangedAccuracyPenalty": -0.07999999821186066,
        "IncreasedMeleeDamage": 0.15000000596046448,
    }
    for effect, expected in expected_tier3.items():
        group = groups.get(effect)
        if not group:
            errors.append(f"Banner extraction missing effect group: {effect}")
            continue
        tier3 = next((tier for tier in group.get("tiers", []) if int(tier.get("level", 0)) == 3), None)
        if tier3 is None:
            errors.append(f"Banner extraction missing tier 3 value for {effect}.")
            continue
        actual = float(tier3.get("bonus", 0))
        if abs(actual - expected) > 1e-6:
            errors.append(f"Banner extraction tier 3 value for {effect} is {actual}, expected {expected}.")

    ranged_group = groups.get("DecreasedRangedAttackDamage")
    if ranged_group and "Ranged" not in str(ranged_group.get("effect_name", "")):
        errors.append("Banner extraction should preserve the DecreasedRangedAttackDamage effect name.")

    return errors


def validate_banner_usage_scan(workspace: Path) -> list[str]:
    errors: list[str] = []
    usage_path = workspace / "Data" / "raw" / "banner-effect-usages.json"
    banner_path = workspace / "Data" / "raw" / "banner-items.json"
    if not usage_path.exists() or not banner_path.exists():
        return errors

    usage_payload = read_json(usage_path)
    banner_payload = read_json(banner_path)
    expected_effects = {str(effect.get("string_id", "")) for effect in banner_payload.get("effect_definitions", [])}
    seen_effects: set[str] = set()
    il_text_by_method = []
    for method in usage_payload.get("methods", []):
        il_text = "\n".join(str(line) for line in method.get("il", []))
        members_text = "\n".join(str(member) for member in method.get("referenced_members", []))
        il_text_by_method.append(f"{members_text}\n{il_text}")
        for member in method.get("referenced_members", []):
            member_text = str(member)
            if "DefaultBannerEffects.get_" not in member_text:
                continue
            effect = member_text.split("get_", 1)[1].split("(", 1)[0]
            if effect != "Instance":
                seen_effects.add(effect)

    for effect in sorted(expected_effects - seen_effects):
        errors.append(f"Banner usage scan missing formula reference for effect: {effect}")

    all_text = "\n".join(il_text_by_method)
    expected_snippets = {
        "IncreasedTroopMovementSpeed": "set_MaxSpeedMultiplier",
        "IncreasedMountMovementSpeed": "set_MountSpeed",
        "DecreasedRangedAccuracyPenalty": "set_WeaponInaccuracy",
        "DecreasedRangedAttackDamage": "DefaultBannerEffects.get_DecreasedRangedAttackDamage",
        "DecreasedShieldDamage": "DefaultBannerEffects.get_DecreasedShieldDamage",
    }
    for effect, snippet in expected_snippets.items():
        if effect not in seen_effects:
            continue
        if snippet not in all_text:
            errors.append(f"Banner usage scan should show {effect} reaching {snippet}.")

    return errors


def validate(workspace: Path) -> None:
    markdown_root = workspace / "Docs" / "reference"
    override_path = workspace / "Data" / "curated" / "perk-effect-overrides.json"
    raw_perks_path = workspace / "Data" / "raw" / "perks.json"
    generated_path = workspace / "Data" / "intermediate" / "classified-perk-effects.json"
    postprocessed_path = workspace / "Data" / "intermediate" / "postprocessed-perk-effects.json"
    export_path = workspace / "Data" / "export" / "perk-effects.json"
    tag_index_export_path = workspace / "Data" / "export" / "tag-index.json"

    errors: list[str] = []
    
    # Run the perk filter classification consistency validation
    errors.extend(check_perk_filters(workspace))

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

    banner_path = workspace / "Data" / "raw" / "banner-items.json"
    banner_payload = read_json(banner_path) if banner_path.exists() else None
    errors.extend(validate_commander_report_classification(export_rows, banner_payload))
    errors.extend(validate_banner_extraction(workspace))
    errors.extend(validate_banner_usage_scan(workspace))

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
