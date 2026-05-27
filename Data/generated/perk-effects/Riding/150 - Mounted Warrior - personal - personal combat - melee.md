---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 150
perk: "Mounted Warrior"
perk_string_id: "RidingMountedWarrior"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "melee"
trigger_condition:
  - "while mounted"
effect_tags:
  - "mounts"
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "5% mounted melee damage."
effect_template: "{VALUE}% mounted melee damage."
alternative_perk_string_id: "RidingHorseArcher"
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

# Mounted Warrior - personal - personal combat

5% mounted melee damage.
