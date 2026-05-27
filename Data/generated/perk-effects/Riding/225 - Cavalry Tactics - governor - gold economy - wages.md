---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 225
perk: "Cavalry Tactics"
perk_string_id: "RidingCavalryTactics"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "gold economy"
perk_subtype: "wages"
trigger_condition:
  - "party composition"
  - "governed settlement"
effect_tags:
  - "mounts"
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% wages of mounted troops in the governed settlement."
effect_template: "{VALUE}% wages of mounted troops in the governed settlement."
alternative_perk_string_id: "RidingMountedPatrols"
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

# Cavalry Tactics - governor - gold economy

-50% wages of mounted troops in the governed settlement.
