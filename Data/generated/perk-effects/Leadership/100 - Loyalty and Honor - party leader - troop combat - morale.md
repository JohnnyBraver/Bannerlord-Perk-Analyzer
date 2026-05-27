---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 100
perk: "Loyalty and Honor"
perk_string_id: "LeadershipLoyaltyAndHonor"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "morale"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 3
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "Tier 3+ troops in your party no longer retreat due to low morale"
effect_template: "Tier 3+ troops in your party no longer retreat due to low morale"
alternative_perk_string_id: "LeadershipFamousCommander"
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

# Loyalty and Honor - party leader - troop combat

Tier 3+ troops in your party no longer retreat due to low morale
