---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 175
perk: "Camp Building"
perk_string_id: "EngineeringCampBuilding"
effect_slot: "primary"
role: "army leader"
role_value: 4
perk_type: "army management"
perk_subtype: "cohesion"
trigger_condition:
  - "during siege"
effect_tags: []
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% cohesion loss of armies when besieging."
effect_template: "{VALUE}% cohesion loss of armies when besieging."
alternative_perk_string_id: "EngineeringBattlements"
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

# Camp Building - army leader - army management

-50% cohesion loss of armies when besieging.
