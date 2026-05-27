---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 175
perk: "Pick Them Off The Walls"
perk_string_id: "TacticsPickThemOfTheWalls"
effect_slot: "primary"
role: "engineer"
role_value: 8
perk_type: "damage increase"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
effect_tags: []
bonus: 0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "25% chance for dealing double damage to siege defender troops in siege bombardment"
effect_template: "{VALUE}% chance for dealing double damage to siege defender troops in siege bombardment"
alternative_perk_string_id: "TacticsMakeThemPay"
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

# Pick Them Off The Walls - engineer - damage increase

25% chance for dealing double damage to siege defender troops in siege bombardment
