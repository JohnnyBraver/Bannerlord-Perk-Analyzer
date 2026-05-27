---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Two Handed"
level: 225
perk: "Vandal"
perk_string_id: "TwoHandedVandal"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition: []
effect_tags: []
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "infantry"
troop_usage_value: 1
effect: "20% damage against destructible objects by troops in your formation."
effect_template: "{VALUE}% damage against destructible objects by troops in your formation."
alternative_perk_string_id: "TwoHandedBladeMaster"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is infantry, but description only says troops in your formation."
classification_review: ""
---

# Vandal - captain - troop combat

20% damage against destructible objects by troops in your formation.
