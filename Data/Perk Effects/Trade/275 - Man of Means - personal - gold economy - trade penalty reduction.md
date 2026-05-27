---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 275
perk: "Man of Means"
perk_string_id: "TradeManOfMeans"
effect_slot: "secondary"
role: "personal"
role_value: 12
perk_type: "gold economy"
perk_subtype: "trade penalty reduction"
trigger_condition: []
effect_tags:
  - "ransom"
bonus: -0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-30% ransom cost for your freedom."
effect_template: "{VALUE}% ransom cost for your freedom."
alternative_perk_string_id: "TradeTrickleDown"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Ransom-cost reduction is not really a trade penalty; current subtype is a lossy fallback unless a ransom-cost subtype is added."
---

# Man of Means - personal - gold economy

-30% ransom cost for your freedom.
