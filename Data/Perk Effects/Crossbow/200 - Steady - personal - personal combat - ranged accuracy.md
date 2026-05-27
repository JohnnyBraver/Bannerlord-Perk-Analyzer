---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 200
perk: "Steady"
perk_string_id: "CrossbowSteady"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "ranged accuracy"
trigger_condition:
  - "while mounted"
effect_tags:
  - "mounts"
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% accuracy penalty with crossbows while mounted."
effect_template: "{VALUE}% accuracy penalty with crossbows while mounted."
alternative_perk_string_id: "CrossbowLongShots"
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

# Steady - personal - personal combat

-50% accuracy penalty with crossbows while mounted.
