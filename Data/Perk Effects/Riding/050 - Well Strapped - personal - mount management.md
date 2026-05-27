---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 50
perk: "Well Strapped"
perk_string_id: "RidingWellStraped"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "mount management"
perk_subtype: ""
trigger_condition: []
effect_tags:
  - "mounts"
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% chance of your mount dying or becoming lame after it falls in battle."
effect_template: "{VALUE}% chance of your mount dying or becoming lame after it falls in battle."
alternative_perk_string_id: "RidingVeterinary"
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

# Well Strapped - personal - mount management

-50% chance of your mount dying or becoming lame after it falls in battle.
