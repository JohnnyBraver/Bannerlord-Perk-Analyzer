---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 150
perk: "Patrols"
perk_string_id: "ScoutingPatrols"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "simulation bonus"
perk_subtype: ""
trigger_condition:
  - "simulation"
effect_tags:
  - "bandits"
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% advantage against bandits when troops are sent to confront the enemy."
effect_template: "{VALUE}% advantage against bandits when troops are sent to confront the enemy."
alternative_perk_string_id: "ScoutingMountedScouts"
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

# Patrols - party leader - simulation bonus

10% advantage against bandits when troops are sent to confront the enemy.
