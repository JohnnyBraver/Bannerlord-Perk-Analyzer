---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 150
perk: "Content Trades"
perk_string_id: "TradeContentTrades"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "wages"
trigger_condition:
  - "while waiting"
effect_tags: []
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% wages paid while waiting in settlements."
effect_template: "{VALUE}% wages paid while waiting in settlements."
alternative_perk_string_id: "TradeMercenaryConnections"
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

# Content Trades - party leader - gold economy

-50% wages paid while waiting in settlements.
