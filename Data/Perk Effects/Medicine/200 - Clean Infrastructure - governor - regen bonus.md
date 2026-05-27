---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 200
perk: "Clean Infrastructure"
perk_string_id: "MedicineCleanInfrastructure"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "regen bonus"
perk_subtype: ""
trigger_condition:
  - "governed settlement"
effect_tags:
  - "village"
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% recovery rate from raids in villages bound to the governed settlement."
effect_template: "{VALUE}% recovery rate from raids in villages bound to the governed settlement."
alternative_perk_string_id: "MedicinePhysicianOfPeople"
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

# Clean Infrastructure - governor - regen bonus

30% recovery rate from raids in villages bound to the governed settlement.
