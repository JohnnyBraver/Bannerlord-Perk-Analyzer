---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 125
perk: "Lancer"
perk_string_id: "PolearmLancer"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "speed bonus"
trigger_condition:
  - "while mounted"
effect_tags:
  - "weapons"
  - "mounts"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% damage bonus from speed with polearms while mounted."
effect_template: "{VALUE}% damage bonus from speed with polearms while mounted."
alternative_perk_string_id: "PolearmSteadKiller"
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

# Lancer - personal - personal combat

20% damage bonus from speed with polearms while mounted.
