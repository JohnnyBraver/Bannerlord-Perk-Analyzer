---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 125
perk: "Siege Medic"
perk_string_id: "MedicineSiegeMedic"
effect_slot: "secondary"
role: "surgeon"
role_value: 7
perk_type: "death avoidance"
perk_subtype: ""
trigger_condition:
  - "during siege"
effect_tags: []
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% chance to recover from lethal wounds during siege bombardment."
effect_template: "{VALUE}% chance to recover from lethal wounds during siege bombardment."
alternative_perk_string_id: "MedicineVeterinarian"
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

# Siege Medic - surgeon - death avoidance

30% chance to recover from lethal wounds during siege bombardment.
