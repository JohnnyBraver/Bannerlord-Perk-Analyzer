---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 150
perk: "Siege Engineer"
perk_string_id: "EngineeringSiegeEngineer"
effect_slot: "primary"
role: "governor"
role_value: 3
perk_type: "hit points"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
  - "governed settlement"
effect_tags: []
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% hit points to defensive siege engines in the governed settlement."
effect_template: "{VALUE}% hit points to defensive siege engines in the governed settlement."
alternative_perk_string_id: "EngineeringStonecutters"
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

# Siege Engineer - governor - hit points

30% hit points to defensive siege engines in the governed settlement.
