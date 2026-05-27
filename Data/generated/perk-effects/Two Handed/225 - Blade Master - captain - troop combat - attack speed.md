---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Two Handed"
level: 225
perk: "Blade Master"
perk_string_id: "TwoHandedBladeMaster"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "attack speed"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.02
increment_type: "add_factor"
increment_value: 1
troop_usage: "infantry"
troop_usage_value: 1
effect: "2% attack speed to infantry in your formation."
effect_template: "{VALUE}% attack speed to infantry in your formation."
alternative_perk_string_id: "TwoHandedVandal"
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

# Blade Master - captain - troop combat

2% attack speed to infantry in your formation.
