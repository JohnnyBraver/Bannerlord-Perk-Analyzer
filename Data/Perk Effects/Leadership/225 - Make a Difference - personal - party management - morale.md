---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 225
perk: "Make a Difference"
perk_string_id: "LeadershipMakeADifference"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "party management"
perk_subtype: "morale"
trigger_condition:
  - "on kill"
effect_tags: []
bonus: 1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "100% battle morale to troops when you kill an enemy in battle."
effect_template: "{VALUE}% battle morale to troops when you kill an enemy in battle."
alternative_perk_string_id: "LeadershipGreatLeader"
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

# Make a Difference - personal - party management

100% battle morale to troops when you kill an enemy in battle.
