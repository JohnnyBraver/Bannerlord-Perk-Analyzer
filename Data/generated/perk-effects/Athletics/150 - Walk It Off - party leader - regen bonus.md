---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 150
perk: "Walk It Off"
perk_string_id: "AthleticsWalkItOff"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "regen bonus"
perk_subtype: ""
trigger_condition:
  - "while traveling"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% hit point regeneration while traveling."
effect_template: "{VALUE}% hit point regeneration while traveling."
alternative_perk_string_id: "AthleticsAGoodDaysRest"
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

# Walk It Off - party leader - regen bonus

10% hit point regeneration while traveling.
