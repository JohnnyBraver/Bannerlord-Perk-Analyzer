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
            title="Trade Skill And Gold Economy Perks",
            description="Broad index of all Trade skill perks plus non-Trade perks classified as gold economy. This bucket intentionally includes non-price rows such as carrying capacity, relationship, settlement, and unique barter effects.",
            predicate=lambda row: row.get("skill") == "Trade" or row_type(row) == "gold economy",
        ),
        GuideBucket(
            key="gold_economy_perks",
            title="Gold Economy Perks",
            description="Rows classified specifically as gold economy, excluding non-economic Trade skill side effects.",
            predicate=lambda row: row_type(row) == "gold economy",
        ),
    ]
