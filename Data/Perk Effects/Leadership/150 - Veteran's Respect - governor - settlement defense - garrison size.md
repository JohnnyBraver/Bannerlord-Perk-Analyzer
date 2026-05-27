---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 150
perk: "Veteran's Respect"
perk_string_id: "LeadershipVeteransRespect"
effect_slot: "primary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "garrison size"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
  - "garrison"
bonus: 20
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "20 garrison size in the governed settlement."
effect_template: "{VALUE} garrison size in the governed settlement."
alternative_perk_string_id: "LeadershipCitizenMilitia"
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

# Veteran's Respect - governor - settlement defense

20 garrison size in the governed settlement.
