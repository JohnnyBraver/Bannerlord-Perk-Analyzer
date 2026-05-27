---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 200
perk: "Steady"
perk_string_id: "CrossbowSteady"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement economy"
perk_subtype: "settlement income"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "tariff"
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "5% tariff gain in the governed settlement."
effect_template: "{VALUE}% tariff gain in the governed settlement."
alternative_perk_string_id: "CrossbowLongShots"
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

# Steady - governor - settlement economy

5% tariff gain in the governed settlement.
