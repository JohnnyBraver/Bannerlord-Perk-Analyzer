---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 75
perk: "Know-How"
perk_string_id: "RogueryKnowHow"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "loot bonus"
trigger_condition: []
effect_tags:
  - "caravan"
  - "village"
  - "loot"
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "5% more loot from defeated villagers and caravans."
effect_template: "{VALUE}% more loot from defeated villagers and caravans."
alternative_perk_string_id: "RogueryInBestLight"
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

# Know-How - party leader - gold economy

5% more loot from defeated villagers and caravans.
