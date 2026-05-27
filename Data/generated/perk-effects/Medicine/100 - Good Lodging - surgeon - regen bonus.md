---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 100
perk: "Good Lodging"
perk_string_id: "MedicineGoodLodging"
effect_slot: "primary"
role: "surgeon"
role_value: 7
perk_type: "regen bonus"
perk_subtype: ""
trigger_condition:
  - "while waiting"
effect_tags: []
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% healing rate while resting in settlements."
effect_template: "{VALUE}% healing rate while resting in settlements."
alternative_perk_string_id: "MedicineBestMedicine"
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

# Good Lodging - surgeon - regen bonus

20% healing rate while resting in settlements.
