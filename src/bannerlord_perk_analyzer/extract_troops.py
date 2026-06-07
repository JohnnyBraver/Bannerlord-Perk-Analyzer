from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .postprocess import default_workspace
    from .utils import resolve_game_root, run_extractor
except ImportError:
    from postprocess import default_workspace
    from utils import resolve_game_root, run_extractor


def extract_troops(
    workspace: Path,
    game_root: Path | None,
    json_output: Path,
    skip_scan: bool = False,
) -> None:
    if not skip_scan:
        resolved_game_root = resolve_game_root(game_root)
        args = [
            "troops",
            "--game-root",
            str(resolved_game_root),
            "--output",
            str(json_output),
        ]
        run_extractor(workspace, args)
        
    print(f"Troops JSON written: {json_output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Bannerlord troop stats and loadouts.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--game-root", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--skip-scan", action="store_true", help="Reuse existing JSON and do not rerun scanning.")
    args = parser.parse_args()
    
    workspace = args.workspace.resolve()
    json_output = args.json_output or workspace / "Data" / "raw" / "troops.json"
    extract_troops(
        workspace=workspace,
        game_root=args.game_root,
        json_output=json_output,
        skip_scan=args.skip_scan,
    )


if __name__ == "__main__":
    main()
