---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 150
perk: "Citizen Militia"
perk_string_id: "LeadershipCitizenMilitia"
effect_slot: "primary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "militia quality"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
  - "militia"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% rate of militias will spawn as veteran troops in the governed settlement."
effect_template: "{VALUE}% rate of militias will spawn as veteran troops in the governed settlement."
alternative_perk_string_id: "LeadershipVeteransRespect"
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

# Citizen Militia - governor - settlement defense

20% rate of militias will spawn as veteran troops in the governed settlement.
