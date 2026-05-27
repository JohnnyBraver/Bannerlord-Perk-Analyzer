---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 275
perk: "Tactical Mastery"
perk_string_id: "TacticsTacticalMastery"
effect_slot: "primary"
role: "army leader"
role_value: 4
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "simulation"
  - "over skill cap"
effect_tags: []
bonus: 0.005
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "0.5% damage for every skill point above 200 tactics skill when troops are sent to confront the enemy."
effect_template: "{VALUE}% damage for every skill point above 200 tactics skill when troops are sent to confront the enemy."
alternative_perk_string_id: ""
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

# Tactical Mastery - army leader - troop combat

0.5% damage for every skill point above 200 tactics skill when troops are sent to confront the enemy.
