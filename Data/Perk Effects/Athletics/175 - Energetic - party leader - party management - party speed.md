---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 175
perk: "Energetic"
perk_string_id: "AthleticsEnergetic"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "party speed"
trigger_condition: []
effect_tags:
  - "overburden"
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% overburdened speed penalty."
effect_template: "{VALUE}% overburdened speed penalty."
alternative_perk_string_id: "AthleticsDurable"
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

# Energetic - party leader - party management

-20% overburdened speed penalty.
