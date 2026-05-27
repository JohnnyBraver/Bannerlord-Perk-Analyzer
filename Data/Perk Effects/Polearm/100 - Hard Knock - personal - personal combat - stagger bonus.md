---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 100
perk: "Hard Knock"
perk_string_id: "PolearmHardKnock"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "personal combat"
perk_subtype: "stagger bonus"
trigger_condition: []
effect_tags:
  - "weapons"
bonus: 0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "Polearms that can knockdown ignore 25% knockdown resistance on thrust attacks."
effect_template: "Polearms that can knockdown ignore {VALUE}% knockdown resistance on thrust attacks."
alternative_perk_string_id: "PolearmFootwork"
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

# Hard Knock - personal - personal combat

Polearms that can knockdown ignore 25% knockdown resistance on thrust attacks.
