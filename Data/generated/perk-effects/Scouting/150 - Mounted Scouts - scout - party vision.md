---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 150
perk: "Mounted Scouts"
perk_string_id: "ScoutingMountedScouts"
effect_slot: "primary"
role: "scout"
role_value: 9
perk_type: "party vision"
perk_subtype: ""
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% sight range when your party is composed of more than %50 cavalry troops."
effect_template: "{VALUE}% sight range when your party is composed of more than %50 cavalry troops."
alternative_perk_string_id: "ScoutingPatrols"
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

# Mounted Scouts - scout - party vision

10% sight range when your party is composed of more than %50 cavalry troops.
