---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 225
perk: "Improved Tools"
perk_string_id: "EngineeringImprovedTools"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "melee"
trigger_condition: []
effect_tags: []
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "cavalry"
troop_usage_value: 4
effect: "5% melee damage by troops in your formation."
effect_template: "{VALUE}% melee damage by troops in your formation."
alternative_perk_string_id: "EngineeringMetallurgy"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is cavalry, but description only says troops in your formation; likely cavalry-only restriction is missing from text."
classification_review: ""
---

# Improved Tools - captain - troop combat

5% melee damage by troops in your formation.
