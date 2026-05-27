---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 225
perk: "Dirty Fighting"
perk_string_id: "RogueryDirtyFighting"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "food reserve"
trigger_condition:
  - "during siege"
  - "governed settlement"
effect_tags:
  - "defense"
  - "food"
bonus: 2
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "2 random food item will be smuggled to the besieged governed settlement."
effect_template: "{VALUE} random food item will be smuggled to the besieged governed settlement."
alternative_perk_string_id: "RogueryArmsDealer"
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

# Dirty Fighting - governor - settlement defense

2 random food item will be smuggled to the besieged governed settlement.
