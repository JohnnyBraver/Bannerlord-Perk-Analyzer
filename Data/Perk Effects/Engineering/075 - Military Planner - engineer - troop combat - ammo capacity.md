---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 75
perk: "Military Planner"
perk_string_id: "EngineeringMilitaryPlanner"
effect_slot: "primary"
role: "engineer"
role_value: 8
perk_type: "troop combat"
perk_subtype: "ammo capacity"
trigger_condition:
  - "during siege"
  - "party composition"
effect_tags: []
bonus: 0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "50% ammunition to ranged troops when besieging."
effect_template: "{VALUE}% ammunition to ranged troops when besieging."
alternative_perk_string_id: "EngineeringCarpenters"
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

# Military Planner - engineer - troop combat

50% ammunition to ranged troops when besieging.
