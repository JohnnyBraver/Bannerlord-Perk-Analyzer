---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 225
perk: "Arms Dealer"
perk_string_id: "RogueryArmsDealer"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "militia gain"
trigger_condition:
  - "during siege"
  - "governed settlement"
effect_tags:
  - "defense"
  - "militia"
bonus: 2
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "200% militia per day in the besieged governed settlement."
effect_template: "{VALUE}% militia per day in the besieged governed settlement."
alternative_perk_string_id: "RogueryDirtyFighting"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Description renders as 200% militia per day, but game increment_type is add with bonus 2."
classification_review: ""
---

# Arms Dealer - governor - settlement defense

200% militia per day in the besieged governed settlement.
