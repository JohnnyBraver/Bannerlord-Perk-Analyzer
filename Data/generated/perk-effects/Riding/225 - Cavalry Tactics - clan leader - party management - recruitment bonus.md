---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 225
perk: "Cavalry Tactics"
perk_string_id: "RidingCavalryTactics"
effect_slot: "primary"
role: "clan leader"
role_value: 2
perk_type: "party management"
perk_subtype: "recruitment bonus"
trigger_condition:
  - "party composition"
  - "governed settlement"
effect_tags:
  - "mounts"
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% volunteering rate of cavalry troops in the settlements governed by your clan."
effect_template: "{VALUE}% volunteering rate of cavalry troops in the settlements governed by your clan."
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

# Cavalry Tactics - clan leader - party management

30% volunteering rate of cavalry troops in the settlements governed by your clan.
