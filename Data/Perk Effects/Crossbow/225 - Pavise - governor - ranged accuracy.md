---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 225
perk: "Pavise"
perk_string_id: "CrossbowPavise"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "ranged accuracy"
perk_subtype: ""
trigger_condition:
  - "governed settlement"
effect_tags: []
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% accuracy to ballistas in the governed settlement."
effect_template: "{VALUE}% accuracy to ballistas in the governed settlement."
alternative_perk_string_id: "CrossbowHammerBolts"
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

# Pavise - governor - ranged accuracy

30% accuracy to ballistas in the governed settlement.
