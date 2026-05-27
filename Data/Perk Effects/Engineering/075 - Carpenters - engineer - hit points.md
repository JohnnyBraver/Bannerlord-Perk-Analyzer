---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 75
perk: "Carpenters"
perk_string_id: "EngineeringCarpenters"
effect_slot: "primary"
role: "engineer"
role_value: 8
perk_type: "hit points"
perk_subtype: ""
trigger_condition:
  - "during siege"
effect_tags: []
bonus: 0.33000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "33% hit points to rams and siege-towers."
effect_template: "{VALUE}% hit points to rams and siege-towers."
alternative_perk_string_id: "EngineeringMilitaryPlanner"
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

# Carpenters - engineer - hit points

33% hit points to rams and siege-towers.
