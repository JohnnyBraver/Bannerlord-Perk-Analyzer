---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 225
perk: "Strong Legs"
perk_string_id: "AthleticsStrongLegs"
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
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% food consumption in the governed settlement while under siege."
effect_template: "{VALUE}% food consumption in the governed settlement while under siege."
alternative_perk_string_id: "AthleticsStrongArms"
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

# Strong Legs - governor - settlement defense

-20% food consumption in the governed settlement while under siege.
