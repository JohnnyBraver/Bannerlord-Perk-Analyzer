---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 200
perk: "Ransom Broker"
perk_string_id: "RogueryRansomBroker"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "trade penalty reduction"
trigger_condition: []
effect_tags:
  - "ransom"
  - "trade"
bonus: 0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "25% better deals for heroes from ransom brokers."
effect_template: "{VALUE}% better deals for heroes from ransom brokers."
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

# Ransom Broker - party leader - gold economy

25% better deals for heroes from ransom brokers.
