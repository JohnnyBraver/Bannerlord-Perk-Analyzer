---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 225
perk: "Keen Sight"
perk_string_id: "ScoutingKeenSight"
effect_slot: "primary"
role: "scout"
role_value: 9
perk_type: "party vision"
perk_subtype: ""
trigger_condition:
  - "terrain"
  - "while traveling"
effect_tags: []
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% sight penalty for traveling in forests."
effect_template: "{VALUE}% sight penalty for traveling in forests."
alternative_perk_string_id: "ScoutingVantagePoint"
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

# Keen Sight - scout - party vision

-50% sight penalty for traveling in forests.
