---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 225
perk: "Long Reach"
perk_string_id: "ThrowingLongReach"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "morale"
trigger_condition:
  - "after battle"
effect_tags: []
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% morale and renown gained from battles won."
effect_template: "{VALUE}% morale and renown gained from battles won."
alternative_perk_string_id: "ThrowingPerfectTechnique"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Composite effect spans morale and renown; single classification is partial."
---

# Long Reach - party leader - party management

20% morale and renown gained from battles won.
