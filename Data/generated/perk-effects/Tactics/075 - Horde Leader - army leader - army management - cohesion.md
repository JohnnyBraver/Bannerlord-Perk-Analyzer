---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 75
perk: "Horde Leader"
perk_string_id: "TacticsHordeLeader"
effect_slot: "secondary"
role: "army leader"
role_value: 4
perk_type: "army management"
perk_subtype: "cohesion"
trigger_condition: []
effect_tags: []
bonus: -0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-5% army cohesion loss to commanded armies."
effect_template: "{VALUE}% army cohesion loss to commanded armies."
alternative_perk_string_id: "TacticsSmallUnitTactics"
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

# Horde Leader - army leader - army management

-5% army cohesion loss to commanded armies.
