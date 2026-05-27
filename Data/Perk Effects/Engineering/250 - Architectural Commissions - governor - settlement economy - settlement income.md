---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 250
perk: "Architectural Commissions"
perk_string_id: "EngineeringArchitecturalCommissions"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement economy"
perk_subtype: "settlement income"
trigger_condition:
  - "project active"
  - "governed settlement"
effect_tags:
  - "projects"
bonus: 20
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "20 gold per day for continuous projects in the governed settlement."
effect_template: "{VALUE} gold per day for continuous projects in the governed settlement."
alternative_perk_string_id: "EngineeringClockwork"
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

# Architectural Commissions - governor - settlement economy

20 gold per day for continuous projects in the governed settlement.
