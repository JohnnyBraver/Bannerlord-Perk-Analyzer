---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 50
perk: "Dungeon Architect"
perk_string_id: "EngineeringDungeonArchitect"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "party management"
perk_subtype: "prisoners"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "prisoner escape"
bonus: -0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-25% escape chance to prisoners in dungeons of governed settlements."
effect_template: "{VALUE}% escape chance to prisoners in dungeons of governed settlements."
alternative_perk_string_id: "EngineeringSiegeWorks"
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

# Dungeon Architect - governor - party management

-25% escape chance to prisoners in dungeons of governed settlements.
