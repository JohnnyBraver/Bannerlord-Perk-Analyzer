---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Two Handed"
level: 25
perk: "Strong Grip"
perk_string_id: "TwoHandedStrongGrip"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "skill bonus"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 30
increment_type: "add"
increment_value: 0
troop_usage: "infantry, formation"
troop_usage_value: 65
effect: "30 two handed skill to infantry troops in your formation."
effect_template: "{VALUE} two handed skill to infantry troops in your formation."
alternative_perk_string_id: "TwoHandedWoodChopper"
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

# Strong Grip - captain - troop combat

30 two handed skill to infantry troops in your formation.
