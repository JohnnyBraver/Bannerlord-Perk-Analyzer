---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 125
perk: "Logistician"
perk_string_id: "StewardLogistician"
effect_slot: "primary"
role: "quartermaster"
role_value: 10
perk_type: "party management"
perk_subtype: "morale"
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
bonus: 4
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "4 party morale when number of mounts is greater than number of foot troops in your party."
effect_template: "{VALUE} party morale when number of mounts is greater than number of foot troops in your party."
alternative_perk_string_id: "StewardForeseeableFuture"
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

# Logistician - quartermaster - party management

4 party morale when number of mounts is greater than number of foot troops in your party.
