---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 250
perk: "Spartan"
perk_string_id: "AthleticsSpartan"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "food consumption"
trigger_condition: []
effect_tags:
  - "food"
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% food consumption in your party."
effect_template: "{VALUE}% food consumption in your party."
alternative_perk_string_id: "AthleticsIgnorePain"
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

# Spartan - party leader - party management

-20% food consumption in your party.
