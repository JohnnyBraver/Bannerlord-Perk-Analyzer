#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add src/ and src/bannerlord_perk_analyzer directories to the path so we can import package and modules
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent / "src" / "bannerlord_perk_analyzer"))

try:
    from bannerlord_perk_analyzer.extract_character_creation import extract_character_creation
    from bannerlord_perk_analyzer.extract_combat_formulas import extract_combat_formulas
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


if __name__ == "__main__":
    main()
