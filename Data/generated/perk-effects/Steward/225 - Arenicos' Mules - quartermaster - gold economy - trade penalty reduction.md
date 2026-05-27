---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 225
perk: "Arenicos' Mules"
perk_string_id: "StewardArenicosMules"
effect_slot: "secondary"
role: "quartermaster"
role_value: 10
perk_type: "gold economy"
perk_subtype: "trade penalty reduction"
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
  - "trade"
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% trade penalty for trading pack animals."
effect_template: "{VALUE}% trade penalty for trading pack animals."
alternative_perk_string_id: "StewardArenicosHorses"
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

# Arenicos' Mules - quartermaster - gold economy

-20% trade penalty for trading pack animals.
