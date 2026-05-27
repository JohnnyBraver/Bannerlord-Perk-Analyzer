---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 50
perk: "Form Fitting Armor"
perk_string_id: "AthleticsFormFittingArmor"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "movement speed"
trigger_condition:
  - "party composition"
effect_tags:
  - "combat"
bonus: 0.04
increment_type: "add_factor"
increment_value: 1
troop_usage: "infantry"
troop_usage_value: 1
effect: "4% combat movement speed to tier 3+ foot troops in your formation."
effect_template: "{VALUE}% combat movement speed to tier 3+ foot troops in your formation."
alternative_perk_string_id: "AthleticsFury"
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

# Form Fitting Armor - captain - troop combat

4% combat movement speed to tier 3+ foot troops in your formation.
