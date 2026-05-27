---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Social"
skill: "Leadership"
level: 100
perk: "Loyalty and Honor"
perk_string_id: "LeadershipLoyaltyAndHonor"
effect_slot: "secondary"
role: "party leader"
role_value: 5
perk_type: "party management"
perk_subtype: "prisoner recruitment"
trigger_condition:
  - "party composition"
effect_tags:
  - "bandits"
  - "prisoners"
bonus: 0.30000001
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "30% faster non-bandit prisoner recruitment."
effect_template: "{VALUE}% faster non-bandit prisoner recruitment."
alternative_perk_string_id: "LeadershipFamousCommander"
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

# Loyalty and Honor - party leader - party management

30% faster non-bandit prisoner recruitment.
