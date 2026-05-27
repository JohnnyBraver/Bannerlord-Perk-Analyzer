---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 175
perk: "Head Hunter"
perk_string_id: "ThrowingHeadHunter"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "recruitment cost"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% recruitment cost of tier 2+ troops."
effect_template: "{VALUE}% recruitment cost of tier 2+ troops."
alternative_perk_string_id: "ThrowingSlingingCompetitions"
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

# Head Hunter - party leader - gold economy

-20% recruitment cost of tier 2+ troops.
