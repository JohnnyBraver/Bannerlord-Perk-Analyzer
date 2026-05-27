---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 200
perk: "Physician of People"
perk_string_id: "MedicinePhysicianOfPeople"
effect_slot: "secondary"
role: "surgeon"
role_value: 7
perk_type: "death avoidance"
perk_subtype: ""
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% chance to recover from lethal wounds for tier 1 and 2 troops"
effect_template: "{VALUE}% chance to recover from lethal wounds for tier 1 and 2 troops"
alternative_perk_string_id: "MedicineCleanInfrastructure"
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

# Physician of People - surgeon - death avoidance

30% chance to recover from lethal wounds for tier 1 and 2 troops
