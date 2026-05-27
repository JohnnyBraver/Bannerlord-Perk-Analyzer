---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 125
perk: "Leader of the Masses"
perk_string_id: "LeadershipLeaderOfMasses"
effect_slot: "primary"
role: "clan leader"
role_value: 2
perk_type: "party management"
perk_subtype: "party size"
trigger_condition: []
effect_tags: []
bonus: 5
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "5 party size for each town you control."
effect_template: "{VALUE} party size for each town you control."
alternative_perk_string_id: "LeadershipPresence"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Scales with controlled towns; no dedicated controlled-settlement trigger condition exists."
classification_review: ""
---

# Leader of the Masses - clan leader - party management

5 party size for each town you control.
