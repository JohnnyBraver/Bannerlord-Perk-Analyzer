---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 250
perk: "Picked Shots"
perk_string_id: "CrossbowBoltenGuard"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "wages"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% wages of tier 4+ ranged troops."
effect_template: "{VALUE}% wages of tier 4+ ranged troops."
alternative_perk_string_id: "CrossbowTerror"
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

# Picked Shots - party leader - gold economy

-50% wages of tier 4+ ranged troops.
