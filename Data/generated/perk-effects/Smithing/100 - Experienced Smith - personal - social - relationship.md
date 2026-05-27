---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Smithing"
level: 100
perk: "Experienced Smith"
perk_string_id: "ExperiencedSmith"
effect_slot: "secondary"
role: "personal"
role_value: 12
perk_type: "social"
perk_subtype: "relationship"
trigger_condition: []
effect_tags: []
bonus: 2
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "Successful crafting orders of notables increase your relation by 2 with them."
effect_template: "Successful crafting orders of notables increase your relation by {VALUE} with them."
alternative_perk_string_id: "SteelMaker3"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Successful crafting-order condition is not represented by current trigger_condition taxonomy."
classification_review: ""
---

# Experienced Smith - personal - social

Successful crafting orders of notables increase your relation by 2 with them.
