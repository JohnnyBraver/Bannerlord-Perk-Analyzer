---
project: "Bannerlord"
type: "bannerlord_perk_effect"
game_version_target: "1.4.5"
attribute: "Intelligence"
skill: "Steward"
level: 100
perk: "Paid in Promise"
perk_string_id: "StewardPaidInPromise"
effect_slot: "primary"
role: "party leader"
role_value: 5
perk_type: "gold economy"
perk_subtype: "recruitment cost"
trigger_condition: []
effect_tags:
  - "wages"
  - "companions"
bonus: -0.25
increment_type: "add_factor"
increment_value: 1
troop_usage: "all"
troop_usage_value: 65535
effect: "-25% companion wages and recruitment fees."
effect_template: "{VALUE}% companion wages and recruitment fees."
alternative_perk_string_id: "StewardEfficientCampaigner"
source_status: "local_game_assembly"
source: "TaleWorlds.CampaignSystem.dll DefaultPerks.InitializeAll"
source_version: "1.4.5"
needs_review: false
functioning: null
perk_wrong: false
bug_note: ""
notes: ""
classification_review: "Composite effect spans companion wages and recruitment fees; single classification is partial."
---

# Paid in Promise - party leader - gold economy

-25% companion wages and recruitment fees.
