---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 125
perk: "Salvager"
perk_string_id: "EngineeringSalvager"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "build speed"
trigger_condition:
  - "during siege"
effect_tags:
  - "defense"
  - "militia"
bonus: 0.001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "0.1% siege engine build speed increase for each militia."
effect_template: "{VALUE}% siege engine build speed increase for each militia."
alternative_perk_string_id: "EngineeringForeman"
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

# Salvager - governor - settlement defense

0.1% siege engine build speed increase for each militia.
