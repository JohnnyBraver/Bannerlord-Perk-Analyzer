---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 250
perk: "Battle Hardened"
perk_string_id: "MedicineBattleHardened"
effect_slot: "primary"
role: "surgeon"
role_value: 7
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "after battle"
effect_tags: []
bonus: 25
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "25 experience to wounded units at the end of the battle."
effect_template: "{VALUE} experience to wounded units at the end of the battle."
alternative_perk_string_id: "MedicineHelpingHands"
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

# Battle Hardened - surgeon - party management

25 experience to wounded units at the end of the battle.
