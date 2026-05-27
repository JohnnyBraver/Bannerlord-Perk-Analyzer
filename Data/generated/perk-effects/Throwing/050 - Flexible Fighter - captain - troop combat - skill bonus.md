---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 50
perk: "Flexible Fighter"
perk_string_id: "ThrowingFlexibleFighter"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "skill bonus"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 15
increment_type: "add"
increment_value: 0
troop_usage: "infantry"
troop_usage_value: 1
effect: "15 Control skills of infantry, 15 Vigor skills of archers in your formation."
effect_template: "{VALUE} Control skills of infantry, {VALUE} Vigor skills of archers in your formation."
alternative_perk_string_id: "ThrowingHunter"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Troop skill bonus spans infantry Control and archer Vigor; not hero character growth."
---

# Flexible Fighter - captain - troop combat

15 Control skills of infantry, 15 Vigor skills of archers in your formation.
