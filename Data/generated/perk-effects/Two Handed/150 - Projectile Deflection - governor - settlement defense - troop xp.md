---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Two Handed"
level: 150
perk: "Projectile Deflection"
perk_string_id: "TwoHandedProjectileDeflection"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement defense"
perk_subtype: "troop xp"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
  - "garrison"
bonus: 0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "10% experience to garrison troops in the governed settlement."
effect_template: "{VALUE}% experience to garrison troops in the governed settlement."
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

# Projectile Deflection - governor - settlement defense

10% experience to garrison troops in the governed settlement.
