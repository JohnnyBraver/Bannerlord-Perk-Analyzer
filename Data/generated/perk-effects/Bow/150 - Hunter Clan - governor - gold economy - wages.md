---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Bow"
level: 150
perk: "Hunter Clan"
perk_string_id: "BowHunterClan"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "gold economy"
perk_subtype: "wages"
trigger_condition:
  - "governed settlement"
effect_tags:
  - "garrison"
bonus: -0.15000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-15% garrison wages in the governed castle."
effect_template: "{VALUE}% garrison wages in the governed castle."
alternative_perk_string_id: "BowDiscipline"
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

# Hunter Clan - governor - gold economy

-15% garrison wages in the governed castle.
