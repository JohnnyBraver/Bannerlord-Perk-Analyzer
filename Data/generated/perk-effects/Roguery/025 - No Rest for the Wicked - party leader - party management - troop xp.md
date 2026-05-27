---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 25
perk: "No Rest for the Wicked"
perk_string_id: "RogueryNoRestForTheWicked"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "party composition"
effect_tags:
  - "bandits"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% experience gain for bandits in your party."
effect_template: "{VALUE}% experience gain for bandits in your party."
alternative_perk_string_id: "RoguerySweetTalker"
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

# No Rest for the Wicked - party leader - party management

20% experience gain for bandits in your party.
