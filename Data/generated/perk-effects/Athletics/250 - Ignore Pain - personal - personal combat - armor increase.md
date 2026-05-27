---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 250
perk: "Ignore Pain"
perk_string_id: "AthleticsIgnorePain"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "armor increase"
trigger_condition:
  - "on foot"
effect_tags: []
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% armor while on foot."
effect_template: "{VALUE}% armor while on foot."
alternative_perk_string_id: "AthleticsSpartan"
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

# Ignore Pain - personal - personal combat

10% armor while on foot.
