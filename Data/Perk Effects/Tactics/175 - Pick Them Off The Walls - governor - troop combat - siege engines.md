---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 175
perk: "Pick Them Off The Walls"
perk_string_id: "TacticsPickThemOfTheWalls"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "troop combat"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
  - "governed settlement"
effect_tags: []
bonus: 0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "25% chance for dealing double damage to besieging troops in siege bombardment of the governed settlement."
effect_template: "{VALUE}% chance for dealing double damage to besieging troops in siege bombardment of the governed settlement."
alternative_perk_string_id: "TacticsMakeThemPay"
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

# Pick Them Off The Walls - governor - troop combat

25% chance for dealing double damage to besieging troops in siege bombardment of the governed settlement.
