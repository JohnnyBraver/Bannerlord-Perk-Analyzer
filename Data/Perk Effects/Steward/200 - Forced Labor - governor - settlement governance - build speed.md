---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 200
perk: "Forced Labor"
perk_string_id: "StewardForcedLabor"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement governance"
perk_subtype: "build speed"
trigger_condition:
  - "project active"
  - "governed settlement"
effect_tags:
  - "prisoners"
bonus: 0.01
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "1% construction speed per every 3 prisoners."
effect_template: "{VALUE}% construction speed per every 3 prisoners."
alternative_perk_string_id: "StewardContractors"
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

# Forced Labor - governor - settlement governance

1% construction speed per every 3 prisoners.
