---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 225
perk: "Mounted Patrols"
perk_string_id: "RidingMountedPatrols"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "prisoners"
trigger_condition:
  - "party composition"
effect_tags:
  - "prisoner escape"
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% escape chance to prisoners in your party."
effect_template: "{VALUE}% escape chance to prisoners in your party."
alternative_perk_string_id: "RidingCavalryTactics"
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

# Mounted Patrols - party leader - party management

-50% escape chance to prisoners in your party.
