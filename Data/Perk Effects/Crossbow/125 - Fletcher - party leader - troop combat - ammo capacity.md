---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 125
perk: "Fletcher"
perk_string_id: "CrossbowFletcher"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "ammo capacity"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 2
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "2 bolts per quiver to troops in your party."
effect_template: "{VALUE} bolts per quiver to troops in your party."
alternative_perk_string_id: "CrossbowPuncture"
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

# Fletcher - party leader - troop combat

2 bolts per quiver to troops in your party.
