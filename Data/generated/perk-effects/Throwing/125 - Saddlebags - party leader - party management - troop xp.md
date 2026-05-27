---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 125
perk: "Saddlebags"
perk_string_id: "ThrowingSaddlebags"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 daily experience to infantry troops in your party."
effect_template: "{VALUE} daily experience to infantry troops in your party."
alternative_perk_string_id: "ThrowingSkirmisher"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is all, but description says infantry troops in your party."
classification_review: ""
---

# Saddlebags - party leader - party management

1 daily experience to infantry troops in your party.
