---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 225
perk: "Fortitude Tonic"
perk_string_id: "MedicineFortitudeTonic"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "personal combat"
perk_subtype: "hit points"
trigger_condition: []
effect_tags: []
bonus: 10
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "10 hit points to other heroes in your party."
effect_template: "{VALUE} hit points to other heroes in your party."
alternative_perk_string_id: "MedicineCheatDeath"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Applies to other heroes in the party, not troops or the main-hero personal effect."
classification_review: ""
---

# Fortitude Tonic - party leader - personal combat

10 hit points to other heroes in your party.
