---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 275
perk: "Trickle Down"
perk_string_id: "TradeTrickleDown"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "social"
perk_subtype: "relationship"
trigger_condition: []
effect_tags: []
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 relationship with merchants if 10.000 or more denars are spent on a single deal."
effect_template: "{VALUE} relationship with merchants if 10.000 or more denars are spent on a single deal."
alternative_perk_string_id: "TradeManOfMeans"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Single-deal spending threshold is not represented by current trigger_condition taxonomy."
classification_review: ""
---

# Trickle Down - party leader - social

1 relationship with merchants if 10.000 or more denars are spent on a single deal.
