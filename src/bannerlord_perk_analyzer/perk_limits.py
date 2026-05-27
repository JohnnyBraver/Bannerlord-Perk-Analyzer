from __future__ import annotations

from dataclasses import dataclass


MIN_ATTRIBUTE = 2
MAX_ATTRIBUTE = 10
MIN_FOCUS = 0
MAX_FOCUS = 5
PERK_LEVELS = tuple(range(25, 300, 25))


@dataclass(frozen=True)
class SkillInvestment:
    attribute: int
    focus: int
    limit: int
    peak_learning_range: int


def skill_limit(attribute: int, focus: int) -> int:
    return 4 + (14 * (attribute - 1)) + (40 * focus)


def peak_learning_range(attribute: int, focus: int) -> int:
    return max(0, (10 * (attribute - 1)) + (30 * focus))


def minimum_focus_for_level(level: int, attribute: int, minimum_focus: int = MIN_FOCUS) -> int | None:
    for focus in range(max(MIN_FOCUS, minimum_focus), MAX_FOCUS + 1):
        if skill_limit(attribute, focus) >= level:
            return focus
    return None


def frontier_for_level(
    level: int,
    min_attribute: int = MIN_ATTRIBUTE,
    max_attribute: int = MAX_ATTRIBUTE,
    min_focus: int = MIN_FOCUS,
    max_focus: int = MAX_FOCUS,
) -> list[SkillInvestment]:
    feasible: list[SkillInvestment] = []
    for attribute in range(min_attribute, max_attribute + 1):
        for focus in range(min_focus, max_focus + 1):
            limit = skill_limit(attribute, focus)
            if limit >= level:
                feasible.append(
                    SkillInvestment(
                        attribute=attribute,
                        focus=focus,
                        limit=limit,
                        peak_learning_range=peak_learning_range(attribute, focus),
                    )
                )

    frontier: list[SkillInvestment] = []
    for candidate in feasible:
        dominated = False
        for other in feasible:
            if other == candidate:
                continue
            if (
                other.attribute <= candidate.attribute
                and other.focus <= candidate.focus
                and (other.attribute < candidate.attribute or other.focus < candidate.focus)
            ):
                dominated = True
                break
        if not dominated:
            frontier.append(candidate)

    return sorted(frontier, key=lambda item: (-item.focus, item.attribute))


def format_investment(investment: SkillInvestment) -> str:
    parts: list[str] = [f"{investment.attribute} attribute"]
    if investment.focus:
        parts.append(f"{investment.focus} focus")
    return " + ".join(parts)


def cap_grid_markdown(min_attribute: int = 1) -> str:
    lines = [
        "| Attribute | Focus 0 | Focus 1 | Focus 2 | Focus 3 | Focus 4 | Focus 5 |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for attribute in range(min_attribute, MAX_ATTRIBUTE + 1):
        values = [
            f"{skill_limit(attribute, focus)} ({peak_learning_range(attribute, focus)})"
            for focus in range(MIN_FOCUS, MAX_FOCUS + 1)
        ]
        lines.append(f"| {attribute} | " + " | ".join(values) + " |")
    return "\n".join(lines)


def frontier_markdown() -> str:
    lines = [
        "| Perk Level | Non-dominated target splits |",
        "|---:|---|",
    ]
    for level in PERK_LEVELS:
        investments = ", ".join(format_investment(item) for item in frontier_for_level(level))
        lines.append(f"| {level} | {investments} |")
    return "\n".join(lines)


def perk_limits_markdown() -> str:
    return "\n\n".join(
        [
            "# Perk Limits",
            "Bannerlord uses the same skill limit and peak learning range formulas for every skill:",
            "`limit = 4 + 14 * (attribute - 1) + 40 * focus`",
            "`peak learning range = 10 * (attribute - 1) + 30 * focus`",
            "The limit is where learning rate reaches zero. Peak learning range is the lower threshold where the over-limit penalty starts. The planner optimizes against the limit because that is what matters for reaching perks.",
            "Attribute points apply to every skill in the same attribute group. For example, raising Control helps Bow, Crossbow, and Throwing together.",
            "The build planner treats 2 attribute and 0 focus as the default practical floor, but the full grid below includes 1 attribute because it explains the formula.",
            "## Skill Limit Grid",
            "Cells are `limit (peak learning range)`.",
            cap_grid_markdown(min_attribute=1),
            "## Minimum Target Splits",
            "These are the non-dominated attribute/focus splits for each perk tier. A split is omitted when another split reaches the same tier with no more attribute and no more focus.",
            frontier_markdown(),
            "## Player Point Budget",
            "Every player level grants 1 focus point. Every 4 player levels grant 1 attribute point. For point-budget planning, the minimum level-ups needed for a build are `max(total focus points spent, total attribute points spent * 4)`.",
        ]
    ) + "\n"
