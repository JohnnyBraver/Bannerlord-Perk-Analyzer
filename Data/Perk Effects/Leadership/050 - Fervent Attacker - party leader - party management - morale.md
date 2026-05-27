---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 50
perk: "Fervent Attacker"
perk_string_id: "LeadershipFerventAttacker"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "morale"
trigger_condition:
  - "attacking"
effect_tags: []
bonus: 4
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "4 starting battle morale when attacking."
effect_template: "{VALUE} starting battle morale when attacking."
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

4 starting battle morale when attacking.
