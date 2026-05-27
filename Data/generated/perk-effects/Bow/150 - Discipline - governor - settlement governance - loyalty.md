---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 150
perk: "Discipline"
perk_string_id: "BowDiscipline"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement governance"
perk_subtype: "loyalty"
trigger_condition:
  - "governed settlement"
effect_tags: []
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 loyalty per day in the governed settlement."
effect_template: "{VALUE} loyalty per day in the governed settlement."
alternative_perk_string_id: "BowHunterClan"
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

# Discipline - governor - settlement governance

1 loyalty per day in the governed settlement.
