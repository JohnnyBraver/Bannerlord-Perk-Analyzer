---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 175
perk: "One of the Family"
perk_string_id: "RogueryOneOfTheFamily"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "character growth"
perk_subtype: "skill bonus"
trigger_condition:
  - "party composition"
effect_tags:
  - "bandits"
bonus: 10
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "10 bonus Vigor and Control skills to bandit units in your party"
effect_template: "{VALUE} bonus Vigor and Control skills to bandit units in your party"
alternative_perk_string_id: "RoguerySaltTheEarth"
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

# One of the Family - party leader - character growth

10 bonus Vigor and Control skills to bandit units in your party
