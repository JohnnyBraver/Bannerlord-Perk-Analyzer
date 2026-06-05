from __future__ import annotations
from typing import Any

try:
    from ..extract_guide_stats import (
        GuideBucket, GuideStack, PerkRef, is_troop_facing, is_defensive_survival_effect, row_subtype
    )
except ImportError:
    from extract_guide_stats import (
        GuideBucket, GuideStack, PerkRef, is_troop_facing, is_defensive_survival_effect, row_subtype
    )

SURVIVAL_FORMULAS = [
    {
        "key": "regular_troop_death_chance",
        "formula": "deathChance = 1 / ((1 + medicine * 0.01 * eventMultiplier + troopLevel * 0.02 + additiveBonuses) * (1 + factorBonuses))",
        "notes": [
            "Player map event eventMultiplier is 1.0.",
            "Non-player map event eventMultiplier is 0.25.",
            "Medicine is capped at 330 for player-facing skill.",
        ],
    },
    {
        "key": "minister_of_health_max_hp",
        "formula": "maxBonus = max(0, medicineSkill - 250), capped by max skill 330 => +80 HP",
    },
]

HP_STACKS = [
    GuideStack(
        key="any_regular_troop_hp",
        title="Any Regular Troop HP",
        metric="flat HP",
        components=(
            PerkRef("MedicineMinisterOfHealth", "primary", effective_bonus=80, note="Medicine 330"),
            PerkRef("PolearmHardyFrontline", "primary"),
            PerkRef("TwoHandedThickHides", "secondary"),
        ),
        note="Baseline broad troop HP stack.",
    ),
    GuideStack(
        key="foot_infantry_hp",
        title="Foot Infantry HP",
        metric="flat HP",
        components=(
            PerkRef("MedicineMinisterOfHealth", "primary", effective_bonus=80, note="Medicine 330"),
            PerkRef("PolearmHardyFrontline", "primary"),
            PerkRef("TwoHandedThickHides", "secondary"),
            PerkRef("AthleticsWellBuilt", "secondary"),
            PerkRef("OneHandedUnwaveringDefense", "secondary"),
            PerkRef("PolearmHardKnock", "secondary"),
        ),
        note="Largest flat regular troop HP stack from the current guide set.",
    ),
    GuideStack(
        key="foot_ranged_hp",
        title="Foot Ranged HP",
        metric="flat HP",
        components=(
            PerkRef("MedicineMinisterOfHealth", "primary", effective_bonus=80, note="Medicine 330"),
            PerkRef("PolearmHardyFrontline", "primary"),
            PerkRef("TwoHandedThickHides", "secondary"),
            PerkRef("AthleticsWellBuilt", "secondary"),
            PerkRef("CrossbowBoltenGuard", "secondary"),
        ),
        note="Uses Picked Shots, whose string id is CrossbowBoltenGuard in the extracted data.",
    ),
    GuideStack(
        key="troop_mount_hp",
        title="Troop Mount HP",
        metric="mixed mount HP",
        components=(PerkRef("MedicineSledges", "secondary"), PerkRef("RidingVeterinary", "secondary")),
        note="Flat mount HP and percentage mount HP are kept as separate component types.",
    ),
]

ARMOR_STACKS = [
    GuideStack(
        key="any_troop_armor",
        title="Any Troop Armor",
        metric="armor per equipped armor piece",
        components=(PerkRef("EngineeringMetallurgy", "secondary"),),
        note="Broad captain armor layer.",
    ),
    GuideStack(
        key="foot_troop_armor",
        title="Foot Troop Armor",
        metric="armor per equipped armor piece",
        components=(PerkRef("EngineeringMetallurgy", "secondary"), PerkRef("AthleticsIgnorePain", "secondary")),
        note="Best foot-troop armor stack in the current guide set.",
    ),
    GuideStack(
        key="mounted_rider_armor",
        title="Mounted Rider Armor",
        metric="armor per equipped armor piece",
        components=(PerkRef("EngineeringMetallurgy", "secondary"), PerkRef("RidingDauntlessSteed", "secondary")),
        note="Best rider armor stack for mounted troops.",
    ),
    GuideStack(
        key="troop_mount_armor",
        title="Troop Mount Armor",
        metric="mount armor",
        components=(PerkRef("RidingToughSteed", "secondary"),),
        note="Mount armor, not rider armor.",
    ),
]

RESISTANCE_STACKS = [
    GuideStack(
        key="melee_infantry_vs_projectiles",
        title="Melee Infantry Vs Projectiles",
        metric="listed damage taken factors",
        components=(PerkRef("ThrowingSkirmisher", "secondary"), PerkRef("TacticsEliteReserves", "secondary")),
        note="Does not include Skirmish Phase Master because that is ranged-troop scoped.",
    ),
    GuideStack(
        key="bow_ranged_vs_projectiles",
        title="Bow Ranged Troops Vs Projectiles",
        metric="listed damage taken factors",
        components=(
            PerkRef("BowSkirmishPhaseMaster", "secondary"),
            PerkRef("ThrowingSkirmisher", "secondary"),
            PerkRef("TacticsEliteReserves", "secondary"),
        ),
        note="Counter Fire is not included because the live damage code is crossbow-current-weapon gated.",
    ),
    GuideStack(
        key="crossbow_vs_projectiles",
        title="Crossbow Troops Vs Projectiles",
        metric="listed damage taken factors",
        components=(
            PerkRef("BowSkirmishPhaseMaster", "secondary"),
            PerkRef("CrossbowCounterFire", "secondary"),
            PerkRef("ThrowingSkirmisher", "secondary"),
            PerkRef("TacticsEliteReserves", "secondary"),
        ),
        note="Assumes the victim is holding a crossbow for Counter Fire.",
    ),
    GuideStack(
        key="charge_damage_to_formation",
        title="Charge Damage To Formation",
        metric="listed charge damage factors",
        components=(PerkRef("AthleticsBraced", "secondary"), PerkRef("PolearmSureFooted", "secondary")),
        note="Charge-specific layer.",
    ),
]


def get_survival_formulas() -> list[dict[str, Any]]:
    return SURVIVAL_FORMULAS


def get_stacks() -> dict[str, list[GuideStack]]:
    return {
        "hit_points": HP_STACKS,
        "armor": ARMOR_STACKS,
        "damage_reduction": RESISTANCE_STACKS,
    }


def get_buckets() -> list[GuideBucket]:
    defensive_subtypes = {
        "damage resistance",
        "ranged",
        "charge",
        "projectile protection",
        "shield durability",
    }

    return [
        GuideBucket(
            key="troop_survival_hit_points",
            title="Troop Hit Point Perks",
            description="Troop- or mount-facing hit point perks used by the survivability guide.",
            predicate=lambda row: row_subtype(row) == "hit points" and is_troop_facing(row),
        ),
        GuideBucket(
            key="troop_survival_armor",
            title="Troop Armor Perks",
            description="Troop- or mount-facing armor perks used by the survivability guide.",
            predicate=lambda row: row_subtype(row) == "armor increase" and is_troop_facing(row),
        ),
        GuideBucket(
            key="troop_survival_damage_reduction",
            title="Live Troop Damage Reduction And Shield Perks",
            description="Live-battle damage-taken, charge, projectile-protection, and shield durability perks. Simulation-only rows are split into their own bucket.",
            predicate=lambda row: (
                row_subtype(row) in defensive_subtypes
                and "simulation" not in row.get("classification", {}).get("trigger_conditions", [])
                and is_troop_facing(row)
                and is_defensive_survival_effect(row)
            ),
        ),
        GuideBucket(
            key="simulation_troop_damage_reduction",
            title="Simulation Troop Damage Reduction Perks",
            description="Autoresolve/simulation-only defensive rows separated from live-battle survivability tables.",
            predicate=lambda row: (
                row_subtype(row) in defensive_subtypes
                and "simulation" in row.get("classification", {}).get("trigger_conditions", [])
                and is_troop_facing(row)
                and is_defensive_survival_effect(row)
            ),
        ),
    ]
