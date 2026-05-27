---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "One Handed"
level: 175
perk: "Lead by example"
perk_string_id: "OneHandedLeadByExample"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "morale"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 5
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "5 starting battle morale to troops in your party."
effect_template: "{VALUE} starting battle morale to troops in your party."
alternative_perk_string_id: "OneHandedStandUnited"
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

# Lead by example - party leader - party management

5 starting battle morale to troops in your party.
