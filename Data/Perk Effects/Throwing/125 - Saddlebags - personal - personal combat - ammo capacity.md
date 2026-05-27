---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 125
perk: "Saddlebags"
perk_string_id: "ThrowingSaddlebags"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "ammo capacity"
trigger_condition:
  - "while mounted"
effect_tags:
  - "weapons"
  - "mounts"
bonus: 2
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "2 ammunition for throwing weapons when you start a battle mounted."
effect_template: "{VALUE} ammunition for throwing weapons when you start a battle mounted."
alternative_perk_string_id: "ThrowingSkirmisher"
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

# Saddlebags - personal - personal combat

2 ammunition for throwing weapons when you start a battle mounted.
