---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 175
perk: "Phalanx"
perk_string_id: "PolearmPhalanx"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "skill bonus"
trigger_condition: []
effect_tags:
  - "weapons"
bonus: 30
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "30 melee weapon skills to troops in your party while in shield wall formation."
effect_template: "{VALUE} melee weapon skills to troops in your party while in shield wall formation."
alternative_perk_string_id: "PolearmStandardBearer"
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

# Phalanx - party leader - troop combat

30 melee weapon skills to troops in your party while in shield wall formation.
