---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 25
perk: "Scaffolds"
perk_string_id: "EngineeringScaffolds"
effect_slot: "primary"
role: "engineer"
role_value: 8
perk_type: "siege"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
effect_tags:
  - "build speed"
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% build speed to non-ranged siege engines."
effect_template: "{VALUE}% build speed to non-ranged siege engines."
alternative_perk_string_id: "EngineeringTorsionEngines"
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

# Scaffolds - engineer - siege

10% build speed to non-ranged siege engines.
