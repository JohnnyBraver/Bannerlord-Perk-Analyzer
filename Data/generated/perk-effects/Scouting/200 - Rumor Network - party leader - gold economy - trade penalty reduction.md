---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 200
perk: "Rumor Network"
perk_string_id: "ScoutingRumourNetwork"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "trade penalty reduction"
trigger_condition:
  - "own kingdom"
effect_tags:
  - "trade"
bonus: -0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-5% trade penalty within cities of your own kingdom."
effect_template: "{VALUE}% trade penalty within cities of your own kingdom."
alternative_perk_string_id: "ScoutingVillageNetwork"
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

# Rumor Network - party leader - gold economy

-5% trade penalty within cities of your own kingdom.
