---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 125
perk: "Skirmisher"
perk_string_id: "ThrowingSkirmisher"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "ranged"
trigger_condition: []
effect_tags:
  - "weapons"
bonus: -0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-10% damage taken by ranged attacks while holding a throwing weapon."
effect_template: "{VALUE}% damage taken by ranged attacks while holding a throwing weapon."
alternative_perk_string_id: "ThrowingSaddlebags"
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

# Skirmisher - personal - personal combat

-10% damage taken by ranged attacks while holding a throwing weapon.
