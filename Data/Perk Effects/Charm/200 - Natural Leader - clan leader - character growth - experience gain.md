---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Charm"
level: 200
perk: "Natural Leader"
perk_string_id: "CharmNaturalLeader"
effect_slot: "secondary"
role: "clan leader"
role_value: 2
perk_type: "character growth"
perk_subtype: "experience gain"
trigger_condition: []
effect_tags:
  - "companions"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% experience gain for companions."
effect_template: "{VALUE}% experience gain for companions."
alternative_perk_string_id: "CharmMoralLeader"
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

# Natural Leader - clan leader - character growth

20% experience gain for companions.
