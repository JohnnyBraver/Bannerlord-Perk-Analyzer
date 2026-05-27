---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 50
perk: "Stout Defender"
perk_string_id: "LeadershipStoutDefender"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "morale"
trigger_condition:
  - "defending"
effect_tags: []
bonus: 8
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "8 starting battle morale when defending."
effect_template: "{VALUE} starting battle morale when defending."
alternative_perk_string_id: "LeadershipFerventAttacker"
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

# Stout Defender - party leader - troop combat

8 starting battle morale when defending.
