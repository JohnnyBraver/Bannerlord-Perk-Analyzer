---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 225
perk: "Horse Master"
perk_string_id: "BowHorseMaster"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "skill bonus"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
  - "mounts"
bonus: 30
increment_type: "add"
increment_value: 0
troop_usage: "ranged, mounted"
troop_usage_value: 258
effect: "30 bow skill to horse archers in your formation"
effect_template: "{VALUE} bow skill to horse archers in your formation"
alternative_perk_string_id: "BowDeepQuivers"
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

# Horse Master - captain - troop combat

30 bow skill to horse archers in your formation
