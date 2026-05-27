---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 250
perk: "Battle Hardened"
perk_string_id: "MedicineBattleHardened"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "damage resistance"
trigger_condition:
  - "during siege"
  - "governed settlement"
effect_tags:
  - "defense"
bonus: -0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-25% siege attrition loss in the governed settlement."
effect_template: "{VALUE}% siege attrition loss in the governed settlement."
alternative_perk_string_id: "MedicineHelpingHands"
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

# Battle Hardened - governor - settlement defense

-25% siege attrition loss in the governed settlement.
