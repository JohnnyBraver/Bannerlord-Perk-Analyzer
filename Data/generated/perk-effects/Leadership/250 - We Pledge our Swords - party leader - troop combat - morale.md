---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 250
perk: "We Pledge our Swords"
perk_string_id: "LeadershipWePledgeOurSwords"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "troop combat"
perk_subtype: "morale"
trigger_condition:
  - "party composition"
effect_tags: []
bonus: 1
increment_type: "add"
increment_value: 0
troop_usage: "all"
troop_usage_value: 65535
effect: "1 battle morale at the beginning of the battle for each tier 6 troop in the party up to 10 morale."
effect_template: "{VALUE} battle morale at the beginning of the battle for each tier 6 troop in the party up to 10 morale."
alternative_perk_string_id: "LeadershipTalentMagnet"
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

# We Pledge our Swords - party leader - troop combat

1 battle morale at the beginning of the battle for each tier 6 troop in the party up to 10 morale.
