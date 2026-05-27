---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 125
perk: "Improviser"
perk_string_id: "TacticsImproviser"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "battle escape"
perk_subtype: ""
trigger_condition:
  - "during siege"
effect_tags: []
bonus: -0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-25% loss of troops when breaking into or out of a settlement under siege."
effect_template: "{VALUE}% loss of troops when breaking into or out of a settlement under siege."
alternative_perk_string_id: "TacticsSwiftRegroup"
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

# Improviser - party leader - battle escape

-25% loss of troops when breaking into or out of a settlement under siege.
