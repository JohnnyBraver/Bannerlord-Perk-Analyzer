---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 75
perk: "Sheriff"
perk_string_id: "CrossbowSheriff"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "infantry"
troop_usage_value: 1
effect: "10% crossbow damage to infantry by troops in your formation."
effect_template: "{VALUE}% crossbow damage to infantry by troops in your formation."
alternative_perk_string_id: "CrossbowDonkeysSwiftness"
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

# Sheriff - captain - troop combat

10% crossbow damage to infantry by troops in your formation.
