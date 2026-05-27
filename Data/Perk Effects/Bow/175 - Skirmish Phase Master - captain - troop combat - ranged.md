---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 175
perk: "Skirmish Phase Master"
perk_string_id: "BowSkirmishPhaseMaster"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "ranged"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: -0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "horse_archer"
troop_usage_value: 8
effect: "-10% damage taken from projectiles by ranged troops in your formation."
effect_template: "{VALUE}% damage taken from projectiles by ranged troops in your formation."
alternative_perk_string_id: "BowEagleEye"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is horse_archer, but description says ranged troops in your formation without that restriction."
classification_review: ""
---

# Skirmish Phase Master - captain - troop combat

-10% damage taken from projectiles by ranged troops in your formation.
