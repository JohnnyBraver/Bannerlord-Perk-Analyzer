---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 100
perk: "Mounted Archery"
perk_string_id: "BowMountedArchery"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "ranged accuracy"
trigger_condition:
  - "while mounted"
effect_tags:
  - "mounts"
bonus: -0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-30% accuracy penalty using bows while mounted."
effect_template: "{VALUE}% accuracy penalty using bows while mounted."
alternative_perk_string_id: "BowMerryMen"
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

# Mounted Archery - personal - personal combat

-30% accuracy penalty using bows while mounted.
