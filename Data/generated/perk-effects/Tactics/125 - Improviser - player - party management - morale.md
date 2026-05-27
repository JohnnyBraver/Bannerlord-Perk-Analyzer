---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 125
perk: "Improviser"
perk_string_id: "TacticsImproviser"
effect_slot: "primary"
role: "player"
role_value: 11
perk_type: "party management"
perk_subtype: "morale"
trigger_condition:
  - "during siege"
  - "defending"
effect_tags: []
bonus: 0
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "No morale penalty for disorganized state in battles, in sally out or when being attacked."
effect_template: "No morale penalty for disorganized state in battles, in sally out or when being attacked."
alternative_perk_string_id: "TacticsSwiftRegroup"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Effect removes morale penalty from disorganized state; battle escape is only an indirect source of the state."
---

# Improviser - player - party management

No morale penalty for disorganized state in battles, in sally out or when being attacked.
