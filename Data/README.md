# Data Directory

The data tree is split by responsibility:

- `raw/`: extracted game definitions from local Bannerlord assemblies.
- `generated/classified-perk-effects.json`: classifier output before overrides.
- `generated/postprocessed-perk-effects.json`: classifier output after mechanical taxonomy post-processing.
- `generated/xp-award-methods.json`: extracted XP-related method index from local assemblies.
- `generated/perk-effects/`: generated markdown from the final export.
- `generated/reports/`: generated review and tag reports.
- `curated/`: human-maintained corrections and notes.
- `export/`: final merged JSON for analysis tools and UI work.

Do not edit files in `raw/`, `generated/`, or `export/` by hand. Put corrections in `curated/perk-effect-overrides.json` and rebuild.
