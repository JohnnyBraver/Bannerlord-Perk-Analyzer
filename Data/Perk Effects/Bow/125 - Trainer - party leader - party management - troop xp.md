---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 125
perk: "Trainer"
perk_string_id: "BowTrainer"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 3
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "3 daily experience to archers in your party."
effect_template: "{VALUE} daily experience to archers in your party."
alternative_perk_string_id: "BowStrongBows"
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

# Trainer - party leader - party management

3 daily experience to archers in your party.
