---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 50
perk: "Bodkin"
perk_string_id: "BowBodkin"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "armor penetration"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "mounted"
troop_usage_value: 256
effect: "5% armor penetration with bows by troops in your formation."
effect_template: "{VALUE}% armor penetration with bows by troops in your formation."
alternative_perk_string_id: "BowNockingPoint"
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

# Bodkin - captain - troop combat

5% armor penetration with bows by troops in your formation.
