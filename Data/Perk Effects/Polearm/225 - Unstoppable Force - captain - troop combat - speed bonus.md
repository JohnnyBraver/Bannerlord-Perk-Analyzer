---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 225
perk: "Unstoppable Force"
perk_string_id: "PolearmUnstoppableForce"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "speed bonus"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
  - "mounts"
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "ranged, melee"
troop_usage_value: 130
effect: "30% damage bonus from speed with polearms to cavalry in your formation."
effect_template: "{VALUE}% damage bonus from speed with polearms to cavalry in your formation."
alternative_perk_string_id: "PolearmSureFooted"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is ranged and melee, but description says cavalry in your formation."
classification_review: ""
---

# Unstoppable Force - captain - troop combat

30% damage bonus from speed with polearms to cavalry in your formation.
