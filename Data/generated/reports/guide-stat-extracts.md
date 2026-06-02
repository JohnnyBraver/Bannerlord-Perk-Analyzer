# Bannerlord Guide Stat Extracts

Generated: 2026-05-31T18:45:08.771266+03:00

This report collects the perk rows, formulas, and stack definitions behind the manual guide notes. It is meant to make guide updates repeatable: refresh the perk export, re-run this script, and compare the generated stat tables before editing prose.

## Inputs

- Perk export: `Data\export\perk-effects.json`

## Direct Weapon Skill Effects

| Skill | Effects | Per skill point | +30 skill | +80 skill |
| --- | --- | --- | --- | --- |
| One Handed | weapon speed, weapon damage | speed +0.07%, damage +0.15% | speed +2.1%, damage +4.5% | speed +5.6%, damage +12% |
| Two Handed | weapon speed, weapon damage | speed +0.06%, damage +0.16% | speed +1.8%, damage +4.8% | speed +4.8%, damage +12.8% |
| Polearm | weapon speed, weapon damage | speed +0.06%, damage +0.07% | speed +1.8%, damage +2.1% | speed +4.8%, damage +5.6% |
| Bow | damage, accuracy | damage +0.11%, accuracy effect +0.09% | damage +3.3%, accuracy effect +2.7% | damage +8.8%, accuracy effect +7.2% |
| Crossbow | reload speed, accuracy | reload +0.07%, accuracy effect +0.05% | reload +2.1%, accuracy effect +1.5% | reload +5.6%, accuracy effect +4% |
| Throwing | ready speed, damage, accuracy | ready speed +0.07%, damage +0.06%, accuracy effect +0.06% | ready speed +2.1%, damage +1.8%, accuracy effect +1.8% | ready speed +5.6%, damage +4.8%, accuracy effect +4.8% |

Accuracy effects are stored as negative factors in code because they reduce inaccuracy or penalty; this report displays the player-facing positive effect.

## AI Behavior Formulas

| Key | Track | Shape | Formula |
| --- | --- | --- | --- |
| ai_level | base | difficultyFactor = 0.96 | `clamp(effectiveSkill / 300 * difficultyFactor * AILevelMultiplier, 0, 1)` |
| AiShootFreq | ranged | linear | `0.3 + 0.7 * currentAI` |
| AiWaitBeforeShootFactor | ranged | linear reduction | `1 - 0.5 * currentAI` |
| AIBlockOnDecideAbility | melee | diminishing | `lerp(0.5, 0.99, sqrt(meleeAI))` |
| AIParryOnDecideAbility | melee | linear | `lerp(0.5, 0.95, meleeAI)` |
| AIDecideOnRealizeEnemyBlockingAttackAbility | melee | high-skill weighted | `clamp(meleeAI^2.5 - 0.1, 0, 1)` |
| AIRealizeBlockingFromIncorrectSideAbility | melee | high-skill weighted | `clamp(meleeAI^2.5 - 0.01, 0, 1)` |
| AiRandomizedDefendDirectionChance | melee | high-skill mistake reduction | `1 - meleeAI^3` |
| AiUseShieldAgainstEnemyMissileProbability | shield | linear plus defensiveness | `0.1 + 0.6 * meleeAI + 0.2 * (meleeAI + defensiveness)` |

## AI Skill Stacks

| Stack | Total | AI level gain | Components | Note |
| --- | ---: | ---: | --- | --- |
| Foot Polearm Shield Wall | 80 | 0.256 | Clean Thrust (30), Counterweight (20), Phalanx (30) | Strongest clean melee-AI skill stack found so far. |
| Foot One-Handed Shield Wall | 60 | 0.192 | Wrapped Handles (30), Phalanx (30) | Feeds melee reactions and shield AI. |
| Foot Two-Handed Shield Wall | 60 | 0.192 | Strong Grip (30), Phalanx (30) | Offensive melee-AI stack; no shield-specific defensive payoff. |
| Horse Archers | 50 | 0.16 | Dead Aim (20), Horse Master (30) | Improves ranged AI plus bow damage and accuracy. |
| Throwing Infantry | 65 | 0.208 | Flexible Fighter (15), Strong Arms (20), Running Throw (30) | Strong javelin-infantry stack; Flexible Fighter is category-sensitive. |

## Survivability Stacks

### Hit Points

| Stack | Total | Components | Note |
| --- | ---: | --- | --- |
| Any Regular Troop HP | 90 | Minister of Health (80), Hardy Frontline (5), Thick Hides (5) | Baseline broad troop HP stack. |
| Foot Infantry HP | 108 | Minister of Health (80), Hardy Frontline (5), Thick Hides (5), Well Built (5), Unwavering Defense (10), Hard Knock (3) | Largest flat regular troop HP stack from the current guide set. |
| Foot Ranged HP | 100 | Minister of Health (80), Hardy Frontline (5), Thick Hides (5), Well Built (5), Picked Shots (5) | Uses Picked Shots, whose string id is CrossbowBoltenGuard in the extracted data. |
| Troop Mount HP |  | Sledges (15), Veterinary (0.1) | Flat mount HP and percentage mount HP are kept as separate component types. |

### Armor

| Stack | Total | Components | Note |
| --- | ---: | --- | --- |
| Any Troop Armor | 5 | Metallurgy (5) | Broad captain armor layer. |
| Foot Troop Armor | 10 | Metallurgy (5), Ignore Pain (5) | Best foot-troop armor stack in the current guide set. |
| Mounted Rider Armor | 10 | Metallurgy (5), Dauntless Steed (5) | Best rider armor stack for mounted troops. |
| Troop Mount Armor | 10 | Tough Steed (10) | Mount armor, not rider armor. |

### Damage Reduction

| Stack | Total | Components | Note |
| --- | ---: | --- | --- |
| Melee Infantry Vs Projectiles | -8% | Skirmisher (-3%), Elite Reserves (-5%) | Does not include Skirmish Phase Master because that is ranged-troop scoped. |
| Bow Ranged Troops Vs Projectiles | -18% | Skirmish Phase Master (-10%), Skirmisher (-3%), Elite Reserves (-5%) | Counter Fire is not included because the live damage code is crossbow-current-weapon gated. |
| Crossbow Troops Vs Projectiles | -21% | Skirmish Phase Master (-10%), Counter Fire (-3%), Skirmisher (-3%), Elite Reserves (-5%) | Assumes the victim is holding a crossbow for Counter Fire. |
| Charge Damage To Formation | -60% | Braced (-30%), Sure Footed (-30%) | Charge-specific layer. |

## Survival Formulas

| Key | Formula | Notes |
| --- | --- | --- |
| regular_troop_death_chance | `deathChance = 1 / ((1 + medicine * 0.01 * eventMultiplier + troopLevel * 0.02 + additiveBonuses) * (1 + factorBonuses))` | Player map event eventMultiplier is 1.0. Non-player map event eventMultiplier is 0.25. Medicine is capped at 330 for player-facing skill. |
| minister_of_health_max_hp | `maxBonus = max(0, medicineSkill - 250), capped by max skill 330 => +80 HP` |  |

## Smithing Formulas

| Key | Formula |
| --- | --- |
| refining_xp | `round(0.3 * outputMaterialValue * outputCount)` |
| smelting_xp | `round(0.02 * itemValue)` |
| crafting_order_xp | `round(0.1 * itemValue)` |
| free_build_xp | `round(0.02 * itemValue)` |
| crafting_order_base_experience | `0.25 * theoreticalMaxItemMarketValue(requestedDesignItem)` |

## Extracted Perk Buckets

### Smithing And Crafting Perks

Smithing perk effects and crafting-bonus rows.

Rows: 23

| Skill | Level | Perk | Role | Bonus | Scope | Effect |
| --- | ---: | --- | --- | ---: | --- | --- |
| Athletics | 75 | Stamina | personal | 0.5 | all | 50% crafting stamina recovery rate. |
| Smithing | 25 | Efficient Charcoal Maker | personal | 0 | all | You can use a more efficient method of charcoal production that produces three units of charcoal from two units of hardwood. |
| Smithing | 25 | Efficient Iron Maker | personal | 0 | all | You can produce crude iron more efficiently by obtaining three units of crude iron from one unit of iron ore. |
| Smithing | 50 | Curious Smelter | personal | 1 | all | 100% learning rate of new part designs when smelting. |
| Smithing | 50 | Steel Maker | personal | 0 | all | You can refine two units of iron into one unit of steel, and one unit of crude iron as by-product. |
| Smithing | 75 | Curious Smith | personal | 1 | all | 100% learning rate of new part designs when smithing. |
| Smithing | 75 | Steel Maker 2 | personal | 0 | all | You can refine two units of steel into one unit of fine steel, and one unit of crude iron as by-product. |
| Smithing | 100 | Experienced Smith | personal | 0.1 | all | 10% greater chance of creating Fine weapons. |
| Smithing | 100 | Experienced Smith | personal | 2 | all | Successful crafting orders of notables increase your relation by 2 with them. |
| Smithing | 100 | Steel Maker 3 | personal | 0 | all | You can refine two units of fine steel into one unit of Thamaskene steel,{newline}and one unit of crude iron as by-product. |
| Smithing | 100 | Steel Maker 3 | personal | 4 | all | 4 relationships with lords and ladies for successful crafting orders. |
| Smithing | 125 | Practical Refiner | personal | -0.5 | all | -50% stamina spent while refining. |
| Smithing | 125 | Practical Smelter | personal | -0.5 | all | -50% stamina spent while smelting. |
| Smithing | 150 | Controlled Smith | personal | 1 | all | 1 Control attribute. |
| Smithing | 150 | Vigorous Smith | personal | 1 | all | 1 Vigor attribute. |
| Smithing | 175 | Artisan Smith | party leader | -0.5 | all | -50% trade penalty when selling smithing weapons. |
| Smithing | 175 | Practical Smith | personal | -0.5 | all | -50% stamina spent while smithing. |
| Smithing | 200 | Master Smith | personal | 0.075 | all | 7.5% greater chance of creating masterwork weapons. |
| Smithing | 225 | Enduring Smith | personal | 1 | all | 1 Endurance attribute. |
| Smithing | 225 | Fencer Smith | personal | 1 | all | 1 Focus Point to One Handed and Two Handed. |
| Smithing | 250 | Sharpened Edge | personal | 0.02 | all | 2% swing damage of crafted weapons. |
| Smithing | 250 | Sharpened Tip | personal | 0.02 | all | 2% thrust damage of crafted weapons. |
| Smithing | 275 | Legendary Smith | personal | 0.05 | all | 5% greater chance of creating Legendary weapons, chance increases by 1% for every 5 skill points above 275. |

### Troop AI Skill Bonus Perks

Perks that add effective skills to troops and can feed AI formulas when the troop uses that skill.

Rows: 13

| Skill | Level | Perk | Role | Bonus | Scope | Effect |
| --- | ---: | --- | --- | ---: | --- | --- |
| Athletics | 225 | Strong Arms | captain | 20 | thrown_user | 20 throwing skill to troops in your formation. |
| Bow | 25 | Dead Aim | captain | 20 | bow_user | 20 Bow skill to troops in your formation. |
| Bow | 225 | Horse Master | captain | 30 | mounted, bow_user | 30 bow skill to horse archers in your formation |
| Crossbow | 75 | Donkey's Swiftness | captain | 30 | crossbow_user | 30 crossbow skill to troops in your formation. |
| One Handed | 25 | Wrapped Handles | captain | 30 | one_handed_user | 30 one handed skill to infantry troops in your formation. |
| Polearm | 75 | Clean Thrust | captain | 30 | on_foot, polearm_user | 30 polearm skill to infantry in your formation. |
| Polearm | 175 | Phalanx | party leader | 30 | all | 30 melee weapon skills to troops in your party while in shield wall formation. |
| Polearm | 250 | Counterweight | captain | 20 | polearm_user | 20 polearm skill to troops in your formation. |
| Riding | 25 | Nimble Steed | captain | 30 | mounted | 30 riding skill to troops in your formation. |
| Roguery | 175 | One of the Family | party leader | 10 | all | 10 bonus Vigor and Control skills to bandit units in your party |
| Throwing | 50 | Flexible Fighter | captain | 15 | on_foot | 15 Control skills of infantry, 15 Vigor skills of archers in your formation. |
| Throwing | 100 | Running Throw | captain | 30 | thrown_user | 30 throwing skill to troops in your formation. |
| Two Handed | 25 | Strong Grip | captain | 30 | on_foot, two_handed_user | 30 two handed skill to infantry troops in your formation. |

### Troop Armor Perks

Troop- or mount-facing armor perks used by the survivability guide.

Rows: 4

| Skill | Level | Perk | Role | Bonus | Scope | Effect |
| --- | ---: | --- | --- | ---: | --- | --- |
| Athletics | 250 | Ignore Pain | captain | 5 | on_foot | 5 armor to all equipped armor pieces of foot troops in your formation. |
| Engineering | 225 | Metallurgy | captain | 5 | none | 5 armor to all equipped armor pieces of troops in your formation. |
| Riding | 250 | Dauntless Steed | captain | 5 | mounted | 5 armor to all equipped armor pieces of mounted troops in your formation. |
| Riding | 250 | Tough Steed | captain | 10 | mounted | 10 armor to mounts of troops in your formation. |

### Troop Damage Reduction And Shield Perks

Damage-taken, charge, projectile-protection, and shield durability perks.

Rows: 12

| Skill | Level | Perk | Role | Bonus | Scope | Effect |
| --- | ---: | --- | --- | ---: | --- | --- |
| Athletics | 125 | Braced | captain | -0.3 | on_foot | -30% charge damage taken by troops in your formation. |
| Bow | 175 | Skirmish Phase Master | captain | -0.1 | ranged | -10% damage taken from projectiles by ranged troops in your formation. |
| Crossbow | 175 | Counter Fire | captain | -0.03 | none | -3% damage taken from projectiles by your troops. |
| One Handed | 25 | Basher | captain | -0.04 | on_foot | -4% damage taken by infantry while in shield wall formation. |
| One Handed | 125 | Arrow Catcher | captain | 0.01 | shield_user | Larger shield protection area against projectiles for troops in your formation. |
| One Handed | 125 | Shieldwall | captain | 0.01 | shield_user | Larger shield protection area against projectiles to troops in your formation while in shield wall formation. |
| One Handed | 200 | Steel Core Shields | captain | -0.1 | shield_user | -10% damage to shields of infantry troops in your formation. |
| Polearm | 225 | Sure Footed | captain | -0.3 | on_foot | -30% charge damage taken by troops in your formation. |
| Tactics | 25 | Loose Formations | party leader | -0.1 | all | -10% damage to your infantry from ranged troops when troops are sent to confront the enemy. |
| Tactics | 200 | Elite Reserves | party leader | -0.2 | all | -20% less damage to tier 3+ units when troops are sent to confront the enemy. |
| Tactics | 200 | Elite Reserves | captain | -0.05 | none | -5% damage taken by troops in your formation. |
| Throwing | 125 | Skirmisher | captain | -0.03 | none | -3% damage taken by ranged attacks to troops in your formation. |

### Troop Hit Point Perks

Troop- or mount-facing hit point perks used by the survivability guide.

Rows: 9

| Skill | Level | Perk | Role | Bonus | Scope | Effect |
| --- | ---: | --- | --- | ---: | --- | --- |
| Athletics | 25 | Well Built | party leader | 5 | all | 5 hit points to foot troops in your party. |
| Crossbow | 250 | Picked Shots | party leader | 5 | all | 5 hit points to ranged troops in your party. |
| Medicine | 75 | Sledges | party leader | 15 | all | 15 hit points to mounts in your party. |
| Medicine | 275 | Minister of Health | personal | 1 | all | 1 hit point to troops for every skill point above 250. |
| One Handed | 225 | Unwavering Defense | party leader | 10 | all | 10 hit points to infantry in your party. |
| Polearm | 100 | Hard Knock | party leader | 3 | all | 3 hit points to infantry in your party. |
| Polearm | 200 | Hardy Frontline | party leader | 5 | all | 5 hit points to troops in your party. |
| Riding | 50 | Veterinary | party leader | 0.1 | all | 10% hit points to mounts of troops in your party. |
| Two Handed | 200 | Thick Hides | party leader | 5 | all | 5 hit points to troops in your party. |

### Troop XP Perks

Perks that directly mention troop XP or experience gains.

Rows: 36

| Skill | Level | Perk | Role | Bonus | Scope | Effect |
| --- | ---: | --- | --- | ---: | --- | --- |
| Athletics | 150 | A Good Days Rest | party leader | 10 | all | 10 daily experience to foot troops while waiting in settlements. |
| Athletics | 150 | Walk It Off | party leader | 3 | all | 3 daily experience to foot troops while traveling. |
| Bow | 125 | Trainer | party leader | 3 | all | 3 daily experience to archers in your party. |
| Bow | 200 | Bulls Eye | party leader | 0.1 | ranged | 10% bonus experience to ranged troops in your party after every battle. |
| Bow | 200 | Bulls Eye | governor | 3 | all | 3 daily experience to garrison troops in the governed settlement. |
| Crossbow | 100 | Renowned Marksmen | party leader | 2 | all | 2 daily experience to ranged troops in your party. |
| Crossbow | 175 | Mounted Crossbowman | party leader | 0.05 | all | 5% experience gained to ranged troops in your party. |
| Engineering | 200 | Apprenticeship | engineer | 5 | all | 5 experience to troops when a siege engine is built. |
| Leadership | 25 | Combat Tips | party leader | 2 | all | 2 experience per day to all troops in party. |
| Leadership | 25 | Raise The Meek | party leader | 4 | all | 4 experience per day to tier 1 and 2 troops. |
| Leadership | 25 | Raise The Meek | governor | 3 | all | 3 experience per day to each troop in garrison in the governed settlement. |
| Leadership | 100 | Famous Commander | personal | 200 | all | 200 experience to troops on recruitment. |
| Leadership | 125 | Leader of the Masses | party leader | 0.05 | all | 5% experience from battles shared with the troops in your party. |
| Leadership | 175 | Inspiring Leader | captain | 0.05 | none | 5% experience to troops in your formation. |
| Leadership | 200 | Lead by Example | party leader | 0.1 | all | 10% shared experience for cavalry troops. |
| Leadership | 200 | Trusted Commander | party leader | 0.2 | all | 20% experience for troops, when they are sent to confront the enemy. |
| Leadership | 225 | Make a Difference | party leader | 0.1 | all | 10% shared experience for archers. |
| Medicine | 250 | Battle Hardened | surgeon | 25 | all | 25 experience to wounded units at the end of the battle. |
| One Handed | 100 | Trainer | party leader | 0.05 | all | 5% experience to melee troops in your party after every battle. |
| One Handed | 150 | Corps-a-corps | party leader | 0.1 | all | 10% of the total experience gained as a bonus to infantry after battles. |
| One Handed | 150 | Military Tradition | party leader | 2 | all | 2 daily experience to infantry in your party. |
| One Handed | 175 | Lead by example | party leader | 0.05 | all | 5% experience to troops in your party after battle. |
| Polearm | 150 | Guards | governor | 0.2 | all | 20% experience gain to garrisoned cavalry in the governed settlement. |
| Polearm | 200 | Drills | party leader | 0.1 | all | 0.1 bonus daily experience to troops in your party. |
| Roguery | 25 | No Rest for the Wicked | party leader | 0.2 | all | 20% experience gain for bandits in your party. |
| Scouting | 100 | Forced March | party leader | 2 | all | 2 experience per day to all troops while traveling with party morale higher than 75. |
| Scouting | 100 | Unburdened | party leader | 2 | all | 2 experience per day to all troops when traveling while overburdened. |
| Steward | 50 | Drill Sergeant | quartermaster | 2 | all | 2 daily experience to troops in your party. |
| Steward | 50 | Seven Veterans | quartermaster | 4 | all | 4 daily experience for tier 4+ troops in your party. |
| Steward | 100 | Paid in Promise | quartermaster | 0 | all | Discarded armors are donated to troops for increased experience. |
| Steward | 125 | Giving Hands | quartermaster | 0 | all | Discarded weapons are donated to troops for increased experience. |
| Throwing | 125 | Saddlebags | party leader | 1 | all | 1 daily experience to infantry troops in your party. |
| Throwing | 200 | Resourceful | party leader | 0.1 | all | 10% experience from battles to troops in your party equipped with throwing weapons. |
| Two Handed | 75 | Baptised in Blood | personal | 5 | all | 5 experience to infantry in your party for each enemy you kill with a two handed weapon. |
| Two Handed | 75 | Baptised in Blood | party leader | 0.05 | all | 5% experience to melee troops in your party after every battle. |
| Two Handed | 150 | Projectile Deflection | governor | 0.1 | all | 10% experience to garrison troops in the governed settlement. |

## Outputs

- JSON: `Data\generated\guide-stat-extracts.json`
- Report: `Data\generated\reports\guide-stat-extracts.md`
