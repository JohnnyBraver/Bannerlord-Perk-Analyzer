---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 100
perk: "Sprint"
perk_string_id: "AthleticsSprint"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "movement speed"
trigger_condition: []
effect_tags:
  - "shield penalty"
  - "weapons"
  - "combat"
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "5% combat movement speed when you have no shields and no ranged weapons equipped."
effect_template: "{VALUE}% combat movement speed when you have no shields and no ranged weapons equipped."
alternative_perk_string_id: "AthleticsPowerful"
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

# Sprint - personal - personal combat

5% combat movement speed when you have no shields and no ranged weapons equipped.
