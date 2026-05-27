---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 225
perk: "Arenicos' Horses"
perk_string_id: "StewardArenicosHorses"
effect_slot: "secondary"
role: "personal"
role_value: 12
perk_type: "gold economy"
perk_subtype: "trade penalty reduction"
trigger_condition: []
effect_tags:
  - "mounts"
  - "trade"
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% trade penalty for trading mounts."
effect_template: "{VALUE}% trade penalty for trading mounts."
alternative_perk_string_id: "StewardArenicosMules"
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

# Arenicos' Horses - personal - gold economy

-20% trade penalty for trading mounts.
