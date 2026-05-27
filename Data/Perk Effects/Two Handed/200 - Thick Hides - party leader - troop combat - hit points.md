---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Two Handed"
level: 200
perk: "Thick Hides"
perk_string_id: "TwoHandedThickHides"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "hit points"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 5
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "5 hit points to troops in your party."
effect_template: "{VALUE} hit points to troops in your party."
alternative_perk_string_id: "TwoHandedRecklessCharge"
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

# Thick Hides - party leader - troop combat

5 hit points to troops in your party.
