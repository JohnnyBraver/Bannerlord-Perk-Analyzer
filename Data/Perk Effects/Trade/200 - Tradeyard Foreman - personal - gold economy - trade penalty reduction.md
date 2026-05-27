---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 200
perk: "Tradeyard Foreman"
perk_string_id: "TradeTradeyardForeman"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "gold economy"
perk_subtype: "trade penalty reduction"
trigger_condition: []
effect_tags:
  - "trade"
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% price penalty while selling pottery, tools, silk and jewelry."
effect_template: "{VALUE}% price penalty while selling pottery, tools, silk and jewelry."
alternative_perk_string_id: "TradeGranaryAccountant"
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

# Tradeyard Foreman - personal - gold economy

-20% price penalty while selling pottery, tools, silk and jewelry.
