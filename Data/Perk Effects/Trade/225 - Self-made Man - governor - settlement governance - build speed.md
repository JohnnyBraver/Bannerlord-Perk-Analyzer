---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 225
perk: "Self-made Man"
perk_string_id: "TradeSelfMadeMan"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement governance"
perk_subtype: "build speed"
trigger_condition:
  - "project active"
  - "governed settlement"
effect_tags:
  - "projects"
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% build speed for marketplace, kiln and aqueduct projects."
effect_template: "{VALUE}% build speed for marketplace, kiln and aqueduct projects."
alternative_perk_string_id: "TradeSwordForBarter"
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

# Self-made Man - governor - settlement governance

30% build speed for marketplace, kiln and aqueduct projects.
