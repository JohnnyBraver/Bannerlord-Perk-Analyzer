---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 75
perk: "Nomadic Traditions"
perk_string_id: "RidingNomadicTraditions"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "speed bonus"
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "ranged, cavalry"
troop_usage_value: 6
effect: "10% melee damage bonus from speed to mounted troops in your formation."
effect_template: "{VALUE}% melee damage bonus from speed to mounted troops in your formation."
alternative_perk_string_id: "RidingDeeperSacks"
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

# Nomadic Traditions - captain - troop combat

10% melee damage bonus from speed to mounted troops in your formation.
