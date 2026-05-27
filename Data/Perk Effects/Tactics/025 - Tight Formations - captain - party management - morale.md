---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 25
perk: "Tight Formations"
perk_string_id: "TacticsTightFormations"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "party management"
perk_subtype: "morale"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: -0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "none"
troop_usage_value: 0
effect: "-25% morale penalty when troops in your formation use shield wall, square, skein, column formations."
effect_template: "{VALUE}% morale penalty when troops in your formation use shield wall, square, skein, column formations."
alternative_perk_string_id: "TacticsLooseFormations"
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

# Tight Formations - captain - party management

-25% morale penalty when troops in your formation use shield wall, square, skein, column formations.
