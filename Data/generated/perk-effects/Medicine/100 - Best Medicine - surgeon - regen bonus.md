---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 100
perk: "Best Medicine"
perk_string_id: "MedicineBestMedicine"
effect_slot: "primary"
role: "surgeon"
role_value: 7
perk_type: "regen bonus"
perk_subtype: ""
trigger_condition:
  - "morale threshold"
effect_tags: []
bonus: 0.15000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "15% healing rate while party morale is above 70."
effect_template: "{VALUE}% healing rate while party morale is above 70."
alternative_perk_string_id: "MedicineGoodLodging"
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

# Best Medicine - surgeon - regen bonus

15% healing rate while party morale is above 70.
