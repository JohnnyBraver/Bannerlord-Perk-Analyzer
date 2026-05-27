---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 275
perk: "Price of Loyalty"
perk_string_id: "StewardPriceOfLoyalty"
effect_slot: "primary"
role: "quartermaster"
role_value: 10
perk_type: "troop combat"
perk_subtype: "morale damage"
trigger_condition:
  - "over skill cap"
effect_tags:
  - "combat"
  - "food"
  - "wages"
bonus: -0.005
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-0.5% to food consumption, wages and combat related morale loss for each steward point above 250 in your party."
effect_template: "{VALUE}% to food consumption, wages and combat related morale loss for each steward point above 250 in your party."
alternative_perk_string_id: ""
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Composite effect spans food consumption, wages, and combat morale loss; troop-combat classification captures only the morale-loss component."
---

# Price of Loyalty - quartermaster - troop combat

-0.5% to food consumption, wages and combat related morale loss for each steward point above 250 in your party.
