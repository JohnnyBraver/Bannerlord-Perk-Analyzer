---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 250
perk: "Terror"
perk_string_id: "CrossbowTerror"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "morale damage"
trigger_condition:
  - "on kill"
effect_tags:
  - "weapons"
bonus: 0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "none"
troop_usage_value: 1024
effect: "25% morale loss to enemy due to crossbow kills by troops in your formation."
effect_template: "{VALUE}% morale loss to enemy due to crossbow kills by troops in your formation."
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

# Terror - captain - troop combat

25% morale loss to enemy due to crossbow kills by troops in your formation.
