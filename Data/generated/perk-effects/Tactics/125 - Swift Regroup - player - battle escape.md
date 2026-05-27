---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 125
perk: "Swift Regroup"
perk_string_id: "TacticsSwiftRegroup"
effect_slot: "primary"
role: "player"
role_value: 11
perk_type: "battle escape"
perk_subtype: ""
trigger_condition:
  - "during siege"
effect_tags: []
bonus: -0.15000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-15% disorganized state duration when a raid or siege is broken."
effect_template: "{VALUE}% disorganized state duration when a raid or siege is broken."
alternative_perk_string_id: "TacticsImproviser"
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

# Swift Regroup - player - battle escape

-15% disorganized state duration when a raid or siege is broken.
