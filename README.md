# Bannerlord Perk Analyzer

This repository extracts Bannerlord perk effect data from the local game assemblies, applies post-processing and curated review data, and emits review-friendly datasets for analysis or a future browser UI.

## Data Layout

- `Data/raw/` contains extracted game data before custom classification or overrides.
- `Data/intermediate/` contains classifier output, post-processed snapshots, and intermediate analysis data.
- `Data/curated/` contains human-maintained overrides, review notes, and suspected game-data issues.
- `Data/export/` contains merged JSON intended for tools and UI work.
- `Docs/reports/` contains generated reports and `Docs/reference/` contains generated perk reference markdown.
- `Docs/guides/` contains manual guide notes.

Game values and custom fields are kept separate in the source layout. The merged export keeps the split visible with `game`, `classification`, `review`, `source`, and `provenance` sections.

The pipeline is intentionally staged:

1. `Data/raw/perks.json`: raw game extraction.
2. `Data/intermediate/classified-perk-effects.json`: generated classifier output before overrides.
3. `Data/intermediate/postprocessed-perk-effects.json`: mechanical taxonomy post-processing.
4. `Data/export/perk-effects.json`: final export with curated review fields applied.

## Rebuild

```text
python .\src\bannerlord_perk_analyzer\rebuild.py --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord"
```

You can also set `BANNERLORD_GAME_ROOT` and omit `--game-root`.

The rebuild command uses the local .NET extractor in `tools/BannerlordExtractor/` for Bannerlord assembly reading, then Python handles classification, post-processing, markdown/report generation, and validation. Use `--skip-extract` to regenerate custom fields from the existing `Data/raw/perks.json` without reading the game install.

## Post-process

```text
python .\src\bannerlord_perk_analyzer\postprocess.py
```

## Build Generator

Generate a terminal build plan from skill levels or perk names:

```text
python .\src\bannerlord_perk_analyzer\build_generator.py --target "Bow:275" --target "Riding:225" --perk "Minister of Health"
```

The planner uses the game-wide skill limit and peak learning range formulas, 1 focus point per player level, and 1 attribute point per 4 player levels. Attribute points apply to every skill in their attribute group, so raising Control helps Bow, Crossbow, and Throwing together. By default it may add Athletics/Smithing enabler targets when Endurance attribute perks reduce the total point budget; pass `--no-auto-endurance` to use only the requested build targets.

Character creation choices can be applied by option id or title after generating the character creation data:

```text
python .\src\bannerlord_perk_analyzer\build_generator.py --target "Bow:275" --creation-choice "empire_hunter_option" --creation-choice "childhood_detail_option" --creation-choice "age_selection_adult_option"
```

Fixed character creation choices add their listed starting attributes/focus to the base plan. Sandbox age choices add flexible unspent focus and attribute points, so those reduce the required level-up budget without being tied to a specific skill. Story campaign does not use the sandbox age menu; its final escape choice replaces age 20 by fixing that +1 attribute/+2 focus budget to one attribute and two skills, with +10 starting levels in those two skills.

Campaign family members are separate from those player-choice effects. Their culture, names, appearance, equipment, and home settlement can be set during story character creation, but their attribute/focus/skill distribution comes from fixed StoryMode hero templates plus the normal HeroCreator/HeroDeveloper initialization flow.

## XP Extraction

Generate a first-pass map of XP award logic from the local compiled assemblies:

```text
python .\src\bannerlord_perk_analyzer\extract_xp_awards.py --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord" --include-il
```

The script writes `Data/raw/xp-award-methods.json`, `Docs/reports/xp-awards.md`, and, with `--include-il`, `Docs/reports/xp-award-il.md`. The default scan covers `TaleWorlds.Core` and `TaleWorlds.CampaignSystem`; use `--deep-scan-callers` for a slower pass that inspects every method body for calls into XP sinks.

Dig into broader XP formula candidates across campaign, mission, sandbox, and story assemblies:

```text
python .\src\bannerlord_perk_analyzer\extract_xp_formulas.py --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord"
```

This wraps the `.NET` extractor's method search in thematic scans for combat, hero progression, troop XP, crafting/discard XP, and activity XP. It writes `Data/raw/xp-formula-methods.json`, `Docs/reports/xp-formulas.md`, and the friendlier guide `Docs/reports/xp-insights.md`; pass `--no-il` for a smaller JSON file, or `--keep-temp` to preserve the per-scan temporary JSON files under `Data/intermediate/xp-formula-scan-temp/`.

Generate a skill-by-skill source map for XP gain:

```text
python .\src\bannerlord_perk_analyzer\extract_skill_xp_sources.py --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord"
```

This writes `Data/raw/skill-xp-source-methods.json` and `Docs/reports/skill-xp-sources.md`, grouping direct and inferred XP sources under each player-facing skill.

Generate the character creation option map:

```text
python .\src\bannerlord_perk_analyzer\extract_character_creation.py --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord"
```

This writes `Data/raw/character-creation-options.json` and `Docs/reports/character-creation-options.md`, including family/background, childhood, education, youth, adulthood, sandbox age, story-mode escape choices, campaign family mechanical stats, and the HeroCreator initialization flow that applies to family members.

Generate banner item/effect data:

```text
python .\cli.py extract-banners --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord"
```

This writes `Data/raw/banner-items.json`, `Data/raw/banner-effect-usages.json`, and `Docs/reports/banner-effects.md`, joining singleplayer banner item XML to `DefaultBannerEffects.InitializeAll` so each banner item has its effect id, tier, and actual numeric bonus. It also scans the local game assemblies for `DefaultBannerEffects` formula usage so the report can explain what each effect actually modifies. The command uses singleplayer `SandBoxCore` banners by default; pass `--include-mp` only if you explicitly want multiplayer banner XML too, or `--skip-usage-scan` if you only want to refresh item data.

Generate guide-facing stat extracts from the current perk export:

```text
python .\src\bannerlord_perk_analyzer\extract_guide_stats.py
```

This writes `Data/export/guide-stat-extracts.json` and `Docs/reports/guide-stat-extracts.md`, collecting the perk rows, direct weapon skill constants, AI stack definitions, survivability stacks, and smithing formulas used by the manual guide notes.

Generate the doctrine-ranked commander perk report:

```text
python .\cli.py commander-report
```

This writes `Data/intermediate/commander_perks_extracted.json`, `Data/intermediate/commander_perks_report.txt`, and `Docs/reports/commander-banner-package-comparison.md`. The report is tuned for an elite shock-infantry-heavy one-party army: live troop lethality first, campaign engagement control second, and party size/logistics after the party can still catch worthwhile targets. It deliberately separates campaign party speed, troop combat movement, weapon handling speed, projectile speed, and siege speed so keyword matches do not overstate mobility value. The focused package comparison uses banner-centered full alternative-pick packages; use `Docs/reports/banner-effects.md` as the mechanics reference for what each banner actually modifies.

Generate perk investment cost analysis:

```text
python .\src\bannerlord_perk_analyzer\analyze_perk_investment.py
```

This writes `Data/intermediate/perk-investment-costs.json` and `Docs/reports/perk-investment-costs.md`, assigning each perk tier a low/medium/high investment category, additive allocation cost, level gate, above-focus-only summary, shared-attribute examples, and Endurance-stretch comparison for expensive targets.

For focused IL debugging, call the extractor directly:

```text
dotnet run --project .\tools\BannerlordExtractor -- dump-il --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord" --assembly TaleWorlds.CampaignSystem --type TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultPerks --method InitializeAll
```

For targeted method searches across game and module assemblies:

```text
dotnet run --project .\tools\BannerlordExtractor -- find-methods --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord" --assembly SandBox --assembly TaleWorlds.MountAndBlade --query shotDifficulty --include-il --output Data\raw\shot-difficulty-methods.json
```

## Validate

```text
python .\src\bannerlord_perk_analyzer\validate.py
```
