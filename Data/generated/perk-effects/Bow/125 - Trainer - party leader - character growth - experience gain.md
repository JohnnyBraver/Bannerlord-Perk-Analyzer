---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 125
perk: "Trainer"
perk_string_id: "BowTrainer"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "character growth"
perk_subtype: "experience gain"
trigger_condition: []
effect_tags:
  - "weapons"
bonus: 6
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "Daily Bow skill experience bonus to the party member with the lowest bow skill."
effect_template: "Daily Bow skill experience bonus to the party member with the lowest bow skill."
alternative_perk_string_id: "BowStrongBows"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Party member wording likely targets hero party members (companions/family/main hero if lowest Bow); game bonus is +6 but description has no numeric placeholder."
classification_review: ""
---

# Trainer - party leader - character growth

Daily Bow skill experience bonus to the party member with the lowest bow skill.
