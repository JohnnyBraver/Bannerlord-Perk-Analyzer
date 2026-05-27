---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 50
perk: "Water Diviner"
perk_string_id: "ScoutingWaterDiviner"
effect_slot: "primary"
role: "scout"
role_value: 9
perk_type: "party vision"
perk_subtype: ""
trigger_condition:
  - "while traveling"
  - "terrain"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% sight range while traveling on steppes and plains."
effect_template: "{VALUE}% sight range while traveling on steppes and plains."
alternative_perk_string_id: "ScoutingPathfinder"
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

# Water Diviner - scout - party vision

10% sight range while traveling on steppes and plains.
