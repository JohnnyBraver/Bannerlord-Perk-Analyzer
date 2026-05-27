---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 100
perk: "Wall Breaker"
perk_string_id: "EngineeringWallBreaker"
effect_slot: "primary"
role: "engineer"
role_value: 8
perk_type: "damage increase"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
effect_tags: []
bonus: 0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "25% damage dealt to walls during siege bombardment."
effect_template: "{VALUE}% damage dealt to walls during siege bombardment."
alternative_perk_string_id: "EngineeringDreadfulSieger"
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

# Wall Breaker - engineer - damage increase

25% damage dealt to walls during siege bombardment.
