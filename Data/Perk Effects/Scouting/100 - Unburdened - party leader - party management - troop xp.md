---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 100
perk: "Unburdened"
perk_string_id: "ScoutingUnburdened"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "while traveling"
effect_tags:
  - "overburden"
bonus: 2
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "2 experience per day to all troops when traveling while overburdened."
effect_template: "{VALUE} experience per day to all troops when traveling while overburdened."
alternative_perk_string_id: "ScoutingForcedMarch"
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

# Unburdened - party leader - party management

2 experience per day to all troops when traveling while overburdened.
