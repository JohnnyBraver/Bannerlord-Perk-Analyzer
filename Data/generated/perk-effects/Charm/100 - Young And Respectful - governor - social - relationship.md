---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Charm"
level: 100
perk: "Young And Respectful"
perk_string_id: "CharmYoungAndRespectful"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "social"
perk_subtype: "relationship"
trigger_condition:
  - "governed settlement"
effect_tags: []
bonus: 0.02
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "2% daily chance to increase relations with a random notable of same sex in the governed settlement."
effect_template: "{VALUE}% daily chance to increase relations with a random notable of same sex in the governed settlement."
alternative_perk_string_id: "CharmInBloom"
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

# Young And Respectful - governor - social

2% daily chance to increase relations with a random notable of same sex in the governed settlement.
