---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Charm"
level: 200
perk: "Moral Leader"
perk_string_id: "CharmMoralLeader"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "social"
perk_subtype: "dialog checks"
trigger_condition:
  - "same culture"
effect_tags: []
bonus: -1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "-1 persuasion success required against characters of your own culture."
effect_template: "{VALUE} persuasion success required against characters of your own culture."
alternative_perk_string_id: "CharmNaturalLeader"
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

# Moral Leader - personal - social

-1 persuasion success required against characters of your own culture.
