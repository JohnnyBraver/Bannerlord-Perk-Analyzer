---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 100
perk: "Coaching"
perk_string_id: "TacticsCoaching"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "damage increase"
perk_subtype: ""
trigger_condition:
  - "simulation"
effect_tags: []
bonus: 0.03
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "3% damage when your troops are sent to confront the enemy."
effect_template: "{VALUE}% damage when your troops are sent to confront the enemy."
alternative_perk_string_id: "TacticsLawkeeper"
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

# Coaching - party leader - damage increase

3% damage when your troops are sent to confront the enemy.
