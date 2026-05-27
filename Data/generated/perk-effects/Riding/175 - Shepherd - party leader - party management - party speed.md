---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 175
perk: "Shepherd"
perk_string_id: "RidingShepherd"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "party speed"
trigger_condition: []
effect_tags: []
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% herding speed penalty."
effect_template: "{VALUE}% herding speed penalty."
alternative_perk_string_id: "RidingBreeder"
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

# Shepherd - party leader - party management

-50% herding speed penalty.
