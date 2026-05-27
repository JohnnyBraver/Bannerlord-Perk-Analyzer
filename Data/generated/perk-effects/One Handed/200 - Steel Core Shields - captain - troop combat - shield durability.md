---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "One Handed"
level: 200
perk: "Steel Core Shields"
perk_string_id: "OneHandedSteelCoreShields"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "shield durability"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: -0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "non_hero"
troop_usage_value: 32
effect: "-10% damage to shields of infantry troops in your formation."
effect_template: "{VALUE}% damage to shields of infantry troops in your formation."
alternative_perk_string_id: "OneHandedFleetOfFoot"
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

# Steel Core Shields - captain - troop combat

-10% damage to shields of infantry troops in your formation.
