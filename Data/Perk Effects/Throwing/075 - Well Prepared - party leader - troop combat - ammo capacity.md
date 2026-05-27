---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 75
perk: "Well Prepared"
perk_string_id: "ThrowingWellPrepared"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "ammo capacity"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 ammunition for throwing weapons to troops in your party."
effect_template: "{VALUE} ammunition for throwing weapons to troops in your party."
alternative_perk_string_id: "ThrowingMountedSkirmisher"
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

# Well Prepared - party leader - troop combat

1 ammunition for throwing weapons to troops in your party.
