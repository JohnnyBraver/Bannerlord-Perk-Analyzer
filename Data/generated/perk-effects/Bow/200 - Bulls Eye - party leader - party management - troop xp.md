---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 200
perk: "Bulls Eye"
perk_string_id: "BowBullsEye"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "after battle"
  - "party composition"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "horse_archer"
troop_usage_value: 8
effect: "10% bonus experience to ranged troops in your party after every battle."
effect_template: "{VALUE}% bonus experience to ranged troops in your party after every battle."
alternative_perk_string_id: "BowRenownedArcher"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is horse_archer, but description says ranged troops in your party without that restriction."
classification_review: ""
---

# Bulls Eye - party leader - party management

10% bonus experience to ranged troops in your party after every battle.
