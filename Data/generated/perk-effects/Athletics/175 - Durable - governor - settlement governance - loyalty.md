---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 175
perk: "Durable"
perk_string_id: "AthleticsDurable"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement governance"
perk_subtype: "loyalty"
trigger_condition:
  - "governed settlement"
effect_tags: []
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 daily loyalty in the governed settlement."
effect_template: "{VALUE} daily loyalty in the governed settlement."
alternative_perk_string_id: "AthleticsEnergetic"
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

# Durable - governor - settlement governance

1 daily loyalty in the governed settlement.
