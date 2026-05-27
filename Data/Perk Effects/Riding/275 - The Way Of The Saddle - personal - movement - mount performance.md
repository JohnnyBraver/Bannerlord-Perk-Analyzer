---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 275
perk: "The Way Of The Saddle"
perk_string_id: "RidingTheWayOfTheSaddle"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "movement"
perk_subtype: "mount performance"
trigger_condition:
  - "over skill cap"
effect_tags: []
bonus: 0.30000001
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "0.3 charge damage and maneuvering for every skill point above 250."
effect_template: "{VALUE} charge damage and maneuvering for every skill point above 250."
alternative_perk_string_id: ""
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Composite effect spans multiple classification categories."
---

# The Way Of The Saddle - personal - movement

0.3 charge damage and maneuvering for every skill point above 250.
