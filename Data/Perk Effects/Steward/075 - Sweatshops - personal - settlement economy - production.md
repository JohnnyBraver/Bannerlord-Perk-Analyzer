---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 75
perk: "Sweatshops"
perk_string_id: "StewardSweatshops"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "settlement economy"
perk_subtype: "production"
trigger_condition: []
effect_tags:
  - "workshop"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% production rate to owned workshops."
effect_template: "{VALUE}% production rate to owned workshops."
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

# Sweatshops - personal - settlement economy

20% production rate to owned workshops.
