---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Two Handed"
level: 125
perk: "Confidence"
perk_string_id: "TwoHandedConfidence"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "damage increase"
trigger_condition:
  - "health threshold"
effect_tags:
  - "weapons"
bonus: 0.15000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "15% damage with two handed weapons while you have more than 90% of your hit points."
effect_template: "{VALUE}% damage with two handed weapons while you have more than 90% of your hit points."
alternative_perk_string_id: "TwoHandedBerserker"
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

# Confidence - personal - personal combat

15% damage with two handed weapons while you have more than 90% of your hit points.
