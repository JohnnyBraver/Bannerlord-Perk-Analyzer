---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 250
perk: "Dauntless Steed"
perk_string_id: "RidingDauntlessSteed"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "armor increase"
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
bonus: 5
increment_type: "add"
increment_value: 0
troop_usage: "ranged"
troop_usage_value: 2
effect: "5 armor to all equipped armor pieces of mounted troops in your formation."
effect_template: "{VALUE} armor to all equipped armor pieces of mounted troops in your formation."
alternative_perk_string_id: "RidingToughSteed"
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

# Dauntless Steed - captain - troop combat

5 armor to all equipped armor pieces of mounted troops in your formation.
