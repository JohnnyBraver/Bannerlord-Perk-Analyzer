from __future__ import annotations
from typing import Any

try:
    from ..extract_guide_stats import GuideBucket, row_type
except ImportError:
    from extract_guide_stats import GuideBucket, row_type


def get_buckets() -> list[GuideBucket]:
    return [
        GuideBucket(
            key="medicine_healing_perks",
            title="Medicine and Healing Rate Perks",
            description="Perks from the Medicine skill or perks that boost healing rate/survival factors.",
            predicate=lambda row: row.get("skill") == "Medicine" or row_type(row) == "regen bonus",
        ),
    ]
