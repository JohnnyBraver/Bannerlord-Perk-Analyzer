---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 75
perk: "Deeper Sacks"
perk_string_id: "RidingDeeperSacks"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "carrying capacity"
trigger_condition: []
effect_tags:
  - "mounts"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% carrying capacity for pack animals in your party."
effect_template: "{VALUE}% carrying capacity for pack animals in your party."
alternative_perk_string_id: "RidingNomadicTraditions"
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

# Deeper Sacks - party leader - party management

20% carrying capacity for pack animals in your party.
