---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 150
perk: "Patrols"
perk_string_id: "ScoutingPatrols"
effect_slot: "primary"
role: "scout"
role_value: 9
perk_type: "party management"
perk_subtype: "morale"
trigger_condition: []
effect_tags:
  - "bandits"
bonus: 5
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "5 battle morale against bandit parties."
effect_template: "{VALUE} battle morale against bandit parties."
alternative_perk_string_id: "ScoutingMountedScouts"
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

# Patrols - scout - party management

5 battle morale against bandit parties.
