---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 50
perk: "Fervent Attacker"
perk_string_id: "LeadershipFerventAttacker"
effect_slot: "secondary"
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
effect: "50% recruitment rate of tier 1, 2 and 3 prisoners."
effect_template: "{VALUE}% recruitment rate of tier 1, 2 and 3 prisoners."
alternative_perk_string_id: "LeadershipStoutDefender"
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

# Fervent Attacker - party leader - party management

50% recruitment rate of tier 1, 2 and 3 prisoners.
