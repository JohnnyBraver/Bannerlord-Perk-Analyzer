---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 125
perk: "Tracker"
perk_string_id: "ScoutingTracker"
effect_slot: "secondary"
role: "scout"
role_value: 9
perk_type: "party management"
perk_subtype: "party speed"
trigger_condition:
  - "while traveling"
effect_tags: []
bonus: 0.02
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "2% travel speed while following a hostile party."
effect_template: "{VALUE}% travel speed while following a hostile party."
alternative_perk_string_id: "ScoutingRanger"
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

# Tracker - scout - party management

2% travel speed while following a hostile party.
