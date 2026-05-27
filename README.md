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

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Scripts\RebuildPerkEffectsFromGame.ps1 -GameRoot "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord"
```

You can also set `BANNERLORD_GAME_ROOT` and omit `-GameRoot`.

The rebuild script still uses PowerShell for local .NET assembly extraction, but post-processing, markdown/report generation, and validation are Python.

## Post-process

```powershell
python .\src\bannerlord_perk_analyzer\postprocess.py
```

## Build Generator

Generate a terminal build plan from skill levels or perk names:

```powershell
python .\src\bannerlord_perk_analyzer\build_generator.py --target "Bow:275" --target "Riding:225" --perk "Minister of Health"
```

The planner uses the game-wide skill limit and peak learning range formulas, 1 focus point per player level, and 1 attribute point per 4 player levels. Attribute points apply to every skill in their attribute group, so raising Control helps Bow, Crossbow, and Throwing together. By default it may add Athletics/Smithing enabler targets when Endurance attribute perks reduce the total point budget; pass `--no-auto-endurance` to use only the requested build targets.

## XP Extraction

Generate a first-pass map of XP award logic from the local compiled assemblies:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Scripts\ExtractXpAwardModel.ps1 -GameRoot "E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord" -IncludeIl
```

The script writes `Data/generated/xp-award-methods.json`, `Data/generated/reports/xp-awards.md`, and, with `-IncludeIl`, `Data/generated/reports/xp-award-il.md`. The default scan covers `TaleWorlds.Core` and `TaleWorlds.CampaignSystem`; use `-DeepScanCallers` for a slower pass that inspects every method body for calls into XP sinks.

## Validate

```powershell
python .\src\bannerlord_perk_analyzer\validate.py
```
