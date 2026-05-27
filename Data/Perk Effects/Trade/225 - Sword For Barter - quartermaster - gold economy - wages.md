---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Trade"
level: 225
perk: "Sword For Barter"
perk_string_id: "TradeSwordForBarter"
effect_slot: "secondary"
role: "quartermaster"
role_value: 10
perk_type: "gold economy"
perk_subtype: "wages"
trigger_condition: []
effect_tags:
  - "caravan"
bonus: -0.15000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-15% caravan guard wages."
effect_template: "{VALUE}% caravan guard wages."
alternative_perk_string_id: "TradeSelfMadeMan"
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

# Sword For Barter - quartermaster - gold economy

-15% caravan guard wages.
