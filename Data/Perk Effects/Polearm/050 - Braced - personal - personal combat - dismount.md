---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 50
perk: "Braced"
perk_string_id: "PolearmBraced"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "dismount"
trigger_condition: []
effect_tags:
  - "weapons"
  - "mounts"
bonus: 0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "Polearms that can dismount ignore 25% dismount resistance on attacks against cavalry."
effect_template: "Polearms that can dismount ignore {VALUE}% dismount resistance on attacks against cavalry."
alternative_perk_string_id: "PolearmKeepAtBay"
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

# Braced - personal - personal combat

Polearms that can dismount ignore 25% dismount resistance on attacks against cavalry.
