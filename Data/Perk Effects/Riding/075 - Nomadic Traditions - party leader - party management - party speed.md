---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 75
perk: "Nomadic Traditions"
perk_string_id: "RidingNomadicTraditions"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "party speed"
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% party speed bonus from footmen on horses."
effect_template: "{VALUE}% party speed bonus from footmen on horses."
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

# Nomadic Traditions - party leader - party management

30% party speed bonus from footmen on horses.
