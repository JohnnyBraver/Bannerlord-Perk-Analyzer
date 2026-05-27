---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 100
perk: "Efficient Campaigner"
perk_string_id: "StewardEfficientCampaigner"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "food reserve"
trigger_condition: []
effect_tags:
  - "food"
  - "village"
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 extra food for each food taken during village raids for your party."
effect_template: "{VALUE} extra food for each food taken during village raids for your party."
alternative_perk_string_id: "StewardPaidInPromise"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Applies when taking food during village raids; no dedicated raid trigger condition exists."
classification_review: ""
---

# Efficient Campaigner - party leader - party management

1 extra food for each food taken during village raids for your party.
