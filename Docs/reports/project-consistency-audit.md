# Project Consistency Audit And Remediation Log

Generated from the current workspace using `Data/export/perk-effects.json` as the perk source of truth. The existing validator passes:

```text
OK: checked 721 perk effect files, 721 generated rows, 52 overrides.
```

Current worktree note: `Data/intermediate/commander_perks_extracted.json` and `Data/intermediate/commander_perks_report.txt` are untracked existing/generated files and were not touched.

Slot terminology note: `primary` and `secondary` are extraction slot labels only. They do not imply that one effect is more important, more build-defining, or the main reason to choose a perk. Different builds may correctly value either slot as the decisive effect, so guide corrections should name the role/effect/scope rather than treating slot order as priority.

Remediation status: the findings below were applied in the follow-up fix pass. They are retained as a review log rather than a list of current open issues.

## Critical Correctness Issues

These are guide claims where the cited perk, level, role, scope, or numeric effect conflicts with the final perk export.

| Severity | Location | Current claim | Source of truth | Why this is inconsistent | Suggested fix |
|---|---|---|---|---|---|
| P1 | `Docs/guides/commander-perks-and-build-optimization.md:93`, `:117`; `Docs/guides/hero-progression-and-builds.md:285`, `:476` | Two-Handed `Projectile Deflection` is treated as a level 100 target reachable with 1 focus at effective Vigor 5. | `TwoHandedProjectileDeflection|primary`: Two Handed 150, personal, "You can deflect projectiles with two handed swords by blocking." | The build math says 1 focus at attribute 5 reaches limit 100, which cannot unlock a level 150 perk. | Either raise the Two Handed target to 150 and recalculate focus/attribute cost, or keep the level 100 target and replace `Projectile Deflection` with an actual level 100 perk such as `Beast Slayer` or `Shield breaker`. |
| P1 | `Docs/guides/commander-perks-and-build-optimization.md:107` | Medicine target is "level 275 `Physician of People` ($+30% low-tier survival)." | `MedicinePhysicianOfPeople` is Medicine 200; `MedicineMinisterOfHealth|primary` is Medicine 275 and gives "1 hit point to troops for every skill point above 250." | This merges the Medicine 200 low-tier survival perk with the Medicine 275 scaling HP perk. | Split into "Medicine 200 `Physician of People` for Tier 1/2 lethal-wound recovery" and "Medicine 275 `Minister of Health` for troop HP scaling above 250." |
| P1 | `Docs/guides/commander-perks-and-build-optimization.md:109` | Formerly, Steward 250 `Master of Warcraft` was described as a siege attrition or cohesion-style reduction. | `StewardMasterOfWarcraft|primary`: "-25% troop wages while your party is in a siege camp"; secondary: "-5% food consumption of town population in the governed settlement." | That phrasing was not the exported effect and could be confused with cohesion, food decay, or attrition. | Replace with "reduced troop wages while in a siege camp" or cite the governor food-consumption row if that is the intended context. |
| P1 | `Docs/guides/commander-perks-and-build-optimization.md:112` | Formerly, Roguery 75 `Know-How` was described as increasing alley income. | `RogueryKnowHow|primary`: "5% more loot from defeated villagers and caravans"; secondary: "1 security per day in the governed settlement." | The exported perk data has no alley-income effect for this row. | Replace the effect with the loot/security effects, or cite the actual alley perk if a different Roguery row was intended. |
| P2 | `Docs/guides/commander-perks-and-build-optimization.md:114` | Charm 50 `Oratory` is summarized as "+2 Renown / +1 Influence." | `CharmOratory|primary`: "1 renown and influence for each issue resolved"; secondary: "1 relationship with a random notable of your kingdom when an enemy lord is defeated." | The guide overstates renown if the export text means 1 renown and 1 influence. | Change to "+1 renown and +1 influence per issue resolved"; mention the secondary relationship effect separately if relevant. |
| P2 | `Docs/guides/hero-progression-and-builds.md:376` | Athletics 150 `A Good Days Rest`: "Town resting recovery speed +20%." | `AthleticsAGoodDaysRest|primary`: "10% hit point regeneration while waiting in settlements"; secondary: "10 daily experience to foot troops while waiting in settlements." | The exported regeneration value is 10%, not 20%, and the troop-XP row is separate. | Change to "10% hit point regeneration while waiting in settlements"; keep the +10 troop XP/day only in troop-training contexts. |
| P2 | `Docs/guides/military-and-troop-tactics.md:165` | Formerly, Athletics 150 used apostrophe spelling inconsistent with the export. | Exported perk name is `A Good Days Rest` with string id `AthleticsAGoodDaysRest`. | This is a naming mismatch that breaks strict guide-to-export checks. | Use exported spelling in code/data-facing tables, or add a note that the human-readable apostrophe form is intentional if preferred for prose. |
| P2 | `Docs/guides/trade-and-market-economy.md:86`; `Docs/guides/commander-perks-and-build-optimization.md:115` | `Caravan Master` is described only as price-color UI. | `TradeCaravanMaster|primary`: Quartermaster, "30% carrying capacity for your party"; `TradeCaravanMaster|secondary`: personal, "Item prices are marked relative to the average price." | The claim is true for the personal price-display effect, but the same perk also has a Quartermaster logistics effect that may be the build driver in another context. | Add role/effect clarity without implying slot priority: "`Caravan Master` can be taken for personal price marking or for the Quartermaster +30% carrying capacity effect, depending on build role." |

### Settlement And Siege Table Drift

`Docs/guides/fiefs-and-settlement-governance.md:133-142` contains a compact perk table whose effects are largely not supported by `Data/export/perk-effects.json`.

| Location | Current claim | Exported row(s) | Suggested fix |
|---|---|---|---|
| `:133` | Steward 175 `Sound Reserves`: "+20% garrison size limit." | `StewardSoundReserves|primary`: -10% troop upgrade costs; secondary: -10% food consumption during sieges in your party. | Remove from garrison-capacity table or replace with its upgrade-cost/siege-food effects. |
| `:134` | Engineering 25 `Torsion Engines`: "+20% siege engine build speed." | `EngineeringTorsionEngines|primary`: 10% build speed to ranged siege engines. | Change value to 10% and specify ranged siege engines. |
| `:135` | Engineering 100 `Dreadful Besieger`: "+20% damage to enemy engines." | `EngineeringDreadfulSieger|primary`: 10% accuracy to your siege engines during siege bombardments in governed settlement; secondary: 5% crossbow damage by troops in formation. | Replace with the accuracy/crossbow effects or cite a different damage perk. |
| `:136` | Engineering 100 `Wall Breaker`: "+20% wall damage." | `EngineeringWallBreaker|primary`: 25% damage dealt to walls during siege bombardment. | Change value to 25%. |
| `:138` | Engineering 150 `Siege Engineer`: "-30% siege build times." | `EngineeringSiegeEngineer|primary`: 30% hit points to defensive siege engines; secondary: fire versions can be constructed. | Replace with siege-engine HP/fire-engine unlock. |
| `:139` | Engineering 175 `Camp Building`: "+20% camp prep build speed." | `EngineeringCampBuilding|primary`: -50% army cohesion loss when besieging; secondary: -20% casualty chance from siege bombardments. | Replace with cohesion/casualty effects. |
| `:141` | Engineering 200 `Apprenticeship`: "+10% troop training rate." | `EngineeringApprenticeship|primary`: 5 experience to troops when a siege engine is built; secondary: 1% prosperity gain per unique project. | Change to +5 XP per siege engine built, or move to prosperity/project discussion. |
| `:142` | Engineering 250 `Clockwork`: "-10% garrison wage." | `EngineeringClockwork|primary`: 25% ballista reload speed during siege bombardment; secondary: 20% boost-project effect. | Replace with reload/project effects; do not present as wage reduction. |

### Campaign Speed Table Drift

`Docs/guides/military-and-troop-tactics.md:86-97` appears to have several Scouting/Steward effects from another version or a different source. The current 1.4.5 export does not support these speed claims.

| Location | Current claim | Exported row(s) | Suggested fix |
|---|---|---|---|
| `:86` | `Mounted Scouts`: +2 speed if at least 50% party is mounted. | Primary: 10% sight range when party is more than 50% cavalry; secondary: +5 party size. | Move to sight/party-size table, not speed. |
| `:87` | `Patrols`: -15 prisoner speed penalty. | Primary: +5 battle morale against bandits; secondary: +10% bandit autoresolve advantage. | Replace with bandit morale/simulation effect. |
| `:88` | `Foragers`: -20 wounded speed penalty. | Primary: -10% food consumption in steppes/forests; secondary: -15% disorganized state duration. | Replace with food/disorganized-state effect. |
| `:90` | `Village Network`: +4 speed inside own territory. | Primary: -10% trade penalty with same-culture villages; secondary: 10% villager party size in governed settlement. | Replace with trade/governor effect. |
| `:91` | `Keen Sight`: -10 forest/swamp speed penalty. | Primary: -50% sight penalty in forests; secondary: -50% prisoner lord escape chance. | Replace with sight/prisoner effect. |
| `:92` | `Vantage Point`: +2 speed in hills and +20% spotting. | Primary: +25% sight range while stationary for at least an hour; secondary: +10 prisoner limit. | Replace with stationary sight/prisoner limit. |
| `:93` | Formerly, `Rearguard` was described as a pursuit-speed modifier. | Primary: +20% wounded troop recovery speed while in an army; secondary: +10% damage when defending at siege camp. | Replace with recovery/siege-defense effect. |
| `:94` | Formerly, `Vanguard` was described as a pursuit-speed modifier. | Primary: +5% simulation damage as attackers; secondary: +10% simulation sally-out damage. | Replace with simulation attack/sally-out effects. |
| `:97` | Formerly, Steward 150 `Aid Corps` was described as mitigating wounded-troop map-speed loss. | Primary: wounded troops no longer paid wages; secondary: 20% hearth growth in bound villages. | Replace with wages/hearth growth, or cite Medicine 75 `Sledges` for wounded speed penalty. |

## Aggregate And Table Classification Issues

The aggregate extract is useful as a broad index, but some bucket names read narrower than their predicates. If guide prose consumes these buckets without an additional scope filter, it can overstate live-battle, economy, or troop-training value.

| Severity | Evidence | Current bucket behavior | Risk | Suggested fix |
|---|---|---|---|---|
| P2 | `Data/export/guide-stat-extracts.json:14187`, `:14206` | `troop_survival_damage_reduction` includes `TacticsLooseFormations|primary` and `TacticsEliteReserves|primary`, both party-leader simulation rows. | A reader may treat simulation/autoresolve mitigation as live captain/formation protection. | Split into `live_troop_damage_reduction` and `simulation_damage_reduction`, or add a `Mode` column and filter live guide tables to non-simulation captain rows. |
| P2 | `Data/export/guide-stat-extracts.json:5593`, `:5663`, `:6328` | `trade_economy_perks` includes every Trade-skill row plus gold-economy rows, including carrying capacity, relationship, governor production, project effects, and `Everything Has a Price`. | The bucket title implies price/gold effects, but rows include social, unique, party-management, and settlement-governance effects. | Rename to `trade_skill_and_gold_economy_perks`, or tighten the predicate to `row_type == "gold economy"` plus explicitly selected settlement revenue rows. |
| P2 | `Data/export/guide-stat-extracts.json:9487`, `:9544`, `:9651`, `:9723`, `:10020` | `troop_xp` includes governor, engineer, captain, surgeon, and personal rows, not only party leader/quartermaster passive training. | Troop XP tables can mix garrison XP, siege-engine build XP, formation XP, personal kill-trigger XP, and possibly bugged/no-op rows. | Split by role/trigger: party passive training, garrison training, siege/build XP, formation XP, personal kill-trigger XP, and reviewed bug/no-op rows. |
| P3 | `src/bannerlord_perk_analyzer/guide_extractors/party_management.py` | `party_leader_quartermaster_perks` includes all party-leader and quartermaster rows regardless of subtype. | Good for discovery, but too broad for logistics or build recommendations. | Keep broad bucket but label it as an index; create narrower buckets for party size, speed, wages, prisoners, food, and carrying capacity. |

## Structural And Documentation Seams

| Severity | Location | Evidence | Suggested fix |
|---|---|---|---|
| P1 | `cli.py:292-297` | `extract-creation` calls `extract_character_creation(... skip_scan=args.skip_scan)`, but `python cli.py extract-creation --help` lists only `--workspace` and `--game-root`. | Add `parser_creation.add_argument("--skip-scan", action="store_true", ...)`, matching the standalone extractor and the XP source command. |
| P2 | `README.md:8`, `:18-19`, `:66`, `:74`, `:82`, `:90`, `:98`, `:106`, `:117` | README documented the old generated data tree, while the current CLI writes raw scans to `Data/raw`, classified/postprocessed rows to `Data/intermediate`, exports to `Data/export`, and reports to `Docs/reports`. | Updated README paths to the current layout. |
| P2 | `src/bannerlord_perk_analyzer/extract_xp_formulas.py:618`, `:826`; `src/bannerlord_perk_analyzer/extract_combat_formulas.py:416` | Generator text/help referenced old generated temp/report paths. | Updated generator strings to `Data/intermediate/...` for temp scan files and `Docs/reports/...` for reports. |
| P2 | `Docs/reports/xp-insights.md:5`, `:168`; `Docs/reports/xp-formulas.md:474-475`; `Docs/reports/xp-awards.md:274-275`; `Docs/reports/skill-xp-sources.md:231-232`; `Docs/reports/character-creation-options.md:227-228` | Generated report footers pointed to the old generated tree. | Regenerated reports where possible and updated stale XP report footers that require a fresh game-root scan. |
| P3 | `Docs/guides/battanian-starts.md:60`; `Docs/guides/hero-progression-and-builds.md:420`, `:450` | Manual guide links used absolute local workspace URLs. | Replaced with relative Markdown links. |

## Tone Calibration Notes

The project should keep strategic language when it is tied to explicit assumptions and exported math. The Engineering 225 `Metallurgy` "trap" language is defensible because the guide states the 7 INT / 7 CNG build context, the focus cost, and the relatively small +5 armor payoff.

Findings to calibrate rather than flatten:

| Location | Tone issue | Suggested treatment |
|---|---|---|
| `Docs/guides/commander-perks-and-build-optimization.md:18` | "Medicine to 275+ is the single most powerful troop survival tool" is plausible, but the same page mislabels `Physician of People` as the 275 target. | After correcting the perk target, qualify as "for party-wide troop durability in this commander build" and distinguish Medicine 200 low-tier recovery from Medicine 275 HP scaling. |
| `Docs/guides/commander-perks-and-build-optimization.md:54`, `:59` | Tactics/Roguery are called low/irrelevant for combat commanders. | Keep if scoped to personally commanded battles and the stated build; add that Tactics simulation perks matter for autoresolve-heavy play and Roguery has economy/security uses. |
| `Docs/guides/military-and-troop-tactics.md:99`, `:101` | "Mandatory" / "Indispensable" language appears in campaign-speed recommendations. | Keep only where the exported effect actually supports the described use case; otherwise downgrade to conditional phrasing. |

## Suggested Validation Additions

1. Add a guide-audit script that parses Markdown tables with `Skill`, `Level`, `Perk`, and `Effect` columns, then compares each perk to `Data/export/perk-effects.json`.
2. Check numeric values in guide effect cells against all exported rows for the same skill/level/perk, with an allowlist for derived calculations.
3. Check guide build-target tables for level reachability. Example: if a target says "level 100 `Projectile Deflection`", verify the named perk exists at level 100.
4. Add a slot-neutrality check for audit prose and guide generation: `primary`/`secondary` may identify rows, but recommendation text should not use those labels as priority language.
5. Add aggregate bucket assertions for guide-facing buckets, such as "live survivability table must not include `simulation` triggers" and "passive troop XP table must declare role/trigger groups."
6. Add a path hygiene check for stale old generated-tree strings and absolute local workspace links.
7. Add a CLI smoke test that runs `python cli.py <subcommand> --help` for every subcommand and verifies referenced arguments exist before command dispatch.
