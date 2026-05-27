---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 200
perk: "Annoying Buzz"
perk_string_id: "RidingAnnoyingBuzz"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "morale damage"
trigger_condition:
  - "on kill"
effect_tags:
  - "mounts"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% battle morale penalty to enemies with mounted ranged kills."
effect_template: "{VALUE}% battle morale penalty to enemies with mounted ranged kills."
alternative_perk_string_id: "RidingThunderousCharge"
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

# Annoying Buzz - personal - personal combat

20% battle morale penalty to enemies with mounted ranged kills.
