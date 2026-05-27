---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 150
perk: "A Good Days Rest"
perk_string_id: "AthleticsAGoodDaysRest"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "while waiting"
  - "party composition"
effect_tags: []
bonus: 10
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "10 daily experience to foot troops while waiting in settlements."
effect_template: "{VALUE} daily experience to foot troops while waiting in settlements."
alternative_perk_string_id: "AthleticsWalkItOff"
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

# A Good Days Rest - party leader - party management

10 daily experience to foot troops while waiting in settlements.
