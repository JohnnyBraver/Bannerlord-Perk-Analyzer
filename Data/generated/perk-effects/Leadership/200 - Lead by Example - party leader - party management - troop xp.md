---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 200
perk: "Lead by Example"
perk_string_id: "LeadershipLeadByExample"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% shared experience for cavalry troops."
effect_template: "{VALUE}% shared experience for cavalry troops."
alternative_perk_string_id: "LeadershipTrustedCommander"
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

# Lead by Example - party leader - party management

10% shared experience for cavalry troops.
