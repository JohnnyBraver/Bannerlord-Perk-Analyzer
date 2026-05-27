---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 225
perk: "Keen Sight"
perk_string_id: "ScoutingKeenSight"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "prisoners"
trigger_condition: []
effect_tags:
  - "hero prisoners"
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% chance of prisoner lords escaping from your party."
effect_template: "{VALUE}% chance of prisoner lords escaping from your party."
alternative_perk_string_id: "ScoutingVantagePoint"
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

# Keen Sight - party leader - party management

-50% chance of prisoner lords escaping from your party.
