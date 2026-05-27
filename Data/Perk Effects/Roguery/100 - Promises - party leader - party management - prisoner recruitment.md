---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 100
perk: "Promises"
perk_string_id: "RogueryPromises"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "prisoner recruitment"
trigger_condition:
  - "party composition"
effect_tags:
  - "bandits"
  - "prisoners"
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% recruitment rate for bandit prisoners in your party."
effect_template: "{VALUE}% recruitment rate for bandit prisoners in your party."
alternative_perk_string_id: "RogueryManhunter"
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

# Promises - party leader - party management

30% recruitment rate for bandit prisoners in your party.
