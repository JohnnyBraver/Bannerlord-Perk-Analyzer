---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 50
perk: "Siegeworks"
perk_string_id: "EngineeringSiegeWorks"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "siege"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
  - "governed settlement"
effect_tags: []
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 prebuilt catapult to the settlement when a siege starts in the governed settlement."
effect_template: "{VALUE} prebuilt catapult to the settlement when a siege starts in the governed settlement."
alternative_perk_string_id: "EngineeringDungeonArchitect"
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

# Siegeworks - governor - siege

1 prebuilt catapult to the settlement when a siege starts in the governed settlement.
