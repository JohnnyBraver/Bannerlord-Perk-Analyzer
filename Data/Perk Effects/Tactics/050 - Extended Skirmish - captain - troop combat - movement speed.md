---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 50
perk: "Extended Skirmish"
perk_string_id: "TacticsExtendedSkirmish"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "movement speed"
trigger_condition:
  - "terrain"
  - "party composition"
effect_tags: []
bonus: 0.02
increment_type: "add_factor"
increment_value: 1
troop_usage: "none"
troop_usage_value: 0
effect: "2% movement speed to troops in your formation in snowy and forest terrains."
effect_template: "{VALUE}% movement speed to troops in your formation in snowy and forest terrains."
alternative_perk_string_id: "TacticsDecisiveBattle"
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

# Extended Skirmish - captain - troop combat

2% movement speed to troops in your formation in snowy and forest terrains.
