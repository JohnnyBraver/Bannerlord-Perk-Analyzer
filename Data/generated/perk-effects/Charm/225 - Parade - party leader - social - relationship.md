---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Charm"
level: 225
perk: "Parade"
perk_string_id: "CharmParade"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "social"
perk_subtype: "relationship"
trigger_condition: []
effect_tags: []
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "5% daily chance to gain +1 relationship with a random lord in the same army."
effect_template: "{VALUE}% daily chance to gain +1 relationship with a random lord in the same army."
alternative_perk_string_id: "CharmPublicSpeaker"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Same-army condition is not represented by current trigger_condition taxonomy."
classification_review: ""
---

# Parade - party leader - social

5% daily chance to gain +1 relationship with a random lord in the same army.
