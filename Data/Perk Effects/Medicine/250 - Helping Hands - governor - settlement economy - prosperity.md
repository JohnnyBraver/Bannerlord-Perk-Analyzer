---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 250
perk: "Helping Hands"
perk_string_id: "MedicineHelpingHands"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement economy"
perk_subtype: "prosperity"
trigger_condition: []
effect_tags:
  - "food"
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% prosperity loss from starvation."
effect_template: "{VALUE}% prosperity loss from starvation."
alternative_perk_string_id: "MedicineBattleHardened"
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

# Helping Hands - governor - settlement economy

-50% prosperity loss from starvation.
