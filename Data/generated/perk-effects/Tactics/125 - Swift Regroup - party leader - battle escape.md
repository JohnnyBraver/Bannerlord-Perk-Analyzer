---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 125
perk: "Swift Regroup"
perk_string_id: "TacticsSwiftRegroup"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "battle escape"
perk_subtype: ""
trigger_condition:
  - "after battle"
effect_tags: []
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% troops left behind when escaping from battles."
effect_template: "{VALUE}% troops left behind when escaping from battles."
alternative_perk_string_id: "TacticsImproviser"
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

# Swift Regroup - party leader - battle escape

-50% troops left behind when escaping from battles.
