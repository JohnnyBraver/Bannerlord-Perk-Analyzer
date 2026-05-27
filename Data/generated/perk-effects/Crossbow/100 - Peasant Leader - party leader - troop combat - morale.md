---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 100
perk: "Peasant Leader"
perk_string_id: "CrossbowPeasantLeader"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "morale"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% battle morale to tier 1 to 3 troops"
effect_template: "{VALUE}% battle morale to tier 1 to 3 troops"
alternative_perk_string_id: "CrossbowRenownMarksmen"
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

# Peasant Leader - party leader - troop combat

10% battle morale to tier 1 to 3 troops
