---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 175
perk: "Rapid Development"
perk_string_id: "TradeRapidDevelopment"
effect_slot: "primary"
role: "clan leader"
role_value: 2
perk_type: "gold economy"
perk_subtype: "income"
trigger_condition: []
effect_tags:
  - "workshop"
bonus: 5000
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "5000 denar return for each workshop when workshop's town is captured by an enemy."
effect_template: "{VALUE} denar return for each workshop when workshop's town is captured by an enemy."
alternative_perk_string_id: "TradeInsurancePlans"
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

# Rapid Development - clan leader - gold economy

5000 denar return for each workshop when workshop's town is captured by an enemy.
