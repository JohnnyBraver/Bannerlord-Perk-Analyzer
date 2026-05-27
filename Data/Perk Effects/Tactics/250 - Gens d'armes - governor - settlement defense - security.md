---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 250
perk: "Gens d'armes"
perk_string_id: "TacticsGensdarmes"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "security"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 daily security in the governed settlement."
effect_template: "{VALUE} daily security in the governed settlement."
alternative_perk_string_id: "TacticsCounteroffensive"
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

# Gens d'armes - governor - settlement defense

1 daily security in the governed settlement.
