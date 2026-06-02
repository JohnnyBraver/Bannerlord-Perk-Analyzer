from __future__ import annotations
from typing import Any

try:
    from ..extract_guide_stats import GuideBucket
except ImportError:
    from extract_guide_stats import GuideBucket


def get_buckets() -> list[GuideBucket]:
    return [
        GuideBucket(
            key="governor_settlement_perks",
            title="Governor and Settlement Governance Perks",
            description="Perks that apply to a Governor role for governing fiefs, settlements, and castles.",
            predicate=lambda row: row.get("game", {}).get("role", "") == "governor",
        ),
    ]
