---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 200
perk: "Strong"
perk_string_id: "AthleticsStrong"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "party speed"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "5% party speed by foot troops in your party."
effect_template: "{VALUE}% party speed by foot troops in your party."
alternative_perk_string_id: "AthleticsSteady"
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

# Strong - party leader - party management

5% party speed by foot troops in your party.
