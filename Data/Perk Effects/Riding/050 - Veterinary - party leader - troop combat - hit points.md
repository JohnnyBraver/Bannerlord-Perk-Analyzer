---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 50
perk: "Veterinary"
perk_string_id: "RidingVeterinary"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "hit points"
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% hit points to mounts of troops in your party."
effect_template: "{VALUE}% hit points to mounts of troops in your party."
alternative_perk_string_id: "RidingWellStraped"
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

# Veterinary - party leader - troop combat

10% hit points to mounts of troops in your party.
