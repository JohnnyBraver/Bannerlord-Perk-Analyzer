---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 50
perk: "Seven Veterans"
perk_string_id: "StewardSevenVeterans"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "militia quality"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
  - "militia"
bonus: 0.1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "10% rate of militias will spawn as veteran troops in the governed settlement."
effect_template: "{VALUE}% rate of militias will spawn as veteran troops in the governed settlement."
alternative_perk_string_id: "StewardDrillSergant"
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

# Seven Veterans - governor - settlement defense

10% rate of militias will spawn as veteran troops in the governed settlement.
