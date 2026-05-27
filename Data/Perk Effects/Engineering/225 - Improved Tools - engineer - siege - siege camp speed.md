---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 225
perk: "Improved Tools"
perk_string_id: "EngineeringImprovedTools"
effect_slot: "primary"
role: "engineer"
role_value: 8
perk_type: "siege"
perk_subtype: "siege camp speed"
trigger_condition:
  - "during siege"
effect_tags: []
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% siege camp preparation speed."
effect_template: "{VALUE}% siege camp preparation speed."
alternative_perk_string_id: "EngineeringMetallurgy"
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

# Improved Tools - engineer - siege

20% siege camp preparation speed.
