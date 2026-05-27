---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 100
perk: "Forced March"
perk_string_id: "ScoutingForcedMarch"
effect_slot: "primary"
role: "scout"
role_value: 9
perk_type: "party management"
perk_subtype: "party speed"
trigger_condition:
  - "while traveling"
  - "morale threshold"
effect_tags: []
bonus: 0.025
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "2.5% travel speed when the party morale is higher than 75."
effect_template: "{VALUE}% travel speed when the party morale is higher than 75."
alternative_perk_string_id: "ScoutingUnburdened"
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

# Forced March - scout - party management

2.5% travel speed when the party morale is higher than 75.
