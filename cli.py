#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add src/ and src/bannerlord_perk_analyzer directories to the path so we can import package and modules
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent / "src" / "bannerlord_perk_analyzer"))

try:
    from bannerlord_perk_analyzer.analyze_battanian_starts import analyze_battanian_starts, analyze_culture_start_leaks
    from bannerlord_perk_analyzer.extract_banners import extract_banners
    from bannerlord_perk_analyzer.extract_character_creation import extract_character_creation
    from bannerlord_perk_analyzer.extract_combat_formulas import extract_combat_formulas
    from bannerlord_perk_analyzer.extract_commander_perks import extract_commander_perks
    from bannerlord_perk_analyzer.extract_guide_stats import extract_guide_stats
    from bannerlord_perk_analyzer.extract_skill_xp_sources import extract_skill_xp_sources
    from bannerlord_perk_analyzer.extract_xp_awards import extract_xp_awards
    from bannerlord_perk_analyzer.extract_xp_formulas import extract_xp_formulas
    from bannerlord_perk_analyzer.prune_overrides import prune_overrides
    from bannerlord_perk_analyzer.rebuild import rebuild
    from bannerlord_perk_analyzer.validate import validate
except ImportError as e:
    print(f"Error importing modules: {e}", file=sys.stderr)
    print("Ensure you are running this from the repository root directory.", file=sys.stderr)
    sys.exit(1)


def default_workspace() -> Path:
    return Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Unified CLI for Bannerlord Perk Analyzer tools.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommand to execute")

    # Rebuild subcommand
    parser_rebuild = subparsers.add_parser(
        "rebuild",
        help="Run the standard rebuild pipeline (extraction, classification, postprocess, and override pruning)."
    )
    parser_rebuild.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="Path to workspace directory"
    )
    parser_rebuild.add_argument(
        "--game-root",
        type=Path,
        default=None,
        help="Bannerlord game root directory. Overrides BANNERLORD_GAME_ROOT env var."
    )
    parser_rebuild.add_argument(
        "--skip-extract",
        action="store_true",
        help="Use existing Data/raw/perks.json instead of extracting fresh from game assemblies."
    )

    # Validate subcommand
    parser_validate = subparsers.add_parser(
        "validate",
        help="Run the perk effect validation suite."
    )
    parser_validate.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="Path to workspace directory"
    )

    # Prune subcommand
    parser_prune = subparsers.add_parser(
        "prune",
        help="Manually prune redundant curated overrides already handled by the classifier."
    )
    parser_prune.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="Path to workspace directory"
    )
    parser_prune.add_argument(
        "--dry-run",
        action="store_true",
        help="Output what would be pruned without modifying the overrides file."
    )

    # Extract-xp subcommand
    parser_xp = subparsers.add_parser(
        "extract-xp",
        help="Run the XP award, formula, and skill XP source extractions."
    )
    parser_xp.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="Path to workspace directory"
    )
    parser_xp.add_argument(
        "--game-root",
        type=Path,
        default=None,
        help="Bannerlord game root directory. Overrides BANNERLORD_GAME_ROOT env var."
    )
    parser_xp.add_argument(
        "--assembly",
        action="append",
        default=[],
        help="Assembly name without .dll to scan in XP awards. Repeat to scan multiple assemblies."
    )
    parser_xp.add_argument(
        "--deep-scan-callers",
        action="store_true",
        help="Perform a deep scan of callers in XP awards."
    )
    parser_xp.add_argument(
        "--include-contracts",
        action="store_true",
        help="Include contract classes in XP awards."
    )
    parser_xp.add_argument(
        "--include-il",
        action="store_true",
        help="Include IL instructions in XP awards."
    )
    parser_xp.add_argument(
        "--no-il",
        action="store_true",
        help="Do not keep IL instructions in the formula scan output."
    )
    parser_xp.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep per-scan temporary JSON files under Data/intermediate/xp-formula-scan-temp."
    )
    parser_xp.add_argument(
        "--skip-scan",
        action="store_true",
        help="Skip fresh C# scanning for skill XP sources and reuse existing JSON output to regenerate reports."
    )

    # Extract-creation subcommand
    parser_creation = subparsers.add_parser(
        "extract-creation",
        help="Run the character creation background options extraction."
    )
    parser_creation.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="Path to workspace directory"
    )
    parser_creation.add_argument(
        "--game-root",
        type=Path,
        default=None,
        help="Bannerlord game root directory. Overrides BANNERLORD_GAME_ROOT env var."
    )
    parser_creation.add_argument(
        "--skip-scan",
        action="store_true",
        help="Skip fresh C# scanning and reuse the existing character creation JSON output to regenerate the report."
    )
    # Extract-combat subcommand
    parser_combat = subparsers.add_parser(
        "extract-combat",
        help="Run the combat damage, armor mitigation, and shield formulas extractions."
    )
    parser_combat.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="Path to workspace directory"
    )
    parser_combat.add_argument(
        "--game-root",
        type=Path,
        default=None,
        help="Bannerlord game root directory. Overrides BANNERLORD_GAME_ROOT env var."
    )
    parser_combat.add_argument(
        "--no-il",
        action="store_true",
        help="Do not keep IL instructions in the formula scan output."
    )
    parser_combat.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep per-scan temporary JSON files under Data/intermediate/combat-formula-scan-temp."
    )

    # Extract-banners subcommand
    parser_banners = subparsers.add_parser(
        "extract-banners",
        help="Run the banner item/effect extraction."
    )
    parser_banners.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="Path to workspace directory"
    )
    parser_banners.add_argument(
        "--game-root",
        type=Path,
        default=None,
        help="Bannerlord game root directory. Overrides BANNERLORD_GAME_ROOT env var."
    )
    parser_banners.add_argument(
        "--json-output",
        type=Path,
        default=None,
        help="Path to save banner JSON. Defaults to Data/raw/banner-items.json."
    )
    parser_banners.add_argument(
        "--markdown-output",
        type=Path,
        default=None,
        help="Path to save banner markdown. Defaults to Docs/reports/banner-effects.md."
    )
    parser_banners.add_argument(
        "--usage-output",
        type=Path,
        default=None,
        help="Path to save banner effect usage JSON. Defaults to Data/raw/banner-effect-usages.json."
    )
    parser_banners.add_argument(
        "--skip-scan",
        action="store_true",
        help="Skip fresh extraction and reuse existing banner JSON to regenerate the report."
    )
    parser_banners.add_argument(
        "--skip-usage-scan",
        action="store_true",
        help="Do not refresh Data/raw/banner-effect-usages.json while extracting banners."
    )
    parser_banners.add_argument(
        "--include-mp",
        action="store_true",
        help="Also include multiplayer banner XML; off by default to avoid duplicate singleplayer item IDs."
    )

    # Stats subcommand
    parser_stats = subparsers.add_parser(
        "stats",
        help="Extract guide-facing stat tables from generated Bannerlord perk data."
    )
    parser_stats.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="Path to workspace directory"
    )
    parser_stats.add_argument(
        "--perk-export",
        type=Path,
        default=None,
        help="Path to generated perk export JSON. Defaults to Data/export/perk-effects.json."
    )
    parser_stats.add_argument(
        "--json-output",
        type=Path,
        default=None,
        help="Path to save guide stat JSON. Defaults to Data/export/guide-stat-extracts.json."
    )
    parser_stats.add_argument(
        "--markdown-output",
        type=Path,
        default=None,
        help="Path to save guide stat markdown. Defaults to Docs/reports/guide-stat-extracts.md."
    )

    # Commander report subcommand
    parser_commander = subparsers.add_parser(
        "commander-report",
        help="Extract doctrine-ranked commander perk reports for elite one-party builds."
    )
    parser_commander.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="Path to workspace directory"
    )
    parser_commander.add_argument(
        "--perk-export",
        type=Path,
        default=None,
        help="Path to generated perk export JSON. Defaults to Data/export/perk-effects.json."
    )
    parser_commander.add_argument(
        "--json-output",
        type=Path,
        default=None,
        help="Path to save commander report JSON. Defaults to Data/intermediate/commander_perks_extracted.json."
    )
    parser_commander.add_argument(
        "--markdown-output",
        type=Path,
        default=None,
        help="Path to save commander report markdown. Defaults to Data/intermediate/commander_perks_report.txt."
    )
    parser_commander.add_argument(
        "--package-output",
        type=Path,
        default=None,
        help="Path to save the banner package comparison. Defaults to Docs/reports/commander-banner-package-comparison.md."
    )
    parser_commander.add_argument(
        "--investment-output",
        type=Path,
        default=None,
        help="Path to save the commander perk investment bars. Defaults to Docs/reports/commander-perk-investment-bars.md."
    )

    # Battanian start leak analysis subcommand
    parser_battanian = subparsers.add_parser(
        "battanian-starts",
        help="Brute-force Battanian character creation paths and classify focus leaks."
    )
    parser_battanian.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="Path to workspace directory"
    )
    parser_battanian.add_argument(
        "--culture",
        default="Battania",
        help="Culture family options to use."
    )
    parser_battanian.add_argument(
        "--json-output",
        type=Path,
        default=None,
        help="Path to save leak JSON. Defaults to Data/intermediate/battanian_start_leaks.json."
    )
    parser_battanian.add_argument(
        "--markdown-output",
        type=Path,
        default=None,
        help="Path to save leak markdown. Defaults to Docs/reports/battanian-start-leaks.md."
    )
    parser_battanian.add_argument(
        "--top",
        type=int,
        default=20,
        help="Number of top paths/profiles to include in the report."
    )

    # Culture start leak comparison subcommand
    parser_culture_starts = subparsers.add_parser(
        "culture-starts",
        help="Compare character creation focus leaks across all cultures."
    )
    parser_culture_starts.add_argument(
        "--workspace",
        type=Path,
        default=default_workspace(),
        help="Path to workspace directory"
    )
    parser_culture_starts.add_argument(
        "--culture",
        action="append",
        default=[],
        help="Culture to include. Repeat to compare a subset. Defaults to all family cultures."
    )
    parser_culture_starts.add_argument(
        "--json-output",
        type=Path,
        default=None,
        help="Path to save comparison JSON. Defaults to Data/intermediate/culture_start_leaks.json."
    )
    parser_culture_starts.add_argument(
        "--markdown-output",
        type=Path,
        default=None,
        help="Path to save comparison markdown. Defaults to Docs/reports/culture-start-leaks.md."
    )
    parser_culture_starts.add_argument(
        "--top",
        type=int,
        default=20,
        help="Number of top paths/profiles to include per culture."
    )

    args = parser.parse_args()

    # Execute the requested command
    workspace = args.workspace.resolve()

    if args.command == "rebuild":
        rebuild(
            workspace=workspace,
            game_root=args.game_root,
            skip_extract=args.skip_extract,
        )

    elif args.command == "validate":
        validate(workspace=workspace)

    elif args.command == "prune":
        before, after, removed_fields = prune_overrides(
            workspace=workspace,
            dry_run=args.dry_run,
        )
        action = "Would prune" if args.dry_run else "Pruned"
        print(f"{action} {before - after} override entries and {removed_fields} machine fields.")
        print(f"Overrides: {before} -> {after}")

    elif args.command == "extract-xp":
        # 1. Run XP awards extraction
        print("=== Running XP Awards Extraction ===")
        json_output_awards = workspace / "Data" / "raw" / "xp-award-methods.json"
        markdown_output_awards = workspace / "Docs" / "reports" / "xp-awards.md"
        il_output_awards = workspace / "Docs" / "reports" / "xp-award-il.md"
        extract_xp_awards(
            workspace=workspace,
            game_root=args.game_root,
            assemblies=args.assembly,
            json_output=json_output_awards,
            markdown_output=markdown_output_awards,
            il_output=il_output_awards,
            deep_scan_callers=args.deep_scan_callers,
            include_contracts=args.include_contracts,
            include_il=args.include_il,
        )

        # 2. Run XP formulas extraction
        print("\n=== Running XP Formulas Extraction ===")
        json_output_formulas = workspace / "Data" / "raw" / "xp-formula-methods.json"
        markdown_output_formulas = workspace / "Docs" / "reports" / "xp-formulas.md"
        insights_output_formulas = workspace / "Docs" / "reports" / "xp-insights.md"
        extract_xp_formulas(
            workspace=workspace,
            game_root=args.game_root,
            json_output=json_output_formulas,
            markdown_output=markdown_output_formulas,
            insights_output=insights_output_formulas,
            include_il=not args.no_il,
            keep_temp=args.keep_temp,
        )

        # 3. Run Skill XP sources extraction
        print("\n=== Running Skill XP Sources Extraction ===")
        json_output_sources = workspace / "Data" / "raw" / "skill-xp-source-methods.json"
        markdown_output_sources = workspace / "Docs" / "reports" / "skill-xp-sources.md"
        extract_skill_xp_sources(
            workspace=workspace,
            game_root=args.game_root,
            json_output=json_output_sources,
            markdown_output=markdown_output_sources,
            skip_scan=args.skip_scan,
        )

    elif args.command == "extract-creation":
        json_output = workspace / "Data" / "raw" / "character-creation-options.json"
        markdown_output = workspace / "Docs" / "reports" / "character-creation-options.md"
        extract_character_creation(
            workspace=workspace,
            game_root=args.game_root,
            json_output=json_output,
            markdown_output=markdown_output,
            skip_scan=args.skip_scan,
        )

    elif args.command == "extract-combat":
        json_output = workspace / "Data" / "raw" / "combat-formula-methods.json"
        markdown_output = workspace / "Docs" / "reports" / "combat-formulas.md"
        insights_output = workspace / "Docs" / "reports" / "combat-insights.md"
        extract_combat_formulas(
            workspace=workspace,
            game_root=args.game_root,
            json_output=json_output,
            markdown_output=markdown_output,
            insights_output=insights_output,
            include_il=not args.no_il,
            keep_temp=args.keep_temp,
        )

    elif args.command == "extract-banners":
        json_output = args.json_output or workspace / "Data" / "raw" / "banner-items.json"
        markdown_output = args.markdown_output or workspace / "Docs" / "reports" / "banner-effects.md"
        usage_output = args.usage_output or workspace / "Data" / "raw" / "banner-effect-usages.json"
        extract_banners(
            workspace=workspace,
            game_root=args.game_root,
            json_output=json_output,
            markdown_output=markdown_output,
            usage_output=usage_output,
            skip_scan=args.skip_scan,
            skip_usage_scan=args.skip_usage_scan,
            include_mp=args.include_mp,
        )

    elif args.command == "stats":
        perk_export_path = args.perk_export or workspace / "Data" / "export" / "perk-effects.json"
        json_output = args.json_output or workspace / "Data" / "export" / "guide-stat-extracts.json"
        markdown_output = args.markdown_output or workspace / "Docs" / "reports" / "guide-stat-extracts.md"
        extract_guide_stats(
            workspace=workspace,
            perk_export_path=perk_export_path.resolve(),
            json_output=json_output,
            markdown_output=markdown_output,
        )

    elif args.command == "commander-report":
        perk_export_path = args.perk_export or workspace / "Data" / "export" / "perk-effects.json"
        json_output = args.json_output or workspace / "Data" / "intermediate" / "commander_perks_extracted.json"
        markdown_output = args.markdown_output or workspace / "Data" / "intermediate" / "commander_perks_report.txt"
        package_output = args.package_output or workspace / "Docs" / "reports" / "commander-banner-package-comparison.md"
        investment_output = args.investment_output or workspace / "Docs" / "reports" / "commander-perk-investment-bars.md"
        extract_commander_perks(
            workspace=workspace,
            perk_export_path=perk_export_path.resolve(),
            json_output=json_output,
            markdown_output=markdown_output,
            package_output=package_output,
            investment_output=investment_output,
        )

    elif args.command == "battanian-starts":
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
        print(
            "  minimum default focus leaks: {leaks} ({paths} paths)".format(
                leaks=summary["minimum_default_focus_leaks"],
                paths=summary["paths_at_minimum_default_focus_leaks"],
            )
        )
        print(f"  no-hard-leak paths: {summary['no_hard_focus_leak_paths']}")
        print(f"  no-hard/no-tactics paths: {summary['no_hard_no_tactics_paths']}")

    elif args.command == "culture-starts":
        json_output = args.json_output or workspace / "Data" / "intermediate" / "culture_start_leaks.json"
        markdown_output = args.markdown_output or workspace / "Docs" / "reports" / "culture-start-leaks.md"
        payload = analyze_culture_start_leaks(
            workspace=workspace,
            cultures=args.culture or None,
            json_output=json_output,
            markdown_output=markdown_output,
            top=args.top,
        )
        print(f"Culture start leak JSON written: {json_output}")
        print(f"Culture start leak report written: {markdown_output}")
        for item in payload["cultures"]:
            summary = item["summary"]
            print(
                "  {culture}: min-leaks {min_leaks} ({paths} paths), valid {valid}, no-hard {no_hard}, zero-leak {zero}".format(
                    culture=item["culture"],
                    min_leaks=summary["minimum_default_focus_leaks"],
                    paths=summary["paths_at_minimum_default_focus_leaks"],
                    valid=summary["attribute_valid_paths"],
                    no_hard=summary["no_hard_focus_leak_paths"],
                    zero=summary["zero_default_focus_leak_paths"],
                )
            )


if __name__ == "__main__":
    main()
