---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 100
perk: "Toll Gates"
perk_string_id: "TradeTollgates"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement economy"
perk_subtype: "settlement income"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "caravan"
bonus: 30
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "30 gold for each caravan visiting the governed settlement."
effect_template: "{VALUE} gold for each caravan visiting the governed settlement."
alternative_perk_string_id: "TradeTravelingRumors"
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

# Toll Gates - governor - settlement economy

30 gold for each caravan visiting the governed settlement.
