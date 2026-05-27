---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Two Handed"
level: 200
perk: "Reckless Charge"
perk_string_id: "TwoHandedRecklessCharge"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "speed bonus"
trigger_condition:
  - "on foot"
effect_tags:
  - "weapons"
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% damage bonus from speed with two handed weapons while on foot."
effect_template: "{VALUE}% damage bonus from speed with two handed weapons while on foot."
alternative_perk_string_id: "TwoHandedThickHides"
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

# Reckless Charge - personal - personal combat

20% damage bonus from speed with two handed weapons while on foot.
