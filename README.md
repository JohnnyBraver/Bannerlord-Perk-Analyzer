# Bannerlord Perk Analyzer

This repository extracts Bannerlord perk effect data from the local game assemblies, applies post-processing and curated review data, and emits review-friendly datasets for analysis or a future browser UI.

## Data Layout

- `Data/raw/` contains extracted game data before custom classification or overrides.
- `Data/generated/` contains classifier output, post-processed snapshots, generated markdown notes, and reports.
- `Data/curated/` contains human-maintained overrides, review notes, and suspected game-data issues.
- `Data/export/` contains merged JSON intended for tools and UI work.
- `Docs/` contains supporting notes and the old Obsidian view definition.

Game values and custom fields are kept separate in the source layout. The merged export keeps the split visible with `game`, `classification`, `review`, `source`, and `provenance` sections.

The pipeline is intentionally staged:

1. `Data/raw/perks.json`: raw game extraction.
2. `Data/generated/classified-perk-effects.json`: generated classifier output before overrides.
3. `Data/generated/postprocessed-perk-effects.json`: mechanical taxonomy post-processing.
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

Fixed character creation choices add their listed starting attributes/focus to the base plan. Sandbox age choices add flexible unspent focus and attribute points, so those reduce the required level-up budget without being tied to a specific skill.

## XP Extraction

Generate a first-pass map of XP award logic from the local compiled assemblies:

```text
python .\src\bannerlord_perk_analyzer\extract_xp_awards.py --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord" --include-il
```

The script writes `Data/generated/xp-award-methods.json`, `Data/generated/reports/xp-awards.md`, and, with `--include-il`, `Data/generated/reports/xp-award-il.md`. The default scan covers `TaleWorlds.Core` and `TaleWorlds.CampaignSystem`; use `--deep-scan-callers` for a slower pass that inspects every method body for calls into XP sinks.

Dig into broader XP formula candidates across campaign, mission, sandbox, and story assemblies:

```text
python .\src\bannerlord_perk_analyzer\extract_xp_formulas.py --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord"
```

This wraps the `.NET` extractor's method search in thematic scans for combat, hero progression, troop XP, crafting/discard XP, and activity XP. It writes `Data/generated/xp-formula-methods.json`, `Data/generated/reports/xp-formulas.md`, and the friendlier guide `Data/generated/reports/xp-insights.md`; pass `--no-il` for a smaller JSON file, or `--keep-temp` to preserve the per-scan intermediate JSON files.

Generate a skill-by-skill source map for XP gain:

```text
python .\src\bannerlord_perk_analyzer\extract_skill_xp_sources.py --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord"
```

This writes `Data/generated/skill-xp-source-methods.json` and `Data/generated/reports/skill-xp-sources.md`, grouping direct and inferred XP sources under each player-facing skill.

Generate the character creation option map:

```text
python .\src\bannerlord_perk_analyzer\extract_character_creation.py --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord"
```

This writes `Data/generated/character-creation-options.json` and `Data/generated/reports/character-creation-options.md`, including family/background, childhood, education, youth, adulthood, sandbox age, and story-mode escape choices.

For focused IL debugging, call the extractor directly:

```text
dotnet run --project .\tools\BannerlordExtractor -- dump-il --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord" --assembly TaleWorlds.CampaignSystem --type TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultPerks --method InitializeAll
```

For targeted method searches across game and module assemblies:

```text
dotnet run --project .\tools\BannerlordExtractor -- find-methods --game-root "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord" --assembly SandBox --assembly TaleWorlds.MountAndBlade --query shotDifficulty --include-il --output Data\generated\shot-difficulty-methods.json
```

## Validate

```text
python .\src\bannerlord_perk_analyzer\validate.py
```
