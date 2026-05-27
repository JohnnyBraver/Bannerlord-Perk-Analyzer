---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 200
perk: "Bulls Eye"
perk_string_id: "BowBullsEye"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "troop xp"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
  - "garrison"
bonus: 3
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "3 daily experience to garrison troops in the governed settlement."
effect_template: "{VALUE} daily experience to garrison troops in the governed settlement."
alternative_perk_string_id: "BowRenownedArcher"
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

# Bulls Eye - governor - settlement defense

3 daily experience to garrison troops in the governed settlement.
