---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Charm"
level: 50
perk: "Warlord"
perk_string_id: "CharmWarlord"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "social"
perk_subtype: "relationship"
trigger_condition:
  - "after battle"
  - "own kingdom"
effect_tags: []
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 relationship with a random lord of your kingdom when an enemy lord is defeated."
effect_template: "{VALUE} relationship with a random lord of your kingdom when an enemy lord is defeated."
alternative_perk_string_id: "CharmOratory"
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

# Warlord - party leader - social

1 relationship with a random lord of your kingdom when an enemy lord is defeated.
