---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "One Handed"
level: 50
perk: "To Be Blunt"
perk_string_id: "OneHandedToBeBlunt"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "security"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
bonus: 0.5
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "0.5 daily security to governed settlement."
effect_template: "{VALUE} daily security to governed settlement."
alternative_perk_string_id: "OneHandedSwiftStrike"
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

# To Be Blunt - governor - settlement defense

0.5 daily security to governed settlement.
