---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 200
perk: "Long Shots"
perk_string_id: "CrossbowLongShots"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "militia gain"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
  - "militia"
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 daily militia recruitment in the governed settlement."
effect_template: "{VALUE} daily militia recruitment in the governed settlement."
alternative_perk_string_id: "CrossbowSteady"
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

# Long Shots - governor - settlement defense

1 daily militia recruitment in the governed settlement.
