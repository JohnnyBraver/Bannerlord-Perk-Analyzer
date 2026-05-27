---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 75
perk: "Local Connection"
perk_string_id: "TradeLocalConnection"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "social"
perk_subtype: "relationship"
trigger_condition: []
effect_tags: []
bonus: 2
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "Double the relationship gain by resolved issues with merchants."
effect_template: "Double the relationship gain by resolved issues with merchants."
alternative_perk_string_id: "TradeDistributedGoods"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Description says double relationship gain, but game increment_type is add while paired Distributed Goods uses add_factor."
classification_review: ""
---

# Local Connection - personal - social

Double the relationship gain by resolved issues with merchants.
