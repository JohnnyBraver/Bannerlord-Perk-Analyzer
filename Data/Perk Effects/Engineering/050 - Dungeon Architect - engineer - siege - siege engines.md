---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 50
perk: "Dungeon Architect"
perk_string_id: "EngineeringDungeonArchitect"
effect_slot: "primary"
role: "engineer"
role_value: 8
perk_type: "siege"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
effect_tags: []
bonus: -0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-25% chance of ranged siege engines getting hit while under bombardment."
effect_template: "{VALUE}% chance of ranged siege engines getting hit while under bombardment."
alternative_perk_string_id: "EngineeringSiegeWorks"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: ""
---

# Dungeon Architect - engineer - siege

-25% chance of ranged siege engines getting hit while under bombardment.
