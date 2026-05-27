---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 200
perk: "Carver"
perk_string_id: "RogueryCarver"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.02
increment_type: "add_factor"
increment_value: 1
troop_usage: "heroes"
troop_usage_value: 16
effect: "2% one handed damage by troops under your formation."
effect_template: "{VALUE}% one handed damage by troops under your formation."
alternative_perk_string_id: "RogueryRansomBroker"
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

# Carver - captain - troop combat

2% one handed damage by troops under your formation.
