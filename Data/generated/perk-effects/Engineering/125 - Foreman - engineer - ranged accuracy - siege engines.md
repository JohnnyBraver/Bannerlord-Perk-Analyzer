---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 125
perk: "Foreman"
perk_string_id: "EngineeringForeman"
effect_slot: "primary"
role: "engineer"
role_value: 8
perk_type: "ranged accuracy"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% mangonel and trebuchet accuracy during siege bombardment."
effect_template: "{VALUE}% mangonel and trebuchet accuracy during siege bombardment."
alternative_perk_string_id: "EngineeringSalvager"
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

# Foreman - engineer - ranged accuracy

10% mangonel and trebuchet accuracy during siege bombardment.
