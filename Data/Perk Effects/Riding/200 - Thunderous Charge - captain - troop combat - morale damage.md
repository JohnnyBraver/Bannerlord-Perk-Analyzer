---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 200
perk: "Thunderous Charge"
perk_string_id: "RidingThunderousCharge"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "morale damage"
trigger_condition:
  - "on kill"
effect_tags:
  - "mounts"
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "ranged, cavalry"
troop_usage_value: 6
effect: "10% battle morale penalty to enemies with mounted melee kills by troops in your formation."
effect_template: "{VALUE}% battle morale penalty to enemies with mounted melee kills by troops in your formation."
alternative_perk_string_id: "RidingAnnoyingBuzz"
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

# Thunderous Charge - captain - troop combat

10% battle morale penalty to enemies with mounted melee kills by troops in your formation.
