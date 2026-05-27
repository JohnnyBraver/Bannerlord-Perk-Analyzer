---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 75
perk: "Sledges"
perk_string_id: "MedicineSledges"
effect_slot: "primary"
role: "surgeon"
role_value: 7
perk_type: "party management"
perk_subtype: "party speed"
trigger_condition: []
effect_tags: []
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% party speed penalty from the wounded."
effect_template: "{VALUE}% party speed penalty from the wounded."
alternative_perk_string_id: "MedicineDoctorsOath"
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

# Sledges - surgeon - party management

-50% party speed penalty from the wounded.
