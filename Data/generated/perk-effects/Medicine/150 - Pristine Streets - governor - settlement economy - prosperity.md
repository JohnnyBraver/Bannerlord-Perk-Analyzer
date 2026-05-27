---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 150
perk: "Pristine Streets"
perk_string_id: "MedicinePristineStreets"
effect_slot: "primary"
role: "governor"
role_value: 3
perk_type: "settlement economy"
perk_subtype: "prosperity"
trigger_condition:
  - "governed settlement"
effect_tags: []
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 settlement prosperity every day in governed settlements."
effect_template: "{VALUE} settlement prosperity every day in governed settlements."
alternative_perk_string_id: "MedicineBushDoctor"
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

# Pristine Streets - governor - settlement economy

1 settlement prosperity every day in governed settlements.
