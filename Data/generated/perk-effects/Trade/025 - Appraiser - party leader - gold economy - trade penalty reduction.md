---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 25
perk: "Appraiser"
perk_string_id: "TradeAppraiser"
effect_slot: "primary"
role: "party leader"
role_value: 5
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
effect: "-15% price penalty while selling equipment."
effect_template: "{VALUE}% price penalty while selling equipment."
alternative_perk_string_id: "TradeWholeSeller"
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

# Appraiser - party leader - gold economy

-15% price penalty while selling equipment.
