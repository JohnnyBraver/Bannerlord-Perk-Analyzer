---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 250
perk: "Master of Planning"
perk_string_id: "StewardMasterOfPlanning"
effect_slot: "primary"
role: "quartermaster"
role_value: 10
perk_type: "party management"
perk_subtype: "food consumption"
trigger_condition:
  - "during siege"
effect_tags:
  - "food"
bonus: -0.40000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-40% food consumption while your party is in a siege camp."
effect_template: "{VALUE}% food consumption while your party is in a siege camp."
alternative_perk_string_id: "StewardMasterOfWarcraft"
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

# Master of Planning - quartermaster - party management

-40% food consumption while your party is in a siege camp.
