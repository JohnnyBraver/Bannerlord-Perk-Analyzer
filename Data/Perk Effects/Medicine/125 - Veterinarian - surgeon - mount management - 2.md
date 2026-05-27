---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 125
perk: "Veterinarian"
perk_string_id: "MedicineVeterinarian"
effect_slot: "secondary"
role: "surgeon"
role_value: 7
perk_type: "mount management"
perk_subtype: ""
trigger_condition:
  - "party composition"
  - "after battle"
effect_tags:
  - "mounts"
bonus: 0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "50% chance to recover mounts of dead cavalry troops in battles."
effect_template: "{VALUE}% chance to recover mounts of dead cavalry troops in battles."
alternative_perk_string_id: "MedicineSiegeMedic"
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

# Veterinarian - surgeon - mount management

50% chance to recover mounts of dead cavalry troops in battles.
