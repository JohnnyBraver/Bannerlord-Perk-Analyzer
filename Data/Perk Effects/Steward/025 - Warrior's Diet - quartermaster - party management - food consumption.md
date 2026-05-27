---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 25
perk: "Warrior's Diet"
perk_string_id: "StewardWarriorsDiet"
effect_slot: "primary"
role: "quartermaster"
role_value: 10
perk_type: "party management"
perk_subtype: "food consumption"
trigger_condition: []
effect_tags:
  - "food"
bonus: -0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-10% food consumption in your party."
effect_template: "{VALUE}% food consumption in your party."
alternative_perk_string_id: "StewardFrugal"
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

# Warrior's Diet - quartermaster - party management

-10% food consumption in your party.
