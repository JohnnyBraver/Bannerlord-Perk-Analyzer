---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Control"
skill: "Crossbow"
level: 275
perk: "Mighty Pull"
perk_string_id: "CrossbowMightyPull"
effect_slot: "secondary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "damage increase"
trigger_condition:
  - "over skill cap"
effect_tags: []
bonus: 0.005
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "0.5% damage with crossbows for every skill point above 200."
effect_template: "{VALUE}% damage with crossbows for every skill point above 200."
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

# Mighty Pull - personal - personal combat

0.5% damage with crossbows for every skill point above 200.
