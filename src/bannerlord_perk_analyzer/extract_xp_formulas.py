from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from .postprocess import default_workspace
    from .xp_reports import display_path, table_escape
except ImportError:
    from postprocess import default_workspace
    from xp_reports import display_path, table_escape


DEFAULT_ASSEMBLIES = [
    "TaleWorlds.CampaignSystem",
    "TaleWorlds.Core",
    "TaleWorlds.MountAndBlade",
    "SandBox",
    "StoryMode",
]


@dataclass(frozen=True)
class FormulaScan:
    key: str
    title: str
    assemblies: list[str]
    queries: list[str]
    notes: list[str]


FORMULA_SCANS = [
    FormulaScan(
        key="combat_hit_xp",
        title="Combat Hit, Kill, Shot, And Riding XP",
        assemblies=["TaleWorlds.CampaignSystem", "TaleWorlds.MountAndBlade", "SandBox", "StoryMode"],
        queries=[
            "GetXpFromHit",
            "GetBattleXpBonusFromPerks",
            "GetXpfMultiplierForMissionType",
            "GetXpMultiplierFromShotDifficulty",
            "GetShootDifficulty",
            "OnCombatHit",
            "OnGainingRidingExperience",
        ],
        notes=[
            "Includes the direct hit/kill XP model, mission-side shot difficulty, campaign shot-difficulty XP factor, and mounted Riding XP hook.",
        ],
    ),
    FormulaScan(
        key="hero_progression",
        title="Hero Skill XP, Learning, And Level Progression",
        assemblies=["TaleWorlds.CampaignSystem"],
        queries=[
            "AddSkillXp",
            "GainRawXp",
            "GetFocusFactor",
            "CalculateLearningLimit",
            "CalculateLearningRate",
            "InitializeXpRequiredForSkillLevel",
            "GetXpRequiredForSkillLevel",
            "GetSkillLevelChange",
            "GetXpAmountForSkillLevelChange",
            "GetXpRequiredForLevel",
            "SkillsRequiredForLevel",
        ],
        notes=[
            "Captures the path from raw skill XP through learning-rate/focus scaling and skill/character level thresholds.",
        ],
    ),
    FormulaScan(
        key="troop_xp",
        title="Troop XP, Shared XP, Upgrade Costs, And Daily Training",
        assemblies=["TaleWorlds.CampaignSystem"],
        queries=[
            "GetXpReward",
            "GenerateSharedXp",
            "CalculateXpGainFromBattles",
            "GetEffectiveDailyExperience",
            "GetPerkExperiencesForTroops",
            "CanTroopGainXp",
            "PartyAddSharedXp",
            "GetMaximumXpAmountPartyCanGet",
            "AddXpToTroop",
            "GetXpCostForUpgrade",
            "GetSkillXpFromUpgradingTroops",
            "CalculateDailyTroopXpBonus",
            "CalculateTroopXpBonusInternal",
            "CalculateGarrisonXpBonusMultiplier",
        ],
        notes=[
            "Covers battle troop XP conversion, shared party XP distribution, upgrade XP caps/costs, and garrison/daily training bonuses.",
        ],
    ),
    FormulaScan(
        key="crafting_and_discard",
        title="Smithing, Crafting Orders, And Item Discard XP",
        assemblies=["TaleWorlds.CampaignSystem"],
        queries=[
            "GetSkillXpForSmithing",
            "GetSkillXpForRefining",
            "GetSkillXpForSmelting",
            "GetOrderExperience",
            "GetXpBonusForDiscardingItem",
            "GetXpBonusForDiscardingItems",
            "XpGainFromDonations",
            "DonationXpChange",
        ],
        notes=[
            "Covers smithing/free-build/refine/smelt/order constants and donation/discard XP conversions.",
        ],
    ),
    FormulaScan(
        key="activity_xp",
        title="Activity, Quest, Tournament, Persuasion, Hideout, Alley, And Healing XP",
        assemblies=["TaleWorlds.CampaignSystem", "SandBox", "StoryMode"],
        queries=[
            "GetSkillXpFromHealingTroop",
            "GetSkillXpGainFromTournament",
            "GetSkillXpFromPersuasion",
            "GetRogueryXpGain",
            "GetCharmExperience",
            "GetTradeXp",
            "GetDailyXpGain",
            "GetInitialXpGain",
            "GetXpGainAfterSuccessfulAlleyDefenseForMainHero",
            "PartyExperienceChance",
            "CompanionSkillRewardXP",
        ],
        notes=[
            "Collects non-combat and quest/activity XP methods. Many issue rewards are simple constants multiplied by issue difficulty.",
        ],
    ),
]


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def resolve_game_root(game_root: Path | None) -> Path:
    env_game_root = os.environ.get("BANNERLORD_GAME_ROOT")
    if game_root is None and not env_game_root:
        raise SystemExit("Bannerlord game root is required. Pass --game-root or set BANNERLORD_GAME_ROOT.")
    return (game_root or Path(str(env_game_root))).resolve()


def run_find_methods(
    workspace: Path,
    game_root: Path,
    scan: FormulaScan,
    include_il: bool,
    temp_dir: Path,
) -> dict[str, Any]:
    project = workspace / "tools" / "BannerlordExtractor" / "BannerlordExtractor.csproj"
    if not project.exists():
        raise SystemExit(f"Extractor project is missing: {project}")

    output = temp_dir / f"{scan.key}.json"
    command = [
        "dotnet",
        "run",
        "--project",
        str(project),
        "--",
        "find-methods",
        "--game-root",
        str(game_root),
        "--output",
        str(output),
    ]
    for assembly in scan.assemblies:
        command.extend(["--assembly", assembly])
    for query in scan.queries:
        command.extend(["--query", query])
    if include_il:
        command.append("--include-il")

    subprocess.run(command, check=True)
    payload = read_json(output)
    payload["scan_key"] = scan.key
    payload["scan_title"] = scan.title
    payload["scan_notes"] = scan.notes
    return payload


def method_key(method: dict[str, Any]) -> str:
    return f"{method.get('assembly', '')}|{method.get('type', '')}|{method.get('method', '')}|{method.get('signature', '')}"


def compact_method(method: dict[str, Any]) -> dict[str, Any]:
    return {
        "matched_queries": method.get("matched_queries", []),
        "assembly": method.get("assembly", ""),
        "assembly_path": method.get("assembly_path", ""),
        "type": method.get("type", ""),
        "method": method.get("method", ""),
        "signature": method.get("signature", ""),
        "visibility": method.get("visibility", ""),
        "is_static": method.get("is_static", False),
        "parameters": method.get("parameters", []),
        "il_bytes": method.get("il_bytes", 0),
        "numeric_constants": method.get("numeric_constants", []),
        "string_literals": method.get("string_literals", []),
        "referenced_members": method.get("referenced_members", []),
        "il": method.get("il", []),
        "errors": method.get("errors", []),
    }


def merge_scan_payloads(scan_payloads: list[dict[str, Any]], include_il: bool) -> dict[str, Any]:
    methods_by_key: dict[str, dict[str, Any]] = {}
    scans: list[dict[str, Any]] = []
    for payload in scan_payloads:
        scan_key = payload["scan_key"]
        scan_methods: list[str] = []
        for method in payload.get("methods", []):
            key = method_key(method)
            scan_methods.append(key)
            if key not in methods_by_key:
                methods_by_key[key] = compact_method(method)
                methods_by_key[key]["formula_scan_keys"] = []
            if scan_key not in methods_by_key[key]["formula_scan_keys"]:
                methods_by_key[key]["formula_scan_keys"].append(scan_key)

        scans.append(
            {
                "key": scan_key,
                "title": payload["scan_title"],
                "notes": payload["scan_notes"],
                "queries": payload.get("queries", []),
                "assemblies_scanned": payload.get("assemblies_scanned", []),
                "load_errors": payload.get("load_errors", []),
                "methods_scanned": payload.get("methods_scanned", 0),
                "methods_matched": payload.get("methods_matched", 0),
                "method_keys": sorted(set(scan_methods)),
            }
        )

    methods = sorted(
        methods_by_key.values(),
        key=lambda method: (
            method.get("assembly", ""),
            method.get("type", ""),
            method.get("method", ""),
            method.get("signature", ""),
        ),
    )
    if not include_il:
        for method in methods:
            method["il"] = []

    return {
        "generated_at": __import__("datetime").datetime.now().astimezone().isoformat(),
        "include_il": include_il,
        "scans": scans,
        "methods_matched": len(methods),
        "methods": methods,
    }


def find_method(payload: dict[str, Any], type_suffix: str, method_name: str) -> dict[str, Any] | None:
    for method in payload.get("methods", []):
        if str(method.get("type", "")).endswith(type_suffix) and method.get("method") == method_name:
            return method
    return None


def format_number(value: Any) -> str:
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        rounded = round(value, 6)
        if abs(value - rounded) <= max(1e-8, abs(value) * 1e-7):
            return f"{rounded:.6f}".rstrip("0").rstrip(".")
    return str(value)


def format_constants(constants: list[Any], limit: int | None = None) -> str:
    shown = constants if limit is None else constants[:limit]
    text = ", ".join(format_number(value) for value in shown)
    if limit is not None and len(constants) > limit:
        text += ", ..."
    return text


def constants_text(method: dict[str, Any] | None) -> str:
    if method is None:
        return ""
    return format_constants(method.get("numeric_constants", []), limit=16)


def method_anchor(method: dict[str, Any] | None) -> str:
    if method is None:
        return ""
    return f"`{method.get('type')}.{method.get('method')}`"


def write_formula_report(payload: dict[str, Any], path: Path, workspace: Path, json_output: Path) -> None:
    get_xp_from_hit = find_method(payload, "DefaultCombatXpModel", "GetXpFromHit")
    get_shoot_difficulty = find_method(payload, ".Mission", "GetShootDifficulty")
    shot_multiplier = find_method(payload, "DefaultCombatXpModel", "GetXpMultiplierFromShotDifficulty")
    on_combat_hit = find_method(payload, "DefaultSkillLevelingManager", "OnCombatHit")
    riding = find_method(payload, "DefaultSkillLevelingManager", "OnGainingRidingExperience")
    troop_reward = find_method(payload, "DefaultPartyTrainingModel", "GetXpReward")
    healing = find_method(payload, "DefaultPartyHealingModel", "GetSkillXpFromHealingTroop")
    add_skill_xp = find_method(payload, "HeroDeveloper", "AddSkillXp")
    learning_limit = find_method(payload, "DefaultCharacterDevelopmentModel", "CalculateLearningLimit")
    learning_rate = find_method(payload, "DefaultCharacterDevelopmentModel", "CalculateLearningRate")
    party_shared_xp = find_method(payload, "MobilePartyHelper", "PartyAddSharedXp")
    troop_can_gain_xp = find_method(payload, "MobilePartyHelper", "CanTroopGainXp")
    upgrade_xp_cost = find_method(payload, "DefaultPartyTroopUpgradeModel", "GetXpCostForUpgrade")
    daily_troop_xp = find_method(payload, "DefaultDailyTroopXpBonusModel", "CalculateTroopXpBonusInternal")
    travel_on_foot = find_method(payload, "DefaultSkillLevelingManager", "OnTravelOnFoot")
    travel_on_horse = find_method(payload, "DefaultSkillLevelingManager", "OnTravelOnHorse")
    simulation_kill = find_method(payload, "DefaultSkillLevelingManager", "OnSimulationCombatKill")
    smith_refining = find_method(payload, "DefaultSmithingModel", "GetSkillXpForRefining")
    smith_smelting = find_method(payload, "DefaultSmithingModel", "GetSkillXpForSmelting")
    smith_order = find_method(payload, "DefaultSmithingModel", "GetSkillXpForSmithingInCraftingOrderMode")
    smith_free = find_method(payload, "DefaultSmithingModel", "GetSkillXpForSmithingInFreeBuildMode")
    crafting_order = find_method(payload, "CraftingOrder", "GetOrderExperience")
    tournament = find_method(payload, "DefaultTournamentModel", "GetSkillXpGainFromTournament")
    hideout_ghost = find_method(payload, "DefaultHideoutModel", "GetRogueryXpGainAsGhost")
    hideout_end = find_method(payload, "DefaultHideoutModel", "GetRogueryXpGainOnHideoutMissionEnd")
    alley_initial = find_method(payload, "DefaultAlleyModel", "GetInitialXpGainForMainHero")
    alley_daily_main = find_method(payload, "DefaultAlleyModel", "GetDailyXpGainForMainHero")
    alley_daily_assigned = find_method(payload, "DefaultAlleyModel", "GetDailyXpGainForAssignedClanMember")
    alley_defense = find_method(payload, "DefaultAlleyModel", "GetXpGainAfterSuccessfulAlleyDefenseForMainHero")
    persuasion = find_method(payload, "DefaultPersuasionModel", "GetSkillXpFromPersuasion")
    workshop = find_method(payload, "DefaultWorkshopModel", "GetTradeXpPerWarehouseProduction")
    charm_relation = find_method(payload, "DefaultDiplomacyModel", "GetCharmExperienceFromRelationGain")

    lines = [
        "# Bannerlord XP Formula Extraction",
        "",
        f"Generated: {payload.get('generated_at', '')}",
        "",
        "This report is produced by `src/bannerlord_perk_analyzer/extract_xp_formulas.py`, which uses the local .NET extractor's `find-methods` command to search campaign, mission, and module assemblies for XP formula candidates.",
        "",
        "## Confirmed Formula Leads",
        "",
        "### Combat Hit And Kill XP",
        "",
        f"Source: {method_anchor(get_xp_from_hit)}",
        "",
        "```text",
        "effectiveDamage = min(damage, targetHp) + (targetHp if isFatal else 0)",
        "baseXp = 0.4 * (attackerPower + 0.5) * (targetPower + 0.5) * effectiveDamage * missionTypeMultiplier",
        "```",
        "",
        f"Constants found: `{constants_text(get_xp_from_hit)}`",
        "",
        "### Shot Difficulty XP",
        "",
        f"Mission-side source: {method_anchor(get_shoot_difficulty)}",
        f"Campaign-side source: {method_anchor(shot_multiplier)} and {method_anchor(on_combat_hit)}",
        "",
        "```text",
        "rawDifficulty = 0.3 * ((distance + 4) / 4) * ((4 + lateralMotion * relativeSpeed) / 4)",
        "shotDifficulty = clamp(rawDifficulty, 1, 12)",
        "if isHeadShot: shotDifficulty *= 1.2",
        "shotDifficultyFactor = lerp(0, 2, (min(shotDifficulty, 14.4) - 1) / 13.4)",
        "finalXp = baseXp * (1 + skillFactor * shotDifficultyFactor)",
        "skillFactor = 0.5 for Bow, 1.0 for other ranged skills",
        "```",
        "",
        f"Mission constants found: `{constants_text(get_shoot_difficulty)}`",
        f"Campaign constants found: `{constants_text(shot_multiplier)}`",
        "",
        "### Riding XP From Mounted Combat",
        "",
        f"Source: {method_anchor(riding)}",
        "",
        "```text",
        "ridingXp = baseXpAmount * (1 + horse.Difficulty * 0.02)",
        "```",
        "",
        f"Constants found: `{constants_text(riding)}`",
        "",
        "### Troop Battle XP Reward",
        "",
        f"Source: {method_anchor(troop_reward)}",
        "",
        "```text",
        "troopBattleXpReward = (troopLevel + 6)^2 / 3",
        "```",
        "",
        f"Constants found: `{constants_text(troop_reward)}`",
        "",
        "### Healing XP",
        "",
        f"Source: {method_anchor(healing)}",
        "",
        f"Constants found: `{constants_text(healing)}`",
        "",
        "The healing method is tiny in IL and should be decompiled or hand-read before turning the constant into prose.",
        "",
        "### Hero Skill XP, Learning Rate, And Limits",
        "",
        f"Sources: {method_anchor(add_skill_xp)}, {method_anchor(learning_limit)}, {method_anchor(learning_rate)}",
        "",
        "```text",
        "genericXp = rawXp * GenericXpModel.GetXpMultiplier(hero)",
        "skillXpDelta = genericXp * learningRate if isAffectedByFocusFactor else genericXp",
        "peakLearningRange = max(0, 10 * (averageAttribute - 1)) + 30 * focus",
        "skillLimit = peakLearningRange + 4 * averageAttribute + 10 * focus",
        "learningRate starts at 1.25",
        "learningRate factors include +0.4 * averageAttribute and +1.0 * focus",
        "if currentSkill > peakLearningRange: over-limit factor is -1.0 - 0.1 * (currentSkill - peakLearningRange)",
        "learningRate is clamped to at least 0",
        "```",
        "",
        f"Learning constants found: `{constants_text(learning_rate)}`",
        "",
        "### Troop XP Distribution And Upgrade Costs",
        "",
        f"Sources: {method_anchor(troop_can_gain_xp)}, {method_anchor(party_shared_xp)}, {method_anchor(upgrade_xp_cost)}, {method_anchor(daily_troop_xp)}",
        "",
        "```text",
        "troopBattleXpReward = (troopLevel + 6)^2 / 3",
        "upgradeCost sums each tier step from current tier + 1 through target tier",
        "upgrade tier costs: <=1:100, 2:300, 3:550, 4:900, 5:1300, 6:1700, 7:2100",
        "upgrade fallback per higher tier: int(1.333 * (targetLevel + 4)^2)",
        "sharedXpCapacity is the remaining XP needed by stacks that can still upgrade",
        "sharedXpAddedToStack = floor(max(1, remainingSharedXp * stackCapacity / remainingCapacity))",
        "daily town troop XP starts from buildings plus RaiseTheMeek and ProjectileDeflection perk bonuses",
        "```",
        "",
        f"Upgrade constants found: `{constants_text(upgrade_xp_cost)}`",
        "",
        "### Travel And Simulation XP",
        "",
        f"Sources: {method_anchor(travel_on_foot)}, {method_anchor(travel_on_horse)}, {method_anchor(simulation_kill)}",
        "",
        "```text",
        "travelOnFootAthleticsXp = roundRandomized(0.2 * speed) + 1",
        "travelOnHorseRidingXp = OnGainingRidingExperience(roundRandomized(0.3 * speed), horse)",
        "simulationKillWeaponXp = GetXpReward(killedCharacter)",
        "simulationKillMovementXp = roundRandomized(0.3 * simulationKillWeaponXp) to Riding if mounted, otherwise Athletics",
        "simulationCommanderTacticsXp = ceil(0.02 * simulationKillWeaponXp) when a different valid commander party is present",
        "```",
        "",
        f"Simulation constants found: `{constants_text(simulation_kill)}`",
        "",
        "### Smithing And Crafting Order XP",
        "",
        f"Sources: {method_anchor(smith_refining)}, {method_anchor(smith_smelting)}, {method_anchor(smith_order)}, {method_anchor(smith_free)}, {method_anchor(crafting_order)}",
        "",
        "```text",
        "refiningXp = round(0.3 * outputMaterialValue * outputCount)",
        "smeltingXp = round(0.02 * itemValue)",
        "smithingCraftingOrderXp = round(0.1 * itemValue)",
        "smithingFreeBuildXp = round(0.02 * itemValue)",
        "craftingOrderBaseExperience = 0.25 * theoreticalMaxItemMarketValue(requestedDesignItem)",
        "crafting order checks can halve the base and apply a clamped tier-difference factor",
        "```",
        "",
        f"Smithing constants found: `{constants_text(smith_refining)} | {constants_text(smith_smelting)} | {constants_text(smith_order)} | {constants_text(smith_free)}`",
        f"Crafting order constants found: `{constants_text(crafting_order)}`",
        "",
        "### Activity XP Constants And Small Formulas",
        "",
        f"Sources: {method_anchor(tournament)}, {method_anchor(hideout_ghost)}, {method_anchor(hideout_end)}, {method_anchor(persuasion)}, {method_anchor(workshop)}, {method_anchor(charm_relation)}",
        "",
        "```text",
        "tournamentXp = one random combat/movement skill from 5 equal 20% bands, amount 500",
        "hideoutGhostRogueryXp = randomFloat(1000, 1400)",
        "hideoutMissionRogueryXp = randomInt(700, 1000) on success, randomInt(225, 400) on failure",
        "alleyInitialMainHeroXp = 1500; alleyDailyMainHeroXp = 40; alleyDailyAssignedClanMemberXp = 200",
        "alleySuccessfulDefenseMainHeroXp = 6000",
        "persuasionXp = difficultyEnumValue * 5 * argumentDifficultyBonusCoefficient",
        "warehouseProductionTradeXp = 0.1 * productionBaseValue",
        "charmRelationXp = round(relationChange * branchMultiplier), with branch multipliers built from 20, 10, 20, and 30",
        "```",
        "",
        f"Alley constants found: `{constants_text(alley_initial)} | {constants_text(alley_daily_main)} | {constants_text(alley_daily_assigned)} | {constants_text(alley_defense)}`",
        f"Activity constants found: `{constants_text(tournament)} | {constants_text(hideout_ghost)} | {constants_text(hideout_end)} | {constants_text(persuasion)} | {constants_text(workshop)} | {constants_text(charm_relation)}`",
        "",
        "## Scan Groups",
        "",
    ]

    methods_by_key = {method_key(method): method for method in payload.get("methods", [])}
    for scan in payload.get("scans", []):
        lines += [
            f"### {scan['title']}",
            "",
            *[f"- {note}" for note in scan.get("notes", [])],
            f"- Queries: `{', '.join(scan.get('queries', []))}`",
            f"- Methods scanned: {scan.get('methods_scanned', 0)}",
            f"- Methods matched in scan: {scan.get('methods_matched', 0)}",
            "",
            "| Method | Constants | IL bytes | Matched queries |",
            "| --- | --- | ---: | --- |",
        ]
        for key in scan.get("method_keys", []):
            method = methods_by_key.get(key)
            if method is None:
                continue
            constants = format_constants(method.get("numeric_constants", []), limit=12)
            queries = ", ".join(method.get("matched_queries", []))
            lines.append(
                "| {method} | {constants} | {il_bytes} | {queries} |".format(
                    method=table_escape(f"`{method.get('type')}.{method.get('method')}`"),
                    constants=table_escape(constants),
                    il_bytes=method.get("il_bytes", 0),
                    queries=table_escape(queries),
                )
            )
        lines.append("")

    lines += [
        "## Outputs",
        "",
        f"- JSON: `{display_path(json_output, workspace)}`",
        f"- Report: `{display_path(path, workspace)}`",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_insights_report(payload: dict[str, Any], path: Path, workspace: Path, formula_report_path: Path) -> None:
    lines = [
        "# Bannerlord XP Insights",
        "",
        f"Generated: {payload.get('generated_at', '')}",
        "",
        "This is the approachable companion to `Data/generated/reports/xp-formulas.md`. The formula report keeps the evidence trail; this guide turns the same findings into gameplay and analysis notes.",
        "",
        "## Fast Takeaways",
        "",
        "- XP usually has three parts: how much raw XP an action creates, which multiplier stack touches it, and which skill or troop stack receives it.",
        "- Combat XP cares about target value and effective damage, not just the damage number shown on screen.",
        "- A lethal hit is special: damage is capped at target max HP, then a kill adds another target max HP chunk. Overkill beyond max HP does not keep scaling.",
        "- Ranged difficulty is a real XP lever. Distance helps, lateral movement helps, and headshots multiply difficulty by `1.2`.",
        "- Riding XP from mounted actions is separate from weapon XP, so mounted ranged play can look like it pays unusually well even when the weapon XP formula is unchanged.",
        "- Learning rate can dominate everything. A high-value action at zero learning rate is still effectively wasted for that skill.",
        "- Troop XP is capacity-based. Stacks that still need XP toward an upgrade can absorb shared XP; stacks that are already capped for upgrades stop being useful sinks.",
        "",
        "## Combat Tips",
        "",
        "Combat hit XP starts from this shape:",
        "",
        "```text",
        "baseXp = 0.4 * attackerPower * targetPower * effectiveDamage * missionTypeMultiplier",
        "effectiveDamage = min(damage, targetHp) + targetHp if the hit is fatal",
        "```",
        "",
        "- Full-health one-shot kills are valuable because they can count as roughly two target-HP chunks: one from capped damage and one from the fatal branch.",
        "- Massive overkill is less special than it feels. Once damage reaches target max HP, extra damage past that point does not increase the damage chunk.",
        "- Stronger targets matter because target troop power is in the base formula. Farming very weak enemies should fall off even if they die quickly.",
        "- Mission type matters: battle is `1.0x`, simulation battle is `0.9x`, tournament is about `0.33x`, and practice fight is `0.0625x`.",
        "- Training in practice fights is therefore a very poor direct combat-XP farm compared with real battles.",
        "",
        "## Ranged Difficulty",
        "",
        "Shot difficulty is built from distance and relative lateral movement, then clamped before the headshot bonus:",
        "",
        "```text",
        "rawDifficulty = 0.3 * ((distance + 4) / 4) * ((4 + lateralMotion * relativeSpeed) / 4)",
        "shotDifficulty = clamp(rawDifficulty, 1, 12)",
        "headshotDifficulty = shotDifficulty * 1.2",
        "```",
        "",
        "- Long shots help directly.",
        "- Targets moving across your aim line are better than targets moving straight toward or away from you.",
        "- Headshots do not add a separate XP award; they raise shot difficulty, which then raises the ranged XP multiplier.",
        "- Non-Bow ranged skills can reach about `3.0x` final ranged XP from capped shot difficulty. Bow uses a smaller skill factor and tops out around `2.0x`.",
        "- The theoretical dream shot is long range, high lateral movement, and a headshot on a valuable target that dies from the hit.",
        "",
        "## Mounted Play",
        "",
        "Mounted actions can produce Riding XP on top of the main action XP:",
        "",
        "```text",
        "ridingXp = baseXpAmount * (1 + horseDifficulty * 0.02)",
        "```",
        "",
        "- A harder horse increases Riding XP by about `2%` per horse difficulty point.",
        "- Mounted ranged play can stack weapon XP, shot-difficulty XP, and Riding XP. That explains why horseback long shots can feel so rewarding.",
        "- Travel on horse also awards Riding XP from `roundRandomized(0.3 * speed)`, routed through the same horse-difficulty bonus.",
        "",
        "## Learning Rate And Build Planning",
        "",
        "Skill XP is scaled by learning rate when the award is focus-affected:",
        "",
        "```text",
        "skillXpDelta = rawXp * genericXpMultiplier * learningRate",
        "peakLearningRange = 10 * (attribute - 1) + 30 * focus",
        "skillLimit = 4 + 14 * (attribute - 1) + 40 * focus",
        "```",
        "",
        "- Focus is narrow but powerful: it helps one skill and pushes both peak learning range and skill limit up.",
        "- Attribute points help every skill under that attribute. Raising Control helps Bow, Crossbow, and Throwing at the same time.",
        "- Past peak learning range, the over-limit penalty starts cutting learning rate. At the skill limit, learning reaches zero.",
        "- The best time to do expensive or rare XP actions is while the target skill is still inside a good learning range.",
        "- Endurance attribute perks remain build-warping because their permanent attribute points can stretch later skill limits across the whole attribute group.",
        "",
        "## Troop XP",
        "",
        "The direct troop battle XP reward grows roughly quadratically with troop level:",
        "",
        "| Killed troop level | XP reward |",
        "| ---: | ---: |",
        "| 1 | 16 |",
        "| 6 | 48 |",
        "| 11 | 96 |",
        "| 16 | 161 |",
        "| 21 | 243 |",
        "| 26 | 341 |",
        "",
        "- Higher-level kills are much better troop-XP fuel than low-level kills.",
        "- Shared XP distribution is proportional to each stack's remaining upgrade capacity.",
        "- If a stack is already sitting on enough XP to upgrade, it stops being a good shared-XP target. Upgrading or diversifying stacks can keep XP from bunching up awkwardly.",
        "- Daily training from towns, buildings, and perks is useful background pressure, but the battle reward formula is the larger lever for fast troop growth.",
        "",
        "## Smithing And Value-Based XP",
        "",
        "Smithing formulas are strongly value-based:",
        "",
        "```text",
        "refiningXp = round(0.3 * outputMaterialValue * outputCount)",
        "smeltingXp = round(0.02 * itemValue)",
        "smithingCraftingOrderXp = round(0.1 * itemValue)",
        "smithingFreeBuildXp = round(0.02 * itemValue)",
        "```",
        "",
        "- Item value is the main signal. More valuable inputs and outputs should matter more than the count of actions alone.",
        "- Crafting-order smithing XP uses `0.1 * itemValue`, which is five times the free-build `0.02 * itemValue` rate before other order logic.",
        "- Refining XP is based on produced material value and output count, so valuable refinement outputs can be more interesting than they look.",
        "- Crafting order experience has extra tier and requirement checks; keep that one as a candidate for deeper hand-reading before turning it into final player advice.",
        "",
        "## Activity XP",
        "",
        "- Tournament model XP is `500` to one random skill from five equal bands: One Handed, Two Handed, Polearm, Riding, or Athletics.",
        "- Hideout Roguery XP is sizable: ghost clearing rolls `1000-1400`, mission success rolls `700-1000`, and failure rolls `225-400`.",
        "- Alley XP has big spikes: initial main hero XP is `1500`, successful defense is `6000`, daily main hero XP is `40`, and daily assigned clan member XP is `200`.",
        "- Persuasion XP scales with difficulty and argument coefficient: `difficultyEnumValue * 5 * argumentDifficultyBonusCoefficient`.",
        "- Warehouse production Trade XP is `0.1 * productionBaseValue`.",
        "- Charm relation XP uses relation change times a branch multiplier. The multiplier branches need friendlier naming, but the constants suggest leaders and notables can matter a lot.",
        "",
        "## Things Worth Checking Next",
        "",
        "- Decode the exact branch names in `GetCharmExperienceFromRelationGain` so the charm multipliers become player-readable.",
        "- Hand-read crafting-order bonus and penalty checks; the IL shows a base, tier factor, and halving path, but the condition names matter.",
        "- Check whether discard/donation XP candidates need a dedicated insight section once the scan query is widened or hand-read.",
        "- Connect perk effects to these formulas, especially troop training perks, battle XP perks, smithing learning perks, and ranged shot-difficulty helpers.",
        "",
        "## Source",
        "",
        f"- Formula evidence: `{display_path(formula_report_path, workspace)}`",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def extract_xp_formulas(
    workspace: Path,
    game_root: Path | None,
    json_output: Path,
    markdown_output: Path,
    insights_output: Path,
    include_il: bool,
    keep_temp: bool,
) -> None:
    resolved_game_root = resolve_game_root(game_root)
    temp_parent = workspace / "Data" / "generated"
    temp_parent.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix=".xp_formula_scan_", dir=temp_parent))
    try:
        scan_payloads = [
            run_find_methods(
                workspace=workspace,
                game_root=resolved_game_root,
                scan=scan,
                include_il=include_il,
                temp_dir=temp_dir,
            )
            for scan in FORMULA_SCANS
        ]
        payload = merge_scan_payloads(scan_payloads, include_il=include_il)
        write_json(json_output, payload)
        write_formula_report(payload, markdown_output, workspace, json_output)
        write_insights_report(payload, insights_output, workspace, markdown_output)
        print(f"Formula methods written: {json_output}")
        print(f"Formula report written: {markdown_output}")
        print(f"Formula insights written: {insights_output}")
        print(f"Methods matched: {payload['methods_matched']}")
        if keep_temp:
            kept = workspace / "Data" / "generated" / "xp-formula-scan-temp"
            if kept.exists():
                shutil.rmtree(kept)
            shutil.move(str(temp_dir), kept)
            print(f"Temporary scan files kept: {kept}")
    finally:
        if not keep_temp:
            shutil.rmtree(temp_dir, ignore_errors=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract broader Bannerlord XP formula candidates from local assemblies.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--game-root", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    parser.add_argument("--insights-output", type=Path, default=None)
    parser.add_argument("--no-il", action="store_true", help="Do not keep IL instructions in the merged JSON output.")
    parser.add_argument("--keep-temp", action="store_true", help="Keep per-scan temporary JSON files under Data/generated/xp-formula-scan-temp.")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    json_output = args.json_output or workspace / "Data" / "generated" / "xp-formula-methods.json"
    markdown_output = args.markdown_output or workspace / "Data" / "generated" / "reports" / "xp-formulas.md"
    insights_output = args.insights_output or workspace / "Data" / "generated" / "reports" / "xp-insights.md"
    extract_xp_formulas(
        workspace=workspace,
        game_root=args.game_root,
        json_output=json_output,
        markdown_output=markdown_output,
        insights_output=insights_output,
        include_il=not args.no_il,
        keep_temp=args.keep_temp,
    )


if __name__ == "__main__":
    main()
