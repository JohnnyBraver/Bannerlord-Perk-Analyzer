---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 25
perk: "Preventive Medicine"
perk_string_id: "MedicinePreventiveMedicine"
effect_slot: "secondary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "hit points"
trigger_condition:
  - "after battle"
effect_tags: []
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% recovery of lost hit points after each battle."
effect_template: "{VALUE}% recovery of lost hit points after each battle."
alternative_perk_string_id: "MedicineSelfMedication"
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

# Preventive Medicine - personal - personal combat

30% recovery of lost hit points after each battle.
