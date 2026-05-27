---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 225
perk: "Vantage Point"
perk_string_id: "ScoutingVantagePoint"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "prisoners"
trigger_condition: []
effect_tags:
  - "prisoner limit"
bonus: 10
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "10 prisoner limit."
effect_template: "{VALUE} prisoner limit."
alternative_perk_string_id: "ScoutingKeenSight"
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

# Vantage Point - party leader - party management

10 prisoner limit.
