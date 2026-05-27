---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 50
perk: "Hunter"
perk_string_id: "ThrowingHunter"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "mounts"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
bonus: 0.08
increment_type: "add_factor"
increment_value: 1
troop_usage: "none"
troop_usage_value: 512
effect: "8% damage to mounts with throwing weapons by troops in your formation."
effect_template: "{VALUE}% damage to mounts with throwing weapons by troops in your formation."
alternative_perk_string_id: "ThrowingFlexibleFighter"
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

# Hunter - captain - troop combat

8% damage to mounts with throwing weapons by troops in your formation.
