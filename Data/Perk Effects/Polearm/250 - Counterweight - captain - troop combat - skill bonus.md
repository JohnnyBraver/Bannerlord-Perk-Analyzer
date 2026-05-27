---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 250
perk: "Counterweight"
perk_string_id: "PolearmCounterweight"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "skill bonus"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
bonus: 20
increment_type: "add"
increment_value: 0
troop_usage: "melee"
troop_usage_value: 128
effect: "20 polearm skill to troops in your formation."
effect_template: "{VALUE} polearm skill to troops in your formation."
alternative_perk_string_id: "PolearmSharpenTheTip"
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

# Counterweight - captain - troop combat

20 polearm skill to troops in your formation.
