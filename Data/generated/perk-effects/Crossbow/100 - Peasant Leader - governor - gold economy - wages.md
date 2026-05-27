---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 100
perk: "Peasant Leader"
perk_string_id: "CrossbowPeasantLeader"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "gold economy"
perk_subtype: "wages"
trigger_condition:
  - "party composition"
  - "governed settlement"
effect_tags:
  - "garrison"
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% garrisoned ranged troop wages in the governed settlement."
effect_template: "{VALUE}% garrisoned ranged troop wages in the governed settlement."
alternative_perk_string_id: "CrossbowRenownMarksmen"
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

# Peasant Leader - governor - gold economy

-20% garrisoned ranged troop wages in the governed settlement.
