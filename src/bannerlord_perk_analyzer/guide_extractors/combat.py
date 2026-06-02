from __future__ import annotations
from typing import Any

try:
    from ..extract_guide_stats import (
        GuideBucket, GuideStack, PerkRef, has_troop_scope, row_type, row_subtype
    )
except ImportError:
    from extract_guide_stats import (
        GuideBucket, GuideStack, PerkRef, has_troop_scope, row_type, row_subtype
    )

DIRECT_WEAPON_EFFECTS = [
    {
        "skill": "One Handed",
        "effects": "weapon speed, weapon damage",
        "per_skill": {"speed_pct": 0.07, "damage_pct": 0.15},
    },
    {
        "skill": "Two Handed",
        "effects": "weapon speed, weapon damage",
        "per_skill": {"speed_pct": 0.06, "damage_pct": 0.16},
    },
    {
        "skill": "Polearm",
        "effects": "weapon speed, weapon damage",
        "per_skill": {"speed_pct": 0.06, "damage_pct": 0.07},
    },
    {
        "skill": "Bow",
        "effects": "damage, accuracy",
        "per_skill": {"damage_pct": 0.11, "accuracy_effect_pct": 0.09},
    },
    {
        "skill": "Crossbow",
        "effects": "reload speed, accuracy",
        "per_skill": {"reload_pct": 0.07, "accuracy_effect_pct": 0.05},
    },
    {
        "skill": "Throwing",
        "effects": "ready speed, damage, accuracy",
        "per_skill": {"ready_speed_pct": 0.07, "damage_pct": 0.06, "accuracy_effect_pct": 0.06},
    },
]

AI_BEHAVIOR_FORMULAS = [
    {
        "key": "ai_level",
        "track": "base",
        "formula": "clamp(effectiveSkill / 300 * difficultyFactor * AILevelMultiplier, 0, 1)",
        "normal_high_difficulty": "difficultyFactor = 0.96",
    },
    {"key": "AiShootFreq", "track": "ranged", "formula": "0.3 + 0.7 * currentAI", "shape": "linear"},
    {
        "key": "AiWaitBeforeShootFactor",
        "track": "ranged",
        "formula": "1 - 0.5 * currentAI",
        "shape": "linear reduction",
    },
    {
        "key": "AIBlockOnDecideAbility",
        "track": "melee",
        "formula": "lerp(0.5, 0.99, sqrt(meleeAI))",
        "shape": "diminishing",
    },
    {
        "key": "AIParryOnDecideAbility",
        "track": "melee",
        "formula": "lerp(0.5, 0.95, meleeAI)",
        "shape": "linear",
    },
    {
        "key": "AIDecideOnRealizeEnemyBlockingAttackAbility",
        "track": "melee",
        "formula": "clamp(meleeAI^2.5 - 0.1, 0, 1)",
        "shape": "high-skill weighted",
    },
    {
        "key": "AIRealizeBlockingFromIncorrectSideAbility",
        "track": "melee",
        "formula": "clamp(meleeAI^2.5 - 0.01, 0, 1)",
        "shape": "high-skill weighted",
    },
    {
        "key": "AiRandomizedDefendDirectionChance",
        "track": "melee",
        "formula": "1 - meleeAI^3",
        "shape": "high-skill mistake reduction",
    },
    {
        "key": "AiUseShieldAgainstEnemyMissileProbability",
        "track": "shield",
        "formula": "0.1 + 0.6 * meleeAI + 0.2 * (meleeAI + defensiveness)",
        "shape": "linear plus defensiveness",
    },
]

AI_SKILL_STACKS = [
    GuideStack(
        key="foot_polearm_shield_wall",
        title="Foot Polearm Shield Wall",
        metric="Polearm skill",
        components=(
            PerkRef("PolearmCleanThrust", "secondary"),
            PerkRef("PolearmCounterweight", "secondary"),
            PerkRef("PolearmPhalanx", "primary"),
        ),
        note="Strongest clean melee-AI skill stack found so far.",
    ),
    GuideStack(
        key="foot_one_handed_shield_wall",
        title="Foot One-Handed Shield Wall",
        metric="One Handed skill",
        components=(PerkRef("OneHandedWrappedHandles", "secondary"), PerkRef("PolearmPhalanx", "primary")),
        note="Feeds melee reactions and shield AI.",
    ),
    GuideStack(
        key="foot_two_handed_shield_wall",
        title="Foot Two-Handed Shield Wall",
        metric="Two Handed skill",
        components=(PerkRef("TwoHandedStrongGrip", "secondary"), PerkRef("PolearmPhalanx", "primary")),
        note="Offensive melee-AI stack; no shield-specific defensive payoff.",
    ),
    GuideStack(
        key="horse_archers",
        title="Horse Archers",
        metric="Bow skill",
        components=(PerkRef("BowDeadAim", "secondary"), PerkRef("BowHorseMaster", "secondary")),
        note="Improves ranged AI plus bow damage and accuracy.",
    ),
    GuideStack(
        key="throwing_infantry",
        title="Throwing Infantry",
        metric="Throwing skill",
        components=(
            PerkRef("ThrowingFlexibleFighter", "secondary"),
            PerkRef("AthleticsStrongArms", "secondary"),
            PerkRef("ThrowingRunningThrow", "secondary"),
        ),
        note="Strong javelin-infantry stack; Flexible Fighter is category-sensitive.",
    ),
]


def get_weapon_effects() -> list[dict[str, Any]]:
    return DIRECT_WEAPON_EFFECTS


def get_behavior_formulas() -> list[dict[str, Any]]:
    return AI_BEHAVIOR_FORMULAS


def get_stacks() -> dict[str, list[GuideStack]]:
    return {
        "ai_skill": AI_SKILL_STACKS
    }


def get_buckets() -> list[GuideBucket]:
    return [
        GuideBucket(
            key="troop_ai_skill_bonuses",
            title="Troop AI Skill Bonus Perks",
            description="Perks that add effective skills to troops and can feed AI formulas when the troop uses that skill.",
            predicate=lambda row: row_subtype(row) == "skill bonus" and has_troop_scope(row),
        ),
        GuideBucket(
            key="personal_combat_perks",
            title="Personal Combat Payoff Perks",
            description="Perks with a Personal role that affect the main hero's combat stats.",
            predicate=lambda row: row.get("game", {}).get("role", "") == "personal" and row_type(row) == "personal combat",
        ),
        GuideBucket(
            key="captain_combat_perks",
            title="Captain and Troop Combat Perks",
            description="Perks with a Captain role that apply combat stat boosts to the formation.",
            predicate=lambda row: row.get("game", {}).get("role", "") == "captain" and row_type(row) == "troop combat",
        ),
    ]
