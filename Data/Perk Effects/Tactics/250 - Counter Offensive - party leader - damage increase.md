---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 250
perk: "Counter Offensive"
perk_string_id: "TacticsCounteroffensive"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "damage increase"
perk_subtype: ""
trigger_condition:
  - "simulation"
  - "attacking"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% damage when troops are sent to confront the attacking enemy in a field battle."
effect_template: "{VALUE}% damage when troops are sent to confront the attacking enemy in a field battle."
alternative_perk_string_id: "TacticsGensdarmes"
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

# Counter Offensive - party leader - damage increase

10% damage when troops are sent to confront the attacking enemy in a field battle.
