---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 100
perk: "Sagittarius"
perk_string_id: "RidingSagittarius"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "ranged accuracy"
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
bonus: -0.15000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "ranged, horse_archer"
troop_usage_value: 10
effect: "-15% accuracy penalty to mounted troops in your formation."
effect_template: "{VALUE}% accuracy penalty to mounted troops in your formation."
alternative_perk_string_id: "RidingSweepingWind"
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

# Sagittarius - captain - troop combat

-15% accuracy penalty to mounted troops in your formation.
