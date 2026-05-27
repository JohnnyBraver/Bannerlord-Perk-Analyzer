---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 25
perk: "Dead Aim"
perk_string_id: "BowDeadAim"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "skill bonus"
trigger_condition: []
effect_tags:
  - "weapons"
bonus: 20
increment_type: "add"
increment_value: 0
troop_usage: "mounted"
troop_usage_value: 256
effect: "20 Bow skill to troops in your formation."
effect_template: "{VALUE} Bow skill to troops in your formation."
alternative_perk_string_id: "BowBowControl"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is mounted, but description says troops in your formation without that restriction."
classification_review: ""
---

# Dead Aim - captain - troop combat

20 Bow skill to troops in your formation.
