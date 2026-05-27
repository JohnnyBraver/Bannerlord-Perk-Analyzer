---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 75
perk: "Authority"
perk_string_id: "LeadershipAuthority"
effect_slot: "primary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "security"
trigger_condition: []
effect_tags:
  - "defense"
  - "garrison"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% security bonus from the town garrison in the governing settlement."
effect_template: "{VALUE}% security bonus from the town garrison in the governing settlement."
alternative_perk_string_id: "LeadershipHeroicLeader"
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

# Authority - governor - settlement defense

20% security bonus from the town garrison in the governing settlement.
