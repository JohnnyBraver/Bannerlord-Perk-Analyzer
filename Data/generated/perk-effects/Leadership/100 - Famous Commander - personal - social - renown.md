---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 100
perk: "Famous Commander"
perk_string_id: "LeadershipFamousCommander"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "social"
perk_subtype: "renown"
trigger_condition:
  - "after battle"
effect_tags: []
bonus: 0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "50% renown gain from battles."
effect_template: "{VALUE}% renown gain from battles."
alternative_perk_string_id: "LeadershipLoyaltyAndHonor"
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

# Famous Commander - personal - social

50% renown gain from battles.
