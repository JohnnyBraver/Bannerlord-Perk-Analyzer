---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 250
perk: "Clockwork"
perk_string_id: "EngineeringClockwork"
effect_slot: "primary"
role: "engineer"
role_value: 8
perk_type: "reload speed"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
effect_tags: []
bonus: 0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "25% reload speed to ballistas during siege bombardment."
effect_template: "{VALUE}% reload speed to ballistas during siege bombardment."
alternative_perk_string_id: "EngineeringArchitecturalCommissions"
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

# Clockwork - engineer - reload speed

25% reload speed to ballistas during siege bombardment.
