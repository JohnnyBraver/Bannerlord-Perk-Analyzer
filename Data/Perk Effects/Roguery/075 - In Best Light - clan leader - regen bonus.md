---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 75
perk: "In Best Light"
perk_string_id: "RogueryInBestLight"
effect_slot: "secondary"
role: "clan leader"
role_value: 2
perk_type: "regen bonus"
perk_subtype: ""
trigger_condition: []
effect_tags:
  - "village"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% faster recovery from raids for your villages."
effect_template: "{VALUE}% faster recovery from raids for your villages."
alternative_perk_string_id: "RogueryKnowHow"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Village raid recovery has no dedicated taxonomy bucket; regen bonus is a fallback."
---

# In Best Light - clan leader - regen bonus

20% faster recovery from raids for your villages.
