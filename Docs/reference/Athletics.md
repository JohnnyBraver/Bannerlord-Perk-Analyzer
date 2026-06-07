---
skill: "Athletics"
attribute: "Endurance"
game_version: "1.4.5"
---

# Athletics Perks

| Level | Perk | Slot | Role | Effect | Type | Subtype | Triggers | Tags | Target Version | Curation/Status | ID |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | Morning Exercise | primary | personal | 3% combat movement speed. | personal combat | movement speed |  | combat | 1.4.5 | OK | AthleticsMorningExercise |
| 25 | Morning Exercise | secondary | captain | 5% combat movement speed to troops in your formation. | troop combat | movement speed |  | combat | 1.4.5 | OK | AthleticsMorningExercise |
| 25 | Well Built | primary | personal | 5 hit points. | personal combat | hit points |  |  | 1.4.5 | OK | AthleticsWellBuilt |
| 25 | Well Built | secondary | party leader | 5 hit points to foot troops in your party. | troop combat | hit points | party composition |  | 1.4.5 | OK | AthleticsWellBuilt |
| 50 | Form Fitting Armor | primary | personal | -15% armor weight. | utility |  |  |  | 1.4.5 | Review: Armor-weight reduction has no dedicated taxonomy bucket; utility is a fallback. | AthleticsFormFittingArmor |
| 50 | Form Fitting Armor | secondary | captain | 4% combat movement speed to tier 3+ foot troops in your formation. | troop combat | movement speed | party composition | combat | 1.4.5 | OK | AthleticsFormFittingArmor |
| 50 | Fury | primary | personal | 10% weapon handling while on foot. | personal combat | weapon handling | on foot | weapons | 1.4.5 | OK | AthleticsFury |
| 50 | Fury | secondary | captain | 10% weapon handling to foot troops in your formation. | troop combat | weapon handling | party composition | weapons | 1.4.5 | OK | AthleticsFury |
| 75 | Imposing Stature | primary | personal | 30% persuasion chance. | social | dialog checks |  |  | 1.4.5 | OK | AthleticsImposingStature |
| 75 | Imposing Stature | secondary | party leader | 5 party size. | party management | party size |  |  | 1.4.5 | OK | AthleticsImposingStature |
| 75 | Stamina | primary | personal | 50% crafting stamina recovery rate. | crafting bonus | crafting stamina |  |  | 1.4.5 | OK | AthleticsStamina |
| 75 | Stamina | secondary | party leader | 5 prisoner limit and -10% escape chance to your prisoners. | party management | prisoners |  | prisoner limit, prisoner escape | 1.4.5 | OK; Notes: PerkObject.SecondaryBonus only stores the +5 prisoner limit; the -10% escape factor (-0.1 AddFactor) is hardcoded in ApplyEscapeChanceToExceededPrisoners IL — verified. Applies to over-capacity troop escape only, not hero DailyHeroTick. | AthleticsStamina |
| 100 | Powerful | primary | personal | 4% damage with melee weapons. | personal combat | melee |  | weapons | 1.4.5 | OK | AthleticsPowerful |
| 100 | Powerful | secondary | captain | 2% melee damage by troops in your formation. | troop combat | melee |  |  | 1.4.5 | OK | AthleticsPowerful |
| 100 | Sprint | primary | personal | 5% combat movement speed when you have no shields and no ranged weapons equipped. | personal combat | movement speed |  | shield penalty, weapons, combat | 1.4.5 | OK | AthleticsSprint |
| 100 | Sprint | secondary | captain | 3% combat movement speed to infantry troops in your formation. | troop combat | movement speed | party composition | combat | 1.4.5 | OK | AthleticsSprint |
| 125 | Braced | primary | personal | -40% charge damage taken. | personal combat | charge |  |  | 1.4.5 | OK | AthleticsBraced |
| 125 | Braced | secondary | captain | -30% charge damage taken by troops in your formation. | troop combat | charge |  |  | 1.4.5 | OK | AthleticsBraced |
| 125 | Surging Blow | primary | personal | 30% damage bonus from speed while on foot. | personal combat | speed bonus | on foot |  | 1.4.5 | OK | AthleticsSurgingBlow |
| 125 | Surging Blow | secondary | captain | 30% damage bonus from speed to troops in your formation. | troop combat | speed bonus |  |  | 1.4.5 | OK | AthleticsSurgingBlow |
| 150 | A Good Days Rest | primary | party leader | 10% hit point regeneration while waiting in settlements. | regen bonus |  | while waiting |  | 1.4.5 | OK | AthleticsAGoodDaysRest |
| 150 | A Good Days Rest | secondary | party leader | 10 daily experience to foot troops while waiting in settlements. | party management | troop xp | while waiting, party composition |  | 1.4.5 | OK | AthleticsAGoodDaysRest |
| 150 | Walk It Off | primary | party leader | 10% hit point regeneration while traveling. | regen bonus |  | while traveling |  | 1.4.5 | OK | AthleticsWalkItOff |
| 150 | Walk It Off | secondary | party leader | 3 daily experience to foot troops while traveling. | party management | troop xp | while traveling, party composition |  | 1.4.5 | OK | AthleticsWalkItOff |
| 175 | Durable | primary | personal | 1 Endurance attribute. | character growth | attribute point |  |  | 1.4.5 | OK | AthleticsDurable |
| 175 | Durable | secondary | governor | 1 daily loyalty in the governed settlement. | settlement governance | loyalty | governed settlement |  | 1.4.5 | OK | AthleticsDurable |
| 175 | Energetic | primary | party leader | -20% overburdened speed penalty. | party management | party speed |  | overburden | 1.4.5 | OK | AthleticsEnergetic |
| 175 | Energetic | secondary | governor | 20% hearth growth in villages bound to the governed settlement. | settlement economy | hearth growth | governed settlement | village | 1.4.5 | OK | AthleticsEnergetic |
| 200 | Steady | primary | personal | 1 Control attribute. | character growth | attribute point |  |  | 1.4.5 | OK | AthleticsSteady |
| 200 | Steady | secondary | governor | 10% production in farms, mines, lumber camps and clay pits bound to the governed settlement. | settlement economy | production | governed settlement |  | 1.4.5 | OK | AthleticsSteady |
| 200 | Strong | primary | personal | 1 Vigor attribute. | character growth | attribute point |  |  | 1.4.5 | OK | AthleticsStrong |
| 200 | Strong | secondary | party leader | 5% party speed by foot troops in your party. | party management | party speed | party composition |  | 1.4.5 | OK | AthleticsStrong |
| 225 | Strong Arms | primary | personal | 5% damage with throwing weapons. | personal combat | damage increase |  | weapons | 1.4.5 | OK | AthleticsStrongArms |
| 225 | Strong Arms | secondary | captain | 20 throwing skill to troops in your formation. | troop combat | skill bonus |  | weapons | 1.4.5 | OK | AthleticsStrongArms |
| 225 | Strong Legs | primary | personal | -50% fall damage taken and +100% kick damage dealt. | personal combat | fall |  |  | 1.4.5 | Review: Composite effect spans fall damage reduction and kick damage; subtype captures fall damage only.; Notes: Bonus stores the -50% fall-damage component; +100% kick damage is not represented by the bonus field. | AthleticsStrongLegs |
| 225 | Strong Legs | secondary | governor | -20% food consumption in the governed settlement while under siege. | settlement defense | food consumption | during siege, governed settlement | defense, food | 1.4.5 | OK | AthleticsStrongLegs |
| 250 | Ignore Pain | primary | personal | 10% armor while on foot. | personal combat | armor increase | on foot |  | 1.4.5 | OK | AthleticsIgnorePain |
| 250 | Ignore Pain | secondary | captain | 5 armor to all equipped armor pieces of foot troops in your formation. | troop combat | armor increase | party composition |  | 1.4.5 | OK | AthleticsIgnorePain |
| 250 | Spartan | primary | personal | 50% resistance to getting staggered while on foot. | personal combat | stagger bonus | on foot |  | 1.4.5 | OK | AthleticsSpartan |
| 250 | Spartan | secondary | party leader | -20% food consumption in your party. | party management | food consumption |  | food | 1.4.5 | OK | AthleticsSpartan |
| 275 | Mighty Blow | primary | personal | You stun your enemies longer after they block your attack. | personal combat | stagger bonus |  |  | 1.4.5 | Review: Blocked-attack condition is not represented by current trigger_condition taxonomy.; Notes: Game bonus is +5% longer stun; description has no numeric placeholder. | AthleticsMightyBlow |
| 275 | Mighty Blow | secondary | personal | 1 hit points for every skill point above 250. | personal combat | hit points | over skill cap |  | 1.4.5 | OK | AthleticsMightyBlow |
