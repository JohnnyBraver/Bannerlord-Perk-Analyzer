---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 200
perk: "Physician of People"
perk_string_id: "MedicinePhysicianOfPeople"
effect_slot: "primary"
role: "governor"
role_value: 3
perk_type: "settlement governance"
perk_subtype: "loyalty"
trigger_condition:
  - "governed settlement"
effect_tags: []
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 loyalty per day in the governed settlement."
effect_template: "{VALUE} loyalty per day in the governed settlement."
alternative_perk_string_id: "MedicineCleanInfrastructure"
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

# Physician of People - governor - settlement governance

1 loyalty per day in the governed settlement.
