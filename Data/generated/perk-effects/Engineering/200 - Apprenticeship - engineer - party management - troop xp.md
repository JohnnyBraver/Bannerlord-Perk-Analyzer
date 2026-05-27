---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 200
perk: "Apprenticeship"
perk_string_id: "EngineeringApprenticeship"
effect_slot: "primary"
role: "engineer"
role_value: 8
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "during siege"
effect_tags: []
bonus: 5
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "5 experience to troops when a siege engine is built."
effect_template: "{VALUE} experience to troops when a siege engine is built."
alternative_perk_string_id: "EngineeringEngineeringGuilds"
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

# Apprenticeship - engineer - party management

5 experience to troops when a siege engine is built.
