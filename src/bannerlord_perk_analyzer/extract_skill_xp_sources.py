from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

try:
    from .postprocess import default_workspace
    from .xp_reports import display_path, table_escape
except ImportError:
    from postprocess import default_workspace
    from xp_reports import display_path, table_escape


SCAN_ASSEMBLIES = [
    "TaleWorlds.CampaignSystem",
    "SandBox",
    "StoryMode",
]

SCAN_QUERIES = [
    "AddSkillXp",
    "DefaultSkills.get_",
    "GetSkillXp",
    "GetCharmExperience",
    "GetTradeXp",
    "GetRogueryXpGain",
    "GetOrderExperience",
]

SKILL_ORDER = [
    "One Handed",
    "Two Handed",
    "Polearm",
    "Bow",
    "Crossbow",
    "Throwing",
    "Riding",
    "Athletics",
    "Smithing",
    "Scouting",
    "Tactics",
    "Roguery",
    "Charm",
    "Leadership",
    "Trade",
    "Steward",
    "Medicine",
    "Engineering",
]

WEAPON_SKILLS = ["One Handed", "Two Handed", "Polearm", "Bow", "Crossbow", "Throwing"]

SKILL_NAME_MAP = {
    "OneHanded": "One Handed",
    "TwoHanded": "Two Handed",
    "Polearm": "Polearm",
    "Bow": "Bow",
    "Crossbow": "Crossbow",
    "Throwing": "Throwing",
    "Riding": "Riding",
    "Athletics": "Athletics",
    "Crafting": "Smithing",
    "Scouting": "Scouting",
    "Tactics": "Tactics",
    "Roguery": "Roguery",
    "Charm": "Charm",
    "Leadership": "Leadership",
    "Trade": "Trade",
    "Steward": "Steward",
    "Medicine": "Medicine",
    "Engineering": "Engineering",
}


SUMMARY_BY_METHOD = {
    "DefaultSkillLevelingManager.OnAIPartiesTravel": "Scouting XP for AI party travel: forest terrain uses roundRandomized(5), other terrain uses roundRandomized(3), and caravan parties receive half.",
    "DefaultSkillLevelingManager.OnHideoutSpotted": "Scouting party-skill exercise when a hideout is spotted; amount is 100 for the Scout party role.",
    "DefaultSkillLevelingManager.OnTrackDetected": "Scouting party-skill exercise when a track is detected; amount comes from MapTrackModel.GetSkillFromTrackDetected(track) for the Scout party role.",
    "DefaultSkillLevelingManager.OnTraverseTerrain": "Scouting party-skill exercise while traversing terrain; requires speed above 1 and calculated XP of at least 5.",
    "CaravanAmbushIssue.AlternativeSolutionEndWithSuccessConsequence": "Alternative solution reward: the assigned hero receives Scouting XP plus a random melee skill reward.",
    "SimpleAgentOrigin.TaleWorlds.Core.IAgentOriginBase.OnScoreHit": "Mission score-hit hook that applies weapon-skill XP to hero attackers.",
    "MobilePartyTrainingBehavior.OnDailyTickParty": "Bow Trainer perk hook: daily Bow XP goes to the hero party member with the lowest Bow skill.",
    "DefaultSkillLevelingManager.OnCombatHit": "Combat hit/kill XP; the skill comes from the weapon used, so it can feed any combat weapon skill.",
    "DefaultSkillLevelingManager.OnSimulationCombatKill": "Simulation kill XP; weapon XP is based on the killed troop reward, with extra Riding or Athletics movement XP.",
    "DefaultSkillLevelingManager.OnTravelOnFoot": "Athletics XP while traveling on foot: roundRandomized(0.2 * speed) + 1.",
    "DefaultSkillLevelingManager.OnGainingRidingExperience": "Riding XP from mounted actions, scaled by horse difficulty.",
    "DefaultTournamentModel.GetSkillXpGainFromTournament": "Tournament reward model: 500 XP to one random skill from five equal bands.",
    "DefaultSkillLevelingManager.OnTradeProfitMade": "Trade XP from profitable trade.",
    "DefaultSkillLevelingManager.OnWarehouseProduction": "Trade XP from warehouse production value.",
    "DefaultSkillLevelingManager.OnGainRelation": "Charm XP from relation gain.",
    "DefaultSkillLevelingManager.OnBoardGameWonAgainstLord": "Steward XP from winning board games against lords; constants show 20, 50, and 100 branches.",
    "DefaultSkillLevelingManager.OnLeadingArmy": "Leadership XP from leading an army.",
    "DefaultSkillLevelingManager.OnInfluenceSpent": "Steward XP from spending influence through a party-leader skill exercise hook.",
    "DefaultSkillLevelingManager.OnTacticsUsed": "Tactics XP from simulated/commander tactics use.",
    "DefaultSkillLevelingManager.OnBattleEnded": "Post-battle skill XP hook; constants suggest tiered battle/participation rewards.",
    "DefaultSkillLevelingManager.OnUpgradeTroops": "Skill XP from upgrading troops; the upgrade model returns 10 as the base skill XP.",
    "DefaultSkillLevelingManager.OnHeroHealedWhileWaiting": "Medicine XP when a hero heals while waiting.",
    "DefaultSkillLevelingManager.OnRegularTroopHealedWhileWaiting": "Medicine XP when regular troops heal while waiting.",
    "DefaultSkillLevelingManager.OnSurgeryApplied": "Medicine XP from surgery/casualty treatment.",
    "DefaultSkillLevelingManager.OnSieging": "Engineering XP while conducting a siege.",
    "DefaultSkillLevelingManager.OnSiegeEngineBuilt": "Engineering XP when siege engines are built.",
    "DefaultSkillLevelingManager.OnSiegeEngineDestroyed": "Engineering XP when siege engines are destroyed.",
    "DefaultSkillLevelingManager.OnWallBreached": "Engineering XP when a wall is breached.",
}


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


def run_find_methods(workspace: Path, game_root: Path, output: Path) -> dict[str, Any]:
    project = workspace / "tools" / "BannerlordExtractor" / "BannerlordExtractor.csproj"
    if not project.exists():
        raise SystemExit(f"Extractor project is missing: {project}")

    command = [
        "dotnet",
        "run",
        "--project",
        str(project),
        "--",
        "find-methods",
        "--game-root",
        str(game_root),
        "--include-il",
        "--output",
        str(output),
    ]
    for assembly in SCAN_ASSEMBLIES:
        command.extend(["--assembly", assembly])
    for query in SCAN_QUERIES:
        command.extend(["--query", query])

    subprocess.run(command, check=True)
    return read_json(output)


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


def format_constants(values: list[Any], limit: int = 10) -> str:
    text = ", ".join(format_number(value) for value in values[:limit])
    if len(values) > limit:
        text += ", ..."
    return text


def method_key(method: dict[str, Any]) -> str:
    return f"{method.get('assembly', '')}|{method.get('type', '')}|{method.get('method', '')}|{method.get('signature', '')}"


def type_short_name(type_name: str) -> str:
    return type_name.split("+")[-1].split(".")[-1]


def full_method_name(method: dict[str, Any]) -> str:
    return f"{method.get('type')}.{method.get('method')}"


def short_method_name(method: dict[str, Any]) -> str:
    return f"{type_short_name(str(method.get('type', '')))}.{method.get('method')}"


def source_summary(method: dict[str, Any]) -> str:
    short_name = short_method_name(method)
    if short_name in SUMMARY_BY_METHOD:
        return SUMMARY_BY_METHOD[short_name]

    name = str(method.get("method", ""))
    if name.startswith("On"):
        words = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name[2:]).lower()
        return f"Skill XP hook for {words}."
    if "AlternativeSolution" in name:
        return "Issue alternative-solution skill XP reward."
    if name.startswith("GetSkillXp") or name.startswith("Get") and "Experience" in name:
        return "Model method that returns a skill XP amount."
    return "Skill XP source candidate."


def referenced_text(method: dict[str, Any]) -> str:
    return "\n".join(str(value) for value in (method.get("referenced_members", []) + method.get("il", [])))


def referenced_skills(method: dict[str, Any]) -> list[str]:
    matches = re.findall(r"TaleWorlds\.Core\.DefaultSkills\.get_([A-Za-z0-9_]+)\(", referenced_text(method))
    skills = [SKILL_NAME_MAP.get(match, match) for match in matches]
    return sorted(set(skills), key=lambda skill: SKILL_ORDER.index(skill) if skill in SKILL_ORDER else 999)


def is_skill_xp_candidate(method: dict[str, Any]) -> bool:
    refs = referenced_text(method)
    if "AddSkillXp" in refs or "SkillExercised" in refs:
        return True
    name = str(method.get("method", ""))
    return bool(
        re.search(
            r"GetSkillXp|GetCharmExperience|GetTradeXp|GetRogueryXpGain|GetOrderExperience",
            name,
        )
    )


def inferred_skills(method: dict[str, Any]) -> list[str]:
    refs = referenced_text(method)
    method_name = str(method.get("method", ""))
    skills: list[str] = []
    if "CombatXpModel.GetSkillForWeapon" in refs or method_name == "OnCombatHit":
        skills.extend(WEAPON_SKILLS)
    return skills


def confidence_for(method: dict[str, Any], skills: list[str]) -> str:
    refs = referenced_text(method)
    if "CombatXpModel.GetSkillForWeapon" in refs:
        return "inferred"
    if "SkillExercised" in refs or "AddSkillXp" in refs:
        return "high"
    if skills:
        return "medium"
    return "candidate"


def extract_sources(payload: dict[str, Any]) -> list[dict[str, Any]]:
    sources_by_key: dict[str, dict[str, Any]] = {}
    for method in payload.get("methods", []):
        if not is_skill_xp_candidate(method):
            continue

        skills = referenced_skills(method)
        for skill in inferred_skills(method):
            if skill not in skills:
                skills.append(skill)
        skills = sorted(set(skills), key=lambda skill: SKILL_ORDER.index(skill) if skill in SKILL_ORDER else 999)
        if not skills:
            continue

        key = method_key(method)
        sources_by_key[key] = {
            "assembly": method.get("assembly", ""),
            "type": method.get("type", ""),
            "method": method.get("method", ""),
            "signature": method.get("signature", ""),
            "short_method": short_method_name(method),
            "full_method": full_method_name(method),
            "skills": skills,
            "summary": source_summary(method),
            "constants": method.get("numeric_constants", []),
            "confidence": confidence_for(method, skills),
            "matched_queries": method.get("matched_queries", []),
        }

    return sorted(
        sources_by_key.values(),
        key=lambda source: (
            min(SKILL_ORDER.index(skill) for skill in source["skills"] if skill in SKILL_ORDER),
            source["short_method"],
        ),
    )


def source_rows_for_skill(sources: list[dict[str, Any]], skill: str) -> list[dict[str, Any]]:
    return [source for source in sources if skill in source.get("skills", [])]


def write_markdown(payload: dict[str, Any], sources: list[dict[str, Any]], path: Path, workspace: Path, json_output: Path) -> None:
    by_skill = {skill: source_rows_for_skill(sources, skill) for skill in SKILL_ORDER}

    lines = [
        "# Bannerlord Skill XP Sources",
        "",
        f"Generated: {payload.get('generated_at', '')}",
        "",
        "This report groups extracted skill-XP source candidates by Bannerlord skill. It is generated from local compiled assemblies by scanning for skill XP sinks such as `AddSkillXp`, party/personal/settlement skill exercise hooks, and skill XP model methods.",
        "",
        "## Reading Notes",
        "",
        "- `high` means the method directly sends a named skill into an XP sink.",
        "- `medium` means the method returns or calculates a skill XP amount but another caller applies it.",
        "- `inferred` means the skill is selected dynamically, usually from the weapon used in combat.",
        "- `Smithing` appears as `Crafting` in the compiled `DefaultSkills` API; this report displays the player-facing skill name.",
        "- This is a coverage map, not a final prose guide. Some event branches still need hand-reading before we turn them into optimized player advice.",
        "",
        "## Scouting Detail",
        "",
        "The scan found these concrete Scouting XP paths:",
        "",
        "- `OnTraverseTerrain`: Scouting party-skill exercise while a mobile party traverses terrain. The formula uses party speed, party size, and a terrain multiplier. Desert, snow, forest, and dune terrain use the higher `0.25` multiplier; other terrain uses `0.15`; caravans get half. XP is only applied when the calculated amount reaches at least `5`.",
        "- `OnTrackDetected`: Scouting party-skill exercise for the main party when a track is detected. The amount comes from `MapTrackModel.GetSkillFromTrackDetected(track)`, and the party role is `Scout`.",
        "- `OnHideoutSpotted`: Scouting party-skill exercise worth `100`, also for the `Scout` role.",
        "- `OnAIPartiesTravel`: direct Scouting XP for AI party travel. Forest terrain gives `roundRandomized(5)`, other terrain gives `roundRandomized(3)`, and caravan parties receive half.",
        "- `CaravanAmbushIssue.AlternativeSolutionEndWithSuccessConsequence`: the assigned hero gets `600 + 800 * IssueDifficultyMultiplier` Scouting XP, plus the same amount to a random melee skill.",
        "",
        "## Skill Coverage Summary",
        "",
        "| Skill | Source count |",
        "| --- | ---: |",
    ]
    for skill in SKILL_ORDER:
        lines.append(f"| {skill} | {len(by_skill[skill])} |")

    lines.append("")
    lines.append("## Sources By Skill")
    lines.append("")

    for skill in SKILL_ORDER:
        rows = by_skill[skill]
        lines += [
            f"### {skill}",
            "",
        ]
        if not rows:
            lines += [
                "No concrete skill-specific XP source was found in this scan.",
                "",
            ]
            continue

        lines += [
            "| Source | Summary | Constants | Confidence |",
            "| --- | --- | --- | --- |",
        ]
        for source in rows:
            lines.append(
                "| {source} | {summary} | {constants} | {confidence} |".format(
                    source=table_escape(f"`{source['short_method']}`"),
                    summary=table_escape(source["summary"]),
                    constants=table_escape(format_constants(source.get("constants", []))),
                    confidence=source["confidence"],
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


def extract_skill_xp_sources(
    workspace: Path,
    game_root: Path | None,
    json_output: Path,
    markdown_output: Path,
    skip_scan: bool,
) -> None:
    if skip_scan and json_output.exists():
        payload = read_json(json_output)
    else:
        payload = run_find_methods(workspace, resolve_game_root(game_root), json_output)
    sources = extract_sources(payload)
    payload["skill_xp_sources"] = sources
    payload["skill_xp_source_count"] = len(sources)
    write_json(json_output, payload)
    write_markdown(payload, sources, markdown_output, workspace, json_output)
    print(f"Skill XP methods written: {json_output}")
    print(f"Skill XP report written: {markdown_output}")
    print(f"Skill XP sources: {len(sources)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Bannerlord skill XP sources grouped by skill.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--game-root", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    parser.add_argument("--skip-scan", action="store_true", help="Reuse the existing JSON output and regenerate only the markdown.")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    json_output = args.json_output or workspace / "Data" / "generated" / "skill-xp-source-methods.json"
    markdown_output = args.markdown_output or workspace / "Data" / "generated" / "reports" / "skill-xp-sources.md"
    extract_skill_xp_sources(
        workspace=workspace,
        game_root=args.game_root,
        json_output=json_output,
        markdown_output=markdown_output,
        skip_scan=args.skip_scan,
    )


if __name__ == "__main__":
    main()
