---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "One Handed"
level: 150
perk: "Corps-a-corps"
perk_string_id: "OneHandedCorpsACorps"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "after battle"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% of the total experience gained as a bonus to infantry after battles."
effect_template: "{VALUE}% of the total experience gained as a bonus to infantry after battles."
alternative_perk_string_id: "OneHandedMilitaryTradition"
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

# Corps-a-corps - party leader - party management

10% of the total experience gained as a bonus to infantry after battles.
