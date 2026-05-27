---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "One Handed"
level: 150
perk: "Corps-a-corps"
perk_string_id: "OneHandedCorpsACorps"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "garrison size"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
  - "garrison"
bonus: 30
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "30 garrison limit in the governed settlement."
effect_template: "{VALUE} garrison limit in the governed settlement."
alternative_perk_string_id: "OneHandedMilitaryTradition"
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

# Corps-a-corps - governor - settlement defense

30 garrison limit in the governed settlement.
