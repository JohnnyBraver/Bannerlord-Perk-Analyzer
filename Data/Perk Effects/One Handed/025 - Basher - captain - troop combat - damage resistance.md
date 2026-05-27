---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "One Handed"
level: 25
perk: "Basher"
perk_string_id: "OneHandedBasher"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage resistance"
trigger_condition: []
effect_tags: []
bonus: -0.04
increment_type: "add_factor"
increment_value: 1
troop_usage: "infantry"
troop_usage_value: 1
effect: "-4% damage taken by infantry while in shield wall formation."
effect_template: "{VALUE}% damage taken by infantry while in shield wall formation."
alternative_perk_string_id: "OneHandedWrappedHandles"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Shield-wall formation condition is not represented by current trigger_condition taxonomy."
---

# Basher - captain - troop combat

-4% damage taken by infantry while in shield wall formation.
