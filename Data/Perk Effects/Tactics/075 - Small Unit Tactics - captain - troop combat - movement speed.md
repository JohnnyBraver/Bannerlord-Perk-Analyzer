---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 75
perk: "Small Unit Tactics"
perk_string_id: "TacticsSmallUnitTactics"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "movement speed"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "none"
troop_usage_value: 0
effect: "5% movement speed to troops in your formation when there are less than 15 soldiers."
effect_template: "{VALUE}% movement speed to troops in your formation when there are less than 15 soldiers."
alternative_perk_string_id: "TacticsHordeLeader"
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

# Small Unit Tactics - captain - troop combat

5% movement speed to troops in your formation when there are less than 15 soldiers.
