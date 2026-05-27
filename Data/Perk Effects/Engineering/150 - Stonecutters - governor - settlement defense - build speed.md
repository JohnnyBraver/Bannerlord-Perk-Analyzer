---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 150
perk: "Stonecutters"
perk_string_id: "EngineeringStonecutters"
effect_slot: "primary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "build speed"
trigger_condition:
  - "project active"
  - "governed settlement"
effect_tags:
  - "defense"
  - "fortifications"
  - "projects"
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% build speed for fortifications, aqueducts and barrack projects in the governed settlement."
effect_template: "{VALUE}% build speed for fortifications, aqueducts and barrack projects in the governed settlement."
alternative_perk_string_id: "EngineeringSiegeEngineer"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Composite project set spans fortifications, aqueducts, and barracks; settlement-defense classification is partial."
---

# Stonecutters - governor - settlement defense

30% build speed for fortifications, aqueducts and barrack projects in the governed settlement.
