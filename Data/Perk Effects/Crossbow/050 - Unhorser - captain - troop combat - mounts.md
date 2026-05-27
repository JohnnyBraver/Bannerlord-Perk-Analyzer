---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 50
perk: "Unhorser"
perk_string_id: "CrossbowUnhorser"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "mounts"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "none"
troop_usage_value: 1024
effect: "20% damage against mounts to crossbow troops in your formation."
effect_template: "{VALUE}% damage against mounts to crossbow troops in your formation."
alternative_perk_string_id: "CrossbowWindWinder"
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

# Unhorser - captain - troop combat

20% damage against mounts to crossbow troops in your formation.
