---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 200
perk: "Splinters"
perk_string_id: "ThrowingSplinters"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "shields"
trigger_condition: []
effect_tags:
  - "weapons"
bonus: 3
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "Triple damage against shields with throwing axes."
effect_template: "Triple damage against shields with throwing axes."
alternative_perk_string_id: "ThrowingResourceful"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Description says triple shield damage, but bonus 3 with add_factor appears to apply +300% damage, or 4x total, unless this path treats the factor as a direct multiplier."
classification_review: ""
---

# Splinters - personal - personal combat

Triple damage against shields with throwing axes.
