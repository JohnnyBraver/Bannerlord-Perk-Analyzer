---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 250
perk: "Dash and Slash"
perk_string_id: "RogueryDashAndSlash"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "speed bonus"
trigger_condition:
  - "on foot"
effect_tags: []
bonus: 0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "50% damage bonus from speed while on foot."
effect_template: "{VALUE}% damage bonus from speed while on foot."
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

# Dash and Slash - personal - personal combat

50% damage bonus from speed while on foot.
