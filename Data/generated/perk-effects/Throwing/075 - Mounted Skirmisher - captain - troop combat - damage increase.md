---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 75
perk: "Mounted Skirmisher"
perk_string_id: "ThrowingMountedSkirmisher"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
  - "mounts"
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "ranged"
troop_usage_value: 514
effect: "10% damage with throwing weapons by mounted troops in your formation."
effect_template: "{VALUE}% damage with throwing weapons by mounted troops in your formation."
alternative_perk_string_id: "ThrowingWellPrepared"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is ranged, but description says mounted troops in your formation."
classification_review: ""
---

# Mounted Skirmisher - captain - troop combat

10% damage with throwing weapons by mounted troops in your formation.
