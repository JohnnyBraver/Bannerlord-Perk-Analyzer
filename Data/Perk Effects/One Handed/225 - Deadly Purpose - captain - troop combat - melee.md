---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "One Handed"
level: 225
perk: "Deadly Purpose"
perk_string_id: "OneHandedDeadlyPurpose"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "melee"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "infantry, cavalry"
troop_usage_value: 5
effect: "10% melee weapon damage by infantry in your formation."
effect_template: "{VALUE}% melee weapon damage by infantry in your formation."
alternative_perk_string_id: "OneHandedUnwaveringDefense"
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

# Deadly Purpose - captain - troop combat

10% melee weapon damage by infantry in your formation.
