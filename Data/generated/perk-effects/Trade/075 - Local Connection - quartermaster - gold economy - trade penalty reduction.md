---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 75
perk: "Local Connection"
perk_string_id: "TradeLocalConnection"
effect_slot: "secondary"
role: "quartermaster"
role_value: 10
perk_type: "gold economy"
perk_subtype: "trade penalty reduction"
trigger_condition: []
effect_tags:
  - "trade"
bonus: -0.15000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-15% price penalty while selling animals."
effect_template: "{VALUE}% price penalty while selling animals."
alternative_perk_string_id: "TradeDistributedGoods"
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

# Local Connection - quartermaster - gold economy

-15% price penalty while selling animals.
