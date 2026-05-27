---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 150
perk: "Horse Archer"
perk_string_id: "RidingHorseArcher"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "ranged"
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "ranged, mounted"
troop_usage_value: 258
effect: "5% damage by mounted archers in your formation."
effect_template: "{VALUE}% damage by mounted archers in your formation."
alternative_perk_string_id: "RidingMountedWarrior"
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

# Horse Archer - captain - troop combat

5% damage by mounted archers in your formation.
