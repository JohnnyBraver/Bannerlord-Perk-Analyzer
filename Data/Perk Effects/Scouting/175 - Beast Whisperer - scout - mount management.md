---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Cunning"
skill: "Scouting"
level: 175
perk: "Beast Whisperer"
perk_string_id: "ScoutingBeastWhisperer"
effect_slot: "primary"
role: "scout"
role_value: 9
perk_type: "mount management"
perk_subtype: ""
trigger_condition:
  - "while traveling"
  - "terrain"
effect_tags:
  - "mounts"
bonus: 0.05
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "5% chance to find a mount when traveling through steppes and plains."
effect_template: "{VALUE}% chance to find a mount when traveling through steppes and plains."
alternative_perk_string_id: "ScoutingForagers"
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

# Beast Whisperer - scout - mount management

5% chance to find a mount when traveling through steppes and plains.
