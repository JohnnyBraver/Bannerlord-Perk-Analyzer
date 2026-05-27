---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 175
perk: "Perfect Health"
perk_string_id: "MedicinePerfectHealth"
effect_slot: "primary"
role: "surgeon"
role_value: 7
perk_type: "regen bonus"
perk_subtype: ""
trigger_condition: []
effect_tags:
  - "food"
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "5% recovery rate for each type of food in party inventory."
effect_template: "{VALUE}% recovery rate for each type of food in party inventory."
alternative_perk_string_id: "MedicineHealthAdvise"
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

# Perfect Health - surgeon - regen bonus

5% recovery rate for each type of food in party inventory.
