---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Medicine"
level: 275
perk: "Minister of Health"
perk_string_id: "MedicineMinisterOfHealth"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "troop combat"
perk_subtype: "hit points"
trigger_condition:
  - "over skill cap"
effect_tags: []
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 hit point to troops for every skill point above 250."
effect_template: "{VALUE} hit point to troops for every skill point above 250."
alternative_perk_string_id: ""
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Role is personal, but effect text targets troops; classified by effect target."
classification_review: ""
---

# Minister of Health - personal - troop combat

1 hit point to troops for every skill point above 250.
