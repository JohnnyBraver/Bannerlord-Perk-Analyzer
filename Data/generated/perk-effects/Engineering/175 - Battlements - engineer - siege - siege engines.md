---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 175
perk: "Battlements"
perk_string_id: "EngineeringBattlements"
effect_slot: "primary"
role: "engineer"
role_value: 8
perk_type: "siege"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
effect_tags: []
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 prebuilt ballista when you set up a siege camp."
effect_template: "{VALUE} prebuilt ballista when you set up a siege camp."
alternative_perk_string_id: "EngineeringCampBuilding"
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

# Battlements - engineer - siege

1 prebuilt ballista when you set up a siege camp.
