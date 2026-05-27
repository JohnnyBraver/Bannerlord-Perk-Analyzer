---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Charm"
level: 150
perk: "Effort For The People"
perk_string_id: "CharmEffortForThePeople"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "social"
perk_subtype: "relationship"
trigger_condition: []
effect_tags: []
bonus: 3
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "3 relation with the nearest settlement owner clan when you clear a hideout. +1 town loyalty if it is your clan."
effect_template: "{VALUE} relation with the nearest settlement owner clan when you clear a hideout. +1 town loyalty if it is your clan."
alternative_perk_string_id: "CharmSlickNegotiator"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Hideout-clear condition is not represented by current trigger_condition taxonomy."
classification_review: "Composite effect spans relationship and town loyalty; single classification is partial."
---

# Effort For The People - personal - social

3 relation with the nearest settlement owner clan when you clear a hideout. +1 town loyalty if it is your clan.
