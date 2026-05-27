---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 175
perk: "Insurance Plans"
perk_string_id: "TradeInsurancePlans"
effect_slot: "primary"
role: "clan leader"
role_value: 2
perk_type: "gold economy"
perk_subtype: "income"
trigger_condition: []
effect_tags:
  - "caravan"
bonus: 5000
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "5000 denar return when one of your caravans is destroyed."
effect_template: "{VALUE} denar return when one of your caravans is destroyed."
alternative_perk_string_id: "TradeRapidDevelopment"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Caravan-destroyed condition is not represented by current trigger_condition taxonomy."
classification_review: ""
---

# Insurance Plans - clan leader - gold economy

5000 denar return when one of your caravans is destroyed.
