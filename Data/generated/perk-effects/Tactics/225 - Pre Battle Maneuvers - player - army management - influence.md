---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 225
perk: "Pre Battle Maneuvers"
perk_string_id: "TacticsPreBattleManeuvers"
effect_slot: "primary"
role: "player"
role_value: 11
perk_type: "army management"
perk_subtype: "influence"
trigger_condition:
  - "after battle"
effect_tags: []
bonus: 0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "25% influence gain from winning battles."
effect_template: "{VALUE}% influence gain from winning battles."
alternative_perk_string_id: "TacticsBesieged"
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

# Pre Battle Maneuvers - player - army management

25% influence gain from winning battles.
