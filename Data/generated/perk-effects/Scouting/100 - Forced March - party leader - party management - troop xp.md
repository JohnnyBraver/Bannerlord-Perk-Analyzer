---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 100
perk: "Forced March"
perk_string_id: "ScoutingForcedMarch"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "while traveling"
  - "morale threshold"
effect_tags: []
bonus: 2
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "2 experience per day to all troops while traveling with party morale higher than 75."
effect_template: "{VALUE} experience per day to all troops while traveling with party morale higher than 75."
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

# Forced March - party leader - party management

2 experience per day to all troops while traveling with party morale higher than 75.
