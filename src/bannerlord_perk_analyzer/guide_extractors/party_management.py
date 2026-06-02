from __future__ import annotations
from typing import Any

try:
    from ..extract_guide_stats import GuideBucket, row_subtype
except ImportError:
    from extract_guide_stats import GuideBucket, row_subtype


def get_buckets() -> list[GuideBucket]:
    return [
        GuideBucket(
            key="troop_xp",
            title="Troop XP Perks",
            description="Perks that directly mention troop XP or experience gains.",
            predicate=lambda row: row_subtype(row) == "troop xp",
        ),
        GuideBucket(
            key="party_leader_quartermaster_perks",
            title="Party Leader and Quartermaster Perks",
            description="Perks that apply to a Party Leader or Quartermaster role to manage party size, speed, wages, and limits.",
            predicate=lambda row: row.get("game", {}).get("role", "") in {"party leader", "quartermaster"},
        ),
    ]
