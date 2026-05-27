---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 125
perk: "White Lies"
perk_string_id: "RogueryWhiteLies"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "social"
perk_subtype: "relationship"
trigger_condition:
  - "governed settlement"
effect_tags: []
bonus: 0.02
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "2% chance to get 1 relation per day with a random notable in the governed settlement."
effect_template: "{VALUE}% chance to get 1 relation per day with a random notable in the governed settlement."
alternative_perk_string_id: "RogueryScarface"
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

# White Lies - governor - social

2% chance to get 1 relation per day with a random notable in the governed settlement.
