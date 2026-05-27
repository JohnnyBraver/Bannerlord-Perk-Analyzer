---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 200
perk: "Elite Reserves"
perk_string_id: "TacticsEliteReserves"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage resistance"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: -0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "none"
troop_usage_value: 0
effect: "-5% damage taken by troops in your formation."
effect_template: "{VALUE}% damage taken by troops in your formation."
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

# Elite Reserves - captain - troop combat

-5% damage taken by troops in your formation.
