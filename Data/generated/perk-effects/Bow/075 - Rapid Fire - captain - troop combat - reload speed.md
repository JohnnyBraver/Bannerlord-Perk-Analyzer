---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 75
perk: "Rapid Fire"
perk_string_id: "BowRapidFire"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "reload speed"
trigger_condition: []
effect_tags: []
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "horse_archer"
troop_usage_value: 8
effect: "5% reload speed to troops in your formation."
effect_template: "{VALUE}% reload speed to troops in your formation."
alternative_perk_string_id: "BowQuickAdjustments"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is horse_archer, but description says troops in your formation without that restriction."
classification_review: ""
---

# Rapid Fire - captain - troop combat

5% reload speed to troops in your formation.
