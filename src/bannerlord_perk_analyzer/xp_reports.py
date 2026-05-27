from __future__ import annotations

from pathlib import Path
from typing import Any


CATEGORY_ORDER = [
    "hero progression",
    "combat xp",
    "troop xp",
    "healing xp",
    "crafting xp",
    "activity xp",
    "xp multiplier",
    "other xp",
]

ANCHOR_METHODS = [
    "TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.AddSkillXp",
    "TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GainRawXp",
    "TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.CalculateLearningRate",
    "TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetXpFromHit",
    "TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetBattleXpBonusFromPerks",
    "TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GetEffectiveDailyExperience",
    "TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GenerateSharedXp",
    "Helpers.MobilePartyHelper.CanTroopGainXp",
    "Helpers.MobilePartyHelper.PartyAddSharedXp",
    "TaleWorlds.CampaignSystem.MapEvents.MapEventParty.CommitXpGain",
    "TaleWorlds.CampaignSystem.CampaignBehaviors.CampaignBattleRecoveryBehavior.GiveTroopXp",
    "TaleWorlds.CampaignSystem.Roster.TroopRoster.AddXpToTroop",
]


def has_method(methods: list[dict[str, Any]], method_name: str) -> bool:
    return any(row.get("method") == method_name for row in methods)


def table_escape(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def display_path(path: Path, workspace: Path) -> str:
    full_path = path.resolve()
    try:
        return str(full_path.relative_to(workspace.resolve()))
    except ValueError:
        return "<local path>"


def combat_xp_details(methods: list[dict[str, Any]]) -> list[str]:
    if not has_method(methods, "GetXpFromHit"):
        return []

    lines = [
        "## Combat XP Details",
        "",
        "### Damage And Kill XP",
        "",
        "`DefaultCombatXpModel.GetXpFromHit(...)` builds the direct combat XP award from troop power, effective damage, mission type, and perk factors.",
        "",
        "```text",
        "targetHp = attackedTroop.MaxHitPoints()",
        "attackerPower = MilitaryPowerModel.GetTroopPower(attackerTroop, attackerSide, context, leaderSimulationModifier) + 0.5",
        "targetPower = MilitaryPowerModel.GetTroopPower(attackedTroop, oppositeSide, context, leaderSimulationModifier) + 0.5",
        "effectiveDamage = min(damage, targetHp) + (targetHp if isFatal else 0)",
        "baseXp = 0.4 * attackerPower * targetPower * effectiveDamage * missionTypeMultiplier",
        "finalXp = baseXp with applicable perk factors",
        "```",
        "",
        "Kill credit is the `isFatal` branch: it adds one full target max-HP chunk after damage has already been capped at target max HP. A full-health kill can therefore count as roughly two target-HP chunks of effective damage.",
        "",
        "| Mission type | Multiplier |",
        "| --- | ---: |",
        "| Battle | 1 |",
        "| Practice fight | 0.0625 |",
        "| Tournament | 0.33 |",
        "| Simulation battle | 0.9 |",
        "| No XP | 0 |",
        "",
        "### Shot Difficulty",
        "",
    ]

    if has_method(methods, "GetXpMultiplierFromShotDifficulty"):
        lines += [
            "A targeted module scan found the source value in `TaleWorlds.MountAndBlade.Mission.GetShootDifficulty(affectedAgent, affectorAgent, isHeadShot)`:",
            "",
            "```text",
            "relativeVelocity = affectedAgent.MovementVelocity - affectorAgent.MovementVelocity",
            "shotVector = affectedAgent.Position - affectorAgent.Position",
            "distance = length(shotVector)",
            "relativeSpeed = length(relativeVelocity)",
            "lateralMotion = perpendicular share of relativeVelocity against shotVector",
            "rawDifficulty = 0.3 * ((distance + 4) / 4) * ((4 + lateralMotion * relativeSpeed) / 4)",
            "shotDifficulty = clamp(rawDifficulty, 1, 12)",
            "if isHeadShot: shotDifficulty *= 1.2",
            "```",
            "",
            "So distance matters directly, target/shooter relative movement matters when it is lateral to the shot line, and headshots multiply the clamped difficulty by `1.2`. That headshot multiplier is what lets difficulty reach the campaign XP cap of `14.4`; without a headshot, the mission-side difficulty is capped at `12`.",
            "",
            "`GetXpMultiplierFromShotDifficulty(shotDifficulty)` then caps `shotDifficulty` at `14.4`, and linearly maps the range from `1` to `14.4` onto an XP factor from `0` to `2`:",
            "",
            "```text",
            "cappedDifficulty = min(shotDifficulty, 14.4)",
            "shotDifficultyFactor = lerp(0, 2, (cappedDifficulty - 1) / 13.4)",
            "skillFactor = 0.5 if the hit skill is Bow else 1.0",
            "finalXp = baseXp * (1 + skillFactor * shotDifficultyFactor)",
            "```",
            "",
            "| Shot difficulty | Raw factor | Final Bow multiplier | Final non-Bow ranged multiplier |",
            "| ---: | ---: | ---: | ---: |",
            "| 1 | 0.00 | 1.00x | 1.00x |",
            "| 3 | 0.30 | 1.15x | 1.30x |",
            "| 5 | 0.60 | 1.30x | 1.60x |",
            "| 7.7 | 1.00 | 1.50x | 2.00x |",
            "| 12 | 1.64 | 1.82x | 2.64x |",
            "| 14.4+ | 2.00 | 2.00x | 3.00x |",
            "",
        ]
    else:
        lines += [
            "No shot-difficulty multiplier method was found in this extraction. Re-run with `--deep-scan-callers --include-il` before assuming ranged difficulty is absent.",
            "",
        ]

    if has_method(methods, "OnGainingRidingExperience"):
        lines += [
            "### Horseback XP",
            "",
            "`DefaultSkillLevelingManager.OnGainingRidingExperience(hero, baseXpAmount, horse)` awards separate Riding XP when a horse is present:",
            "",
            "```text",
            "ridingXp = baseXpAmount * (1 + horse.Difficulty * 0.02)",
            "```",
            "",
            "That means mounted actions can look like they produce more XP overall even when `GetXpFromHit` itself has no direct `while mounted` multiplier. Some mounted ranged shots may also have higher shot difficulty upstream.",
            "",
        ]

    lines += [
        "### Perk Factors",
        "",
        "`GetBattleXpBonusFromPerks` applies perk factors after base hit XP is constructed. The extracted references include `OneHanded.Trainer`, `TwoHanded.BaptisedInBlood`, `Throwing.Resourceful`, `OneHanded.CorpsACorps`, `OneHanded.LeadByExample`, `Crossbow.MountedCrossbowman`, `Bow.BullsEye`, `Roguery.NoRestForTheWicked`, `TwoHanded.ProjectileDeflection`, `Polearm.Guards`, and `Leadership.InspiringLeader`.",
        "",
    ]
    return lines


def write_xp_markdown(
    payload: dict[str, Any],
    path: Path,
    workspace: Path,
    json_output_path: Path,
    il_output_path: Path | None = None,
) -> None:
    methods = list(payload.get("methods", []))
    generated_at = payload.get("generated_at", "")
    lines = [
        "# Bannerlord XP Award Extraction",
        "",
        f"Generated: {generated_at}",
        "",
        "This report is extracted from local compiled assemblies. It is a map of XP-related model methods, constants, and XP-relevant references, not source comments or decompiled C#.",
        "",
        "## Inputs",
        "",
        "- Game root: local path omitted; provided by `--game-root` or `BANNERLORD_GAME_ROOT`",
        "- Assemblies loaded: " + ", ".join(f"`{assembly}`" for assembly in payload.get("assemblies_loaded", [])),
        f"- Methods scanned: {payload.get('methods_scanned', 0)}",
        f"- XP-related methods matched: {payload.get('methods_matched', 0)}",
        f"- Deep caller scan: {bool(payload.get('deep_scan_callers'))}",
        f"- Include abstract contracts: {bool(payload.get('include_contracts'))}",
    ]
    if payload.get("load_errors"):
        lines.append(f"- Load warnings: {len(payload['load_errors'])}")

    lines += [
        "",
        "## Reading Notes",
        "",
        "- `hero progression` is where hero skill XP is accepted, scaled, and converted into skill levels and character levels.",
        "- `combat xp` covers hit/kill XP and perk bonuses applied to battle XP.",
        "- `troop xp` covers shared party XP, daily training XP, troop roster XP, and upgrade-related XP.",
        "- `activity xp` covers non-combat sources such as charm, persuasion, tournaments, workshops, alleys, and hideouts.",
        "- Numeric constants are raw IL constants. Some are formula values; some are indexes, enum values, or branch helpers, so they need review before becoming prose.",
        "- Run with `--deep-scan-callers` to inspect every method body for calls into XP sinks. That is slower, especially if extra assemblies are included.",
        "",
    ]

    by_full_name = {f"{row.get('type')}.{row.get('method')}": row for row in methods}
    anchors_found = [by_full_name[anchor] for anchor in ANCHOR_METHODS if anchor in by_full_name]
    if anchors_found:
        lines += ["## High-Signal Entry Points", ""]
        for row in anchors_found:
            lines.append(f"- `{row['type']}.{row['method']}` ({row['category']}, IL bytes: {row['il_bytes']})")
        lines.append("")

    lines += combat_xp_details(methods)

    for category in CATEGORY_ORDER:
        rows = [row for row in methods if row.get("category") == category]
        if not rows:
            continue
        lines += [
            f"## {category[:1].upper() + category[1:]}",
            "",
            "| Method | IL bytes | Constants | XP references |",
            "| --- | ---: | --- | --- |",
        ]
        for row in rows:
            constants = ", ".join(str(value) for value in row.get("numeric_constants", [])[:12])
            if len(row.get("numeric_constants", [])) > 12:
                constants += ", ..."
            refs = "<br>".join(str(value) for value in row.get("xp_references", [])[:5])
            if len(row.get("xp_references", [])) > 5:
                refs += "<br>..."
            method_cell = table_escape(f"`{row.get('type')}.{row.get('method')}`")
            lines.append(f"| {method_cell} | {row.get('il_bytes', 0)} | {table_escape(constants)} | {table_escape(refs)} |")
        lines.append("")

    if payload.get("load_errors"):
        lines += ["## Load Warnings", ""]
        lines.extend(f"- {warning}" for warning in payload["load_errors"])
        lines.append("")

    lines += [
        "## Outputs",
        "",
        f"- JSON index: `{display_path(json_output_path, workspace)}`",
    ]
    if il_output_path is not None:
        lines.append(f"- IL dump: `{display_path(il_output_path, workspace)}`")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_xp_il(payload: dict[str, Any], path: Path) -> None:
    lines = [
        "# Bannerlord XP Award IL Dump",
        "",
        f"Generated: {payload.get('generated_at', '')}",
        "",
    ]
    for row in payload.get("methods", []):
        il = row.get("il", [])
        if not il:
            continue
        lines += [
            f"## {row.get('type')}.{row.get('method')}",
            "",
            "```text",
            *[str(line) for line in il],
            "```",
            "",
        ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
