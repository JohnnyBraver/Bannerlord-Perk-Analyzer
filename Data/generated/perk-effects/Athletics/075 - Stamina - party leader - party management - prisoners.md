---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 75
perk: "Stamina"
perk_string_id: "AthleticsStamina"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "prisoners"
trigger_condition: []
effect_tags:
  - "prisoner limit"
  - "prisoner escape"
bonus: 5
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "5 prisoner limit and -10% escape chance to your prisoners."
effect_template: "{VALUE} prisoner limit and -10% escape chance to your prisoners."
alternative_perk_string_id: "AthleticsImposingStature"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Bonus stores +5 prisoner limit; -10% escape chance is present in the description but not represented by the bonus field."
classification_review: "Composite effect spans prisoner limit and prisoner escape; single subtype is partial."
---

# Stamina - party leader - party management

5 prisoner limit and -10% escape chance to your prisoners.
