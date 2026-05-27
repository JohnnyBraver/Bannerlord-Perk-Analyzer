---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Endurance"
skill: "Smithing"
level: 175
perk: "Artisan Smith"
perk_string_id: "ArtisanSmith"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "trade penalty reduction"
trigger_condition: []
effect_tags:
  - "weapons"
  - "trade"
bonus: -0.5
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-50% trade penalty when selling smithing weapons."
effect_template: "{VALUE}% trade penalty when selling smithing weapons."
alternative_perk_string_id: "PracticalSmith"
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

# Artisan Smith - party leader - gold economy

-50% trade penalty when selling smithing weapons.
