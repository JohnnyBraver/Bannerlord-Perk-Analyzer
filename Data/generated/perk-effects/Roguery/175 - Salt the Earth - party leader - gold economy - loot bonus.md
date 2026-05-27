---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 175
perk: "Salt the Earth"
perk_string_id: "RoguerySaltTheEarth"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "loot bonus"
trigger_condition: []
effect_tags:
  - "village"
  - "loot"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% more loot when villagers comply to your hostile actions."
effect_template: "{VALUE}% more loot when villagers comply to your hostile actions."
alternative_perk_string_id: "RogueryOneOfTheFamily"
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

# Salt the Earth - party leader - gold economy

20% more loot when villagers comply to your hostile actions.
