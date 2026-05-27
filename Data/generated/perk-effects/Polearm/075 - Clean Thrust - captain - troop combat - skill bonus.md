---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 75
perk: "Clean Thrust"
perk_string_id: "PolearmCleanThrust"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "skill bonus"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
bonus: 30
increment_type: "add"
increment_value: 0
troop_usage: "infantry, melee"
troop_usage_value: 129
effect: "30 polearm skill to infantry in your formation."
effect_template: "{VALUE} polearm skill to infantry in your formation."
alternative_perk_string_id: "PolearmSwiftSwing"
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

# Clean Thrust - captain - troop combat

30 polearm skill to infantry in your formation.
