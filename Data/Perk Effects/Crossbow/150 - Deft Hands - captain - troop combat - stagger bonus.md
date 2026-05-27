---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 150
perk: "Deft Hands"
perk_string_id: "CrossbowDeftHands"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "stagger bonus"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "none"
troop_usage_value: 1024
effect: "50% resistance to getting staggered while reloading crossbows to troops in your formation."
effect_template: "{VALUE}% resistance to getting staggered while reloading crossbows to troops in your formation."
alternative_perk_string_id: "CrossbowLooseAndMove"
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

# Deft Hands - captain - troop combat

50% resistance to getting staggered while reloading crossbows to troops in your formation.
