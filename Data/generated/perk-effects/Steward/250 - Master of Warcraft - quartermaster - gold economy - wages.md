---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 250
perk: "Master of Warcraft"
perk_string_id: "StewardMasterOfWarcraft"
effect_slot: "primary"
role: "quartermaster"
role_value: 10
perk_type: "gold economy"
perk_subtype: "wages"
trigger_condition:
  - "during siege"
effect_tags: []
bonus: -0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-25% troop wages while your party is in a siege camp."
effect_template: "{VALUE}% troop wages while your party is in a siege camp."
alternative_perk_string_id: "StewardMasterOfPlanning"
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

# Master of Warcraft - quartermaster - gold economy

-25% troop wages while your party is in a siege camp.
