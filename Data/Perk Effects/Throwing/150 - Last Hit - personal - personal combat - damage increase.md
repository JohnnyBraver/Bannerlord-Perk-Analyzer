---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 150
perk: "Last Hit"
perk_string_id: "ThrowingLastHit"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "damage increase"
trigger_condition:
  - "health threshold"
effect_tags: []
bonus: 0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "50% damage to enemies with less than half of their hit points left."
effect_template: "{VALUE}% damage to enemies with less than half of their hit points left."
alternative_perk_string_id: "ThrowingFocus"
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

# Last Hit - personal - personal combat

50% damage to enemies with less than half of their hit points left.
