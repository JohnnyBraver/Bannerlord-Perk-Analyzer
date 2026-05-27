---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 75
perk: "Sweatshops"
perk_string_id: "StewardSweatshops"
effect_slot: "secondary"
role: "quartermaster"
role_value: 10
perk_type: "siege"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
effect_tags:
  - "build speed"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% siege engine build rate in your party."
effect_template: "{VALUE}% siege engine build rate in your party."
alternative_perk_string_id: "StewardStiffUpperLip"
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

# Sweatshops - quartermaster - siege

20% siege engine build rate in your party.
