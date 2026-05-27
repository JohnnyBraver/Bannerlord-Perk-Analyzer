---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Charm"
level: 225
perk: "Parade"
perk_string_id: "CharmParade"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "settlement governance"
perk_subtype: "loyalty"
trigger_condition:
  - "while waiting"
effect_tags: []
bonus: 5
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "5 loyalty bonus to settlement while waiting in the settlement."
effect_template: "{VALUE} loyalty bonus to settlement while waiting in the settlement."
alternative_perk_string_id: "CharmPublicSpeaker"
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

# Parade - personal - settlement governance

5 loyalty bonus to settlement while waiting in the settlement.
