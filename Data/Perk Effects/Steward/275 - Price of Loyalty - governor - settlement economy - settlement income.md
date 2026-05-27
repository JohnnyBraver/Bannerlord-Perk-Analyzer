---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 275
perk: "Price of Loyalty"
perk_string_id: "StewardPriceOfLoyalty"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "settlement economy"
perk_subtype: "settlement income"
trigger_condition:
  - "governed settlement"
  - "over skill cap"
effect_tags:
  - "tax"
bonus: 0.005
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "0.5% tax income for each skill point above 200 in the governed settlement"
effect_template: "{VALUE}% tax income for each skill point above 200 in the governed settlement"
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

# Price of Loyalty - governor - settlement economy

0.5% tax income for each skill point above 200 in the governed settlement
