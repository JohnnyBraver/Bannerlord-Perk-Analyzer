from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


MIN_ATTRIBUTE = 2
MAX_ATTRIBUTE = 10
MIN_FOCUS = 0
MAX_FOCUS = 5
PERK_LEVELS = tuple(range(25, 300, 25))


# Classification of the final perks for the 18 skills, mapping how they are affected
# when excluding perks that grant the same effects as the base skill leveling benefits.
FINAL_PERKS_CLASSIFICATION = {
    "Athletics": {
        "perk": "Mighty Blow",
        "level": 275,
        "base_passive": "Increases running speed (+0.06% per level)",
        "strict_exclude": False,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Ignore Pain / Spartan"
    },
    "Bow": {
        "perk": "Deadshot",
        "level": 275,
        "base_passive": "Increases damage (+0.11% per level) and accuracy (+0.09% per level)",
        "strict_exclude": True,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Quick Draw / Ranger's Swiftness"
    },
    "Charm": {
        "perk": "Immortal Charm",
        "level": 275,
        "base_passive": "Increases relation gain speed (+0.5% per level)",
        "strict_exclude": False,
        "broad_exclude": False,
        "new_level": 275,
        "new_perks": "Immortal Charm"
    },
    "Crossbow": {
        "perk": "Mighty Pull",
        "level": 275,
        "base_passive": "Increases reload speed (+0.07% per level) and accuracy (+0.09% per level)",
        "strict_exclude": True,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Picked Shots / Terror"
    },
    "Engineering": {
        "perk": "Masterwork",
        "level": 275,
        "base_passive": "Increases siege engine build speed (+0.9% per level) and wall repair speed (+0.9% per level)",
        "strict_exclude": True,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Architectural Commissions / Clockwork"
    },
    "Leadership": {
        "perk": "Ultimate Leader",
        "level": 275,
        "base_passive": "Increases party morale (+0.05% per level) and troop XP gain (+0.1% per level)",
        "strict_exclude": False,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Talent Magnet / We Pledge our Swords"
    },
    "Medicine": {
        "perk": "Minister of Health",
        "level": 275,
        "base_passive": "Increases recovery rate of sick/wounded (+10% per level) and casualty survival (+0.08% per level)",
        "strict_exclude": False,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Battle Hardened / Helping Hands"
    },
    "One Handed": {
        "perk": "Way of the Sword",
        "level": 275,
        "base_passive": "Increases attack speed and damage (+0.07% speed, +0.15% damage per level)",
        "strict_exclude": True,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Chink in the Armor / Prestige"
    },
    "Polearm": {
        "perk": "Way of the Spear",
        "level": 275,
        "base_passive": "Increases attack speed and damage (+0.07% speed, +0.15% damage per level)",
        "strict_exclude": True,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Counterweight / Sharpen the Tip"
    },
    "Riding": {
        "perk": "The Way Of The Saddle",
        "level": 275,
        "base_passive": "Increases mount speed (+0.2% per level) and mount maneuverability (+0.04% per level)",
        "strict_exclude": True,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Dauntless Steed / Tough Steed"
    },
    "Roguery": {
        "perk": "Rogue Extraordinaire",
        "level": 275,
        "base_passive": "Increases loot amount (+0.25% per level) and raid speed (+0.25% per level)",
        "strict_exclude": True,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Dash and Slash / Fleet Footed"
    },
    "Scouting": {
        "perk": "Uncanny Insight",
        "level": 275,
        "base_passive": "Increases track detection, tracking details, and party map speed (+0.07% map speed per level)",
        "strict_exclude": True,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Rearguard / Vanguard"
    },
    "Smithing": {
        "perk": "Legendary Smith",
        "level": 275,
        "base_passive": "Increases learning rate of parts and stamina recovery speed (+0.5% per level)",
        "strict_exclude": False,
        "broad_exclude": False,
        "new_level": 275,
        "new_perks": "Legendary Smith"
    },
    "Steward": {
        "perk": "Price of Loyalty",
        "level": 275,
        "base_passive": "Increases party size limit (+0.25 party size per level)",
        "strict_exclude": False,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Master of Planning / Master of Warcraft"
    },
    "Tactics": {
        "perk": "Tactical Mastery",
        "level": 275,
        "base_passive": "Increases battle simulation advantage (+0.1% per level)",
        "strict_exclude": True,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Counter Offensive / Gens d'armes"
    },
    "Throwing": {
        "perk": "Unstoppable Force",
        "level": 275,
        "base_passive": "Increases damage (+0.13% per level) and accuracy (+0.06% per level)",
        "strict_exclude": True,
        "broad_exclude": True,
        "new_level": 250,
        "new_perks": "Impale / Weak Spot"
    },
    "Trade": {
        "perk": "Everything Has a Price",
        "level": 300,
        "base_passive": "Reduces trade penalty (+0.4% per level)",
        "strict_exclude": False,
        "broad_exclude": False,
        "new_level": 300,
        "new_perks": "Everything Has a Price"
    },
    "Two Handed": {
        "perk": "Way Of The Great Axe",
        "level": 250,
        "base_passive": "Increases attack speed and damage (+0.07% speed, +0.15% damage per level)",
        "strict_exclude": True,
        "broad_exclude": True,
        "new_level": 225,
        "new_perks": "Blade Master / Vandal"
    }
}


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


def check_perk_filters(workspace: Path) -> list[str]:
    """
    Verifies that the actual final perks and levels in Data/export/perk-effects.json
    match our classifications in FINAL_PERKS_CLASSIFICATION.
    """
    export_path = workspace / "Data" / "export" / "perk-effects.json"
    if not export_path.exists():
        return [f"Export perk file does not exist: {export_path}"]

    try:
        with export_path.open("r", encoding="utf-8") as f:
            perk_effects = json.load(f)
    except Exception as e:
        return [f"Failed to load export perk file: {e}"]

    skills = {}
    for entry in perk_effects:
        skill = entry["skill"]
        level = entry["level"]
        perk = entry["perk"]
        if skill not in skills:
            skills[skill] = {}
        if level not in skills[skill]:
            skills[skill][level] = set()
        skills[skill][level].add(perk)

    errors = []
    for skill, expected_info in FINAL_PERKS_CLASSIFICATION.items():
        if skill not in skills:
            errors.append(f"Expected skill '{skill}' not found in perk export data.")
            continue

        max_level = max(skills[skill].keys())
        expected_level = expected_info["level"]

        if max_level != expected_level:
            errors.append(
                f"Mismatch in final perk level for '{skill}': expected level {expected_level}, "
                f"found level {max_level} in data."
            )

        expected_perk = expected_info["perk"]
        actual_perks = skills[skill][max_level]
        if expected_perk not in actual_perks:
            errors.append(
                f"Mismatch in final perk name for '{skill}' at level {max_level}: "
                f"expected perk '{expected_perk}', found {actual_perks} in data."
            )

    return errors


def final_perk_distribution_markdown() -> str:
    # Compute distributions
    raw_dist = {250: 0, 275: 0, 300: 0}
    strict_dist = {225: 0, 250: 0, 275: 0, 300: 0}
    broad_dist = {225: 0, 250: 0, 275: 0, 300: 0}

    for info in FINAL_PERKS_CLASSIFICATION.values():
        # Raw
        raw_dist[info["level"]] = raw_dist.get(info["level"], 0) + 1
        # Strict
        strict_lvl = info["new_level"] if info["strict_exclude"] else info["level"]
        strict_dist[strict_lvl] = strict_dist.get(strict_lvl, 0) + 1
        # Broad
        broad_lvl = info["new_level"] if (info["strict_exclude"] or info["broad_exclude"]) else info["level"]
        broad_dist[broad_lvl] = broad_dist.get(broad_lvl, 0) + 1

    lines = [
        "## Final Perk Level Distribution",
        "Below is the distribution of the highest level perk in each skill. We track how this distribution shifts under two exclusion filters:",
        "1. **Strict Exclusion**: Excludes perks that scale the exact same passive attribute that the skill natively scales (e.g. One Handed speed/damage).",
        "2. **Broad Exclusion**: Excludes any final perk that acts as a linear passive scaling extension of any basic stat (e.g. Medicine scaling troop HP).",
        "",
        "### Distribution Summary Table",
        "| Final Perk Level | Raw (No Exclusions) | Strict Exclusion | Broad Exclusion (Passive Scale) |",
        "| :--- | :---: | :---: | :---: |",
    ]
    for lvl in sorted(strict_dist.keys()):
        raw_val = raw_dist.get(lvl, 0)
        strict_val = strict_dist[lvl]
        broad_val = broad_dist[lvl]
        lines.append(f"| Level {lvl} | {raw_val} skills | {strict_val} skills | {broad_val} skills |")

    lines.extend([
        "",
        "### Skill-by-Skill Active Cap Table",
        "| Skill | Raw Final Perk | Level | Base Passive Leveling Effect | Strict Exclude | Broad Exclude | Active Cap Level | New Last Perk(s) |",
        "| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :--- |"
    ])

    for skill, info in sorted(FINAL_PERKS_CLASSIFICATION.items()):
        active_cap = info["new_level"] if (info["strict_exclude"] or info["broad_exclude"]) else info["level"]
        strict_esc = "Exclude" if info["strict_exclude"] else "Keep"
        broad_esc = "Exclude" if info["broad_exclude"] else "Keep"
        lines.append(
            f"| {skill} | {info['perk']} | {info['level']} | {info['base_passive']} | {strict_esc} | {broad_esc} | **{active_cap}** | {info['new_perks']} |"
        )

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
            final_perk_distribution_markdown()
        ]
    ) + "\n"
