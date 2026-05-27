---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 150
perk: "Bush Doctor"
perk_string_id: "MedicineBushDoctor"
effect_slot: "primary"
role: "governor"
role_value: 3
perk_type: "settlement economy"
perk_subtype: "hearth growth"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "village"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% hearth growth in villages bound to the governed settlement."
effect_template: "{VALUE}% hearth growth in villages bound to the governed settlement."
alternative_perk_string_id: "MedicinePristineStreets"
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

# Bush Doctor - governor - settlement economy

20% hearth growth in villages bound to the governed settlement.
