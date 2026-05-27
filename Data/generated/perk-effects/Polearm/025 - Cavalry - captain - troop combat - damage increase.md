---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 25
perk: "Cavalry"
perk_string_id: "PolearmCavalry"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "party composition"
effect_tags:
  - "mounts"
bonus: 0.02
increment_type: "add_factor"
increment_value: 1
troop_usage: "ranged"
troop_usage_value: 2
effect: "2% damage by cavalry troops in your formation."
effect_template: "{VALUE}% damage by cavalry troops in your formation."
alternative_perk_string_id: "PolearmPikeman"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: true
bug_note: ""
notes: "Game troop_usage is ranged, but description says cavalry troops in your formation."
classification_review: ""
---

# Cavalry - captain - troop combat

2% damage by cavalry troops in your formation.
