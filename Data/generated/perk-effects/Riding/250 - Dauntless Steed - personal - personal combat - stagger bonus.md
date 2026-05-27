---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 250
perk: "Dauntless Steed"
perk_string_id: "RidingDauntlessSteed"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "stagger bonus"
trigger_condition:
  - "while mounted"
effect_tags:
  - "mounts"
bonus: 0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "50% resistance to getting staggered while mounted."
effect_template: "{VALUE}% resistance to getting staggered while mounted."
alternative_perk_string_id: "RidingToughSteed"
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

# Dauntless Steed - personal - personal combat

50% resistance to getting staggered while mounted.
