---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 75
perk: "Heroic Leader"
perk_string_id: "LeadershipHeroicLeader"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "morale damage"
trigger_condition:
  - "on kill"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "none"
troop_usage_value: 0
effect: "10% battle morale penalty to enemies when troops in your formation kill an enemy."
effect_template: "{VALUE}% battle morale penalty to enemies when troops in your formation kill an enemy."
alternative_perk_string_id: "LeadershipAuthority"
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

# Heroic Leader - captain - troop combat

10% battle morale penalty to enemies when troops in your formation kill an enemy.
