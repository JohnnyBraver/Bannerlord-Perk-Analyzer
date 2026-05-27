---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 125
perk: "Presence"
perk_string_id: "LeadershipPresence"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "settlement defense"
perk_subtype: "security"
trigger_condition:
  - "while waiting"
effect_tags:
  - "defense"
bonus: 5
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "5 security per day while waiting in a town."
effect_template: "{VALUE} security per day while waiting in a town."
alternative_perk_string_id: "LeadershipLeaderOfMasses"
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

# Presence - personal - settlement defense

5 security per day while waiting in a town.
