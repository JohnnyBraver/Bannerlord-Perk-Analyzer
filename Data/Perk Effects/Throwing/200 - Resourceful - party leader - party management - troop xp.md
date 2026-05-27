---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 200
perk: "Resourceful"
perk_string_id: "ThrowingResourceful"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% experience from battles to troops in your party equipped with throwing weapons."
effect_template: "{VALUE}% experience from battles to troops in your party equipped with throwing weapons."
alternative_perk_string_id: "ThrowingSplinters"
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

# Resourceful - party leader - party management

10% experience from battles to troops in your party equipped with throwing weapons.
