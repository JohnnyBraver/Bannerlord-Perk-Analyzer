---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "One Handed"
level: 25
perk: "Wrapped Handles"
perk_string_id: "OneHandedWrappedHandles"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "skill bonus"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 30
increment_type: "add"
increment_value: 0
troop_usage: "heroes"
troop_usage_value: 16
effect: "30 one handed skill to infantry troops in your formation."
effect_template: "{VALUE} one handed skill to infantry troops in your formation."
alternative_perk_string_id: "OneHandedBasher"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is heroes, but description says infantry troops in your formation; verify whether this applies only to hero agents."
classification_review: ""
---

# Wrapped Handles - captain - troop combat

30 one handed skill to infantry troops in your formation.
