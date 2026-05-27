---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 150
perk: "Smuggler Connections"
perk_string_id: "RoguerySmugglerConnections"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "trade penalty reduction"
trigger_condition: []
effect_tags:
  - "trade"
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% trade penalty when you are trading with a faction you have crime rating against."
effect_template: "{VALUE}% trade penalty when you are trading with a faction you have crime rating against."
alternative_perk_string_id: "RogueryPartnersInCrime"
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

# Smuggler Connections - party leader - gold economy

-50% trade penalty when you are trading with a faction you have crime rating against.
