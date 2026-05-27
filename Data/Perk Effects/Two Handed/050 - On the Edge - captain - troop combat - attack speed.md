---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Two Handed"
level: 50
perk: "On the Edge"
perk_string_id: "TwoHandedOnTheEdge"
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
troop_usage: "infantry, cavalry"
troop_usage_value: 5
effect: "2% swing speed to infantry in your formation."
effect_template: "{VALUE}% swing speed to infantry in your formation."
alternative_perk_string_id: "TwoHandedHeadBasher"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage includes cavalry, but description says swing speed to infantry in your formation."
classification_review: ""
---

# On the Edge - captain - troop combat

2% swing speed to infantry in your formation.
