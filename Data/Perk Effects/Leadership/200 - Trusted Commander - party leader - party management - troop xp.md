---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 200
perk: "Trusted Commander"
perk_string_id: "LeadershipTrustedCommander"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "simulation"
effect_tags: []
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% experience for troops, when they are sent to confront the enemy."
effect_template: "{VALUE}% experience for troops, when they are sent to confront the enemy."
alternative_perk_string_id: "LeadershipLeadByExample"
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

# Trusted Commander - party leader - party management

20% experience for troops, when they are sent to confront the enemy.
