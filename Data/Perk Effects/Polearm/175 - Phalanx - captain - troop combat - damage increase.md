---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 175
perk: "Phalanx"
perk_string_id: "PolearmPhalanx"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
bonus: 0.03
increment_type: "add_factor"
increment_value: 1
troop_usage: "melee"
troop_usage_value: 128
effect: "3% damage with polearms by troops in your formation."
effect_template: "{VALUE}% damage with polearms by troops in your formation."
alternative_perk_string_id: "PolearmStandardBearer"
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

# Phalanx - captain - troop combat

3% damage with polearms by troops in your formation.
