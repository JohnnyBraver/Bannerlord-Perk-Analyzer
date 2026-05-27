---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Roguery"
level: 275
perk: "Rogue Extraordinaire"
perk_string_id: "RogueryRogueExtraordinaire"
effect_slot: "primary"
role: "personal"
role_value: 12
perk_type: "gold economy"
perk_subtype: "loot bonus"
trigger_condition:
  - "over skill cap"
effect_tags:
  - "loot"
bonus: 0.01
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "1% loot amount for every skill point above 200."
effect_template: "{VALUE}% loot amount for every skill point above 200."
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

# Rogue Extraordinaire - personal - gold economy

1% loot amount for every skill point above 200.
