---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 50
perk: "Deep Pockets"
perk_string_id: "RogueryDeepPockets"
effect_slot: "secondary"
role: "personal"
role_value: 12
perk_type: "gold economy"
perk_subtype: "wages"
trigger_condition: []
effect_tags:
  - "bandits"
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% bandit troop wages."
effect_template: "{VALUE}% bandit troop wages."
alternative_perk_string_id: "RogueryTwoFaced"
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

# Deep Pockets - personal - gold economy

-20% bandit troop wages.
