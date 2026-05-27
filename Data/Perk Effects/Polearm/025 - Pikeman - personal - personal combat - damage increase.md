---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 25
perk: "Pikeman"
perk_string_id: "PolearmPikeman"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "damage increase"
trigger_condition:
  - "on foot"
effect_tags:
  - "weapons"
bonus: 0.02
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "2% damage with polearms on foot."
effect_template: "{VALUE}% damage with polearms on foot."
alternative_perk_string_id: "PolearmCavalry"
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

# Pikeman - personal - personal combat

2% damage with polearms on foot.
