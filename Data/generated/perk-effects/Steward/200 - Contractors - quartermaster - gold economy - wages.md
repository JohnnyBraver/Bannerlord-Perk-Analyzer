---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 200
perk: "Contractors"
perk_string_id: "StewardContractors"
effect_slot: "primary"
role: "quartermaster"
role_value: 10
perk_type: "gold economy"
perk_subtype: "wages"
trigger_condition:
  - "party composition"
effect_tags:
  - "upgrade cost"
bonus: -0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-25% wages and upgrade costs of the mercenary troops in your party."
effect_template: "{VALUE}% wages and upgrade costs of the mercenary troops in your party."
alternative_perk_string_id: "StewardForcedLabor"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Composite effect spans wages and upgrade costs for mercenary troops; single classification is partial."
---

# Contractors - quartermaster - gold economy

-25% wages and upgrade costs of the mercenary troops in your party.
