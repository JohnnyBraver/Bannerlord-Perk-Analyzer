---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 225
perk: "Pre Battle Maneuvers"
perk_string_id: "TacticsPreBattleManeuvers"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "damage increase"
perk_subtype: ""
trigger_condition:
  - "simulation"
effect_tags: []
bonus: 0.01
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "1% damage per 100 skill difference with the enemy when troops are sent to confront the enemy."
effect_template: "{VALUE}% damage per 100 skill difference with the enemy when troops are sent to confront the enemy."
alternative_perk_string_id: "TacticsBesieged"
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

# Pre Battle Maneuvers - party leader - damage increase

1% damage per 100 skill difference with the enemy when troops are sent to confront the enemy.
