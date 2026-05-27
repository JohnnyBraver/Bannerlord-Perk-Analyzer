---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 200
perk: "Steady"
perk_string_id: "AthleticsSteady"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement economy"
perk_subtype: "production"
trigger_condition:
  - "governed settlement"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% production in farms, mines, lumber camps and clay pits bound to the governed settlement."
effect_template: "{VALUE}% production in farms, mines, lumber camps and clay pits bound to the governed settlement."
alternative_perk_string_id: "AthleticsStrong"
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

# Steady - governor - settlement economy

10% production in farms, mines, lumber camps and clay pits bound to the governed settlement.
