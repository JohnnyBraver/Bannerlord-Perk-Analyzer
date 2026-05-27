---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 200
perk: "Clean Infrastructure"
perk_string_id: "MedicineCleanInfrastructure"
effect_slot: "primary"
role: "governor"
role_value: 3
perk_type: "settlement economy"
perk_subtype: "prosperity"
trigger_condition:
  - "project active"
  - "governed settlement"
effect_tags:
  - "projects"
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 prosperity bonus from civilian projects in the governed settlement."
effect_template: "{VALUE} prosperity bonus from civilian projects in the governed settlement."
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

# Clean Infrastructure - governor - settlement economy

1 prosperity bonus from civilian projects in the governed settlement.
