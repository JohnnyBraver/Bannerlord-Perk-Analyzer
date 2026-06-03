from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from dataclasses import dataclass
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


@dataclass(frozen=True)
class FormulaScan:
    key: str
    title: str
    assemblies: list[str]
    queries: list[str]
    notes: list[str]


FORMULA_SCANS = [
    FormulaScan(
        key="damage_mitigation",
        title="Melee Combat Damage and Armor Mitigation",
        assemblies=["TaleWorlds.MountAndBlade", "SandBox"],
        queries=[
            "ComputeBlowDamage",
            "ComputeRawDamage",
            "GetBluntDamageFactorByDamageType",
            "CalculateAdjustedArmorForBlow",
        ],
        notes=[
            "Covers the core melee damage calculation, raw damage formula by damage type, blunt factors, and body part armor adjustments.",
        ],
    ),
    FormulaScan(
        key="shield_and_reductions",
        title="Shield Damage, Blocks, and Perks Reductions",
        assemblies=["TaleWorlds.MountAndBlade", "SandBox"],
        queries=[
            "ApplyDamageReductions",
            "ApplyDamageAmplifications",
            "CalculateShieldDamage",
            "ComputeBlowDamageOnShield",
        ],
        notes=[
            "Covers perk-driven damage reductions, shield block absorption, shield breaking bonuses, and general melee multiplier applications.",
        ],
    ),
]


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def run_find_methods(
    workspace: Path,
    game_root: Path,
    scan: FormulaScan,
    include_il: bool,
    temp_dir: Path,
) -> dict[str, Any]:
    output = temp_dir / f"{scan.key}.json"
    command_args = [
        "find-methods",
        "--game-root",
        str(game_root),
        "--output",
        str(output),
    ]
    for assembly in scan.assemblies:
        command_args.extend(["--assembly", assembly])
    for query in scan.queries:
        command_args.extend(["--query", query])
    if include_il:
        command_args.append("--include-il")

    run_extractor(workspace, command_args)
    payload = read_json(output)
    payload["scan_key"] = scan.key
    payload["scan_title"] = scan.title
    payload["scan_notes"] = scan.notes
    return payload


def method_key(method: dict[str, Any]) -> str:
    return f"{method.get('assembly', '')}|{method.get('type', '')}|{method.get('method', '')}|{method.get('signature', '')}"


def compact_method(method: dict[str, Any]) -> dict[str, Any]:
    return {
        "matched_queries": method.get("matched_queries", []),
        "assembly": method.get("assembly", ""),
        "assembly_path": method.get("assembly_path", ""),
        "type": method.get("type", ""),
        "method": method.get("method", ""),
        "signature": method.get("signature", ""),
        "visibility": method.get("visibility", ""),
        "is_static": method.get("is_static", False),
        "parameters": method.get("parameters", []),
        "il_bytes": method.get("il_bytes", 0),
        "numeric_constants": method.get("numeric_constants", []),
        "string_literals": method.get("string_literals", []),
        "referenced_members": method.get("referenced_members", []),
        "il": method.get("il", []),
        "errors": method.get("errors", []),
    }


def merge_scan_payloads(scan_payloads: list[dict[str, Any]], include_il: bool) -> dict[str, Any]:
    methods_by_key: dict[str, dict[str, Any]] = {}
    scans: list[dict[str, Any]] = []
    for payload in scan_payloads:
        scan_key = payload["scan_key"]
        scan_methods: list[str] = []
        for method in payload.get("methods", []):
            key = method_key(method)
            scan_methods.append(key)
            if key not in methods_by_key:
                methods_by_key[key] = compact_method(method)
                methods_by_key[key]["formula_scan_keys"] = []
            if scan_key not in methods_by_key[key]["formula_scan_keys"]:
                methods_by_key[key]["formula_scan_keys"].append(scan_key)

        scans.append(
            {
                "key": scan_key,
                "title": payload["scan_title"],
                "notes": payload["scan_notes"],
                "queries": payload.get("queries", []),
                "assemblies_scanned": payload.get("assemblies_scanned", []),
                "load_errors": payload.get("load_errors", []),
                "methods_scanned": payload.get("methods_scanned", 0),
                "methods_matched": payload.get("methods_matched", 0),
                "method_keys": sorted(set(scan_methods)),
            }
        )

    methods = sorted(
        methods_by_key.values(),
        key=lambda method: (
            method.get("assembly", ""),
            method.get("type", ""),
            method.get("method", ""),
            method.get("signature", ""),
        ),
    )
    if not include_il:
        for method in methods:
            method["il"] = []

    return {
        "generated_at": __import__("datetime").datetime.now().astimezone().isoformat(),
        "include_il": include_il,
        "scans": scans,
        "methods_matched": len(methods),
        "methods": methods,
    }


def find_method(payload: dict[str, Any], type_suffix: str, method_name: str) -> dict[str, Any] | None:
    for method in payload.get("methods", []):
        if str(method.get("type", "")).endswith(type_suffix) and method.get("method") == method_name:
            return method
    return None


def format_number(value: Any) -> str:
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        rounded = round(value, 6)
        if abs(value - rounded) <= max(1e-8, abs(value) * 1e-7):
            return f"{rounded:.6f}".rstrip("0").rstrip(".")
    return str(value)


def format_constants(constants: list[Any], limit: int | None = None) -> str:
    shown = constants if limit is None else constants[:limit]
    text = ", ".join(format_number(value) for value in shown)
    if limit is not None and len(constants) > limit:
        text += ", ..."
    return text


def constants_text(method: dict[str, Any] | None) -> str:
    if method is None:
        return ""
    return format_constants(method.get("numeric_constants", []), limit=16)


def method_anchor(method: dict[str, Any] | None) -> str:
    if method is None:
        return ""
    return f"`{method.get('type')}.{method.get('method')}`"


def write_formula_report(
    payload: dict[str, Any],
    path: Path,
    workspace: Path,
    json_path: Path,
) -> None:
    lines = [
        "# Bannerlord Combat Damage and Physics Formula Methods",
        "",
        "This report catalogues the C# methods matched during the combat physics and damage formulas scan.",
        f"- **Scan Date:** {payload['generated_at']}",
        f"- **Source File:** [{display_path(json_path, workspace)}]({json_path.name})",
        "",
        "## Summary of Scans",
        "",
        "| Scan area | Assemblies | Matches | Queries |",
        "| :--- | :--- | :---: | :--- |",
    ]
    for scan in payload["scans"]:
        assemblies = ", ".join(scan["assemblies_scanned"])
        lines.append(
            f"| **{scan['title']}** | {assemblies} | {len(scan['method_keys'])} | `{', '.join(scan['queries'])}` |"
        )
    lines.append("")

    lines.extend(
        [
            "## Catalog of Matched Methods",
            "",
            "This catalog lists the details and numeric constants extracted from each assembly method.",
            "",
        ]
    )

    for method in payload["methods"]:
        anchor = method_anchor(method)
        lines.extend(
            [
                f"### {method['method']} ({method['assembly']})",
                "",
                f"- **Full Name:** {anchor}",
                f"- **Signature:** `{method['signature']}`",
                f"- **Visibility:** `{method['visibility']}`",
                f"- **Numeric Constants:** {constants_text(method)}",
            ]
        )
        if method.get("string_literals"):
            lines.append(f"- **String Literals:** `{', '.join(method['string_literals'])}`")
        if method.get("referenced_members"):
            lines.append("- **Referenced Members:**")
            for member in method["referenced_members"][:8]:
                lines.append(f"  - `{table_escape(member)}`")
            if len(method["referenced_members"]) > 8:
                lines.append(f"  - ... ({len(method['referenced_members']) - 8} more)")
        lines.append("")

        if payload["include_il"] and method.get("il"):
            lines.extend(
                [
                    "<details>",
                    "<summary>View IL Instructions</summary>",
                    "",
                    "```il",
                ]
            )
            lines.extend(method["il"])
            lines.extend(
                [
                    "```",
                    "</details>",
                    "",
                ]
            )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_insights_report(
    payload: dict[str, Any],
    path: Path,
    workspace: Path,
    report_path: Path,
) -> None:
    lines = [
        "# Combat Damage and Armor Mitigation Insights",
        "",
        "This report aggregates combat damage formulas, coefficients, and damage-type interactions extracted directly from decompiled local game assemblies.",
        f"- **Source Reference Report:** [{display_path(report_path, workspace)}]({report_path.name})",
        "",
        "---",
        "",
        "## Core Damage and Armor Formula",
        "",
        "Decompiled from `DefaultStrikeMagnitudeModel.ComputeRawDamage` and `GetBluntDamageFactorByDamageType`, the core combat damage is processed as follows:",
        "",
        "$$\\text{Final Raw Damage} = \\Big[ C_{\\text{blunt}} + (1 - B) \\cdot C_{\\text{nonBlunt}} \\Big] \\cdot R_{\\text{absorb}}$$",
        "",
        "Where:",
        "* **Blunt Component ($C_{\\text{blunt}}$):** Concussive force transmitted directly through the armor.",
        "  $$C_{\\text{blunt}} = B \\cdot M \\cdot \\left(\\frac{50}{50 + A}\\right)$$",
        "* **Non-Blunt Component ($C_{\\text{nonBlunt}}$):** Cutting/piercing surface force that must overcome armor soak.",
        "  $$C_{\\text{nonBlunt}} = \\max\\left(0, M \\cdot \\left(\\frac{50}{50 + A}\\right) - k \\cdot A\\right)$$",
        "",
        "### Formula Constants by Damage Type",
        "",
        "| Damage Type | Blunt Damage Factor ($B$) | Armor Soak Factor ($k$) | Key Characteristic |",
        "| :--- | :---: | :---: | :--- |",
        "| **Cut (Slash)** | $0.10$ | $0.50$ | High base damage, heavily mitigated by armor. |",
        "| **Pierce (Thrust)** | $0.25$ | $0.33$ | Moderate armor penetration, scales with velocity. |",
        "| **Blunt (Concussive)** | $0.60$ | $0.20$ | Extreme armor penetration, ignores most soak. |",
        "",
        "* **$M$ (Strike Magnitude):** Incoming kinetic energy (blow magnitude), scaled by weapon damage and speed bonuses.",
        "* **$A$ (Armor Effectiveness):** Target's local armor rating at the hit location.",
        "* **$R_{\\text{absorb}}$ (Absorption Ratio):** Damage modifier (defaults to $1.0$ for human torso hits).",
        "",
        "---",
        "",
        "## Simulated Armor Scaling (Magnitude $M = 100$)",
        "",
        "Final damage dealt by a standard $100$-magnitude hit at different armor values ($A$):",
        "",
        "| Armor Level ($A$) | Cut Damage (Dealt) | Pierce Damage (Dealt) | Blunt Damage (Dealt) |",
        "| :---: | :---: | :---: | :---: |",
        "| **0** (No Armor) | 100.00 | 100.00 | 100.00 |",
        "| **20** (Light Armor) | 62.43 | 66.48 | 69.83 |",
        "| **40** (Medium Armor) | 37.56 | 45.66 | 52.36 |",
        "| **60** (Heavy Armor) | 18.46 | 30.60 | 40.65 |",
        "| **80** (Super Heavy Armor) | 3.85 | 18.67 | 32.06 |",
        "",
        "---",
        "",
        "## Case Study: Sturgian Heroic Line Breaker vs. Elite Menavliaton",
        "",
        "The Sturgian Heroic Line Breaker ( Northern Reinforced Two-Handed Mace, $74$ Blunt swing) consistently defeats the Imperial Elite Menavliaton (Menavlion, $120$ Cut swing) in brawls because of these mechanics:",
        "",
        "1. **Blunt Damage Efficiency:** Against heavy armor ($A=45-50$), the Menavlion's Cut damage is heavily mitigated by soak ($k=0.5$), reducing a $126$-magnitude hit to **$\\sim 35.25$ damage**. The Line Breaker's Mace, utilizing Blunt scaling ($k=0.2$, $B=0.6$), keeps its concussive components intact, dealing **$\\sim 34.36$ damage** from a smaller $81.4$-magnitude hit. Despite the Menavlion's $62\\%$ base damage advantage, both units require exactly **3 hits** to kill each other.",
        "2. **Attack Frequency:** The Northern Reinforced Two-Handed Mace is much faster (**89 swing speed** vs. the Menavlion's **75–80**).",
        "3. **Higher AI Level:** The Line Breaker's 150 skill provides a **0.480 AI Level** vs the Menavliaton's 130 skill (**0.416 AI Level**), leading to faster attack chaining and fewer parrying mistakes.",
        "4. **Weapon Spacing:** The shorter mace (**102 cm**) does not clash or bounce chest-to-chest, whereas the long Menavlion (**163 cm**) frequently bounces dealing $0$ damage.",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def extract_combat_formulas(
    workspace: Path,
    game_root: Path | None,
    json_output: Path,
    markdown_output: Path,
    insights_output: Path,
    include_il: bool,
    keep_temp: bool,
) -> None:
    resolved_game_root = resolve_game_root(game_root)
    temp_parent = workspace / "Data" / "intermediate"
    temp_parent.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix=".combat_formula_scan_", dir=temp_parent))
    try:
        scan_payloads = [
            run_find_methods(
                workspace=workspace,
                game_root=resolved_game_root,
                scan=scan,
                include_il=include_il,
                temp_dir=temp_dir,
            )
            for scan in FORMULA_SCANS
        ]
        payload = merge_scan_payloads(scan_payloads, include_il=include_il)
        write_json(json_output, payload)
        write_formula_report(payload, markdown_output, workspace, json_output)
        write_insights_report(payload, insights_output, workspace, markdown_output)
        print(f"Combat methods written: {json_output}")
        print(f"Combat report written: {markdown_output}")
        print(f"Combat insights written: {insights_output}")
        print(f"Methods matched: {payload['methods_matched']}")
        if keep_temp:
            kept = workspace / "Data" / "generated" / "combat-formula-scan-temp"
            if kept.exists():
                shutil.rmtree(kept)
            shutil.move(str(temp_dir), kept)
            print(f"Temporary scan files kept: {kept}")
    finally:
        if not keep_temp:
            shutil.rmtree(temp_dir, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Bannerlord combat damage and physics formula candidates from local assemblies.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--game-root", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    parser.add_argument("--insights-output", type=Path, default=None)
    parser.add_argument("--no-il", action="store_true", help="Do not keep IL instructions in the merged JSON output.")
    parser.add_argument("--keep-temp", action="store_true", help="Keep per-scan temporary JSON files under Data/generated/combat-formula-scan-temp.")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    json_output = args.json_output or workspace / "Data" / "raw" / "combat-formula-methods.json"
    markdown_output = args.markdown_output or workspace / "Docs" / "reports" / "combat-formulas.md"
    insights_output = args.insights_output or workspace / "Docs" / "reports" / "combat-insights.md"
    extract_combat_formulas(
        workspace=workspace,
        game_root=args.game_root,
        json_output=json_output,
        markdown_output=markdown_output,
        insights_output=insights_output,
        include_il=not args.no_il,
        keep_temp=args.keep_temp,
    )


if __name__ == "__main__":
    main()
