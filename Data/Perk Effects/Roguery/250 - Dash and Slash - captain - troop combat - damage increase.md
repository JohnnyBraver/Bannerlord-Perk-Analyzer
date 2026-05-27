---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 250
perk: "Dash and Slash"
perk_string_id: "RogueryDashAndSlash"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
bonus: 0.02
increment_type: "add_factor"
increment_value: 1
troop_usage: "formation"
troop_usage_value: 64
effect: "2% two handed weapon damage by troops in your formation."
effect_template: "{VALUE}% two handed weapon damage by troops in your formation."
alternative_perk_string_id: "RogueryFleetFooted"
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

# Dash and Slash - captain - troop combat

2% two handed weapon damage by troops in your formation.
