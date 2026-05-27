---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 50
perk: "Nocking Point"
perk_string_id: "BowNockingPoint"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "movement speed"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.03
increment_type: "add_factor"
increment_value: 1
troop_usage: "mounted"
troop_usage_value: 256
effect: "3% movement speed to archers in your formation."
effect_template: "{VALUE}% movement speed to archers in your formation."
alternative_perk_string_id: "BowBodkin"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is mounted, but description says archers in your formation without that restriction."
classification_review: ""
---

# Nocking Point - captain - troop combat

3% movement speed to archers in your formation.
