---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Two Handed"
level: 100
perk: "Beast Slayer"
perk_string_id: "TwoHandedBeastSlayer"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "mounts"
trigger_condition: []
effect_tags:
  - "mounts"
  - "weapons"
bonus: 0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "50% damage to mounts with two handed weapons."
effect_template: "{VALUE}% damage to mounts with two handed weapons."
alternative_perk_string_id: "TwoHandedShieldBreaker"
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

# Beast Slayer - personal - personal combat

50% damage to mounts with two handed weapons.
