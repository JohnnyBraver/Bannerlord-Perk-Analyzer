---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 75
perk: "Forest Kin"
perk_string_id: "ScoutingForestKin"
effect_slot: "primary"
role: "scout"
role_value: 9
perk_type: "party management"
perk_subtype: "party speed"
trigger_condition:
  - "while traveling"
  - "terrain"
  - "party composition"
effect_tags: []
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% travel speed penalty from forests if your party is composed of 75% or more infantry units."
effect_template: "{VALUE}% travel speed penalty from forests if your party is composed of 75% or more infantry units."
alternative_perk_string_id: "ScoutingDesertBorn"
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

# Forest Kin - scout - party management

-50% travel speed penalty from forests if your party is composed of 75% or more infantry units.
