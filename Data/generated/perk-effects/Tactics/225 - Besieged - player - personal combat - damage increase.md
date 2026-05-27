---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 225
perk: "Besieged"
perk_string_id: "TacticsBesieged"
effect_slot: "primary"
role: "player"
role_value: 11
perk_type: "personal combat"
perk_subtype: "damage increase"
trigger_condition:
  - "during siege"
  - "simulation"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% damage while besieged when troops are sent to confront the enemy."
effect_template: "{VALUE}% damage while besieged when troops are sent to confront the enemy."
alternative_perk_string_id: "TacticsPreBattleManeuvers"
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

# Besieged - player - personal combat

10% damage while besieged when troops are sent to confront the enemy.
