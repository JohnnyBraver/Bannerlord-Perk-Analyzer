---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Riding"
level: 75
perk: "Deeper Sacks"
perk_string_id: "RidingDeeperSacks"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "trade penalty reduction"
trigger_condition: []
effect_tags:
  - "mounts"
  - "trade"
bonus: -0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-10% trade penalty for mounts."
effect_template: "{VALUE}% trade penalty for mounts."
alternative_perk_string_id: "RidingNomadicTraditions"
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

# Deeper Sacks - party leader - gold economy

-10% trade penalty for mounts.
