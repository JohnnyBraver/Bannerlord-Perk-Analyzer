---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 100
perk: "Mounted Archery"
perk_string_id: "BowMountedArchery"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "security"
trigger_condition:
  - "party composition"
  - "governed settlement"
effect_tags:
  - "defense"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% security provided by archers in the governed settlement."
effect_template: "{VALUE}% security provided by archers in the governed settlement."
alternative_perk_string_id: "BowMerryMen"
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

# Mounted Archery - governor - settlement defense

20% security provided by archers in the governed settlement.
