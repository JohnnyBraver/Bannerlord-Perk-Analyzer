---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 275
perk: "Uncanny Insight"
perk_string_id: "ScoutingUncannyInsight"
effect_slot: "primary"
role: "scout"
role_value: 9
perk_type: "party management"
perk_subtype: "party speed"
trigger_condition:
  - "over skill cap"
effect_tags: []
bonus: 0.001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "0.1% party speed for every skill point above 200 scouting skill."
effect_template: "{VALUE}% party speed for every skill point above 200 scouting skill."
alternative_perk_string_id: ""
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

# Uncanny Insight - scout - party management

0.1% party speed for every skill point above 200 scouting skill.
