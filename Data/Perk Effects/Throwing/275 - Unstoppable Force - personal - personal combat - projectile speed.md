---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Throwing"
level: 275
perk: "Unstoppable Force"
perk_string_id: "ThrowingUnstoppableForce"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "projectile speed"
trigger_condition:
  - "over skill cap"
effect_tags:
  - "weapons"
bonus: 0.002
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "0.2% travel speed to your throwing weapons for every skill point above 200."
effect_template: "{VALUE}% travel speed to your throwing weapons for every skill point above 200."
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

# Unstoppable Force - personal - personal combat

0.2% travel speed to your throwing weapons for every skill point above 200.
