---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 100
perk: "Efficient Campaigner"
perk_string_id: "StewardEfficientCampaigner"
effect_slot: "secondary"
role: "quartermaster"
role_value: 10
perk_type: "gold economy"
perk_subtype: "wages"
trigger_condition: []
effect_tags: []
bonus: -0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-25% troop wages in your party while it is part of an army."
effect_template: "{VALUE}% troop wages in your party while it is part of an army."
alternative_perk_string_id: "StewardPaidInPromise"
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

# Efficient Campaigner - quartermaster - gold economy

-25% troop wages in your party while it is part of an army.
