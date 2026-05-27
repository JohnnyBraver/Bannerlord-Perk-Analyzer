---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 225
perk: "Hammer Bolts"
perk_string_id: "CrossbowHammerBolts"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "none"
troop_usage_value: 1024
effect: "10% damage with crossbows by troops in your formation."
effect_template: "{VALUE}% damage with crossbows by troops in your formation."
alternative_perk_string_id: "CrossbowPavise"
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

# Hammer Bolts - captain - troop combat

10% damage with crossbows by troops in your formation.
