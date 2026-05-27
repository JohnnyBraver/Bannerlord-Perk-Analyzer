---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Athletics"
level: 225
perk: "Strong Legs"
perk_string_id: "AthleticsStrongLegs"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "fall"
trigger_condition: []
effect_tags: []
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% fall damage taken and +100% kick damage dealt."
effect_template: "{VALUE}% fall damage taken and +100% kick damage dealt."
alternative_perk_string_id: "AthleticsStrongArms"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: "Bonus stores the -50% fall-damage component; +100% kick damage is not represented by the bonus field."
classification_review: "Composite effect spans fall damage reduction and kick damage; subtype captures fall damage only."
---

# Strong Legs - personal - personal combat

-50% fall damage taken and +100% kick damage dealt.
