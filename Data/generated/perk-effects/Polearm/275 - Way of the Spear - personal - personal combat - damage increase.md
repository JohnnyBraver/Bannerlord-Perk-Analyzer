---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 275
perk: "Way of the Spear"
perk_string_id: "PolearmWayOfTheSpear"
effect_slot: "secondary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "damage increase"
trigger_condition:
  - "over skill cap"
effect_tags:
  - "weapons"
bonus: 0.005
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "0.5% damage with polearms for every skill point above 250."
effect_template: "{VALUE}% damage with polearms for every skill point above 250."
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

# Way of the Spear - personal - personal combat

0.5% damage with polearms for every skill point above 250.
