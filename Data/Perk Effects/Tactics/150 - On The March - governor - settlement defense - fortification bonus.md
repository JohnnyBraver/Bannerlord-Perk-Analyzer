---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 150
perk: "On The March"
perk_string_id: "TacticsOnTheMarch"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "fortification bonus"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
  - "fortifications"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% fortification bonus to the governed settlement"
effect_template: "{VALUE}% fortification bonus to the governed settlement"
alternative_perk_string_id: "TacticsCallToArms"
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

# On The March - governor - settlement defense

20% fortification bonus to the governed settlement
