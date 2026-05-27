---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 225
perk: "Besieged"
perk_string_id: "TacticsBesieged"
effect_slot: "secondary"
role: "personal"
role_value: 12
perk_type: "army management"
perk_subtype: "influence"
trigger_condition:
  - "during siege"
  - "after battle"
effect_tags: []
bonus: 0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "50% influence gain from winning sieges."
effect_template: "{VALUE}% influence gain from winning sieges."
alternative_perk_string_id: "TacticsPreBattleManeuvers"
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

# Besieged - personal - army management

50% influence gain from winning sieges.
