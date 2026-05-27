---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 50
perk: "Triage Tent"
perk_string_id: "MedicineTriageTent"
effect_slot: "primary"
role: "surgeon"
role_value: 7
perk_type: "regen bonus"
perk_subtype: ""
trigger_condition:
  - "while waiting"
effect_tags: []
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% healing rate when stationary on the campaign map."
effect_template: "{VALUE}% healing rate when stationary on the campaign map."
alternative_perk_string_id: "MedicineWalkItOff"
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

# Triage Tent - surgeon - regen bonus

30% healing rate when stationary on the campaign map.
