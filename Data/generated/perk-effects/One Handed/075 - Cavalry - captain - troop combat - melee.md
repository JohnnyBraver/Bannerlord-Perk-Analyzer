---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "One Handed"
level: 75
perk: "Cavalry"
perk_string_id: "OneHandedCavalry"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "melee"
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "ranged, cavalry"
troop_usage_value: 6
effect: "5% melee damage by cavalry troops in your formation."
effect_template: "{VALUE}% melee damage by cavalry troops in your formation."
alternative_perk_string_id: "OneHandedShieldBearer"
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

# Cavalry - captain - troop combat

5% melee damage by cavalry troops in your formation.
