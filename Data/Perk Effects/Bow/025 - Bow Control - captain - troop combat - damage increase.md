---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 25
perk: "Bow Control"
perk_string_id: "BowBowControl"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "mounted"
troop_usage_value: 256
effect: "5% damage with bows by troops in your formation."
effect_template: "{VALUE}% damage with bows by troops in your formation."
alternative_perk_string_id: "BowDeadAim"
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

# Bow Control - captain - troop combat

5% damage with bows by troops in your formation.
