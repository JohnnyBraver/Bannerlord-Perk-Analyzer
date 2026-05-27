---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 100
perk: "Knock Off"
perk_string_id: "ThrowingKnockOff"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "party composition"
effect_tags:
  - "weapons"
  - "mounts"
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "ranged"
troop_usage_value: 514
effect: "5% throwing weapon damage to cavalry by troops in your formation."
effect_template: "{VALUE}% throwing weapon damage to cavalry by troops in your formation."
alternative_perk_string_id: "ThrowingRunningThrow"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is ranged, but description only says troops in your formation damaging cavalry; hidden ranged-troop restriction is not in the description."
classification_review: ""
---

# Knock Off - captain - troop combat

5% throwing weapon damage to cavalry by troops in your formation.
