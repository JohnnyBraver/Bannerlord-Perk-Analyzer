---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 200
perk: "Trusted Commander"
perk_string_id: "LeadershipTrustedCommander"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "prisoner recruitment"
trigger_condition:
  - "party composition"
effect_tags:
  - "prisoners"
bonus: 0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "50% recruitment rate for ranged prisoners."
effect_template: "{VALUE}% recruitment rate for ranged prisoners."
alternative_perk_string_id: "LeadershipLeadByExample"
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

# Trusted Commander - party leader - party management

50% recruitment rate for ranged prisoners.
