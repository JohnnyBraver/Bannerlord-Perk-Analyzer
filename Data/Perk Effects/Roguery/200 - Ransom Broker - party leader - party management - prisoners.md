---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 200
perk: "Ransom Broker"
perk_string_id: "RogueryRansomBroker"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "prisoners"
trigger_condition:
  - "party composition"
effect_tags:
  - "hero prisoners"
  - "prisoner escape"
bonus: -0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-30% escape chance for hero prisoners."
effect_template: "{VALUE}% escape chance for hero prisoners."
alternative_perk_string_id: "RogueryCarver"
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

# Ransom Broker - party leader - party management

-30% escape chance for hero prisoners.
