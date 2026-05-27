---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 50
perk: "Triage Tent"
perk_string_id: "MedicineTriageTent"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "food consumption"
trigger_condition:
  - "during siege"
  - "governed settlement"
effect_tags:
  - "defense"
  - "food"
bonus: -0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-5% food consumption for besieged governed settlement."
effect_template: "{VALUE}% food consumption for besieged governed settlement."
alternative_perk_string_id: "MedicineWalkItOff"
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

# Triage Tent - governor - settlement defense

-5% food consumption for besieged governed settlement.
