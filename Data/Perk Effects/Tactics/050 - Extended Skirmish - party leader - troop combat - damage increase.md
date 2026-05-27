---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 50
perk: "Extended Skirmish"
perk_string_id: "TacticsExtendedSkirmish"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "simulation"
  - "terrain"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% damage in snowy and forest terrains when troops are sent to confront the enemy."
effect_template: "{VALUE}% damage in snowy and forest terrains when troops are sent to confront the enemy."
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

# Extended Skirmish - party leader - troop combat

10% damage in snowy and forest terrains when troops are sent to confront the enemy.
