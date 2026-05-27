---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 100
perk: "Unburdened"
perk_string_id: "ScoutingUnburdened"
effect_slot: "primary"
role: "scout"
role_value: 9
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
effect: "-20% overburden penalty."
effect_template: "{VALUE}% overburden penalty."
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

# Unburdened - scout - party management

-20% overburden penalty.
