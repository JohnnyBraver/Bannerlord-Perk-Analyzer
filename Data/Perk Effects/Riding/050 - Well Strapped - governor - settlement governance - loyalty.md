---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 50
perk: "Well Strapped"
perk_string_id: "RidingWellStraped"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement governance"
perk_subtype: "loyalty"
trigger_condition:
  - "governed settlement"
effect_tags: []
bonus: 0.5
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "0.5 daily loyalty to the governed settlement."
effect_template: "{VALUE} daily loyalty to the governed settlement."
alternative_perk_string_id: "RidingVeterinary"
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

# Well Strapped - governor - settlement governance

0.5 daily loyalty to the governed settlement.
