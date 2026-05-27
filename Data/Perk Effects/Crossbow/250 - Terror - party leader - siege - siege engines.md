---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 250
perk: "Terror"
perk_string_id: "CrossbowTerror"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "siege"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
effect_tags: []
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% chance of increasing the siege bombardment casualties per hit by 1."
effect_template: "{VALUE}% chance of increasing the siege bombardment casualties per hit by 1."
alternative_perk_string_id: "CrossbowBoltenGuard"
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

# Terror - party leader - siege

20% chance of increasing the siege bombardment casualties per hit by 1.
