---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "One Handed"
level: 175
perk: "Stand United"
perk_string_id: "OneHandedStandUnited"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "security"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
  - "garrison"
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% security provided by troops in the garrison of the governed settlement."
effect_template: "{VALUE}% security provided by troops in the garrison of the governed settlement."
alternative_perk_string_id: "OneHandedLeadByExample"
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

# Stand United - governor - settlement defense

30% security provided by troops in the garrison of the governed settlement.
