from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .postprocess import default_workspace
    from .utils import resolve_game_root, run_extractor
    from .xp_reports import display_path, table_escape
except ImportError:
    from postprocess import default_workspace
    from utils import resolve_game_root, run_extractor
    from xp_reports import display_path, table_escape


MECHANICAL_SUMMARIES = {
    "IncreasedMeleeDamage": "+{bonus} melee damage dealt by troops in the formation.",
    "IncreasedMeleeDamageAgainstMountedTroops": "+{bonus} melee damage dealt by troops in the formation against cavalry or mounted targets.",
    "IncreasedRangedDamage": "+{bonus} ranged damage dealt by troops in the formation.",
    "IncreasedChargeDamage": "+{bonus} charge damage dealt by mounted troops in the formation.",
    "DecreasedChargeDamage": "{bonus} charge damage taken by mounted troops in the formation.",
    "DecreasedRangedAccuracyPenalty": "{bonus} ranged accuracy penalty for ranged troops in the formation.",
    "DecreasedMoraleShock": "{bonus} morale penalty from casualties to troops in the formation.",
    "DecreasedMeleeAttackDamage": "{bonus} melee attack damage taken by troops in the formation.",
    "DecreasedRangedAttackDamage": "{bonus} ranged attack damage taken by troops in the formation.",
    "DecreasedShieldDamage": "{bonus} damage taken by shields of troops in the formation.",
    "IncreasedTroopMovementSpeed": "+{bonus} infantry movement speed in the formation.",
    "IncreasedMountMovementSpeed": "+{bonus} mount movement speed in the formation.",
    "IncreasedMoraleShockByMeleeTroops": "+{bonus} morale shock from melee troops in the formation.",
}

COMMANDER_SHORTLIST = {
    "IncreasedTroopMovementSpeed": "Core shock-infantry banner: tier 3 is the huge +30% foot movement breakpoint.",
    "IncreasedMountMovementSpeed": "Mounted version of the speed idea, but much smaller: tier 3 is +10% mount movement.",
    "DecreasedRangedAttackDamage": "Core anti-arrow banner. The raw game description string is misleading, but combat formulas use this as ranged damage taken reduction.",
    "DecreasedRangedAccuracyPenalty": "Specialist archer-commander banner for dense ranged formations.",
    "IncreasedMeleeDamage": "Looks strong on paper, but may be less valuable when elite shock troops already overkill common targets.",
}

USAGE_SCAN_ASSEMBLIES = [
    "TaleWorlds.Core",
    "TaleWorlds.MountAndBlade",
    "TaleWorlds.CampaignSystem",
    "SandBox",
    "SandBoxCore",
]

BANNER_MECHANICS = {
    "IncreasedMeleeDamage": {
        "applies_to": "Outgoing melee attack damage by troops in the active banner formation.",
        "formula_usage": "Added in the melee branch of ApplyDamageAmplifications.",
        "practical_read": "Best when it changes hits-to-kill; less valuable when elite melee troops already overkill.",
        "caveat": "Not ranged damage, charge damage, or a party-wide passive.",
    },
    "IncreasedMeleeDamageAgainstMountedTroops": {
        "applies_to": "Outgoing melee attack damage when the victim has a mount agent.",
        "formula_usage": "Added in ApplyDamageAmplifications after the victim-mounted check.",
        "practical_read": "Specialist anti-cavalry damage banner for formations fighting mounted targets.",
        "caveat": "Does nothing against foot troops.",
    },
    "IncreasedRangedDamage": {
        "applies_to": "Outgoing ranged/projectile damage by troops in the active banner formation.",
        "formula_usage": "Added in the ranged/consumable weapon branch of ApplyDamageAmplifications.",
        "practical_read": "Direct ranged lethality; better when ranged damage breakpoints matter.",
        "caveat": "Does not improve accuracy, projectile speed, or reload behavior.",
    },
    "IncreasedChargeDamage": {
        "applies_to": "Outgoing horse charge damage.",
        "formula_usage": "Added in the horse-charge branch of ApplyDamageAmplifications.",
        "practical_read": "Cavalry charge specialist effect.",
        "caveat": "Does not affect normal melee swings.",
    },
    "DecreasedChargeDamage": {
        "applies_to": "Incoming charge damage on the charge-damage branch.",
        "formula_usage": "Added as a negative factor in the charge branch of ApplyDamageAmplifications.",
        "practical_read": "Anti-charge durability for the relevant formation.",
        "caveat": "Not general melee or ranged resistance.",
    },
    "DecreasedRangedAccuracyPenalty": {
        "applies_to": "AgentDrivenProperties.WeaponInaccuracy for ranged weapons.",
        "formula_usage": "Added in SetPerkAndBannerEffectsOnAgent/SetBannerEffectsOnAgent, then written to WeaponInaccuracy.",
        "practical_read": "Reduces base weapon spread/inaccuracy. Tier 3 -8% means roughly 0.92x the affected inaccuracy component.",
        "caveat": "Not direct hit chance; does not touch movement, unsteady, or rotational accuracy penalties.",
    },
    "DecreasedMoraleShock": {
        "applies_to": "Morale penalty from casualties and panic.",
        "formula_usage": "Added in CalculateMaxMoraleChangeDueToAgentIncapacitated and CalculateMaxMoraleChangeDueToAgentPanicked.",
        "practical_read": "Keeps the formation morale steadier when troops die or panic.",
        "caveat": "Not HP, damage resistance, or troop survival chance.",
    },
    "DecreasedMeleeAttackDamage": {
        "applies_to": "Incoming melee attack damage to troops in the active banner formation.",
        "formula_usage": "Added in the melee branch of ApplyDamageReductions.",
        "practical_read": "General anti-melee durability.",
        "caveat": "Does not reduce ranged or shield-only damage.",
    },
    "DecreasedRangedAttackDamage": {
        "applies_to": "Incoming ranged attack damage to troops in the active banner formation.",
        "formula_usage": "Added in the ranged branch of ApplyDamageReductions.",
        "practical_read": "The anti-arrow banner: tier 3 -15% is a real ranged damage taken reduction.",
        "caveat": "The raw description string is wrong and reuses morale text.",
    },
    "DecreasedShieldDamage": {
        "applies_to": "Damage dealt to shields of troops in the victim formation.",
        "formula_usage": "Added in CalculateShieldDamage.",
        "practical_read": "Protects shields, which indirectly preserves shield wall uptime.",
        "caveat": "Does not directly reduce HP damage when an attack bypasses or breaks through the shield.",
    },
    "IncreasedTroopMovementSpeed": {
        "applies_to": "AgentDrivenProperties.MaxSpeedMultiplier for troops in the active banner formation.",
        "formula_usage": "Added in SetPerkAndBannerEffectsOnAgent/SetBannerEffectsOnAgent, then written to MaxSpeedMultiplier.",
        "practical_read": "The shock-infantry speed banner. Tier 3 +30% is a major close-to-contact and formation responsiveness effect.",
        "caveat": "Not campaign map speed, projectile speed, reload speed, or CombatMaxSpeedMultiplier.",
    },
    "IncreasedMountMovementSpeed": {
        "applies_to": "Mount speed in UpdateHorseStats.",
        "formula_usage": "Added to the horse-speed explained/factored number before MountSpeed is written.",
        "practical_read": "Mounted formation speed banner; tier 3 is +10% mount speed.",
        "caveat": "Not campaign map speed and not primarily a mount maneuver bonus.",
    },
    "IncreasedMoraleShockByMeleeTroops": {
        "applies_to": "Morale shock inflicted by melee troops when agents are incapacitated.",
        "formula_usage": "Added in CalculateMaxMoraleChangeDueToAgentIncapacitated.",
        "practical_read": "Offensive morale-pressure banner for melee-heavy formations.",
        "caveat": "Not raw damage; value depends on morale shock mattering in the fight.",
    },
}


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def format_bonus(value: Any, force_plus: bool = False) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    percent = number * 100.0
    if abs(percent - round(percent)) < 1e-6:
        text = f"{round(percent):.0f}%"
    else:
        text = f"{percent:.4f}".rstrip("0").rstrip(".") + "%"
    if force_plus and not text.startswith("-"):
        return "+" + text
    return text


def mechanical_summary(effect: str, bonus: Any) -> str:
    template = MECHANICAL_SUMMARIES.get(effect)
    if not template:
        return ""
    force_plus = template.startswith("+")
    bonus_text = format_bonus(bonus, force_plus=False)
    if force_plus:
        bonus_text = bonus_text.lstrip("+")
    return template.format(bonus=bonus_text)


def tier_summary(group: dict[str, Any]) -> str:
    parts = []
    for tier in group.get("tiers", []):
        parts.append(f"T{tier['level']} {tier['display_bonus']}")
    return ", ".join(parts)


def effect_source(effect_definitions: dict[str, dict[str, Any]], groups: dict[str, dict[str, Any]], effect: str) -> dict[str, Any]:
    return groups.get(effect) or effect_definitions.get(effect, {})


def top_tier_items(items: list[dict[str, Any]], effect: str) -> list[dict[str, Any]]:
    matching = [item for item in items if item["effect"] == effect]
    if not matching:
        return []
    max_level = max(int(item["banner_level"]) for item in matching)
    return [item for item in matching if int(item["banner_level"]) == max_level]


def banner_effect_usages(usage_payload: dict[str, Any] | None) -> dict[str, list[str]]:
    if not usage_payload:
        return {}
    usages: dict[str, set[str]] = {}
    for method in usage_payload.get("methods", []):
        method_label = f"{method.get('assembly', '')}: {method.get('type', '')}.{method.get('method', '')}"
        for member in method.get("referenced_members", []):
            if "DefaultBannerEffects.get_" not in str(member):
                continue
            effect = str(member).split("get_", 1)[1].split("(", 1)[0]
            if effect == "Instance":
                continue
            usages.setdefault(effect, set()).add(method_label)
    return {effect: sorted(labels) for effect, labels in usages.items()}


def usage_cell(usages: dict[str, list[str]], effect: str) -> str:
    labels = usages.get(effect, [])
    if not labels:
        return "No usage scan available"
    short_labels = []
    for label in labels:
        label = label.replace("SandBox.GameComponents.", "")
        label = label.replace("TaleWorlds.MountAndBlade.", "")
        short_labels.append(label)
    return "<br>".join(short_labels)


def top_tier_names(items: list[dict[str, Any]], effect: str) -> str:
    tier_items = top_tier_items(items, effect)
    if not tier_items:
        return "No singleplayer banner item"
    return ", ".join(item["name"] for item in tier_items)


def read_optional_json(path: Path) -> Any | None:
    if not path.exists():
        return None
    return read_json(path)


def write_markdown(payload: dict[str, Any], path: Path, workspace: Path, json_output: Path) -> None:
    effect_definitions = {definition["string_id"]: definition for definition in payload.get("effect_definitions", [])}
    groups = {group["effect"]: group for group in payload.get("groups", [])}
    effect_ids = sorted(effect_definitions)
    items = payload.get("items", [])
    usage_path = workspace / "Data" / "raw" / "banner-effect-usages.json"
    usage_payload = read_optional_json(usage_path)
    usages = banner_effect_usages(usage_payload)

    lines = [
        "# Banner Effects",
        "",
        f"Generated: {payload.get('generated_at', '')}",
        "",
        "This report joins singleplayer banner item XML to `DefaultBannerEffects.InitializeAll`, then cross-checks effect IDs against formula usage from the local game assemblies.",
        "",
        "## Inputs",
        "",
        f"- JSON: `{display_path(json_output, workspace)}`",
    ]
    for source in payload.get("inputs", {}).get("banner_xml", []):
        lines.append(f"- Banner XML: `{source}`")
    if usage_payload:
        lines.append(f"- Usage scan: `{display_path(usage_path, workspace)}`")
    lines.extend(
        [
            "",
            "> [!WARNING]",
            "> `DecreasedRangedAttackDamage` has a misleading raw description string in `DefaultBannerEffects.InitializeAll`: it reuses morale-penalty wording. The formulas reference the `DecreasedRangedAttackDamage` effect for ranged damage reduction, so this report treats it mechanically as ranged damage taken reduction.",
            "",
            "## How Banner Effects Apply",
            "",
            "- Battle banners are formation-scoped. Combat/stat models ask `BattleBannerBearersModel.GetActiveBanner(formation)` and add the matching active banner effect to an explained/factored number.",
            "- Damage-dealt banners use the attacker's active banner formation; damage-taken and shield-damage banners use the victim/defending formation path.",
            "- Movement banners are live-battle agent stats, not campaign party speed.",
            "- Accuracy banner mechanics are narrow: the ranged accuracy banner modifies `WeaponInaccuracy`, not every accuracy penalty property and not direct hit chance.",
            f"- Usage confirmation: {len(usages)} banner effects were found in formula usage scan." if usages else "- Usage confirmation: run `extract-banners` without `--skip-usage-scan` to refresh formula usage evidence.",
            "",
            "## Commander Shortlist",
            "",
            "| Effect | Tiers | Tier 3 items | Mechanical read | Note |",
            "| --- | --- | --- | --- | --- |",
        ]
    )

    for effect, note in COMMANDER_SHORTLIST.items():
        group = groups.get(effect)
        if not group:
            continue
        tier3_items = top_tier_items(items, effect)
        tier3_names = ", ".join(item["name"] for item in tier3_items)
        tier3_bonus = tier3_items[0]["bonus"] if tier3_items else ""
        lines.append(
            "| {effect} | {tiers} | {items} | {mechanics} | {note} |".format(
                effect=table_escape(group.get("effect_name", effect)),
                tiers=table_escape(tier_summary(group)),
                items=table_escape(tier3_names),
                mechanics=table_escape(mechanical_summary(effect, tier3_bonus)),
                note=table_escape(note),
            )
        )

    lines.extend(
        [
            "",
            "## Mechanics Reference",
            "",
            "| Effect ID | Tier values | Top tier items | Applies mechanically to | Formula usage | Confirmed methods | Practical read | Caveat |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for effect in effect_ids:
        source = effect_source(effect_definitions, groups, effect)
        mechanics = BANNER_MECHANICS.get(effect, {})
        lines.append(
            "| {effect} | {tiers} | {items} | {applies} | {formula} | {methods} | {read} | {caveat} |".format(
                effect=table_escape(effect),
                tiers=table_escape(tier_summary(source)),
                items=table_escape(top_tier_names(items, effect)),
                applies=table_escape(mechanics.get("applies_to", "")),
                formula=table_escape(mechanics.get("formula_usage", "")),
                methods=table_escape(usage_cell(usages, effect)),
                read=table_escape(mechanics.get("practical_read", "")),
                caveat=table_escape(mechanics.get("caveat", "")),
            )
        )

    lines.extend(
        [
            "",
            "## All Banner Effects",
            "",
            "| Effect ID | Name | Tiers | Mechanical tier 3 read | Items |",
            "| --- | --- | --- | --- | ---: |",
        ]
    )
    for effect in effect_ids:
        source = effect_source(effect_definitions, groups, effect)
        tier3 = next((tier for tier in source.get("tiers", []) if int(tier["level"]) == 3), None)
        group = groups.get(effect, {})
        item_count = sum(int(tier.get("item_count", 0)) for tier in group.get("tiers", []))
        lines.append(
            "| {effect} | {name} | {tiers} | {mechanics} | {count} |".format(
                effect=table_escape(effect),
                name=table_escape(source.get("effect_name", source.get("name", ""))),
                tiers=table_escape(tier_summary(source)),
                mechanics=table_escape(mechanical_summary(effect, tier3["bonus"]) if tier3 else ""),
                count=item_count,
            )
        )

    lines.extend(
        [
            "",
            "## Banner Items",
            "",
            "| Effect | Tier | Item | Culture | Bonus | Mechanical read | Raw description |",
            "| --- | ---: | --- | --- | ---: | --- | --- |",
        ]
    )
    for item in sorted(items, key=lambda row: (row["effect"], int(row["banner_level"]), row["name"])):
        lines.append(
            "| {effect} | {tier} | {item} | {culture} | {bonus} | {mechanics} | {raw} |".format(
                effect=table_escape(item["effect"]),
                tier=item["banner_level"],
                item=table_escape(item["name"]),
                culture=table_escape(item.get("culture", "")),
                bonus=table_escape(item["display_bonus"]),
                mechanics=table_escape(mechanical_summary(item["effect"], item["bonus"])),
                raw=table_escape(item.get("display_effect", "")),
            )
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def extract_banners(
    workspace: Path,
    game_root: Path | None,
    json_output: Path,
    markdown_output: Path,
    usage_output: Path | None = None,
    skip_scan: bool = False,
    skip_usage_scan: bool = False,
    include_mp: bool = False,
) -> None:
    if usage_output is None:
        usage_output = workspace / "Data" / "raw" / "banner-effect-usages.json"
    if not skip_scan:
        resolved_game_root = resolve_game_root(game_root)
        args = [
            "banners",
            "--game-root",
            str(resolved_game_root),
            "--output",
            str(json_output),
        ]
        if include_mp:
            args.append("--include-mp")
        run_extractor(workspace, args)

        if not skip_usage_scan:
            usage_args = [
                "find-methods",
                "--game-root",
                str(resolved_game_root),
                "--query",
                "DefaultBannerEffects.get_",
                "--include-il",
                "--output",
                str(usage_output),
            ]
            for assembly in USAGE_SCAN_ASSEMBLIES:
                usage_args.extend(["--assembly", assembly])
            run_extractor(workspace, usage_args)

    payload = read_json(json_output)
    write_markdown(payload, markdown_output, workspace, json_output)
    print(f"Banner item JSON written: {json_output}")
    if usage_output.exists():
        print(f"Banner effect usage JSON written: {usage_output}")
    print(f"Banner effect report written: {markdown_output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Bannerlord banner item effects and write a report.")
    parser.add_argument("--workspace", type=Path, default=default_workspace())
    parser.add_argument("--game-root", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, default=None)
    parser.add_argument("--markdown-output", type=Path, default=None)
    parser.add_argument("--usage-output", type=Path, default=None)
    parser.add_argument("--skip-scan", action="store_true", help="Reuse existing banner JSON and regenerate only the report.")
    parser.add_argument("--skip-usage-scan", action="store_true", help="Do not refresh Data/raw/banner-effect-usages.json while extracting banners.")
    parser.add_argument("--include-mp", action="store_true", help="Also include multiplayer banner XML; off by default to avoid duplicate singleplayer item IDs.")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    json_output = args.json_output or workspace / "Data" / "raw" / "banner-items.json"
    markdown_output = args.markdown_output or workspace / "Docs" / "reports" / "banner-effects.md"
    usage_output = args.usage_output or workspace / "Data" / "raw" / "banner-effect-usages.json"
    extract_banners(
        workspace=workspace,
        game_root=args.game_root,
        json_output=json_output,
        markdown_output=markdown_output,
        usage_output=usage_output,
        skip_scan=args.skip_scan,
        skip_usage_scan=args.skip_usage_scan,
        include_mp=args.include_mp,
    )


if __name__ == "__main__":
    main()
