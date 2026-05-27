---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 200
perk: "Elite Reserves"
perk_string_id: "TacticsEliteReserves"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "damage resistance"
perk_subtype: ""
trigger_condition:
  - "simulation"
  - "party composition"
effect_tags: []
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% less damage to tier 3+ units when troops are sent to confront the enemy."
effect_template: "{VALUE}% less damage to tier 3+ units when troops are sent to confront the enemy."
alternative_perk_string_id: "TacticsEncirclement"
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

# Elite Reserves - party leader - damage resistance

-20% less damage to tier 3+ units when troops are sent to confront the enemy.
