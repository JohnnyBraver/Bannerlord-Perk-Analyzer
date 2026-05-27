---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 100
perk: "Knock Off"
perk_string_id: "ThrowingKnockOff"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "dismount"
trigger_condition: []
effect_tags:
  - "weapons"
  - "mounts"
bonus: 0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "Thrown weapons can now dismount and ignore 25% dismount resistance on attacks against cavalry."
effect_template: "Thrown weapons can now dismount and ignore {VALUE}% dismount resistance on attacks against cavalry."
alternative_perk_string_id: "ThrowingRunningThrow"
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

# Knock Off - personal - personal combat

Thrown weapons can now dismount and ignore 25% dismount resistance on attacks against cavalry.
