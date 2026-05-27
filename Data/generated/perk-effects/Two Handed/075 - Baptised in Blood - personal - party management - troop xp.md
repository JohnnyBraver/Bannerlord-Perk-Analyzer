---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Two Handed"
level: 75
perk: "Baptised in Blood"
perk_string_id: "TwoHandedBaptisedInBlood"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "party management"
perk_subtype: "troop xp"
trigger_condition:
  - "party composition"
  - "on kill"
effect_tags:
  - "weapons"
bonus: 5
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "5 experience to infantry in your party for each enemy you kill with a two handed weapon."
effect_template: "{VALUE} experience to infantry in your party for each enemy you kill with a two handed weapon."
alternative_perk_string_id: "TwoHandedShowOfStrength"
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

# Baptised in Blood - personal - party management

5 experience to infantry in your party for each enemy you kill with a two handed weapon.
