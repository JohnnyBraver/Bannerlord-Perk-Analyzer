---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 250
perk: "Fleet Footed"
perk_string_id: "RogueryFleetFooted"
effect_slot: "secondary"
role: "personal"
role_value: 12
perk_type: "party management"
perk_subtype: "prisoners"
trigger_condition: []
effect_tags:
  - "prisoner escape"
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% escape chance when imprisoned by mobile parties."
effect_template: "{VALUE}% escape chance when imprisoned by mobile parties."
alternative_perk_string_id: "RogueryDashAndSlash"
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

# Fleet Footed - personal - party management

30% escape chance when imprisoned by mobile parties.
