from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .perk_limits import perk_limits_markdown
    from .postprocess import default_workspace
except ImportError:
    from perk_limits import perk_limits_markdown
    from postprocess import default_workspace


def main() -> None:
    parser = argparse.ArgumentParser(description="Write the readable perk limits reference.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    args = parser.parse_args()

    path = args.workspace.resolve() / "Docs" / "notes" / "perk-limits.md"
    path.write_text(perk_limits_markdown(), encoding="utf-8", newline="\n")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
