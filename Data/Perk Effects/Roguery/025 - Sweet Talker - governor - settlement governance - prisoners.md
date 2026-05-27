---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 25
perk: "Sweet Talker"
perk_string_id: "RoguerySweetTalker"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement governance"
perk_subtype: "prisoners"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "prisoner escape"
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% prisoner escape chance in the governed settlement."
effect_template: "{VALUE}% prisoner escape chance in the governed settlement."
alternative_perk_string_id: "RogueryNoRestForTheWicked"
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

# Sweet Talker - governor - settlement governance

-20% prisoner escape chance in the governed settlement.
