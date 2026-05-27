---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 200
perk: "Forced Labor"
perk_string_id: "StewardForcedLabor"
effect_slot: "primary"
role: "quartermaster"
role_value: 10
perk_type: "party management"
perk_subtype: "carrying capacity"
trigger_condition:
  - "party composition"
effect_tags:
  - "prisoners"
bonus: 0
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "Prisoners in your party provide carry capacity as if they are standard troops."
effect_template: "Prisoners in your party provide carry capacity as if they are standard troops."
alternative_perk_string_id: "StewardContractors"
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

# Forced Labor - quartermaster - party management

Prisoners in your party provide carry capacity as if they are standard troops.
