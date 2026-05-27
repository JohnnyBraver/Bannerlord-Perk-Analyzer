from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any

try:
    from .postprocess import default_workspace
    from .xp_reports import write_xp_il, write_xp_markdown
except ImportError:
    from postprocess import default_workspace
    from xp_reports import write_xp_il, write_xp_markdown


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def extract_xp_awards(
    workspace: Path,
    game_root: Path | None,
    assemblies: list[str],
    json_output: Path,
    markdown_output: Path,
    il_output: Path,
    deep_scan_callers: bool,
    include_contracts: bool,
    include_il: bool,
) -> None:
    env_game_root = os.environ.get("BANNERLORD_GAME_ROOT")
    if game_root is None and not env_game_root:
        raise SystemExit("Bannerlord game root is required. Pass --game-root or set BANNERLORD_GAME_ROOT.")
    resolved_game_root = game_root or Path(str(env_game_root))
    project = workspace / "tools" / "BannerlordExtractor" / "BannerlordExtractor.csproj"
    if not project.exists():
        raise SystemExit(f"Extractor project is missing: {project}")

    command = [
        "dotnet",
        "run",
        "--project",
        str(project),
        "--",
        "xp-methods",
        "--game-root",
        str(resolved_game_root.resolve()),
        "--json-output",
        str(json_output),
    ]
    for assembly in assemblies:
        command.extend(["--assembly", assembly])
    if deep_scan_callers:
        command.append("--deep-scan-callers")
    if include_contracts:
        command.append("--include-contracts")
    if include_il:
        command.append("--include-il")

    subprocess.run(command, check=True)
    payload = read_json(json_output)
    write_xp_markdown(
        payload,
        markdown_output,
        workspace,
        json_output_path=json_output,
        il_output_path=il_output if include_il else None,
    )
    if include_il:
        write_xp_il(payload, il_output)

    print(f"Report written: {markdown_output}")
    if include_il:
        print(f"IL written: {il_output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract a first-pass map of Bannerlord XP award logic.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--game-root", type=Path, default=None)
    parser.add_argument("--assembly", action="append", default=[], help="Assembly name without .dll. Repeat to scan multiple assemblies.")
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    parser.add_argument("--il-output", type=Path, default=None)
    parser.add_argument("--deep-scan-callers", action="store_true")
    parser.add_argument("--include-contracts", action="store_true")
    parser.add_argument("--include-il", action="store_true")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    json_output = args.json_output or workspace / "Data" / "generated" / "xp-award-methods.json"
    markdown_output = args.markdown_output or workspace / "Data" / "generated" / "reports" / "xp-awards.md"
    il_output = args.il_output or workspace / "Data" / "generated" / "reports" / "xp-award-il.md"
    extract_xp_awards(
        workspace=workspace,
        game_root=args.game_root,
        assemblies=args.assembly,
        json_output=json_output,
        markdown_output=markdown_output,
        il_output=il_output,
        deep_scan_callers=args.deep_scan_callers,
        include_contracts=args.include_contracts,
        include_il=args.include_il,
    )


if __name__ == "__main__":
    main()
