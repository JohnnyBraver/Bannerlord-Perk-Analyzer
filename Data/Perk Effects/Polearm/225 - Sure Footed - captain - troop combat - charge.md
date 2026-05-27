---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 225
perk: "Sure Footed"
perk_string_id: "PolearmSureFooted"
effect_slot: "secondary"
role: "captain"
role_value: 13
perk_type: "troop combat"
perk_subtype: "charge"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: -0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "infantry"
troop_usage_value: 1
effect: "-30% charge damage taken by troops in your formation."
effect_template: "{VALUE}% charge damage taken by troops in your formation."
alternative_perk_string_id: "PolearmUnstoppableForce"
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

# Sure Footed - captain - troop combat

-30% charge damage taken by troops in your formation.
