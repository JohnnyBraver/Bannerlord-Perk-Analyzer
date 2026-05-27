---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 225
perk: "Great Leader"
perk_string_id: "LeadershipGreatLeader"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "morale"
trigger_condition:
  - "same culture"
effect_tags: []
bonus: 5
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "5 battle morale to troops that are of same culture as you."
effect_template: "{VALUE} battle morale to troops that are of same culture as you."
alternative_perk_string_id: "LeadershipMakeADifference"
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

# Great Leader - party leader - troop combat

5 battle morale to troops that are of same culture as you.
