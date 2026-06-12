from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from .perk_limits import MAX_ATTRIBUTE, MAX_FOCUS, MIN_ATTRIBUTE, peak_learning_range, skill_limit
    from .postprocess import default_workspace
    from .xp_reports import display_path, table_escape
except ImportError:
    from perk_limits import MAX_ATTRIBUTE, MAX_FOCUS, MIN_ATTRIBUTE, peak_learning_range, skill_limit
    from postprocess import default_workspace
    from xp_reports import display_path, table_escape


CATEGORY_META = {
    "core_troop_lethality": {
        "title": "Core Troop Lethality",
        "description": (
            "Direct live-battle power per soldier: damage, combat skill, attack cadence, accuracy, "
            "melee pressure, and troop combat movement. For shock infantry, movement speed is treated "
            "as a lethality multiplier because it shortens arrow exposure and helps force melee contact."
        ),
    },
    "combat_staying_power": {
        "title": "Combat Staying Power",
        "description": (
            "Live-battle durability for elite troops: hit points, armor, damage reduction, shield coverage, "
            "stagger resistance, and survival-facing combat effects."
        ),
    },
    "engagement_control": {
        "title": "Engagement Control",
        "description": (
            "Campaign movement and pursuit tools that let the party choose fights, avoid bad ones, and later "
            "run down parties of equal or smaller size."
        ),
    },
    "party_scaling": {
        "title": "Party Scaling",
        "description": (
            "Party size and logistics that scale the elite stack. These are valuable, but they come after "
            "per-troop dominance and enough map speed to pick engagements."
        ),
    },
    "low_priority_misleading": {
        "title": "Low Priority or Misleading for This Doctrine",
        "description": (
            "Personal-only, governor-only, siege-only, simulation-only, projectile-speed, and weapon-handling "
            "rows that can look relevant in a keyword report but do not provide core one-party shock-infantry value."
        ),
    },
}

CATEGORY_ORDER = tuple(CATEGORY_META)
RATING_ORDER = {"high": 0, "medium": 1, "low": 2}

COMMANDER_ROLES = {
    "captain",
    "party leader",
    "quartermaster",
    "scout",
    "surgeon",
    "clan leader",
    "army leader",
}

SPEED_KIND_DESCRIPTIONS = {
    "campaign_party_speed": "Strategic party or army movement on the campaign map.",
    "troop_combat_movement": "Live battle movement speed for troops or formations.",
    "personal_combat_movement": "Live battle movement speed for the player hero only.",
    "weapon_handling_speed": "Reload, draw, aiming, swing, attack, or loadout movement handling.",
    "projectile_speed": "Projectile travel speed for arrows, bolts, or thrown weapons.",
    "siege_speed": "Siege engine build, preparation, bombardment, or reload speed.",
}

BANNER_COMPARISON_EFFECTS = {
    "infantry_speed": {
        "effect": "IncreasedTroopMovementSpeed",
        "role": "Speed-minded shock infantry",
        "summary": "Best default banner when the main problem is reaching melee contact under fire.",
    },
    "mounted_speed": {
        "effect": "IncreasedMountMovementSpeed",
        "role": "Mounted mobility",
        "summary": "Mounted version of the speed plan; useful for cavalry or horse archer formations, but much smaller.",
    },
    "ranged_resistance": {
        "effect": "DecreasedRangedAttackDamage",
        "role": "Anti-arrow staying power",
        "summary": "Best defensive rival to the infantry speed banner when the formation must trade under ranged fire.",
    },
    "archer_accuracy": {
        "effect": "DecreasedRangedAccuracyPenalty",
        "role": "Archer-heavy specialist",
        "summary": "Specialist banner for dense archer formations; not a shock-infantry survival tool.",
    },
    "melee_damage": {
        "effect": "IncreasedMeleeDamage",
        "role": "Melee damage breakpoint test",
        "summary": "Strong on paper, but may be wasted when elite troops already overkill common targets.",
    },
}

PACKAGE_METRIC_KEYS = (
    "infantry_movement_percent",
    "ranged_movement_percent",
    "mounted_movement_percent",
    "campaign_speed_percent",
    "melee_damage_percent",
    "ranged_damage_percent",
    "ranged_armor_penetration_percent",
    "ranged_accuracy_penalty_reduction_percent",
    "weapon_inaccuracy_reduction_percent",
    "melee_skill_bonus",
    "ranged_skill_bonus",
    "hit_points",
    "armor",
    "ranged_damage_taken_reduction_percent",
    "shield_damage_reduction_percent",
    "party_size",
    "troop_xp_percent",
)

PACKAGE_DEFINITIONS = {
    "shock_speed": {
        "title": "Shock Speed",
        "banner_key": "infantry_speed",
        "doctrine": "Elite shock infantry reaching melee alive and fast.",
        "weights": {
            "infantry_movement_percent": 3.5,
            "melee_damage_percent": 1.7,
            "melee_skill_bonus": 0.25,
            "hit_points": 0.35,
            "armor": 0.8,
            "ranged_damage_taken_reduction_percent": 1.2,
            "shield_damage_reduction_percent": 0.6,
            "campaign_speed_percent": 1.0,
            "party_size": 0.5,
        },
    },
    "anti_arrow": {
        "title": "Anti-Arrow Durability",
        "banner_key": "ranged_resistance",
        "doctrine": "Infantry that expects to trade under ranged fire before contact.",
        "weights": {
            "hit_points": 1.2,
            "armor": 2.0,
            "ranged_damage_taken_reduction_percent": 4.0,
            "shield_damage_reduction_percent": 1.5,
            "infantry_movement_percent": 1.4,
            "melee_damage_percent": 1.0,
            "melee_skill_bonus": 0.18,
            "campaign_speed_percent": 0.8,
            "party_size": 0.5,
        },
    },
    "archer_accuracy": {
        "title": "Archer Accuracy",
        "banner_key": "archer_accuracy",
        "doctrine": "Ranged-heavy formation where hit rate is the bottleneck.",
        "weights": {
            "weapon_inaccuracy_reduction_percent": 4.0,
            "ranged_accuracy_penalty_reduction_percent": 4.0,
            "ranged_damage_percent": 2.2,
            "ranged_armor_penetration_percent": 2.2,
            "ranged_skill_bonus": 0.3,
            "ranged_movement_percent": 1.0,
            "hit_points": 0.35,
            "campaign_speed_percent": 0.8,
            "party_size": 0.5,
        },
    },
    "melee_damage": {
        "title": "Melee Damage",
        "banner_key": "melee_damage",
        "doctrine": "Shock infantry damage breakpoints and fast cleanup.",
        "weights": {
            "melee_damage_percent": 5.0,
            "melee_skill_bonus": 0.32,
            "infantry_movement_percent": 2.0,
            "hit_points": 0.4,
            "armor": 0.8,
            "ranged_damage_taken_reduction_percent": 0.8,
            "shield_damage_reduction_percent": 0.5,
            "campaign_speed_percent": 0.8,
            "party_size": 0.5,
        },
    },
}

BAND_META = {
    "worth": {
        "title": "Worth It",
        "description": "A strong commander target for the default elite one-party doctrine.",
    },
    "context": {
        "title": "Meh or Contextual",
        "description": "Useful in the right composition or if the attribute/focus is already paid, but not a clean reason to push alone.",
    },
    "skip": {
        "title": "Usually Skip",
        "description": "Too personal, too narrow, too simulation/siege focused, or too small for the focus/attribute cost.",
    },
}

ATTRIBUTE_ORDER = ("Vigor", "Control", "Endurance", "Cunning", "Social", "Intelligence")
PHYSICAL_ATTRIBUTES = {"Vigor", "Control", "Endurance"}
ENDURANCE_ASSISTED_PHYSICAL_BASELINE = 4

INVESTMENT_BAR_CONFIG = {
    "Athletics": {
        "default_stop": 200,
        "stretch_stop": 250,
        "worth": "25-200; 250 if Athletics is already core",
        "context": "225 is mostly a throwing/personal dead band",
        "skip": "275",
        "point_read": (
            "Do not buy extra Endurance only for Strong Arms. Stop at 200 for foot-party speed; "
            "250 is the real stretch because Ignore Pain gives foot troops +5 armor."
        ),
        "details": {
            200: ("worth", "Strong is the clean foot-party campaign speed capstone."),
            225: ("context", "Strong Arms is throwing-skill support, not a shock-infantry reason to push."),
            250: ("worth", "Ignore Pain is the real stretch target: +5 armor to all equipped armor pieces of foot troops."),
            275: ("skip", "Mighty Blow is personal scaling and does not justify high Endurance by itself."),
        },
    },
    "Riding": {
        "default_stop": 100,
        "stretch_stop": 100,
        "worth": "25-100",
        "context": "125+ only for niche logistics, prisoners, or mounted armies",
        "skip": "200+ for infantry commanders",
        "point_read": (
            "For an infantry-heavy party, Sweeping Wind at 100 is the main prize. Past 100, the tree is "
            "ally-battle morale, herding, prisoner handling, mounted-only captain value, mounted armor, or personal mount scaling."
        ),
        "details": {
            100: ("worth", "Sweeping Wind gives campaign speed, which directly supports fight selection."),
            125: ("context", "Relief Force is ally-battle morale; it is not a normal infantry commander target."),
            175: ("context", "Shepherd is only a logistics pickup if herding penalty is a recurring problem."),
            200: ("skip", "Mounted kill morale perks are cavalry/horse-archer value, not infantry doctrine."),
            225: ("context", "Mounted Patrols is prisoner control; useful campaign utility, not infantry combat power."),
            250: ("skip", "Mount and mounted-troop armor are real for cavalry, but not infantry value."),
            275: ("skip", "Way of the Saddle is personal mount scaling."),
        },
    },
    "One Handed": {
        "default_stop": 225,
        "stretch_stop": 250,
        "worth": "25-225; 250 as part of the Vigor package",
        "context": "250 is much better when Polearm is also pushed",
        "skip": "275",
        "point_read": "This is the best Vigor skill to push past 200 for shield infantry. If Vigor is already moving from 4 to 5, Prestige's +15 party size is a worthwhile extension.",
        "details": {
            125: ("worth", "Shield coverage perks are major arrow-survival tools for infantry."),
            200: ("worth", "Fleet of Foot or Steel Core Shields keeps the 200 tier relevant."),
            225: ("worth", "Deadly Purpose is a strong infantry damage stretch; Unwavering Defense is the HP alternative."),
            250: ("worth", "Prestige's +15 party size can justify the Vigor 5 extension when Polearm 250 is also wanted."),
            275: ("skip", "Way of the Sword is personal one-handed scaling."),
        },
    },
    "Two Handed": {
        "default_stop": 175,
        "stretch_stop": 225,
        "worth": "25-175; 175 can be 3 focus at Vigor 5",
        "context": "200 is a small optional bump; 225 is a costly attack-speed stretch",
        "skip": "250 unless personal weapon priority",
        "point_read": (
            "The efficient commander stop is 175. At Vigor 5, 3/4/5 focus reaches 175/200/225-250. "
            "The fourth focus buys only +2% infantry movement and damage or +5 troop HP, and the fifth "
            "focus buys the nice-but-small +2% infantry attack speed at 225. Those are hard to justify "
            "unless Two Handed is also a personal weapon priority or the build has spare focus."
        ),
        "details": {
            100: ("worth", "Shield and mount damage help shock infantry solve common battlefield blockers."),
            175: ("worth", "Hope is +5 party size if this skill is already climbing."),
            200: ("context", "Reckless Charge is only +2% infantry damage and movement speed, while Thick Hides is +5 troop HP; useful, but thin for an extra focus point."),
            225: (
                "context",
                "Blade Master's +2% infantry attack speed is nice, but it costs two extra focus over the efficient 175 stop; Vandal is destructible-object damage.",
            ),
            250: ("skip", "Way of the Great Axe is personal scaling and only starts paying above 250."),
        },
    },
    "Polearm": {
        "default_stop": 175,
        "stretch_stop": 250,
        "worth": "25-175; 250 as part of the Vigor package",
        "context": "200-225 depending on cavalry threat",
        "skip": "275",
        "point_read": "Clean Thrust and Footwork are excellent cheap targets. If Vigor is already moving from 4 to 5, Counterweight's +20 polearm skill makes 250 a worthwhile extension.",
        "details": {
            75: ("worth", "Clean Thrust's +30 Polearm skill is the stronger level-75 troop perk for polearm infantry."),
            100: ("worth", "Footwork adds infantry movement speed, a scarce shock-infantry stat."),
            175: ("worth", "Phalanx offers broad melee-skill and polearm damage value."),
            200: ("context", "Hardy Frontline is useful; Drills is effectively a trap because the daily XP is tiny and can round away."),
            225: ("context", "Sure Footed is strong against charge damage, but not a general lethality breakpoint."),
            250: ("worth", "Counterweight's +20 Polearm skill is enough troop-facing value to pair well with One Handed 250 in a Vigor 5 package."),
            275: ("skip", "Way of the Spear is personal scaling."),
        },
    },
    "Bow": {
        "default_stop": 0,
        "stretch_stop": 175,
        "worth": "None for default shock infantry",
        "context": "100 only if +5 party size is worth two focus; 175+ only for archer-heavy commanders",
        "skip": "100+ for strict shock infantry",
        "point_read": (
            "For shock infantry, Bow is not a default target. At assisted Control 4, Bow 100 still needs "
            "2 focus, and Merry Men's +5 party size is too thin compared with Steward, Medicine, Scouting, "
            "Throwing 125, or a shared Vigor package. The captain bonuses are archer/ranged value, and "
            "Skirmish Phase Master protects ranged troops, not melee infantry."
        ),
        "details": {
            100: ("context", "Merry Men is +5 party size, but it is a poor two-focus deal for strict shock infantry."),
            175: ("context", "Skirmish Phase Master is excellent for ranged troops, but does not protect melee infantry."),
            225: ("context", "Deep Quivers/Horse Master are archer or horse-archer investments, not shock-infantry breakpoints."),
            250: ("skip", "Quick Draw and Ranger's Swiftness are personal/governor value."),
            275: ("skip", "Deadshot is personal scaling."),
        },
    },
    "Crossbow": {
        "default_stop": 0,
        "stretch_stop": 175,
        "worth": "None for shock infantry; only for crossbow formations",
        "context": "175 for crossbow-user projectile mitigation, not infantry resistance",
        "skip": "225+ for shock infantry",
        "point_read": (
            "This tree is the classic wording trap. Counter Fire's description sounds broad, but the curated "
            "damage-model note says it applies to crossbow users, so it does not protect melee infantry."
        ),
        "details": {
            125: ("context", "Fletcher is good crossbow ammunition, not infantry durability."),
            175: ("context", "Counter Fire is crossbow-user projectile mitigation, not universal ranged resistance for infantry."),
            225: ("context", "Hammer Bolts is crossbow damage only."),
            250: ("context", "Picked Shots/Terror are ranged-specialist economy, HP, or morale pressure."),
            275: ("skip", "Mighty Pull is personal scaling."),
        },
    },
    "Throwing": {
        "default_stop": 125,
        "stretch_stop": 225,
        "worth": "50 and 125",
        "context": "225 for morale/renown; 250 for throwing-heavy troops",
        "skip": "275",
        "point_read": (
            "Flexible Fighter and Skirmisher are the broad Control pickups. Assisted Control 4 reaches "
            "Throwing 125 with 2 focus, so the default shock-infantry plan can drop the bought Control "
            "point. After 125, the tree becomes throwing-specialist, morale/renown utility, or "
            "personal/projectile-speed value."
        ),
        "details": {
            50: ("worth", "Flexible Fighter is the cheap mixed-skill troop bonus."),
            125: ("worth", "Skirmisher gives all troops -3% ranged damage taken."),
            225: ("context", "Long Reach is morale/renown utility; Perfect Technique is projectile speed, not troop movement."),
            250: ("context", "Impale/Weak Spot are good only for throwing-heavy formations."),
            275: ("skip", "Unstoppable Force is personal scaling/projectile speed."),
        },
    },
    "Tactics": {
        "default_stop": 75,
        "stretch_stop": 200,
        "worth": "50-75",
        "context": "200 if Cunning/focus is already available",
        "skip": "225+ for live-command doctrine",
        "point_read": "Tactics is almost free up to Horde Leader in a high-Cunning build. Pushing to 200 buys a real live -5% damage taken, but most later rows are simulation-only.",
        "details": {
            75: ("worth", "Horde Leader is +10 party size and can be free with high Cunning."),
            200: ("context", "Elite Reserves has a live -5% damage taken side, but the alternative row is autoresolve."),
            225: ("skip", "Pre Battle Maneuvers is simulation damage."),
            250: ("context", "Gens d'armes is cavalry-vs-infantry damage; Counter Offensive is simulation."),
            275: ("skip", "Tactical Mastery is army/autoresolve scaling."),
        },
    },
    "Scouting": {
        "default_stop": 275,
        "stretch_stop": 275,
        "worth": "25-150 and 275",
        "context": "175-225 are path utility on the way to Uncanny Insight",
        "skip": "250 combat rows",
        "point_read": (
            "Scouting 275 is the engagement-control capstone. Uncanny Insight gives +7.5% party speed the "
            "moment it unlocks at 275, then continues scaling; the 175/225 rows are useful path pickups, not the reason to invest."
        ),
        "details": {
            150: ("worth", "Mounted Scouts is +5 party size on top of the early campaign speed chain."),
            175: ("context", "Foragers/Beast Whisperer are useful path logistics, not the investment thesis."),
            225: ("context", "Keen Sight/Vantage Point are useful path utility, not the investment thesis."),
            250: ("skip", "Rearguard/Vanguard are siege or simulation rows."),
            275: ("worth", "Uncanny Insight is +7.5% party speed immediately at unlock and keeps scaling above 275."),
        },
    },
    "Roguery": {
        "default_stop": 0,
        "stretch_stop": 200,
        "worth": "Bandit builds only",
        "context": "200-250 if already leveling Roguery for loot",
        "skip": "General commander investment",
        "point_read": "Roguery has scattered commander rows, but they are too niche to pull focus away from Scouting/Medicine/Steward.",
        "details": {
            100: ("context", "Prisoner and bandit logistics are useful only for that playstyle."),
            200: ("context", "Carver is small all-formation one-handed damage if Roguery is already high."),
            250: ("context", "Dash and Slash adds small two-handed troop damage, but this is a loot/crime skill first."),
            275: ("skip", "Rogue Extraordinaire is loot scaling."),
        },
    },
    "Leadership": {
        "default_stop": 175,
        "stretch_stop": 250,
        "worth": "75 and 175",
        "context": "250-275 for Social-heavy commanders",
        "skip": "225 as a reason to buy attributes",
        "point_read": "Leadership is excellent, but with low Social the practical stop is 175. Buy Social attributes only if party-size scaling is a deliberate build pillar.",
        "details": {
            175: ("worth", "Uplifting Spirit is +10 party size."),
            225: ("context", "Morale and archer shared XP are useful but not worth Social attributes alone."),
            250: ("worth", "Talent Magnet is another +10 party size if Social is already being pushed."),
            275: ("context", "Ultimate Leader scales party size, but only dedicated Leadership builds should chase it."),
        },
    },
    "Steward": {
        "default_stop": 250,
        "stretch_stop": 275,
        "worth": "200-250",
        "context": "275 if the player is the long-term quartermaster",
        "skip": "None for quartermaster builds; delegate otherwise",
        "point_read": "Steward is not a combat skill, but it scales the elite stack. It is a good place to spend points freed from late physical perks.",
        "details": {
            200: ("worth", "Wages/carrying-capacity rows help keep the one-party army moving and affordable."),
            225: ("context", "Carry capacity is useful, but not a combat breakpoint."),
            250: ("worth", "Master of Planning/Warcraft are strong siege-camp logistics."),
            275: ("context", "Price of Loyalty is attractive for a true quartermaster, but it is a high-skill stretch."),
        },
    },
    "Medicine": {
        "default_stop": 275,
        "stretch_stop": 330,
        "worth": "200 and 275",
        "context": "250 for recovery/XP support",
        "skip": "225 for troop commander value",
        "point_read": "This is one of the best destinations for saved physical points. Minister of Health turns extra Medicine skill into troop HP.",
        "details": {
            200: ("worth", "Physician of People improves low-tier lethal-wound recovery."),
            225: ("context", "Fortitude Tonic helps heroes, not regular troops; Cheat Death is personal."),
            250: ("context", "Battle Hardened/Helping Hands are useful recovery and XP support."),
            275: ("worth", "Minister of Health is the big troop HP scaling breakpoint."),
        },
    },
    "Engineering": {
        "default_stop": 0,
        "stretch_stop": 225,
        "worth": "Delegate by default",
        "context": "150/225 if the player is the active engineer",
        "skip": "250+ for field commander value",
        "point_read": "Engineering is the best hard leak to inherit from origins: dead in setup if delegated, but INT-heavy origins and starting Engineering focus can convert into Engineering 225 Metallurgy for +5 armor. With 3 focus, INT 8 caps at 222 and misses; INT 9 caps at 236 and clears it.",
        "details": {
            150: ("context", "Fire siege engines are useful if the player personally handles engineering."),
            225: ("context", "Metallurgy is +5 armor to all troop armor pieces; consider it when origins already seed Engineering/INT, but treat it as a trap when taken from zero."),
            250: ("skip", "Siege-engine reload/project rows are outside the default field commander doctrine."),
            275: ("skip", "Masterwork is siege-engine scaling."),
        },
    },
    "Smithing": {
        "default_stop": 225,
        "stretch_stop": 225,
        "worth": "225 as an attribute/focus enabler",
        "context": "250-275 for crafting economy",
        "skip": "Combat commander value after enablers",
        "point_read": "Smithing is here for permanent attribute/focus manipulation and money, not live commander perks.",
        "details": {
            225: (
                "worth",
                "Enduring Smith gives +1 Endurance; Fencer Smith instead gives +1 focus to both One Handed and Two Handed, which can save manual focus during a Vigor stretch.",
            ),
            250: ("context", "Crafted-weapon damage is personal/equipment economy, not a troop commander breakpoint."),
            275: ("context", "Legendary Smith is an economy/crafting stretch."),
        },
    },
    "Charm": {
        "default_stop": 50,
        "stretch_stop": 125,
        "worth": "Early QoL only",
        "context": "225+ for diplomacy builds",
        "skip": "Commander combat investment",
        "point_read": "Charm is not where freed physical points usually go unless the campaign plan needs diplomacy/renown.",
        "details": {
            50: ("context", "Early renown/influence perks are quality-of-life picks."),
            225: ("context", "Public Speaker is strong renown, but it is campaign economy rather than troop combat."),
            250: ("context", "Camaraderie's companion limit is useful if the clan plan needs it."),
            275: ("context", "Immortal Charm is influence income for Social-heavy campaigns."),
        },
    },
    "Trade": {
        "default_stop": 50,
        "stretch_stop": 300,
        "worth": "50 for QoL",
        "context": "300 only for settlement trading",
        "skip": "Commander combat investment",
        "point_read": "One focus for price marking is great. Everything Has a Price is a separate campaign goal, not a commander perk target.",
        "details": {
            50: ("worth", "Price marking is one of the best one-focus quality-of-life upgrades."),
            225: ("context", "Late trade perks are economy or caravan support."),
            275: ("context", "Man of Means/Trickle Down are campaign-economy perks."),
            300: ("context", "Everything Has a Price is transformative only if settlement barter is a campaign goal."),
        },
    },
}


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def row_effect(row: dict[str, Any]) -> str:
    return str(row.get("game", {}).get("effect", ""))


def row_effect_lower(row: dict[str, Any]) -> str:
    return row_effect(row).lower()


def row_role(row: dict[str, Any]) -> str:
    return str(row.get("game", {}).get("role", ""))


def row_type(row: dict[str, Any]) -> str:
    return str(row.get("classification", {}).get("perk_type", ""))


def row_subtype(row: dict[str, Any]) -> str:
    return str(row.get("classification", {}).get("perk_subtype", ""))


def row_triggers(row: dict[str, Any]) -> set[str]:
    return {str(item) for item in row.get("classification", {}).get("trigger_conditions", [])}


def row_tags(row: dict[str, Any]) -> set[str]:
    return {str(item) for item in row.get("classification", {}).get("effect_tags", [])}


def matches(text: str, pattern: str) -> bool:
    return bool(re.search(pattern, text))


def is_siege_text(text: str) -> bool:
    return matches(text, r"siege|ballista|mangonel|trebuchet|bombardment|ram|siege camp|engine")


def classify_speed_kind(row: dict[str, Any]) -> str | None:
    text = row_effect_lower(row)
    subtype = row_subtype(row)
    role = row_role(row)

    has_speed_text = "speed" in text or "faster" in text or subtype in {
        "party speed",
        "movement speed",
        "projectile speed",
        "reload speed",
        "attack speed",
    }
    if not has_speed_text:
        return None

    if is_siege_text(text) and matches(text, r"speed|faster|reload|build|preparation"):
        return "siege_speed"

    if subtype == "projectile speed" or matches(text, r"travel speed to .*weapons?|throwing weapons"):
        return "projectile_speed"

    if subtype == "party speed" or matches(
        text,
        r"\bparty speed\b|travel speed (?:during|on|when|while|from|penalty)|"
        r"speed penalty from (?:forests?|wounded|herding|overburdened)|"
        r"movement speed to parties called",
    ):
        return "campaign_party_speed"

    if matches(
        text,
        r"reload speed|draw speed|aiming speed|attack speed|swing speed|weapon handling|ready speed|"
        r"movement speed penalty while reloading|wielding shields",
    ):
        return "weapon_handling_speed"

    if subtype == "movement speed" or "movement speed" in text or "combat movement" in text:
        if role == "captain" or matches(
            text,
            r"troops?|infantry|archers?|ranged|mounted|cavalry|formation|tier \d|foot",
        ):
            return "troop_combat_movement"
        return "personal_combat_movement"

    return None


def troop_classes(row: dict[str, Any]) -> list[str]:
    text = f"{row_effect_lower(row)} {row.get('game', {}).get('troop_usage', '')}".lower()
    classes: set[str] = set()
    restricted_scope = matches(
        text,
        r"infantry|foot troops?|footmen|on_foot|melee troops|archers?|ranged troops?|bow_user|"
        r"crossbow|thrown_user|throwing|cavalry|mounted troops?|mounted melee|horse archers?",
    )

    if "all troops" in text or (
        not restricted_scope
        and matches(
            text,
            r"\bto troops\b|\btroops in your formation\b|\btroops in your party\b|\btroops under your formation\b",
        )
    ):
        classes.add("all_troops")
    if matches(text, r"infantry|foot troops?|footmen|on_foot|melee troops"):
        classes.add("infantry_or_foot")
    if "melee troops" in text:
        classes.add("melee")
    if matches(text, r"archers?|bow_user"):
        classes.update({"ranged", "archers"})
    if matches(text, r"ranged troops?|crossbow|bow|thrown_user|throwing weapons"):
        classes.add("ranged")
    if matches(text, r"crossbow"):
        classes.add("crossbow")
    if matches(text, r"throwing|thrown_user"):
        classes.add("throwing")
    if matches(text, r"cavalry|mounted troops?|mounted melee|mounts? of troops"):
        classes.update({"mounted", "cavalry"})
    if matches(text, r"horse archers?|mounted archers"):
        classes.update({"mounted", "ranged", "horse_archers"})
    if "garrison" in text:
        classes.add("garrison")
    if is_siege_text(text):
        classes.add("siege")

    return sorted(classes)


def troop_facing(row: dict[str, Any], classes: list[str]) -> bool:
    if classes:
        return True
    text = row_effect_lower(row)
    return row_role(row) == "captain" or matches(
        text,
        r"troops?|formation|infantry|archers?|ranged|mounted|cavalry|party|garrison|units?",
    )


def default_force_fit(row: dict[str, Any], classes: list[str], speed_kind: str | None) -> str:
    role = row_role(row)
    text = row_effect_lower(row)
    if role == "personal" and not matches(text, r"\btroops?\b|infantry|formation|party"):
        return "personal only"
    if role == "governor" or "governed settlement" in row_triggers(row):
        return "governor/settlement only"
    if role == "army leader":
        return "army-only support"
    if "simulation" in row_triggers(row):
        return "simulation only"
    if "all_troops" in classes:
        return "all troops"
    if "infantry_or_foot" in classes or "melee" in classes:
        return "shock-infantry fit"
    if speed_kind == "campaign_party_speed":
        return "one-party mobility"
    if "ranged" in classes:
        return "ranged-specific"
    if "mounted" in classes or "cavalry" in classes:
        return "mounted-specific"
    if role == "personal":
        return "personal only"
    if row_subtype(row) == "party size":
        return "one-party scaling"
    return "situational"


CORE_SUBTYPES = {
    "damage increase",
    "skill bonus",
    "attack speed",
    "reload speed",
    "ranged accuracy",
    "armor penetration",
    "shield damage",
    "morale damage",
    "ammo capacity",
}

STAYING_SUBTYPES = {
    "hit points",
    "armor",
    "armor increase",
    "damage resistance",
    "survival chance",
    "shield protection",
    "shield durability",
    "stagger resistance",
    "morale",
}

SCALING_SUBTYPES = {
    "party size",
    "wages",
    "recruitment",
    "prisoner recruitment",
    "food",
    "carrying capacity",
    "morale",
    "troop xp",
}


def doctrine_category(row: dict[str, Any], speed_kind: str | None, classes: list[str]) -> str:
    role = row_role(row)
    subtype = row_subtype(row)
    ptype = row_type(row)
    text = row_effect_lower(row)
    triggers = row_triggers(row)

    if role == "governor" or "governed settlement" in triggers or "simulation" in triggers:
        return "low_priority_misleading"
    if speed_kind in {"projectile_speed", "siege_speed", "personal_combat_movement", "weapon_handling_speed"}:
        return "low_priority_misleading"
    if role == "personal" and not classes:
        return "low_priority_misleading"
    if speed_kind == "troop_combat_movement":
        return "core_troop_lethality"
    if ptype == "troop combat" and subtype in STAYING_SUBTYPES:
        return "combat_staying_power"
    if ptype == "troop combat" and subtype in CORE_SUBTYPES:
        return "core_troop_lethality"
    if ptype == "troop combat" and matches(text, r"damage|skill|accuracy|armor penetration|shield"):
        return "core_troop_lethality"
    if role in {"surgeon", "party leader"} and ptype in {"death avoidance", "regen bonus"} and matches(
        text, r"troops?|wounded|recovery|casualt"
    ):
        return "combat_staying_power"
    if subtype in STAYING_SUBTYPES and troop_facing(row, classes):
        return "combat_staying_power"
    if speed_kind == "campaign_party_speed":
        return "engagement_control"
    if subtype == "party size" or "party size" in text:
        return "party_scaling"
    if role in COMMANDER_ROLES and (subtype in SCALING_SUBTYPES or matches(text, r"food|wage|recruit|prisoner|carry|morale")):
        return "party_scaling"
    return "low_priority_misleading"


def value_rating(row: dict[str, Any], category: str, speed_kind: str | None, fit: str) -> str:
    subtype = row_subtype(row)
    role = row_role(row)
    text = row_effect_lower(row)
    skill = str(row.get("skill", ""))
    level = int(row.get("level", 0) or 0)

    if category == "low_priority_misleading":
        return "low"
    if skill == "Riding" and level > 100:
        return "medium"
    if category == "core_troop_lethality":
        if speed_kind == "troop_combat_movement" and fit in {"all troops", "shock-infantry fit"}:
            return "high"
        if fit in {"all troops", "shock-infantry fit"}:
            return "high"
        return "medium"
    if category == "combat_staying_power":
        if subtype in {"damage resistance", "armor", "armor increase", "shield protection"}:
            return "high"
        if subtype == "hit points" and "for every skill point above" in text:
            return "high"
        return "medium"
    if category == "engagement_control":
        if role in {"party leader", "scout", "surgeon"} and not matches(text, r"army|raid"):
            return "high"
        return "medium"
    if category == "party_scaling":
        if subtype == "party size" or "party size" in text:
            return "high"
        return "medium"
    return "low"


def comparison_note(
    row: dict[str, Any],
    speed_kind: str | None,
    alternatives_by_perk: dict[str, list[dict[str, Any]]],
) -> str:
    alt_id = str(row.get("alternative_perk_string_id", ""))
    if not alt_id:
        return ""

    alternatives = alternatives_by_perk.get(alt_id, [])
    alt_has_troop_hp = any(row_subtype(alt) == "hit points" and troop_facing(alt, troop_classes(alt)) for alt in alternatives)
    alt_has_troop_speed = any(classify_speed_kind(alt) == "troop_combat_movement" for alt in alternatives)

    if speed_kind == "troop_combat_movement" and alt_has_troop_hp:
        return (
            "Speed competes with a troop HP alternative here. For shock infantry, speed can be the scarcer "
            "multiplier because Medicine and resistance stacks already add a lot of survivability."
        )
    if row_subtype(row) == "hit points" and troop_facing(row, troop_classes(row)) and alt_has_troop_speed:
        return (
            "HP competes with a troop speed alternative here. Take HP when the formation already reaches contact "
            "reliably; otherwise speed may prevent more arrow exposure than the flat HP absorbs."
        )
    return ""


def record_notes(
    row: dict[str, Any],
    category: str,
    speed_kind: str | None,
    fit: str,
    comparison: str,
) -> list[str]:
    notes: list[str] = []
    subtype = row_subtype(row)
    role = row_role(row)

    if speed_kind == "troop_combat_movement":
        if fit in {"all troops", "shock-infantry fit"}:
            notes.append(
                "Shock-infantry multiplier: closes under fire faster, keeps melee pressure, and improves formation responsiveness."
            )
        else:
            notes.append(
                "Troop movement speed for this troop class; useful tactically, but not an infantry-wide mobility buff."
            )
    elif speed_kind == "campaign_party_speed":
        notes.append("Engagement-control perk: helps choose, refuse, or chase fights on the campaign map.")
    elif speed_kind == "projectile_speed":
        notes.append("Projectile travel speed, not party mobility or troop foot speed.")
    elif speed_kind == "weapon_handling_speed":
        notes.append("Weapon handling or personal reload/loadout movement; do not count as party mobility.")
    elif speed_kind == "siege_speed":
        notes.append("Siege-speed effect; useful in sieges but outside the default one-party shock-infantry doctrine.")

    if subtype == "hit points" and category == "combat_staying_power":
        notes.append("HP is useful, but it is easier to stack through Medicine than troop combat speed is.")
    if subtype == "party size":
        notes.append("Party size is always welcome, but larger parties are naturally slower, so it ranks after combat power and mobility.")
    if role == "army leader":
        notes.append("Army-leader effect; weaker fit for a single-party commander.")
    if "simulation" in row_triggers(row):
        notes.append("Simulation/autoresolve row, not live tactical combat.")
    if str(row.get("skill", "")) == "Riding" and int(row.get("level", 0) or 0) > 100:
        notes.append("Post-100 Riding is niche for infantry: logistics, prisoners, mounted-only value, or personal mount scaling.")
    if str(row.get("perk_string_id", "")) == "CrossbowCounterFire":
        notes.append("Hidden current-weapon gate: benefits crossbow users, not melee infantry or bow archers.")
    if fit in {"ranged-specific", "mounted-specific"}:
        notes.append(f"{fit}; do not assume it buffs infantry.")
    if comparison:
        notes.append(comparison)

    return notes


def commander_candidate(row: dict[str, Any]) -> bool:
    role = row_role(row)
    subtype = row_subtype(row)
    ptype = row_type(row)
    text = row_effect_lower(row)
    speed_kind = classify_speed_kind(row)
    classes = troop_classes(row)

    if role in COMMANDER_ROLES and (
        speed_kind
        or ptype in {"troop combat", "party management", "troop management"}
        or (
            ptype in {"death avoidance", "regen bonus"}
            and matches(text, r"troops?|wounded|recovery|casualt")
        )
        or subtype in CORE_SUBTYPES
        or subtype in STAYING_SUBTYPES
        or subtype in SCALING_SUBTYPES
        or matches(text, r"party size|travel speed|party speed|recruit|wage|food|prisoner")
    ):
        return True

    if speed_kind in {
        "troop_combat_movement",
        "campaign_party_speed",
        "weapon_handling_speed",
        "projectile_speed",
        "siege_speed",
        "personal_combat_movement",
    }:
        return True

    if matches(text, r"damage bonus from speed|movement speed"):
        return True

    if role == "personal" and classes and (
        ptype == "troop combat"
        or subtype in CORE_SUBTYPES
        or subtype in STAYING_SUBTYPES
        or subtype in SCALING_SUBTYPES
    ):
        return True

    return False


def compact_record(row: dict[str, Any], alternatives_by_perk: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    speed_kind = classify_speed_kind(row)
    classes = troop_classes(row)
    fit = default_force_fit(row, classes, speed_kind)
    category = doctrine_category(row, speed_kind, classes)
    rating = value_rating(row, category, speed_kind, fit)
    comparison = comparison_note(row, speed_kind, alternatives_by_perk)
    game = row.get("game", {})
    classification = row.get("classification", {})

    return {
        "id": row.get("id", f"{row.get('perk_string_id', '')}|{row.get('effect_slot', '')}"),
        "skill": row.get("skill", ""),
        "level": row.get("level", 0),
        "perk": row.get("perk", ""),
        "perk_string_id": row.get("perk_string_id", ""),
        "effect_slot": row.get("effect_slot", ""),
        "alternative_perk_string_id": row.get("alternative_perk_string_id", ""),
        "role": game.get("role", ""),
        "bonus": game.get("bonus", 0),
        "increment_type": game.get("increment_type", ""),
        "troop_usage": game.get("troop_usage", ""),
        "perk_type": classification.get("perk_type", ""),
        "perk_subtype": classification.get("perk_subtype", ""),
        "trigger_conditions": classification.get("trigger_conditions", []),
        "effect_tags": classification.get("effect_tags", []),
        "effect": game.get("effect", ""),
        "speed_kind": speed_kind,
        "troop_classes": classes,
        "default_force_fit": fit,
        "doctrine_category": category,
        "value_rating": rating,
        "comparison_note": comparison,
        "notes": record_notes(row, category, speed_kind, fit, comparison),
    }


def record_sort_key(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        CATEGORY_ORDER.index(record["doctrine_category"]),
        RATING_ORDER.get(record["value_rating"], 9),
        0 if record["default_force_fit"] in {"all troops", "shock-infantry fit", "one-party mobility"} else 1,
        int(record.get("level", 0)),
        str(record.get("skill", "")),
        str(record.get("perk", "")),
        str(record.get("effect_slot", "")),
    )


def build_commander_records(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    alternatives_by_perk: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        alternatives_by_perk[str(row.get("perk_string_id", ""))].append(row)

    records = [compact_record(row, alternatives_by_perk) for row in rows if commander_candidate(row)]
    return sorted(records, key=record_sort_key)


def investment_split_for_level(level: int, baseline_attribute: int = MIN_ATTRIBUTE) -> dict[str, Any]:
    baseline_attribute = max(MIN_ATTRIBUTE, min(MAX_ATTRIBUTE, baseline_attribute))
    if level <= 0:
        return {
            "baseline_attribute": baseline_attribute,
            "attribute": baseline_attribute,
            "focus": 0,
            "limit": skill_limit(baseline_attribute, 0),
            "peak_learning_range": peak_learning_range(baseline_attribute, 0),
            "purchased_attributes": 0,
            "focus_points": 0,
            "allocation_points": 0,
            "weighted_allocation_cost": 0,
            "level_gate_cost": 0,
            "category": "none",
            "pressure": "no investment",
        }

    candidates: list[dict[str, Any]] = []
    for attribute in range(baseline_attribute, MAX_ATTRIBUTE + 1):
        for focus in range(0, MAX_FOCUS + 1):
            limit = skill_limit(attribute, focus)
            if limit < level:
                continue
            purchased_attributes = max(0, attribute - baseline_attribute)
            focus_points = focus
            weighted = focus_points + purchased_attributes * 4
            candidates.append(
                {
                    "baseline_attribute": baseline_attribute,
                    "attribute": attribute,
                    "focus": focus,
                    "limit": limit,
                    "peak_learning_range": peak_learning_range(attribute, focus),
                    "purchased_attributes": purchased_attributes,
                    "focus_points": focus_points,
                    "allocation_points": purchased_attributes + focus_points,
                    "weighted_allocation_cost": weighted,
                    "level_gate_cost": max(focus_points, purchased_attributes * 4),
                    "category": "low" if purchased_attributes == 0 else "medium" if attribute <= 5 else "high",
                    "pressure": (
                        "assisted baseline"
                        if purchased_attributes == 0 and baseline_attribute > MIN_ATTRIBUTE
                        else "focus-only"
                        if purchased_attributes == 0
                        else "attribute-gated"
                        if attribute <= 5
                        else "specialist"
                    ),
                }
            )

    if not candidates:
        raise ValueError(f"Cannot reach skill level {level} with legal attributes/focus.")
    return sorted(
        candidates,
        key=lambda item: (
            item["weighted_allocation_cost"],
            item["allocation_points"],
            item["level_gate_cost"],
            item["purchased_attributes"],
            item["focus_points"],
            item["attribute"],
        ),
    )[0]


def format_split_from_dict(split: dict[str, Any]) -> str:
    return f"{split['attribute']} attr / {split['focus']} focus"


def format_cost_from_dict(split: dict[str, Any]) -> str:
    return (
        f"{split['purchased_attributes']} attr + {split['focus_points']} focus "
        f"(weighted {split['weighted_allocation_cost']})"
    )


def assisted_baseline_for_attribute(attribute: str) -> int:
    if attribute in PHYSICAL_ATTRIBUTES:
        return ENDURANCE_ASSISTED_PHYSICAL_BASELINE
    return MIN_ATTRIBUTE


def record_level_summary(records: list[dict[str, Any]]) -> str:
    if not records:
        return ""
    useful = [record for record in records if record.get("doctrine_category") != "low_priority_misleading"]
    source = useful or records
    parts = []
    for record in sorted(source, key=lambda item: (RATING_ORDER.get(item.get("value_rating", ""), 9), item["perk"], item["effect_slot"])):
        parts.append(f"{record['perk']}: {record['effect']}")
    return " / ".join(parts[:4])


def build_investment_bars(rows: list[dict[str, Any]], records: list[dict[str, Any]]) -> dict[str, Any]:
    attribute_by_skill = {}
    levels_by_skill: dict[str, set[int]] = defaultdict(set)
    for row in rows:
        skill = str(row.get("skill", ""))
        if not skill:
            continue
        attribute_by_skill.setdefault(skill, str(row.get("attribute", "")))
        levels_by_skill[skill].add(int(row.get("level", 0) or 0))

    records_by_skill_level: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        records_by_skill_level[(str(record["skill"]), int(record["level"]))].append(record)

    skill_rows = []
    detail_rows = []
    for skill, config in sorted(
        INVESTMENT_BAR_CONFIG.items(),
        key=lambda item: (
            ATTRIBUTE_ORDER.index(
                attribute_by_skill.get(item[0], "Intelligence")
                if attribute_by_skill.get(item[0], "Intelligence") in ATTRIBUTE_ORDER
                else "Intelligence"
            ),
            item[0],
        ),
    ):
        default_stop = int(config["default_stop"])
        stretch_stop = int(config["stretch_stop"])
        attribute = attribute_by_skill.get(skill, "")
        is_physical = attribute in PHYSICAL_ATTRIBUTES
        assisted_baseline = assisted_baseline_for_attribute(attribute)
        default_cost = investment_split_for_level(default_stop)
        stretch_cost = investment_split_for_level(stretch_stop)
        assisted_default_cost = (
            investment_split_for_level(default_stop, assisted_baseline) if is_physical else None
        )
        assisted_stretch_cost = (
            investment_split_for_level(stretch_stop, assisted_baseline) if is_physical else None
        )
        detail_config: dict[int, tuple[str, str]] = config["details"]  # type: ignore[assignment]
        skill_rows.append(
            {
                "skill": skill,
                "attribute": attribute,
                "physical_skill": is_physical,
                "assisted_baseline_attribute": assisted_baseline if is_physical else None,
                "default_stop": default_stop,
                "default_cost": default_cost,
                "assisted_default_cost": assisted_default_cost,
                "stretch_stop": stretch_stop,
                "stretch_cost": stretch_cost,
                "assisted_stretch_cost": assisted_stretch_cost,
                "worth": config["worth"],
                "context": config["context"],
                "skip": config["skip"],
                "point_read": config["point_read"],
            }
        )
        for level, (band, note) in sorted(detail_config.items()):
            split = investment_split_for_level(level)
            assisted_split = investment_split_for_level(level, assisted_baseline) if is_physical else None
            detail_rows.append(
                {
                    "skill": skill,
                    "attribute": attribute,
                    "physical_skill": is_physical,
                    "level": level,
                    "band": band,
                    "band_title": BAND_META[band]["title"],
                    "cost": split,
                    "assisted_cost": assisted_split,
                    "extracted_rows": [
                        {
                            "id": record["id"],
                            "perk": record["perk"],
                            "role": record["role"],
                            "category": record["doctrine_category"],
                            "rating": record["value_rating"],
                            "fit": record["default_force_fit"],
                            "effect": record["effect"],
                        }
                        for record in records_by_skill_level.get((skill, level), [])
                    ],
                    "extracted_summary": record_level_summary(records_by_skill_level.get((skill, level), [])),
                    "note": note,
                }
            )

    physical_cut_summary = [
        {
            "skill": "Control baseline",
            "read": "Drop the bought Control point for the default shock-infantry plan. Controlled Smith plus Steady can make effective Control 4, where Throwing 125 needs 2 focus. Bow 100 also needs 2 focus here, but +5 party size is too thin for strict infantry.",
        },
        {
            "skill": "Crossbow",
            "read": "Cut entirely for shock infantry unless the formation is actually crossbow-focused. Counter Fire is crossbow-user mitigation, not universal infantry ranged resistance.",
        },
        {
            "skill": "Bow",
            "read": "Cut for strict shock infantry. Bow 100's Merry Men is only +5 party size for two focus under the assisted Control plan; Bow 175+ is ranged composition value, not infantry protection.",
        },
        {
            "skill": "Throwing",
            "read": "Stop at 125 for Flexible Fighter plus Skirmisher; later tiers are morale/renown utility, projectile speed, or throwing-specialist.",
        },
        {
            "skill": "Scouting",
            "read": "Push to 275 as a core engagement-control target. Uncanny Insight gives +7.5% party speed immediately at unlock, and 175/225 are just path utility.",
        },
        {
            "skill": "Two Handed",
            "read": "Stop at 175 by default. With Vigor 5, 200 costs one extra focus for only +2% infantry speed/damage or +5 HP, while 225 costs two extra focus for +2% infantry attack speed.",
        },
        {
            "skill": "Vigor hyper-stretch",
            "read": "Smithing 225 Fencer Smith stacks with the +2 Vigor package and can save one manual focus in One Handed plus one in Two Handed while those skills are being trained; it does not help Polearm and it competes with Enduring Smith's +1 Endurance.",
        },
        {
            "skill": "Polearm",
            "read": "Stop at 175 by default, but Polearm 250 becomes worthwhile in the Vigor 5 package because +20 Polearm skill pairs with One Handed 250's party size.",
        },
        {
            "skill": "Riding",
            "read": "Stop at 100 for infantry-heavy parties. Past that is niche logistics, prisoner utility, mounted-only captain value, or personal mount scaling.",
        },
    ]

    return {
        "assumptions": {
            "baseline_attribute": MIN_ATTRIBUTE,
            "endurance_assisted_physical_baseline": ENDURANCE_ASSISTED_PHYSICAL_BASELINE,
            "max_focus": MAX_FOCUS,
            "cost_formula": "focus_points + purchased_attribute_points * 4",
            "focus_only_limit": skill_limit(MIN_ATTRIBUTE, MAX_FOCUS),
            "assisted_physical_focus_only_limit": skill_limit(ENDURANCE_ASSISTED_PHYSICAL_BASELINE, MAX_FOCUS),
            "default_lens": "Elite shock-infantry-heavy one-party commander.",
            "assisted_physical_note": (
                "Endurance-skill attribute perks can raise one chosen physical attribute to 4 without purchased "
                "attribute points: Vigor via Smithing 150 plus Athletics 200, Control via the matching alternatives, "
                "or Endurance via Athletics 175 plus Smithing 225. Treat the assisted cost column as a respec state "
                "for the skill currently being trained, not as Vigor, Control, and Endurance all being raised at once. "
                "The build can take turns: Control 4 for Throwing 125, then Vigor 4/5 plus Fencer Smith while training "
                "One-Handed and Two-Handed. Enabler perks still have to be reached before the assisted baseline exists."
            ),
            "vigor_hyper_stretch_note": (
                "At Vigor 5, Two Handed reaches levels 175/200/225/250 with 3/4/5/5 focus. Smithing 225 "
                "Fencer Smith gives +1 focus to One Handed and +1 focus to Two Handed, so it can function as a "
                "temporary training/refund tool for the Vigor package if the build can give up Enduring Smith while "
                "those weapon skills are being pushed. The granted focus is not generic and does not apply to Polearm."
            ),
            "control_baseline_note": (
                "Default shock-infantry Control can be planned as 2 purchased attribute, 4 effective attribute "
                "after Controlled Smith plus Steady. At Control 4, 2 focus reaches level 126, enough for "
                "Throwing 125 Skirmisher. Bow 100 also fits at 2 focus, but Merry Men's +5 party size is "
                "too thin for default shock infantry; treat it as a ranged-side or luxury choice."
            ),
            "non_monotonic_note": (
                "Some bars are not strictly monotonic: a dead 225 tier can be followed by a strong 250 perk. "
                "The report calls those out explicitly instead of pretending every skill has one clean cutoff."
            ),
        },
        "band_meta": BAND_META,
        "physical_cut_summary": physical_cut_summary,
        "skills": skill_rows,
        "details": detail_rows,
    }


def format_percent_from_factor(value: Any, force_plus: bool = False) -> str:
    try:
        percent = float(value) * 100.0
    except (TypeError, ValueError):
        return str(value)

    if abs(percent - round(percent)) < 1e-6:
        text = f"{round(percent):.0f}%"
    else:
        text = f"{percent:.4f}".rstrip("0").rstrip(".") + "%"
    if force_plus and not text.startswith("-"):
        return "+" + text
    return text


def add_factor_percent(record: dict[str, Any]) -> float:
    if record.get("increment_type") != "add_factor":
        return 0.0
    try:
        return float(record.get("bonus", 0)) * 100.0
    except (TypeError, ValueError):
        return 0.0


def add_value(record: dict[str, Any]) -> float:
    if record.get("increment_type") != "add":
        return 0.0
    try:
        return float(record.get("bonus", 0))
    except (TypeError, ValueError):
        return 0.0


def rounded(value: float, digits: int = 4) -> float:
    return round(value, digits)


def record_choice(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record.get("id", ""),
        "skill": record.get("skill", ""),
        "level": record.get("level", 0),
        "perk": record.get("perk", ""),
        "perk_string_id": record.get("perk_string_id", ""),
        "effect_slot": record.get("effect_slot", ""),
        "value": format_bonus(record),
        "bonus": record.get("bonus", 0),
        "increment_type": record.get("increment_type", ""),
        "perk_subtype": record.get("perk_subtype", ""),
        "doctrine_category": record.get("doctrine_category", ""),
        "fit": record.get("default_force_fit", ""),
        "speed_kind": record.get("speed_kind"),
        "effect": record.get("effect", ""),
    }


def useful_alternative_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ignored_fits = {"personal only", "governor/settlement only", "simulation only"}
    useful = [record for record in records if record.get("default_force_fit") not in ignored_fits]
    return useful or records


def banner_choice(banner_payload: dict[str, Any] | None, key: str) -> dict[str, Any]:
    meta = BANNER_COMPARISON_EFFECTS[key]
    choice = {
        "key": key,
        "effect": meta["effect"],
        "role": meta["role"],
        "summary": meta["summary"],
        "available": False,
    }
    if not banner_payload:
        return choice

    groups = {str(group.get("effect", "")): group for group in banner_payload.get("groups", [])}
    group = groups.get(meta["effect"])
    if not group:
        return choice

    tiers = sorted(group.get("tiers", []), key=lambda tier: int(tier.get("level", 0)))
    if not tiers:
        return choice
    top_tier = tiers[-1]
    top_level = int(top_tier.get("level", 0))
    top_items = [
        item
        for item in banner_payload.get("items", [])
        if item.get("effect") == meta["effect"] and int(item.get("banner_level", 0)) == top_level
    ]
    choice.update(
        {
            "available": True,
            "effect_name": group.get("effect_name", meta["effect"]),
            "tier": top_level,
            "bonus": top_tier.get("bonus", 0),
            "bonus_percent": rounded(float(top_tier.get("bonus", 0)) * 100.0),
            "display_bonus": top_tier.get("display_bonus", format_percent_from_factor(top_tier.get("bonus", 0))),
            "items": [str(item.get("name", item.get("id", ""))) for item in top_items],
        }
    )
    return choice


def banner_bonus_percent(choice: dict[str, Any]) -> float:
    if not choice.get("available"):
        return 0.0
    try:
        return float(choice.get("bonus", 0)) * 100.0
    except (TypeError, ValueError):
        return 0.0


def empty_metrics() -> dict[str, float]:
    return {key: 0.0 for key in PACKAGE_METRIC_KEYS}


def merge_metrics(target: dict[str, float], source: dict[str, float]) -> None:
    for key in PACKAGE_METRIC_KEYS:
        target[key] = target.get(key, 0.0) + source.get(key, 0.0)


def clean_metrics(metrics: dict[str, float]) -> dict[str, float]:
    return {key: rounded(value, 3) for key, value in metrics.items() if abs(value) > 1e-9}


def record_scope(record: dict[str, Any]) -> str:
    classes = set(record.get("troop_classes", []))
    fit = str(record.get("default_force_fit", ""))
    if "ranged" in classes and "infantry_or_foot" not in classes and "all_troops" not in classes:
        return "ranged"
    if "mounted" in classes and "all_troops" not in classes:
        return "mounted"
    if fit in {"all troops", "shock-infantry fit"} or classes & {"all_troops", "infantry_or_foot", "melee"}:
        return "infantry"
    return "other"


def record_package_metrics(record: dict[str, Any]) -> dict[str, float]:
    metrics = empty_metrics()
    subtype = str(record.get("perk_subtype", ""))
    text = str(record.get("effect", "")).lower()
    scope = record_scope(record)
    factor = add_factor_percent(record)
    value = add_value(record)

    if record.get("speed_kind") == "troop_combat_movement":
        if scope == "ranged":
            metrics["ranged_movement_percent"] += factor
        elif scope == "mounted":
            metrics["mounted_movement_percent"] += factor
        elif scope == "infantry":
            metrics["infantry_movement_percent"] += factor
    elif record.get("speed_kind") == "campaign_party_speed":
        metrics["campaign_speed_percent"] += abs(factor)

    if subtype == "hit points" and "mount" not in text:
        metrics["hit_points"] += value
    elif subtype in {"armor", "armor increase"}:
        metrics["armor"] += value
    elif subtype == "party size":
        metrics["party_size"] += value
    elif subtype == "troop xp":
        metrics["troop_xp_percent"] += factor or value

    if subtype in {"damage resistance", "projectile protection"} or matches(text, r"damage taken from projectiles|ranged .*damage taken|damage from projectiles"):
        metrics["ranged_damage_taken_reduction_percent"] += abs(factor)
    if subtype in {"shield protection", "shield durability"} or matches(text, r"damage to shields?|shield damage"):
        if "damage" in text:
            metrics["shield_damage_reduction_percent"] += abs(factor)

    if subtype in {"damage increase", "melee", "shield damage", "armor penetration"}:
        if matches(text, r"bow|crossbow|ranged|projectile|arrow"):
            if subtype == "armor penetration":
                metrics["ranged_armor_penetration_percent"] += abs(factor)
            else:
                metrics["ranged_damage_percent"] += factor
        elif scope != "mounted":
            metrics["melee_damage_percent"] += factor
    if "damage and movement speed" in text and scope == "infantry" and subtype != "damage increase":
        metrics["melee_damage_percent"] += factor

    if subtype == "skill bonus":
        if matches(text, r"bow|crossbow|ranged|archers?"):
            metrics["ranged_skill_bonus"] += value
        elif matches(text, r"one handed|two handed|polearm|melee|infantry|troops"):
            metrics["melee_skill_bonus"] += value

    if subtype == "ranged accuracy" and factor < 0:
        metrics["ranged_accuracy_penalty_reduction_percent"] += abs(factor)

    return metrics


def banner_package_metrics(choice: dict[str, Any]) -> dict[str, float]:
    metrics = empty_metrics()
    if not choice.get("available"):
        return metrics
    percent = banner_bonus_percent(choice)
    effect = str(choice.get("effect", ""))
    if effect == "IncreasedTroopMovementSpeed":
        metrics["infantry_movement_percent"] += max(0.0, percent)
    elif effect == "IncreasedMountMovementSpeed":
        metrics["mounted_movement_percent"] += max(0.0, percent)
    elif effect == "DecreasedRangedAttackDamage":
        metrics["ranged_damage_taken_reduction_percent"] += abs(min(0.0, percent))
    elif effect == "DecreasedRangedAccuracyPenalty":
        metrics["weapon_inaccuracy_reduction_percent"] += abs(min(0.0, percent))
    elif effect == "IncreasedMeleeDamage":
        metrics["melee_damage_percent"] += max(0.0, percent)
    return metrics


def metrics_for_records(records: list[dict[str, Any]]) -> dict[str, float]:
    totals = empty_metrics()
    for record in records:
        merge_metrics(totals, record_package_metrics(record))
    return totals


def score_metrics(metrics: dict[str, float], weights: dict[str, float]) -> float:
    return sum(metrics.get(key, 0.0) * weight for key, weight in weights.items())


def score_records(records: list[dict[str, Any]], weights: dict[str, float]) -> float:
    return score_metrics(metrics_for_records(records), weights)


def choice_label(records: list[dict[str, Any]]) -> str:
    if not records:
        return ""
    first = records[0]
    return f"{first.get('skill', '')} {first.get('level', '')} - {first.get('perk', '')}"


def build_alternative_pair_sides(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records_by_perk: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        records_by_perk[str(record.get("perk_string_id", ""))].append(record)

    pairs = []
    seen: set[tuple[str, str]] = set()
    for record in records:
        alt_id = str(record.get("alternative_perk_string_id", ""))
        perk_id = str(record.get("perk_string_id", ""))
        if not alt_id or alt_id not in records_by_perk or not perk_id:
            continue
        pair_key = tuple(sorted([perk_id, alt_id]))
        if pair_key in seen:
            continue
        seen.add(pair_key)
        left = useful_alternative_records(records_by_perk.get(pair_key[0], []))
        right = useful_alternative_records(records_by_perk.get(pair_key[1], []))
        if not left or not right:
            continue
        pairs.append(
            {
                "key": "|".join(pair_key),
                "left_perk_string_id": pair_key[0],
                "right_perk_string_id": pair_key[1],
                "left_label": choice_label(left),
                "right_label": choice_label(right),
                "left_records": left,
                "right_records": right,
            }
        )
    return sorted(
        pairs,
        key=lambda pair: (
            int((pair["left_records"] or pair["right_records"])[0].get("level", 0)),
            str((pair["left_records"] or pair["right_records"])[0].get("skill", "")),
            pair["key"],
        ),
    )


def describe_metric_differences(chosen: dict[str, float], other: dict[str, float]) -> str:
    deltas = []
    labels = {
        "infantry_movement_percent": "infantry movement",
        "ranged_movement_percent": "ranged movement",
        "mounted_movement_percent": "mounted movement",
        "melee_damage_percent": "melee damage",
        "ranged_damage_percent": "ranged damage",
        "ranged_armor_penetration_percent": "ranged armor penetration",
        "ranged_accuracy_penalty_reduction_percent": "accuracy penalty reduction",
        "melee_skill_bonus": "melee skill",
        "ranged_skill_bonus": "ranged skill",
        "hit_points": "HP",
        "armor": "armor",
        "ranged_damage_taken_reduction_percent": "ranged damage reduction",
        "shield_damage_reduction_percent": "shield damage reduction",
        "party_size": "party size",
    }
    for key, label in labels.items():
        delta = chosen.get(key, 0.0) - other.get(key, 0.0)
        if abs(delta) < 1e-9:
            continue
        sign = "+" if delta > 0 else ""
        suffix = "" if key in {"hit_points", "armor", "party_size", "melee_skill_bonus", "ranged_skill_bonus"} else "%"
        deltas.append(f"{sign}{rounded(delta, 2):g}{suffix} {label}")
    return "; ".join(deltas[:4])


def build_banner_package_simulation(
    records: list[dict[str, Any]],
    banner_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    pairs = build_alternative_pair_sides(records)
    packages: dict[str, Any] = {}

    for package_key, definition in PACKAGE_DEFINITIONS.items():
        weights = definition["weights"]
        banner = banner_choice(banner_payload, definition["banner_key"])
        totals = banner_package_metrics(banner)
        choices = []

        for pair in pairs:
            left_records = pair["left_records"]
            right_records = pair["right_records"]
            left_metrics = metrics_for_records(left_records)
            right_metrics = metrics_for_records(right_records)
            left_score = score_metrics(left_metrics, weights)
            right_score = score_metrics(right_metrics, weights)
            if right_score > left_score:
                chosen_side = "right"
                chosen_records = right_records
                other_records = left_records
                chosen_metrics = right_metrics
                other_metrics = left_metrics
                chosen_score = right_score
                other_score = left_score
            else:
                chosen_side = "left"
                chosen_records = left_records
                other_records = right_records
                chosen_metrics = left_metrics
                other_metrics = right_metrics
                chosen_score = left_score
                other_score = right_score

            merge_metrics(totals, chosen_metrics)
            choices.append(
                {
                    "pair_key": pair["key"],
                    "chosen_side": chosen_side,
                    "chosen_label": choice_label(chosen_records),
                    "other_label": choice_label(other_records),
                    "chosen_perk_string_id": str(chosen_records[0].get("perk_string_id", "")),
                    "other_perk_string_id": str(other_records[0].get("perk_string_id", "")),
                    "score_delta": rounded(chosen_score - other_score, 3),
                    "chosen_metrics": clean_metrics(chosen_metrics),
                    "other_metrics": clean_metrics(other_metrics),
                    "summary": describe_metric_differences(chosen_metrics, other_metrics),
                    "chosen_records": [record_choice(record) for record in chosen_records],
                    "other_records": [record_choice(record) for record in other_records],
                }
            )

        packages[package_key] = {
            "key": package_key,
            "title": definition["title"],
            "doctrine": definition["doctrine"],
            "banner": banner,
            "banner_application": accuracy_banner_application() if definition["banner_key"] == "archer_accuracy" else None,
            "metrics": clean_metrics(totals),
            "choices": choices,
        }

    speed_choices = {
        choice["pair_key"]: choice["chosen_perk_string_id"]
        for choice in packages["shock_speed"]["choices"]
    }
    speed_metrics = packages["shock_speed"]["metrics"]
    for package_key, package in packages.items():
        differences = []
        for choice in package["choices"]:
            speed_pick = speed_choices.get(choice["pair_key"])
            if speed_pick and speed_pick != choice["chosen_perk_string_id"]:
                differences.append(choice)
        package["differences_from_shock_speed"] = differences
        package["delta_vs_shock_speed"] = clean_metrics(
            {
                key: float(package["metrics"].get(key, 0.0)) - float(speed_metrics.get(key, 0.0))
                for key in PACKAGE_METRIC_KEYS
            }
        )

    return {
        "assumptions": [
            "This is a deterministic scoring model over extracted commander-relevant perk alternatives, not a battle simulator.",
            "The full chosen perk set is stored in JSON. The markdown focuses on package totals and choices that differ from the shock-speed package.",
            "Banner bonuses are added as package metrics: infantry speed, ranged damage reduction, weapon inaccuracy reduction, or melee damage.",
            "The archer accuracy banner applies to WeaponInaccuracy, so the model treats it as base inaccuracy reduction rather than direct hit chance.",
        ],
        "accuracy_banner_application": accuracy_banner_application(),
        "packages": packages,
    }


def accuracy_banner_application() -> dict[str, Any]:
    return {
        "effect": "DecreasedRangedAccuracyPenalty",
        "method": "SandBox.GameComponents.SandboxAgentStatCalculateModel.SetPerkAndBannerEffectsOnAgent",
        "applied_to": "AgentDrivenProperties.WeaponInaccuracy",
        "mechanical_read": (
            "The banner bonus is added to the WeaponInaccuracy ExplainedNumber and then written back with "
            "set_WeaponInaccuracy. Tier 3 is -8%, so it should multiply the base inaccuracy/spread component by about 0.92."
        ),
        "not_applied_to": [
            "WeaponMaxMovementAccuracyPenalty",
            "WeaponMaxUnsteadyAccuracyPenalty",
            "WeaponRotationalAccuracyPenaltyInRadians",
            "direct hit chance",
        ],
        "evidence": [
            "IL calls DefaultBannerEffects.get_DecreasedRangedAccuracyPenalty().",
            "The banner is added to local WeaponInaccuracy explained number.",
            "The result is assigned through AgentDrivenProperties.set_WeaponInaccuracy().",
        ],
        "practical_read": (
            "Helpful when raw spread is the limiting factor for many ranged troops firing often, but weaker than it looks "
            "if misses are mostly movement, rotation, target motion, range, projectile travel, line of sight, or AI timing."
        ),
    }


def build_payload(workspace: Path, perk_export_path: Path) -> dict[str, Any]:
    rows = read_json(perk_export_path)
    records = build_commander_records(rows)
    banner_path = workspace / "Data" / "raw" / "banner-items.json"
    banner_payload = read_json(banner_path) if banner_path.exists() else None
    category_counts = Counter(record["doctrine_category"] for record in records)
    rating_counts = Counter(record["value_rating"] for record in records)
    inputs = {"perk_export": display_path(perk_export_path, workspace)}
    if banner_path.exists():
        inputs["banner_items"] = display_path(banner_path, workspace)

    return {
        "generated_at": datetime.now().astimezone().isoformat(),
        "inputs": inputs,
        "doctrine": {
            "target": "Elite shock-infantry-heavy one-party army.",
            "priority_order": [
                "Maximize live combat power per troop, including lethal output and enough staying power to keep elites alive.",
                "Preserve engagement control so the party can choose fights.",
                "Scale party size after the force can still catch worthwhile targets.",
            ],
            "speed_note": (
                "Troop combat movement speed is a core combat stat for shock infantry, not generic mobility: "
                "it reduces ranged exposure, forces contact, and improves battlefield responsiveness."
            ),
        },
        "category_meta": CATEGORY_META,
        "speed_kind_descriptions": SPEED_KIND_DESCRIPTIONS,
        "investment_bars": build_investment_bars(rows, records),
        "summary": {
            "total_records": len(records),
            "category_counts": dict(category_counts),
            "rating_counts": dict(rating_counts),
        },
        "banner_package_simulation": build_banner_package_simulation(records, banner_payload),
        "records": records,
    }


def format_bonus(record: dict[str, Any]) -> str:
    bonus = record.get("bonus")
    try:
        value = float(bonus)
    except (TypeError, ValueError):
        return str(bonus)

    if record.get("increment_type") == "add_factor":
        value *= 100
        text = f"{value:.4f}".rstrip("0").rstrip(".")
        return f"{text}%"

    if value.is_integer():
        return str(int(value))
    return f"{value:.4f}".rstrip("0").rstrip(".")


def write_record_table(lines: list[str], records: list[dict[str, Any]]) -> None:
    lines.extend(
        [
            "| Rating | Skill | Level | Perk | Role | Fit | Speed kind | Bonus | Effect | Notes |",
            "| --- | --- | ---: | --- | --- | --- | --- | ---: | --- | --- |",
        ]
    )
    for record in records:
        notes = " ".join(record.get("notes", []))
        speed_kind = record.get("speed_kind") or ""
        lines.append(
            "| {rating} | {skill} | {level} | {perk} | {role} | {fit} | {speed} | {bonus} | {effect} | {notes} |".format(
                rating=table_escape(record["value_rating"]),
                skill=table_escape(record["skill"]),
                level=record["level"],
                perk=table_escape(record["perk"]),
                role=table_escape(record["role"]),
                fit=table_escape(record["default_force_fit"]),
                speed=table_escape(speed_kind),
                bonus=table_escape(format_bonus(record)),
                effect=table_escape(record["effect"]),
                notes=table_escape(notes),
            )
        )
    lines.append("")


def format_banner_cell(choice: dict[str, Any]) -> str:
    if not choice.get("available"):
        return f"{choice.get('effect', '')} (run extract-banners)"
    items = ", ".join(choice.get("items", []))
    return "{effect} T{tier} ({bonus}) - {items}".format(
        effect=choice.get("effect_name", choice.get("effect", "")),
        tier=choice.get("tier", ""),
        bonus=choice.get("display_bonus", ""),
        items=items,
    )


def display_metric(metrics: dict[str, Any], key: str, suffix: str = "%") -> str:
    value = float(metrics.get(key, 0) or 0)
    if abs(value) < 1e-9:
        return ""
    return f"{value:g}{suffix}"


def display_signed_metric(metrics: dict[str, Any], key: str, suffix: str = "%") -> str:
    value = float(metrics.get(key, 0) or 0)
    if abs(value) < 1e-9:
        return ""
    sign = "+" if value > 0 else ""
    return f"{sign}{value:g}{suffix}"


def package_read(package_key: str, package: dict[str, Any]) -> str:
    delta = package.get("delta_vs_shock_speed", {})
    if package_key == "shock_speed":
        return "Baseline package for this comparison."
    if package_key == "anti_arrow":
        return (
            "Trades speed and some damage for a much larger ranged-damage, HP, and shield package."
        )
    if package_key == "archer_accuracy":
        return (
            "Real but specialized: adds base inaccuracy reduction and ranged accuracy perks, while giving up most shock-infantry priorities."
        )
    if package_key == "melee_damage":
        movement_loss = abs(float(delta.get("infantry_movement_percent", 0)))
        damage_gain = float(delta.get("melee_damage_percent", 0))
        return (
            f"Mostly the same perk package as shock speed, but swaps about {movement_loss:g}% infantry movement for {damage_gain:g}% melee damage."
        )
    return ""


def write_package_simulation_markdown(payload: dict[str, Any], path: Path, workspace: Path, json_output: Path) -> None:
    simulation = payload["banner_package_simulation"]
    packages = simulation["packages"]
    accuracy = simulation["accuracy_banner_application"]

    lines = [
        "# Commander Banner Package Comparison",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This report scores full commander-relevant perk alternative sets around each major banner option. It is a package model over extracted perk rows, not a battle simulator.",
        "",
        "Banner mechanics are confirmed in the generated [banner effects reference](banner-effects.md); use that as the source of truth for what each banner modifies before interpreting these package totals.",
        "",
        "## Inputs",
        "",
        f"- Commander JSON: `{display_path(json_output, workspace)}`",
    ]
    for label, input_path in payload.get("inputs", {}).items():
        lines.append(f"- {label}: `{input_path}`")

    lines.extend(
        [
            "",
            "## Package Totals",
            "",
            "| Package | Banner | Infantry movement | Melee damage | Ranged damage taken | Weapon inaccuracy | Accuracy penalty | HP | Shield damage | Differing picks vs speed |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for package_key in PACKAGE_DEFINITIONS:
        package = packages[package_key]
        metrics = package["metrics"]
        lines.append(
            "| {title} | {banner} | {move} | {melee} | {ranged_resist} | {inaccuracy} | {accuracy} | {hp} | {shield} | {diffs} |".format(
                title=table_escape(package["title"]),
                banner=table_escape(format_banner_cell(package["banner"])),
                move=table_escape(display_metric(metrics, "infantry_movement_percent")),
                melee=table_escape(display_metric(metrics, "melee_damage_percent")),
                ranged_resist=table_escape(display_metric(metrics, "ranged_damage_taken_reduction_percent")),
                inaccuracy=table_escape(display_metric(metrics, "weapon_inaccuracy_reduction_percent")),
                accuracy=table_escape(display_metric(metrics, "ranged_accuracy_penalty_reduction_percent")),
                hp=table_escape(display_metric(metrics, "hit_points", "")),
                shield=table_escape(display_metric(metrics, "shield_damage_reduction_percent")),
                diffs=len(package.get("differences_from_shock_speed", [])),
            )
        )

    lines.extend(
        [
            "",
            "## Delta vs Shock Speed",
            "",
            "| Package | Infantry movement | Melee damage | Ranged damage taken | Weapon inaccuracy | Accuracy penalty | HP | Shield damage | Read |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for package_key in PACKAGE_DEFINITIONS:
        if package_key == "shock_speed":
            continue
        package = packages[package_key]
        delta = package.get("delta_vs_shock_speed", {})
        lines.append(
            "| {title} | {move} | {melee} | {ranged_resist} | {inaccuracy} | {accuracy} | {hp} | {shield} | {read} |".format(
                title=table_escape(package["title"]),
                move=table_escape(display_signed_metric(delta, "infantry_movement_percent")),
                melee=table_escape(display_signed_metric(delta, "melee_damage_percent")),
                ranged_resist=table_escape(display_signed_metric(delta, "ranged_damage_taken_reduction_percent")),
                inaccuracy=table_escape(display_signed_metric(delta, "weapon_inaccuracy_reduction_percent")),
                accuracy=table_escape(display_signed_metric(delta, "ranged_accuracy_penalty_reduction_percent")),
                hp=table_escape(display_signed_metric(delta, "hit_points", "")),
                shield=table_escape(display_signed_metric(delta, "shield_damage_reduction_percent")),
                read=table_escape(package_read(package_key, package)),
            )
        )

    lines.extend(
        [
            "",
            "## Accuracy Banner Mechanics",
            "",
            f"- Effect: `{accuracy['effect']}`",
            f"- Applied in: `{accuracy['method']}`",
            f"- Applied to: `{accuracy['applied_to']}`",
            f"- Mechanical read: {accuracy['mechanical_read']}",
            f"- Practical read: {accuracy['practical_read']}",
            "- Not applied to: " + ", ".join(f"`{item}`" for item in accuracy["not_applied_to"]),
            "",
            "That makes the tier 3 accuracy banner real, but narrow: it reduces base weapon inaccuracy/spread by 8%. It does not directly grant 8% hit chance, and it does not reduce the movement, unsteady, or rotational penalty properties that several personal/captain perks touch.",
            "",
            "## Pick Differences vs Shock Speed",
            "",
            "Only choices that differ from the shock-speed package are shown here. The full selected side for every commander-relevant alternative pair is in the JSON output.",
            "",
        ]
    )

    for package_key in PACKAGE_DEFINITIONS:
        if package_key == "shock_speed":
            continue
        package = packages[package_key]
        lines.extend(
            [
                f"### {package['title']}",
                "",
                package["doctrine"],
                "",
            ]
        )
        differences = package.get("differences_from_shock_speed", [])
        if not differences:
            lines.extend(["No perk alternative changes from the shock-speed package.", ""])
            continue
        lines.extend(
            [
                "| Package pick | Shock-speed pick | Why the package flips it |",
                "| --- | --- | --- |",
            ]
        )
        for choice in differences:
            lines.append(
                "| {chosen} | {other} | {summary} |".format(
                    chosen=table_escape(choice.get("chosen_label", "")),
                    other=table_escape(choice.get("other_label", "")),
                    summary=table_escape(choice.get("summary", "")),
                )
            )
        lines.append("")

    lines.extend(["## Assumptions", ""])
    for assumption in simulation.get("assumptions", []):
        lines.append(f"- {assumption}")
    lines.append("- Non-alternative perks common to every package are not re-listed in the markdown comparison.")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_investment_bar_markdown(payload: dict[str, Any], path: Path, workspace: Path, json_output: Path) -> None:
    bars = payload["investment_bars"]
    lines = [
        "# Commander Perk Investment Bars",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This report turns the doctrine-ranked commander perk extract into practical stopping bars: what is worth reaching, what is merely contextual, and what is usually not worth extra focus or attribute points.",
        "",
        "Default lens: elite shock-infantry-heavy one-party commander. The goal is to maximize per-troop live combat power first, preserve engagement control second, and scale party size third.",
        "",
        "> [!NOTE]",
        f"> Cost uses `{bars['assumptions']['cost_formula']}` from a {bars['assumptions']['baseline_attribute']}-attribute floor. With {bars['assumptions']['max_focus']} focus and no purchased attributes, a skill reaches {bars['assumptions']['focus_only_limit']}.",
        "",
        "> [!NOTE]",
        f"> Assisted physical cost starts Vigor, Control, and Endurance from {bars['assumptions']['endurance_assisted_physical_baseline']} attribute when the Endurance-skill attribute perks are assigned that way. With {bars['assumptions']['max_focus']} focus, that reaches {bars['assumptions']['assisted_physical_focus_only_limit']}. {bars['assumptions']['assisted_physical_note']}",
        "",
        "> [!NOTE]",
        f"> {bars['assumptions']['vigor_hyper_stretch_note']}",
        "",
        "> [!NOTE]",
        f"> {bars['assumptions']['control_baseline_note']}",
        "",
        "> [!NOTE]",
        f"> {bars['assumptions']['non_monotonic_note']}",
        "",
        "## How To Read The Bars",
        "",
        "| Band | Meaning |",
        "| --- | --- |",
    ]
    for key in ("worth", "context", "skip"):
        meta = bars["band_meta"][key]
        lines.append(f"| {table_escape(meta['title'])} | {table_escape(meta['description'])} |")

    lines.extend(
        [
            "",
            "## Point-Recovery Summary",
            "",
            "The easiest physical point cuts for this doctrine are:",
            "",
        ]
    )
    for item in bars["physical_cut_summary"]:
        lines.append(f"- **{item['skill']}**: {item['read']}")

    lines.extend(
        [
            "",
            "Broad read: the Endurance-assisted baseline makes physical splashes much cheaper, especially level 225 breakpoints, and can save a bought Vigor or Control attribute point. It does not make every late physical perk worth chasing: weak or personal perks are still weak. Saved purchased attributes usually have a better home in Medicine, Scouting, Steward, or Leadership unless a physical attribute is shared by several pushed weapon skills.",
            "",
            "## Skill Bars",
            "",
            "| Skill | Attr | Default Stop | Default Cost | Assisted Physical Cost | Stretch Stop | Stretch Cost | Assisted Physical Cost | Worth It | Meh / Context | Usually Skip | Point Read |",
            "| --- | --- | ---: | --- | --- | ---: | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in bars["skills"]:
        default_stop = "" if int(row["default_stop"]) <= 0 else str(row["default_stop"])
        stretch_stop = "" if int(row["stretch_stop"]) <= 0 else str(row["stretch_stop"])
        default_cost = "" if int(row["default_stop"]) <= 0 else format_cost_from_dict(row["default_cost"])
        stretch_cost = "" if int(row["stretch_stop"]) <= 0 else format_cost_from_dict(row["stretch_cost"])
        assisted_default = (
            ""
            if int(row["default_stop"]) <= 0 or not row.get("assisted_default_cost")
            else format_cost_from_dict(row["assisted_default_cost"])
        )
        assisted_stretch = (
            ""
            if int(row["stretch_stop"]) <= 0 or not row.get("assisted_stretch_cost")
            else format_cost_from_dict(row["assisted_stretch_cost"])
        )
        lines.append(
            "| {skill} | {attribute} | {default_stop} | {default_cost} | {assisted_default} | {stretch_stop} | {stretch_cost} | {assisted_stretch} | {worth} | {context} | {skip} | {read} |".format(
                skill=table_escape(row["skill"]),
                attribute=table_escape(row["attribute"]),
                default_stop=default_stop,
                default_cost=table_escape(default_cost),
                assisted_default=table_escape(assisted_default),
                stretch_stop=stretch_stop,
                stretch_cost=table_escape(stretch_cost),
                assisted_stretch=table_escape(assisted_stretch),
                worth=table_escape(row["worth"]),
                context=table_escape(row["context"]),
                skip=table_escape(row["skip"]),
                read=table_escape(row["point_read"]),
            )
        )

    lines.extend(
        [
            "",
            "## Threshold Details",
            "",
            "These rows show the levels where the bar changes or where a perk is a known trap/exception.",
            "",
            "| Skill | Level | Band | Neutral Split | Neutral Cost | Assisted Physical Cost | Extracted Commander Rows | Read |",
            "| --- | ---: | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in bars["details"]:
        split = row["cost"]
        assisted_cost = format_cost_from_dict(row["assisted_cost"]) if row.get("assisted_cost") else ""
        extracted = row.get("extracted_summary") or "No commander-facing row in the generated extract."
        lines.append(
            "| {skill} | {level} | {band} | {split} | {cost} | {assisted} | {extracted} | {note} |".format(
                skill=table_escape(row["skill"]),
                level=row["level"],
                band=table_escape(row["band_title"]),
                split=table_escape(format_split_from_dict(split)),
                cost=table_escape(format_cost_from_dict(split)),
                assisted=table_escape(assisted_cost),
                extracted=table_escape(extracted),
                note=table_escape(row["note"]),
            )
        )

    lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- JSON: `{display_path(json_output, workspace)}`",
            f"- Report: `{display_path(path, workspace)}`",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_markdown(payload: dict[str, Any], path: Path, workspace: Path, json_output: Path) -> None:
    lines = [
        "# Commander Perks Report",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This generated report is tuned for an elite one-party commander build: first make every troop as lethal as possible, then keep enough campaign speed to choose fights, then add party size once the force can still catch worthwhile targets.",
        "",
        "> [!NOTE]",
        "> Troop combat movement speed is ranked as core combat power for shock infantry. Closing faster means less arrow exposure, better melee contact, better formation response, and faster cleanup. Small HP gains remain useful, but Medicine and resistance stacking make HP easier to find than movement speed.",
        "",
        "## Speed Kind Legend",
        "",
        "| Speed kind | Meaning |",
        "| --- | --- |",
    ]
    for key, description in SPEED_KIND_DESCRIPTIONS.items():
        lines.append(f"| `{key}` | {table_escape(description)} |")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Records: {payload['summary']['total_records']}",
            "- Doctrine order: core troop lethality, combat staying power, engagement control, party scaling.",
            "- Low-priority rows are retained when they are common keyword traps, such as projectile travel speed or personal reload movement.",
            "",
            "| Category | Rows | Purpose |",
            "| --- | ---: | --- |",
        ]
    )
    category_counts = payload["summary"]["category_counts"]
    for key in CATEGORY_ORDER:
        meta = CATEGORY_META[key]
        lines.append(f"| {meta['title']} | {category_counts.get(key, 0)} | {table_escape(meta['description'])} |")

    records_by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in payload["records"]:
        records_by_category[record["doctrine_category"]].append(record)

    for key in CATEGORY_ORDER:
        meta = CATEGORY_META[key]
        lines.extend(["", f"## {meta['title']}", "", meta["description"], ""])
        write_record_table(lines, records_by_category.get(key, []))

    lines.extend(
        [
            "## Outputs",
            "",
            f"- JSON: `{display_path(json_output, workspace)}`",
            f"- Report: `{display_path(path, workspace)}`",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def extract_commander_perks(
    workspace: Path,
    perk_export_path: Path,
    json_output: Path,
    markdown_output: Path,
    package_output: Path | None = None,
    investment_output: Path | None = None,
) -> None:
    if package_output is None:
        package_output = workspace / "Docs" / "reports" / "commander-banner-package-comparison.md"
    if investment_output is None:
        investment_output = workspace / "Docs" / "reports" / "commander-perk-investment-bars.md"
    payload = build_payload(workspace, perk_export_path)
    write_json(json_output, payload)
    write_markdown(payload, markdown_output, workspace, json_output)
    write_package_simulation_markdown(payload, package_output, workspace, json_output)
    write_investment_bar_markdown(payload, investment_output, workspace, json_output)
    print(f"Commander perk JSON written: {json_output}")
    print(f"Commander perk report written: {markdown_output}")
    print(f"Commander banner package comparison written: {package_output}")
    print(f"Commander perk investment bars written: {investment_output}")
    for key in CATEGORY_ORDER:
        print(f"  {key}: {payload['summary']['category_counts'].get(key, 0)} rows")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract doctrine-ranked commander perk reports.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--perk-export", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    parser.add_argument("--package-output", type=Path, default=None)
    parser.add_argument("--investment-output", type=Path, default=None)
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    perk_export_path = args.perk_export or workspace / "Data" / "export" / "perk-effects.json"
    json_output = args.json_output or workspace / "Data" / "intermediate" / "commander_perks_extracted.json"
    markdown_output = args.markdown_output or workspace / "Data" / "intermediate" / "commander_perks_report.txt"
    package_output = args.package_output or workspace / "Docs" / "reports" / "commander-banner-package-comparison.md"
    investment_output = args.investment_output or workspace / "Docs" / "reports" / "commander-perk-investment-bars.md"
    extract_commander_perks(
        workspace=workspace,
        perk_export_path=perk_export_path.resolve(),
        json_output=json_output,
        markdown_output=markdown_output,
        package_output=package_output,
        investment_output=investment_output,
    )


if __name__ == "__main__":
    main()
