---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Charm"
level: 150
perk: "Slick Negotiator"
perk_string_id: "CharmSlickNegotiator"
effect_slot: "secondary"
role: "personal"
role_value: 12
perk_type: "gold economy"
perk_subtype: "barter"
trigger_condition:
  - "different culture"
effect_tags: []
bonus: -0.1
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-10% barter penalty with lords of different cultures."
effect_template: "{VALUE}% barter penalty with lords of different cultures."
alternative_perk_string_id: "CharmEffortForThePeople"
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

# Slick Negotiator - personal - gold economy

-10% barter penalty with lords of different cultures.
