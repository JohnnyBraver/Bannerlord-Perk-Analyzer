---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 150
perk: "Loose and Move"
perk_string_id: "CrossbowLooseAndMove"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "movement speed"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "horse_archer"
troop_usage_value: 8
effect: "5% movement speed to ranged troops in your formation."
effect_template: "{VALUE}% movement speed to ranged troops in your formation."
alternative_perk_string_id: "CrossbowDeftHands"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is horse_archer, but description says ranged troops in your formation; verify whether this should apply only to mounted ranged troops."
classification_review: ""
---

# Loose and Move - captain - troop combat

5% movement speed to ranged troops in your formation.
