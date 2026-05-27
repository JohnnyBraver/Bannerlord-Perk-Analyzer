---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 50
perk: "Walk It Off"
perk_string_id: "MedicineWalkItOff"
effect_slot: "secondary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "hit points"
trigger_condition:
  - "after battle"
  - "attacking"
effect_tags: []
bonus: 10
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "10 hit points recovery after each offensive battle."
effect_template: "{VALUE} hit points recovery after each offensive battle."
alternative_perk_string_id: "MedicineTriageTent"
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

# Walk It Off - personal - personal combat

10 hit points recovery after each offensive battle.
