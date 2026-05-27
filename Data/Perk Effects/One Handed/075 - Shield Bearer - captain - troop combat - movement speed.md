---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "One Handed"
level: 75
perk: "Shield Bearer"
perk_string_id: "OneHandedShieldBearer"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "movement speed"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.03
increment_type: "add_factor"
increment_value: 1
troop_usage: "infantry"
troop_usage_value: 1
effect: "3% movement speed to infantry in your formation."
effect_template: "{VALUE}% movement speed to infantry in your formation."
alternative_perk_string_id: "OneHandedCavalry"
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

# Shield Bearer - captain - troop combat

3% movement speed to infantry in your formation.
