---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 25
perk: "Combat Tips"
perk_string_id: "LeadershipCombatTips"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "recruitment bonus"
trigger_condition:
  - "same culture"
effect_tags: []
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 to troop tiers when recruiting from same culture."
effect_template: "{VALUE} to troop tiers when recruiting from same culture."
alternative_perk_string_id: "LeadershipRaiseTheMeek"
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

# Combat Tips - party leader - party management

1 to troop tiers when recruiting from same culture.
