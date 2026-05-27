---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 75
perk: "Stiff Upper Lip"
perk_string_id: "StewardStiffUpperLip"
effect_slot: "primary"
role: "quartermaster"
role_value: 10
perk_type: "party management"
perk_subtype: "food consumption"
trigger_condition: []
effect_tags:
  - "food"
bonus: -0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-10% food consumption in your party while it is part of an army."
effect_template: "{VALUE}% food consumption in your party while it is part of an army."
alternative_perk_string_id: "StewardSweatshops"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Applies only while the party is part of an army; no dedicated army-membership trigger condition exists."
classification_review: ""
---

# Stiff Upper Lip - quartermaster - party management

-10% food consumption in your party while it is part of an army.
