---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 125
perk: "Skirmisher"
perk_string_id: "ThrowingSkirmisher"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "ranged"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: -0.03
increment_type: "add_factor"
increment_value: 1
troop_usage: "none"
troop_usage_value: 0
effect: "-3% damage taken by ranged attacks to troops in your formation."
effect_template: "{VALUE}% damage taken by ranged attacks to troops in your formation."
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

# Skirmisher - captain - troop combat

-3% damage taken by ranged attacks to troops in your formation.
