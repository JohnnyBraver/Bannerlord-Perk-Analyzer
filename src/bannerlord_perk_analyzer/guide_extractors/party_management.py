from __future__ import annotations
from typing import Any

try:
    from ..extract_guide_stats import GuideBucket, row_subtype
except ImportError:
    from extract_guide_stats import GuideBucket, row_subtype


def row_role(row: dict[str, Any]) -> str:
    return str(row.get("game", {}).get("role", ""))


def row_triggers(row: dict[str, Any]) -> set[str]:
    return {str(item) for item in row.get("classification", {}).get("trigger_conditions", [])}


def get_buckets() -> list[GuideBucket]:
    return [
        GuideBucket(
            key="troop_xp",
            title="Troop XP Perks",
            description="Broad index of perks that directly mention troop XP or experience gains, across party, garrison, formation, siege, and personal triggers.",
            predicate=lambda row: row_subtype(row) == "troop xp",
        ),
        GuideBucket(
            key="party_passive_troop_xp",
            title="Party Passive Troop XP Perks",
            description="Party leader and quartermaster troop XP rows for passive or party-wide training tables.",
            predicate=lambda row: row_subtype(row) == "troop xp"
            and row_role(row) in {"party leader", "quartermaster"}
            and "governed settlement" not in row_triggers(row),
        ),
        GuideBucket(
            key="garrison_troop_xp",
            title="Garrison Troop XP Perks",
            description="Governor and settlement-defense troop XP rows that apply to garrisons rather than the traveling party.",
            predicate=lambda row: row_subtype(row) == "troop xp" and "governed settlement" in row_triggers(row),
        ),
        GuideBucket(
            key="other_troop_xp",
            title="Other Troop XP Perks",
            description="Troop XP rows with engineer, captain, surgeon, personal, siege, or kill-triggered scopes that should not be merged into passive party-training tables without review.",
            predicate=lambda row: row_subtype(row) == "troop xp"
            and not (
                row_role(row) in {"party leader", "quartermaster"}
                and "governed settlement" not in row_triggers(row)
            )
            and "governed settlement" not in row_triggers(row),
        ),
        GuideBucket(
            key="party_leader_quartermaster_perks",
            title="Party Leader and Quartermaster Perks",
            description="Broad index of perks that apply to a Party Leader or Quartermaster role. Use narrower subtype-specific buckets for recommendations about party size, speed, wages, prisoners, food, or carrying capacity.",
            predicate=lambda row: row_role(row) in {"party leader", "quartermaster"},
        ),
    ]
