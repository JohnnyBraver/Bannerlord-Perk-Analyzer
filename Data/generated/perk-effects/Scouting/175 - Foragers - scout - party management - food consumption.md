---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 175
perk: "Foragers"
perk_string_id: "ScoutingForagers"
effect_slot: "primary"
role: "scout"
role_value: 9
perk_type: "party management"
perk_subtype: "food consumption"
trigger_condition:
  - "while traveling"
  - "terrain"
effect_tags:
  - "food"
bonus: -0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-10% food consumption while traveling through steppes and forests."
effect_template: "{VALUE}% food consumption while traveling through steppes and forests."
alternative_perk_string_id: "ScoutingBeastWhisperer"
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

# Foragers - scout - party management

-10% food consumption while traveling through steppes and forests.
