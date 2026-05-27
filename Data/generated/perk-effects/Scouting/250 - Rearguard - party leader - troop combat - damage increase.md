---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 250
perk: "Rearguard"
perk_string_id: "ScoutingRearguard"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "during siege"
  - "defending"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% damage by your troops when defending at your siege camp."
effect_template: "{VALUE}% damage by your troops when defending at your siege camp."
alternative_perk_string_id: "ScoutingVanguard"
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

# Rearguard - party leader - troop combat

10% damage by your troops when defending at your siege camp.
