---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 50
perk: "Seven Veterans"
perk_string_id: "StewardSevenVeterans"
effect_slot: "primary"
role: "quartermaster"
role_value: 10
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 4
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "4 daily experience for tier 4+ troops in your party."
effect_template: "{VALUE} daily experience for tier 4+ troops in your party."
alternative_perk_string_id: "StewardDrillSergant"
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

# Seven Veterans - quartermaster - party management

4 daily experience for tier 4+ troops in your party.
