---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 25
perk: "Sweet Talker"
perk_string_id: "RoguerySweetTalker"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "crime bonus"
perk_subtype: ""
trigger_condition: []
effect_tags:
  - "bandits"
  - "barter"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% chance for convincing bandits to leave in peace with barter."
effect_template: "{VALUE}% chance for convincing bandits to leave in peace with barter."
alternative_perk_string_id: "RogueryNoRestForTheWicked"
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

# Sweet Talker - party leader - crime bonus

20% chance for convincing bandits to leave in peace with barter.
