---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 100
perk: "Dreadful Besieger"
perk_string_id: "EngineeringDreadfulSieger"
effect_slot: "primary"
role: "governor"
role_value: 3
perk_type: "ranged accuracy"
perk_subtype: ""
trigger_condition:
  - "during siege"
  - "governed settlement"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% accuracy to your siege engines during siege bombardments in the governed settlement."
effect_template: "{VALUE}% accuracy to your siege engines during siege bombardments in the governed settlement."
alternative_perk_string_id: "EngineeringWallBreaker"
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

# Dreadful Besieger - governor - ranged accuracy

10% accuracy to your siege engines during siege bombardments in the governed settlement.
