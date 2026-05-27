---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Two Handed"
level: 175
perk: "Terror"
perk_string_id: "TwoHandedTerror"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "troop combat"
perk_subtype: "morale damage"
trigger_condition:
  - "on kill"
effect_tags: []
bonus: 0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "20% battle morale effect to enemy troops with your two handed kills."
effect_template: "{VALUE}% battle morale effect to enemy troops with your two handed kills."
alternative_perk_string_id: "TwoHandedHope"
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

# Terror - personal - troop combat

20% battle morale effect to enemy troops with your two handed kills.
