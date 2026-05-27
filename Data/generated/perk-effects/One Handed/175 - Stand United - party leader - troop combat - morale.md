---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "One Handed"
level: 175
perk: "Stand United"
perk_string_id: "OneHandedStandUnited"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "morale"
trigger_condition: []
effect_tags: []
bonus: 8
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "8 starting battle morale to troops in your party if you are outnumbered."
effect_template: "{VALUE} starting battle morale to troops in your party if you are outnumbered."
alternative_perk_string_id: "OneHandedLeadByExample"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Outnumbered condition is not represented by current trigger_condition taxonomy."
---

# Stand United - party leader - troop combat

8 starting battle morale to troops in your party if you are outnumbered.
