---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 125
perk: "Steed Killer"
perk_string_id: "PolearmSteadKiller"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "mounts"
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
  - "weapons"
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "infantry, melee"
troop_usage_value: 129
effect: "30% damage to mounts with polearms by infantry in your formation."
effect_template: "{VALUE}% damage to mounts with polearms by infantry in your formation."
alternative_perk_string_id: "PolearmLancer"
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

# Steed Killer - captain - troop combat

30% damage to mounts with polearms by infantry in your formation.
