---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 200
perk: "Renowned Archer"
perk_string_id: "BowRenownedArcher"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "recruitment cost"
trigger_condition:
  - "party composition"
effect_tags:
  - "upgrade cost"
bonus: -0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-30% recruitment and upgrade cost to ranged troops."
effect_template: "{VALUE}% recruitment and upgrade cost to ranged troops."
alternative_perk_string_id: "BowBullsEye"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Composite effect spans recruitment and upgrade costs for ranged troops; single classification is partial."
---

# Renowned Archer - party leader - gold economy

-30% recruitment and upgrade cost to ranged troops.
