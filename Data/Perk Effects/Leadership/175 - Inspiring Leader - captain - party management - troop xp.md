---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 175
perk: "Inspiring Leader"
perk_string_id: "LeadershipInspiringLeader"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "none"
troop_usage_value: 0
effect: "5% experience to troops in your formation."
effect_template: "{VALUE}% experience to troops in your formation."
alternative_perk_string_id: "LeadershipUpliftingSpirit"
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

# Inspiring Leader - captain - party management

5% experience to troops in your formation.
