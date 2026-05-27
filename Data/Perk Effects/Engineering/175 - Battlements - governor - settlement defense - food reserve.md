---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 175
perk: "Battlements"
perk_string_id: "EngineeringBattlements"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "food reserve"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
  - "food"
bonus: 100
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "100 maximum food reserve limits in the governed settlement."
effect_template: "{VALUE} maximum food reserve limits in the governed settlement."
alternative_perk_string_id: "EngineeringCampBuilding"
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

# Battlements - governor - settlement defense

100 maximum food reserve limits in the governed settlement.
