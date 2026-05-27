---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Vigor"
skill: "Polearm"
level: 200
perk: "Hardy Frontline"
perk_string_id: "PolearmHardyFrontline"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "recruitment cost"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: -0.2
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-20% recruitment cost of infantry."
effect_template: "{VALUE}% recruitment cost of infantry."
alternative_perk_string_id: "PolearmDrills"
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

# Hardy Frontline - party leader - gold economy

-20% recruitment cost of infantry.
