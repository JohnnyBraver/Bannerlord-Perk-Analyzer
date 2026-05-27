---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 250
perk: "Spring of Gold"
perk_string_id: "TradeSpringOfGold"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement governance"
perk_subtype: "project effect"
trigger_condition:
  - "project active"
  - "governed settlement"
effect_tags:
  - "projects"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% effect from boosting projects in the governed settlement."
effect_template: "{VALUE}% effect from boosting projects in the governed settlement."
alternative_perk_string_id: "TradeSilverTongue"
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

# Spring of Gold - governor - settlement governance

20% effect from boosting projects in the governed settlement.
