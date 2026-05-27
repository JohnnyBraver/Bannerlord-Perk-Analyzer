---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Two Handed"
level: 200
perk: "Reckless Charge"
perk_string_id: "TwoHandedRecklessCharge"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "damage increase"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 0.02
increment_type: "add_factor"
increment_value: 1
troop_usage: "infantry"
troop_usage_value: 1
effect: "2% damage and movement speed to infantry in your formation."
effect_template: "{VALUE}% damage and movement speed to infantry in your formation."
alternative_perk_string_id: "TwoHandedThickHides"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Composite troop combat effect spans damage and movement speed; subtype captures damage only."
---

# Reckless Charge - captain - troop combat

2% damage and movement speed to infantry in your formation.
