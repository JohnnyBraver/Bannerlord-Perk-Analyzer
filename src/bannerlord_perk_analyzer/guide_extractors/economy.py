from __future__ import annotations
from typing import Any

try:
    from ..extract_guide_stats import GuideBucket, row_type
except ImportError:
    from extract_guide_stats import GuideBucket, row_type


def get_buckets() -> list[GuideBucket]:
    return [
        GuideBucket(
            key="trade_economy_perks",
            title="Trade and Gold Economy Perks",
            description="Perks that affect prices, trade penalties, workshops, caravans, and gold accumulation.",
            predicate=lambda row: row.get("skill") == "Trade" or row_type(row) == "gold economy",
        ),
    ]
