---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 125
perk: "Relief Force"
perk_string_id: "RidingReliefForce"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "security"
trigger_condition:
  - "party composition"
  - "governed settlement"
effect_tags:
  - "defense"
  - "mounts"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% security provided by mounted troops in the governed settlement."
effect_template: "{VALUE}% security provided by mounted troops in the governed settlement."
alternative_perk_string_id: ""
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

# Relief Force - governor - settlement defense

20% security provided by mounted troops in the governed settlement.
