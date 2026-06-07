from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .postprocess import default_workspace
    from .utils import resolve_game_root, run_extractor
    from .xp_reports import display_path, table_escape
except ImportError:
    from postprocess import default_workspace
    from utils import resolve_game_root, run_extractor
    from xp_reports import display_path, table_escape

STAT_LABELS = {
    "damage": "Damage",
    "speed": "Speed",
    "missile_speed": "Missile Speed",
    "armor": "Armor",
    "charge_damage": "Charge Damage",
    "maneuver": "Maneuver",
    "hit_points": "Hit Points",
    "weight": "Weight",
    "handling": "Handling",
    "stack_size": "Stack Size"
}

GROUP_LABELS = {
    "sword": "Swords",
    "bow": "Bows",
    "crossbow": "Crossbows",
    "arrow": "Arrows",
    "bolt": "Bolts",
    "cheap_weapon": "Cheap Weapons",
    "polearm": "Polearms",
    "mace": "Maces",
    "axe": "Axes",
    "axe_throwing": "Throwing Axes",
    "knife_throwing": "Throwing Knives",
    "spear_dart_throwing": "Throwing Spears / Darts",
    "shield": "Shields",
    "plate": "Plate Armor",
    "chain": "Chain Armor",
    "leather": "Leather Armor",
    "cloth": "Cloth Armor",
    "cloth_unarmoured": "Unarmored Cloth",
    "horse": "Horses / Mounts",
    "companion": "Companions"
}

def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def format_stat(key: str, val_str: str) -> str:
    label = STAT_LABELS.get(key, key.replace("_", " ").title())
    try:
        val = float(val_str)
        if val.is_integer():
            val_formatted = f"{int(val)}"
        else:
            val_formatted = f"{val:.2f}".rstrip("0").rstrip(".")
        
        if val > 0:
            return f"+{val_formatted} {label}"
        else:
            return f"{val_formatted} {label}"
    except ValueError:
        return f"{val_str} {label}"

def format_stats(stats: dict[str, str]) -> str:
    if not stats:
        return "None"
    formatted = []
    for key in sorted(stats.keys()):
        formatted.append(format_stat(key, stats[key]))
    return ", ".join(formatted)

def write_markdown(payload: dict[str, Any], path: Path, workspace: Path, json_output: Path) -> None:
    modifiers = payload.get("modifiers", [])
    groups = payload.get("groups", [])
    
    modifiers_by_id = {m["Id"]: m for m in modifiers}
    
    lines = [
        "# Item Quality Modifiers",
        "",
        f"Generated: {payload.get('generated_at', '')}",
        "",
        "This report documents Bannerlord's item quality modifiers (prefixes for weapons, armor, shields, and mounts) parsed from the native game XML files.",
        "",
        "## Inputs",
        "",
        f"- JSON: `{display_path(json_output, workspace)}`",
    ]
    
    inputs_dict = payload.get("inputs", {})
    if "item_modifiers_xml" in inputs_dict:
        lines.append(f"- Modifiers XML: `{inputs_dict['item_modifiers_xml']}`")
    if "item_modifiers_groups_xml" in inputs_dict:
        lines.append(f"- Groups XML: `{inputs_dict['item_modifiers_groups_xml']}`")
        
    lines.extend([
        "",
        "## Modifier Spawning Mechanics",
        "",
        "When an item is spawned as battle loot or in a town's production inventory, it has a chance to receive a quality modifier based on its assigned `ItemModifierGroup`.",
        "Each group has a weight for spawning with no modifier, and each possible modifier in the group has its own weight (drop score).",
        "",
        "The probabilities are calculated as:",
        "- **Loot Spawn Chance**: `loot_drop_score / (no_modifier_loot_score + sum(all_modifier_loot_drop_scores))`",
        "- **Production Spawn Chance**: `production_drop_score / (no_modifier_production_score + sum(all_modifier_production_drop_scores))`",
        "",
        "---",
        ""
    ])
    
    sorted_groups = sorted(groups, key=lambda g: GROUP_LABELS.get(g["Id"], g["Id"]))
    
    for group in sorted_groups:
        group_id = group["Id"]
        pretty_group_name = GROUP_LABELS.get(group_id, group_id.replace("_", " ").title())
        
        no_mod_loot = group["NoModifierLootScore"]
        no_mod_prod = group["NoModifierProductionScore"]
        
        group_modifiers = []
        for mod_ref in group.get("Modifiers", []):
            mod_id = mod_ref["Id"]
            mod_data = modifiers_by_id.get(mod_id)
            if mod_data:
                group_modifiers.append(mod_data)
                
        total_loot = no_mod_loot + sum(m["LootDropScore"] for m in group_modifiers)
        total_prod = no_mod_prod + sum(m["ProductionDropScore"] for m in group_modifiers)
        
        rows = []
        
        normal_row = {
            "name": "[Normal / No Modifier]",
            "price_factor": 1.0,
            "stats": "None",
            "quality": "normal",
            "loot_chance_pct": (no_mod_loot / total_loot * 100.0) if total_loot > 0 else 0.0,
            "loot_chance_str": f"{no_mod_loot} / {total_loot} ({(no_mod_loot / total_loot * 100.0):.2f}%)" if total_loot > 0 else "0%",
            "prod_chance_pct": (no_mod_prod / total_prod * 100.0) if total_prod > 0 else 0.0,
            "prod_chance_str": f"{no_mod_prod} / {total_prod} ({(no_mod_prod / total_prod * 100.0):.2f}%)" if total_prod > 0 else "0%"
        }
        rows.append(normal_row)
        
        for m in group_modifiers:
            loot_score = m["LootDropScore"]
            prod_score = m["ProductionDropScore"]
            loot_chance_pct = (loot_score / total_loot * 100.0) if total_loot > 0 else 0.0
            prod_chance_pct = (prod_score / total_prod * 100.0) if total_prod > 0 else 0.0
            
            display_name = m["Name"].replace("{ITEMNAME}", "[Item]").strip()
            
            rows.append({
                "name": display_name,
                "price_factor": m["PriceFactor"],
                "stats": format_stats(m["Stats"]),
                "quality": m["Quality"],
                "loot_chance_pct": loot_chance_pct,
                "loot_chance_str": f"{loot_score} / {total_loot} ({loot_chance_pct:.2f}%)" if total_loot > 0 else "0%",
                "prod_chance_pct": prod_chance_pct,
                "prod_chance_str": f"{prod_score} / {total_prod} ({prod_chance_pct:.2f}%)" if total_prod > 0 else "0%"
            })
            
        rows.sort(key=lambda r: (-r["price_factor"], r["name"]))
        
        lines.extend([
            f"### Modifier Group: {pretty_group_name} (`{group_id}`)",
            "",
            "| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |",
            "| :--- | :---: | :--- | :---: | :---: | :---: |"
        ])
        
        for row in rows:
            lines.append(
                "| {name} | {pf:.2f}x | {stats} | {quality} | {loot} | {prod} |".format(
                    name=table_escape(row["name"]),
                    pf=row["price_factor"],
                    stats=table_escape(row["stats"]),
                    quality=table_escape(row["quality"]),
                    loot=table_escape(row["loot_chance_str"]),
                    prod=table_escape(row["prod_chance_str"])
                )
            )
        lines.append("")
        
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

def extract_modifiers(
    workspace: Path,
    game_root: Path | None,
    json_output: Path,
    markdown_output: Path,
    skip_scan: bool = False,
) -> None:
    if not skip_scan:
        resolved_game_root = resolve_game_root(game_root)
        args = [
            "modifiers",
            "--game-root",
            str(resolved_game_root),
            "--output",
            str(json_output),
        ]
        run_extractor(workspace, args)
        
    payload = read_json(json_output)
    write_markdown(payload, markdown_output, workspace, json_output)
    print(f"Item modifiers JSON written: {json_output}")
    print(f"Item modifiers report written: {markdown_output}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Bannerlord item quality modifiers and write a report.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--game-root", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    parser.add_argument("--skip-scan", action="store_true", help="Reuse existing JSON and regenerate only the report.")
    args = parser.parse_args()
    
    workspace = args.workspace.resolve()
    json_output = args.json_output or workspace / "Data" / "raw" / "item-modifiers.json"
    markdown_output = args.markdown_output or workspace / "Docs" / "reports" / "item-modifiers.md"
    extract_modifiers(
        workspace=workspace,
        game_root=args.game_root,
        json_output=json_output,
        markdown_output=markdown_output,
        skip_scan=args.skip_scan,
    )

if __name__ == "__main__":
    main()
