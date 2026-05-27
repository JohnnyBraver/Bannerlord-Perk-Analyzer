---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 250
perk: "Fleet Footed"
perk_string_id: "RogueryFleetFooted"
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
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% combat movement speed while no weapons or shields are equipped."
effect_template: "{VALUE}% combat movement speed while no weapons or shields are equipped."
alternative_perk_string_id: "RogueryDashAndSlash"
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

# Fleet Footed - personal - personal combat

10% combat movement speed while no weapons or shields are equipped.
