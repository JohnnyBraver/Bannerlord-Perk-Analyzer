---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 150
perk: "Mercenary Connections"
perk_string_id: "TradeMercenaryConnections"
effect_slot: "primary"
role: "governor"
role_value: 3
perk_type: "settlement economy"
perk_subtype: "production"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "workshop"
bonus: 0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "25% workshop production rate."
effect_template: "{VALUE}% workshop production rate."
alternative_perk_string_id: "TradeContentTrades"
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

# Mercenary Connections - governor - settlement economy

25% workshop production rate.
