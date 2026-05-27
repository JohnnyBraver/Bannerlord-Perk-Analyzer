---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Charm"
level: 225
perk: "Public Speaker"
perk_string_id: "CharmPublicSpeaker"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "social"
perk_subtype: "renown"
trigger_condition:
  - "after battle"
effect_tags: []
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% renown gain from battles."
effect_template: "{VALUE}% renown gain from battles."
alternative_perk_string_id: "CharmParade"
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

# Public Speaker - party leader - social

30% renown gain from battles.
