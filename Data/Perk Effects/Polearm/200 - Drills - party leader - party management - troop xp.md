---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 200
perk: "Drills"
perk_string_id: "PolearmDrills"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "0.1 bonus daily experience to troops in your party."
effect_template: "{VALUE} bonus daily experience to troops in your party."
alternative_perk_string_id: "PolearmHardyFrontline"
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

# Drills - party leader - party management

0.1 bonus daily experience to troops in your party.
