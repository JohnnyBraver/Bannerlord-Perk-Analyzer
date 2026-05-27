---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 250
perk: "Vanguard"
perk_string_id: "ScoutingVanguard"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "damage increase"
perk_subtype: ""
trigger_condition:
  - "simulation"
  - "attacking"
effect_tags: []
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "5% damage by your troops when they are sent as attackers."
effect_template: "{VALUE}% damage by your troops when they are sent as attackers."
alternative_perk_string_id: "ScoutingRearguard"
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

# Vanguard - party leader - damage increase

5% damage by your troops when they are sent as attackers.
