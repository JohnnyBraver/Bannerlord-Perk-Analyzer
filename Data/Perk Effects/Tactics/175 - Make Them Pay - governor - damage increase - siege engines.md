---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Tactics"
level: 175
perk: "Make Them Pay"
perk_string_id: "TacticsMakeThemPay"
effect_slot: "secondary"
role: "governor"
role_value: 3
perk_type: "damage increase"
perk_subtype: "siege engines"
trigger_condition:
  - "during siege"
effect_tags: []
bonus: 0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "25% damage to besieging siege engines."
effect_template: "{VALUE}% damage to besieging siege engines."
alternative_perk_string_id: "TacticsPickThemOfTheWalls"
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

# Make Them Pay - governor - damage increase

25% damage to besieging siege engines.
