# Data Directory

The data tree is split by responsibility:

- `raw/`: extracted game definitions from local Bannerlord assemblies.
- `intermediate/classified-perk-effects.json`: classifier output before overrides.
- `intermediate/postprocessed-perk-effects.json`: classifier output after mechanical taxonomy post-processing.
- `intermediate/`: generated working data for reports that are not final exports, such as commander and character-start analyses.
- `curated/`: human-maintained corrections and notes.
- `export/`: final merged JSON for analysis tools and UI work.
- `export/guide-stat-extracts.json`: guide-facing perk/stat buckets and stack definitions used by the manual guides.

Generated markdown lives under `Docs/`:

- `Docs/reference/`: generated perk reference markdown from the final export.
- `Docs/reports/`: generated extraction reports, review reports, tag reports, and analysis outputs.

Do not edit files in `raw/`, `intermediate/`, or `export/` by hand. Put corrections in `curated/perk-effect-overrides.json` and rebuild.
