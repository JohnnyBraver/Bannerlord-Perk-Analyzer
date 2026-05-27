---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 75
perk: "Desert Born"
perk_string_id: "ScoutingDesertBorn"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement economy"
perk_subtype: "settlement income"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "tax"
bonus: 0.025
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "2.5% tax income from the governed settlement."
effect_template: "{VALUE}% tax income from the governed settlement."
alternative_perk_string_id: "ScoutingForestKin"
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

# Desert Born - governor - settlement economy

2.5% tax income from the governed settlement.
