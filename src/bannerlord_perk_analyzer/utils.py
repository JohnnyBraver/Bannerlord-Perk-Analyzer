from __future__ import annotations

import os
import subprocess
from pathlib import Path


def resolve_game_root(game_root: Path | None) -> Path:
    env_game_root = os.environ.get("BANNERLORD_GAME_ROOT")
    if game_root is None and not env_game_root:
        raise SystemExit("Bannerlord game root is required. Pass --game-root or set BANNERLORD_GAME_ROOT.")
    return Path(game_root or str(env_game_root))


def run_extractor(workspace: Path, args: list[str]) -> None:
    project = workspace / "tools" / "BannerlordExtractor" / "BannerlordExtractor.csproj"
    if not project.exists():
        raise SystemExit(f"Extractor project is missing: {project}")
    command = [
        "dotnet",
        "run",
        "--project",
        str(project),
        "--",
    ] + args
    subprocess.run(command, check=True)
