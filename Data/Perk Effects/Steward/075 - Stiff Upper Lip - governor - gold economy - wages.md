---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 75
perk: "Stiff Upper Lip"
perk_string_id: "StewardStiffUpperLip"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "gold economy"
perk_subtype: "wages"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "defense"
  - "garrison"
  - "fortifications"
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% garrison wages in the governed castle."
effect_template: "{VALUE}% garrison wages in the governed castle."
alternative_perk_string_id: "StewardSweatshops"
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

# Stiff Upper Lip - governor - gold economy

-20% garrison wages in the governed castle.
