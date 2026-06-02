from __future__ import annotations
from typing import Any

try:
    from ..extract_guide_stats import GuideBucket, row_type
except ImportError:
    from extract_guide_stats import GuideBucket, row_type

SMITHING_FORMULAS = [
    {"key": "refining_xp", "formula": "round(0.3 * outputMaterialValue * outputCount)"},
    {"key": "smelting_xp", "formula": "round(0.02 * itemValue)"},
    {"key": "crafting_order_xp", "formula": "round(0.1 * itemValue)"},
    {"key": "free_build_xp", "formula": "round(0.02 * itemValue)"},
    {"key": "crafting_order_base_experience", "formula": "0.25 * theoreticalMaxItemMarketValue(requestedDesignItem)"},
]


def get_smithing_formulas() -> list[dict[str, Any]]:
    return SMITHING_FORMULAS


def get_buckets() -> list[GuideBucket]:
    return [
        GuideBucket(
            key="smithing",
            title="Smithing And Crafting Perks",
            description="Smithing perk effects and crafting-bonus rows.",
            predicate=lambda row: row.get("skill") == "Smithing" or row_type(row) == "crafting bonus",
        ),
    ]
