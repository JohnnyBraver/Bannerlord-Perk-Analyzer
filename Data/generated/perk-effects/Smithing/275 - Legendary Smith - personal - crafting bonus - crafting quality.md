---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Smithing"
level: 275
perk: "Legendary Smith"
perk_string_id: "LegendarySmith"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "crafting bonus"
perk_subtype: "crafting quality"
trigger_condition:
  - "over skill cap"
effect_tags:
  - "weapons"
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "5% greater chance of creating Legendary weapons, chance increases by 1% for every 5 skill points above 275."
effect_template: "{VALUE}% greater chance of creating Legendary weapons, chance increases by 1% for every 5 skill points above 275."
alternative_perk_string_id: ""
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Bonus stores the base +5% Legendary chance; description also includes +1% per 5 Smithing above 275."
classification_review: ""
---

# Legendary Smith - personal - crafting bonus

5% greater chance of creating Legendary weapons, chance increases by 1% for every 5 skill points above 275.
