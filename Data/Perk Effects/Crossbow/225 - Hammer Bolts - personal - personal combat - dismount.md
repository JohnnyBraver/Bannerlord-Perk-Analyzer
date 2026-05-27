---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 225
perk: "Hammer Bolts"
perk_string_id: "CrossbowHammerBolts"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "dismount"
trigger_condition: []
effect_tags:
  - "weapons"
  - "mounts"
bonus: 0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "Crossbows can now dismount and ignore 50% dismount resistance on attacks against cavalry."
effect_template: "Crossbows can now dismount and ignore {VALUE}% dismount resistance on attacks against cavalry."
alternative_perk_string_id: "CrossbowPavise"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: ""
---

# Hammer Bolts - personal - personal combat

Crossbows can now dismount and ignore 50% dismount resistance on attacks against cavalry.
