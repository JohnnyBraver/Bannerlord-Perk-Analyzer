---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Engineering"
level: 275
perk: "Masterwork"
perk_string_id: "EngineeringMasterwork"
effect_slot: "primary"
role: "engineer"
role_value: 8
perk_type: "damage increase"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
  - "over skill cap"
effect_tags: []
bonus: 0.01
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "1% damage for each engineering skill point over 250 for siege engines in siege bombardment."
effect_template: "{VALUE}% damage for each engineering skill point over 250 for siege engines in siege bombardment."
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

# Masterwork - engineer - damage increase

1% damage for each engineering skill point over 250 for siege engines in siege bombardment.
