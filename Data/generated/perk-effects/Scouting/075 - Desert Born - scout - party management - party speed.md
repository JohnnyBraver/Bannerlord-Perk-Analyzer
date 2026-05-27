---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 75
perk: "Desert Born"
perk_string_id: "ScoutingDesertBorn"
effect_slot: "primary"
role: "scout"
role_value: 9
perk_type: "party management"
perk_subtype: "party speed"
trigger_condition:
  - "while traveling"
  - "terrain"
effect_tags: []
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "5% travel speed on deserts and dunes."
effect_template: "{VALUE}% travel speed on deserts and dunes."
alternative_perk_string_id: "ScoutingForestKin"
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

# Desert Born - scout - party management

5% travel speed on deserts and dunes.
