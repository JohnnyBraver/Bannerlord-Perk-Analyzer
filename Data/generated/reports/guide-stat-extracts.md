# Bannerlord Guide Stat Extracts

Generated: 2026-06-02T22:16:59.133427+03:00

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

### Captain and Troop Combat Perks

Perks with a Captain role that apply combat stat boosts to the formation.

Rows: 99

| Skill | Level | Perk | Role | Bonus | Scope | Effect |
| --- | ---: | --- | --- | ---: | --- | --- |
| Athletics | 25 | Morning Exercise | captain | 0.05 | on_foot | 5% combat movement speed to troops in your formation. |
| Athletics | 50 | Form Fitting Armor | captain | 0.04 | on_foot | 4% combat movement speed to tier 3+ foot troops in your formation. |
| Athletics | 50 | Fury | captain | 0.1 | on_foot | 10% weapon handling to foot troops in your formation. |
| Athletics | 100 | Powerful | captain | 0.02 | melee | 2% melee damage by troops in your formation. |
| Athletics | 100 | Sprint | captain | 0.03 | on_foot | 3% combat movement speed to infantry troops in your formation. |
| Athletics | 125 | Braced | captain | -0.3 | on_foot | -30% charge damage taken by troops in your formation. |
| Athletics | 125 | Surging Blow | captain | 0.3 | on_foot | 30% damage bonus from speed to troops in your formation. |
| Athletics | 225 | Strong Arms | captain | 20 | thrown_user | 20 throwing skill to troops in your formation. |
| Athletics | 250 | Ignore Pain | captain | 5 | on_foot | 5 armor to all equipped armor pieces of foot troops in your formation. |
| Bow | 25 | Bow Control | captain | 0.05 | bow_user | 5% damage with bows by troops in your formation. |
| Bow | 25 | Dead Aim | captain | 20 | bow_user | 20 Bow skill to troops in your formation. |
| Bow | 50 | Bodkin | captain | 0.05 | bow_user | 5% armor penetration with bows by troops in your formation. |
| Bow | 50 | Nocking Point | captain | 0.03 | bow_user | 3% movement speed to archers in your formation. |
| Bow | 75 | Quick Adjustments | captain | -0.05 | bow_user | -5% accuracy penalty to archers in your formation. |
| Bow | 75 | Rapid Fire | captain | 0.05 | ranged | 5% reload speed to troops in your formation. |
| Bow | 125 | Strong bows | captain | 0.05 | bow_user | 5% damage with bows by tier 3+ troops in your formation. |
| Bow | 175 | Skirmish Phase Master | captain | -0.1 | ranged | -10% damage taken from projectiles by ranged troops in your formation. |
| Bow | 225 | Horse Master | captain | 30 | mounted, bow_user | 30 bow skill to horse archers in your formation |
| Crossbow | 50 | Unhorser | captain | 0.2 | crossbow_user | 20% damage against mounts to crossbow troops in your formation. |
| Crossbow | 50 | Wind Winder | captain | 0.05 | crossbow_user | 5% crossbow reload speed to troops in your formation. |
| Crossbow | 75 | Donkey's Swiftness | captain | 30 | crossbow_user | 30 crossbow skill to troops in your formation. |
| Crossbow | 75 | Sheriff | captain | 0.1 | on_foot | 10% crossbow damage to infantry by troops in your formation. |
| Crossbow | 125 | Puncture | captain | 0.05 | crossbow_user | 5% armor penetration with crossbows by troops in your formation. |
| Crossbow | 150 | Deft Hands | captain | 0.5 | crossbow_user | 50% resistance to getting staggered while reloading crossbows to troops in your formation. |
| Crossbow | 150 | Loose and Move | captain | 0.05 | ranged | 5% movement speed to ranged troops in your formation. |
| Crossbow | 175 | Counter Fire | captain | -0.03 | none | -3% damage taken from projectiles by your troops. |
| Crossbow | 225 | Hammer Bolts | captain | 0.1 | crossbow_user | 10% damage with crossbows by troops in your formation. |
| Crossbow | 250 | Terror | captain | 0.25 | crossbow_user | 25% morale loss to enemy due to crossbow kills by troops in your formation. |
| Engineering | 100 | Dreadful Besieger | captain | 0.05 | crossbow_user | 5% crossbow damage by troops in your formation. |
| Engineering | 100 | Wall Breaker | captain | 0.1 | none | 10% damage dealt to shields by troops in your formation. |
| Engineering | 225 | Improved Tools | captain | 0.05 | melee | 5% melee damage by troops in your formation. |
| Engineering | 225 | Metallurgy | captain | 5 | none | 5 armor to all equipped armor pieces of troops in your formation. |
| Leadership | 75 | Heroic Leader | captain | 0.1 | none | 10% battle morale penalty to enemies when troops in your formation kill an enemy. |
| One Handed | 25 | Basher | captain | -0.04 | on_foot | -4% damage taken by infantry while in shield wall formation. |
| One Handed | 25 | Wrapped Handles | captain | 30 | one_handed_user | 30 one handed skill to infantry troops in your formation. |
| One Handed | 75 | Cavalry | captain | 0.05 | mounted, melee | 5% melee damage by cavalry troops in your formation. |
| One Handed | 75 | Shield Bearer | captain | 0.03 | on_foot | 3% movement speed to infantry in your formation. |
| One Handed | 125 | Arrow Catcher | captain | 0.01 | shield_user | Larger shield protection area against projectiles for troops in your formation. |
| One Handed | 125 | Shieldwall | captain | 0.01 | shield_user | Larger shield protection area against projectiles to troops in your formation while in shield wall formation. |
| One Handed | 200 | Fleet of Foot | captain | 0.04 | on_foot | 4% movement speed to infantry in your formation. |
| One Handed | 200 | Steel Core Shields | captain | -0.1 | shield_user | -10% damage to shields of infantry troops in your formation. |
| One Handed | 225 | Deadly Purpose | captain | 0.1 | on_foot, melee | 10% melee weapon damage by infantry in your formation. |
| Polearm | 25 | Cavalry | captain | 0.02 | mounted | 2% damage by cavalry troops in your formation. |
| Polearm | 25 | Pikeman | captain | 0.02 | on_foot | 2% damage by infantry troops in your formation. |
| Polearm | 50 | Braced | captain | 0.1 | on_foot | 10% damage by infantry in your formation against cavalry. |
| Polearm | 75 | Clean Thrust | captain | 30 | on_foot, polearm_user | 30 polearm skill to infantry in your formation. |
| Polearm | 75 | Swift Swing | captain | 0.02 | on_foot, melee | 2% swing speed to infantry in your formation. |
| Polearm | 100 | Footwork | captain | 0.02 | on_foot | 2% movement speed to infantry in your formation. |
| Polearm | 125 | Lancer | captain | 0.3 | polearm_user | 30% damage bonus from speed with polearms by troops in your formation. |
| Polearm | 125 | Steed Killer | captain | 0.3 | on_foot, polearm_user | 30% damage to mounts with polearms by infantry in your formation. |
| Polearm | 175 | Phalanx | captain | 0.03 | polearm_user | 3% damage with polearms by troops in your formation. |
| Polearm | 175 | Standard Bearer | captain | -0.2 | none | -20% battle morale loss to troops in your formation. |
| Polearm | 225 | Sure Footed | captain | -0.3 | on_foot | -30% charge damage taken by troops in your formation. |
| Polearm | 225 | Unstoppable Force | captain | 0.3 | mounted, polearm_user | 30% damage bonus from speed with polearms to cavalry in your formation. |
| Polearm | 250 | Counterweight | captain | 20 | polearm_user | 20 polearm skill to troops in your formation. |
| Polearm | 250 | Sharpen the Tip | captain | 0.05 | on_foot, melee | 5% damage with thrust attacks by infantry troops in your formation. |
| Riding | 25 | Full Speed | captain | 0.1 | mounted | 10% charge damage dealt by troops in your formation. |
| Riding | 25 | Nimble Steed | captain | 30 | mounted | 30 riding skill to troops in your formation. |
| Riding | 75 | Nomadic Traditions | captain | 0.1 | mounted, melee | 10% melee damage bonus from speed to mounted troops in your formation. |
| Riding | 100 | Sagittarius | captain | -0.15 | mounted, ranged | -15% accuracy penalty to mounted troops in your formation. |
| Riding | 150 | Horse Archer | captain | 0.05 | mounted, bow_user | 5% damage by mounted archers in your formation. |
| Riding | 150 | Mounted Warrior | captain | 0.05 | mounted, melee | 5% mounted melee damage by troops in your formation. |
| Riding | 200 | Annoying Buzz | captain | 0.05 | mounted, ranged | 5% battle morale penalty to enemies with mounted ranged kills by troops in your formation. |
| Riding | 200 | Thunderous Charge | captain | 0.1 | mounted, melee | 10% battle morale penalty to enemies with mounted melee kills by troops in your formation. |
| Riding | 250 | Dauntless Steed | captain | 5 | mounted | 5 armor to all equipped armor pieces of mounted troops in your formation. |
| Riding | 250 | Tough Steed | captain | 10 | mounted | 10 armor to mounts of troops in your formation. |
| Roguery | 150 | Partners in Crime | captain | 0.02 | none | 2% damage by bandit troops in your formation. |
| Roguery | 200 | Carver | captain | 0.02 | one_handed_user | 2% one handed damage by troops under your formation. |
| Roguery | 250 | Dash and Slash | captain | 0.02 | two_handed_user | 2% two handed weapon damage by troops in your formation. |
| Tactics | 25 | Loose Formations | captain | -0.25 | none | -25% morale penalty when troops in your formation use line, loose, circle or scatter formations. |
| Tactics | 25 | Tight Formations | captain | -0.25 | none | -25% morale penalty when troops in your formation use shield wall, square, skein, column formations. |
| Tactics | 50 | Decisive Battle | captain | 0.05 | none | 5% movement speed to troops in your formation in plains, steppes and deserts. |
| Tactics | 50 | Extended Skirmish | captain | 0.02 | none | 2% movement speed to troops in your formation in snowy and forest terrains. |
| Tactics | 75 | Small Unit Tactics | captain | 0.05 | none | 5% movement speed to troops in your formation when there are less than 15 soldiers. |
| Tactics | 100 | Coaching | captain | 0.01 | none | 1% damage by troops in your formation. |
| Tactics | 100 | Law Keeper | captain | 0.04 | none | 4% damage against bandits by troops in your formation. |
| Tactics | 200 | Elite Reserves | captain | -0.05 | none | -5% damage taken by troops in your formation. |
| Tactics | 250 | Gens d'armes | captain | 0.02 | mounted | 2% damage to infantry by cavalry troops in your formation. |
| Throwing | 25 | Quick Draw | captain | 0.1 | thrown_user | 10% draw speed with throwing weapons to troops in your formation. |
| Throwing | 25 | Shield Breaker | captain | 0.08 | thrown_user | 8% damage to shields with throwing weapons by troops in your formation. |
| Throwing | 50 | Flexible Fighter | captain | 15 | on_foot | 15 Control skills of infantry, 15 Vigor skills of archers in your formation. |
| Throwing | 50 | Hunter | captain | 0.08 | thrown_user | 8% damage to mounts with throwing weapons by troops in your formation. |
| Throwing | 75 | Mounted Skirmisher | captain | 0.1 | mounted, thrown_user | 10% damage with throwing weapons by mounted troops in your formation. |
| Throwing | 100 | Knock Off | captain | 0.05 | mounted, thrown_user | 5% throwing weapon damage to cavalry by troops in your formation. |
| Throwing | 100 | Running Throw | captain | 30 | thrown_user | 30 throwing skill to troops in your formation. |
| Throwing | 125 | Skirmisher | captain | -0.03 | none | -3% damage taken by ranged attacks to troops in your formation. |
| Throwing | 200 | Splinters | captain | 0.5 | thrown_user | 50% damage to shields with throwing weapons by troops in your formation. |
| Throwing | 225 | Perfect Technique | captain | 0.1 | thrown_user | 10% travel speed to throwing weapons of troops in your formation. |
| Throwing | 250 | Impale | captain | 0.1 | thrown_user | 10% damage with throwing weapons by troops in your formation. |
| Throwing | 250 | Weak Spot | captain | 0.1 | thrown_user | 10% armor penetration with throwing weapons by troops in your formation. |
| Two Handed | 25 | Strong Grip | captain | 30 | on_foot, two_handed_user | 30 two handed skill to infantry troops in your formation. |
| Two Handed | 25 | Wood Chopper | captain | 0.15 | none | 15% damage against shields by troops in your formation. |
| Two Handed | 50 | Head Basher | captain | 0.02 | on_foot | 2% damage by infantry in your formation. |
| Two Handed | 50 | On the Edge | captain | 0.02 | on_foot, melee | 2% swing speed to infantry in your formation. |
| Two Handed | 100 | Beast Slayer | captain | 0.1 | none | 10% damage to mounts by troops in your formation. |
| Two Handed | 100 | Shield breaker | captain | 0.1 | none | 10% damage against shields by troops in your formation. |
| Two Handed | 200 | Reckless Charge | captain | 0.02 | on_foot | 2% damage and movement speed to infantry in your formation. |
| Two Handed | 225 | Blade Master | captain | 0.02 | on_foot | 2% attack speed to infantry in your formation. |
| Two Handed | 225 | Vandal | captain | 0.2 | on_foot | 20% damage against destructible objects by troops in your formation. |

### Governor and Settlement Governance Perks

Perks that apply to a Governor role for governing fiefs, settlements, and castles.

Rows: 108

| Skill | Level | Perk | Role | Bonus | Scope | Effect |
| --- | ---: | --- | --- | ---: | --- | --- |
| Athletics | 175 | Durable | governor | 1 | all | 1 daily loyalty in the governed settlement. |
| Athletics | 175 | Energetic | governor | 0.2 | all | 20% hearth growth in villages bound to the governed settlement. |
| Athletics | 200 | Steady | governor | 0.1 | all | 10% production in farms, mines, lumber camps and clay pits bound to the governed settlement. |
| Athletics | 225 | Strong Legs | governor | -0.2 | all | -20% food consumption in the governed settlement while under siege. |
| Bow | 100 | Merry Men | governor | 1 | all | 1 militia recruitment in the governed settlement. |
| Bow | 100 | Mounted Archery | governor | 0.2 | all | 20% security provided by archers in the governed settlement. |
| Bow | 150 | Discipline | governor | 1 | all | 1 loyalty per day in the governed settlement. |
| Bow | 150 | Hunter Clan | governor | -0.15 | all | -15% garrison wages in the governed castle. |
| Bow | 200 | Bulls Eye | governor | 3 | all | 3 daily experience to garrison troops in the governed settlement. |
| Bow | 250 | Quick Draw | governor | 0.05 | all | 5% tax gain in the governed settlement. |
| Bow | 250 | Ranger's Swiftness | governor | 0.2 | all | 20% security provided by archers in the governed settlement. |
| Charm | 25 | Virile | governor | 0.1 | all | 10% daily chance to get +1 relation with a random notable in the governed settlement while a continuous project is active. |
| Charm | 75 | Meaningful Favors | governor | 0.05 | all | 5% daily chance to increase relations with powerful notables in the governed settlement. |
| Charm | 100 | In Bloom | governor | 0.02 | all | 2% daily chance to increase relations with a random notable of opposed sex in the governed settlement. |
| Charm | 100 | Young And Respectful | governor | 0.02 | all | 2% daily chance to increase relations with a random notable of same sex in the governed settlement. |
| Charm | 200 | Moral Leader | governor | 1 | all | 1 relation with settlement notables when a project is completed in the governed settlement. |
| Charm | 225 | Public Speaker | governor | 0.1 | all | 10% effect from forums, marketplaces and festivals. |
| Crossbow | 100 | Peasant Leader | governor | -0.2 | all | -20% garrisoned ranged troop wages in the governed settlement. |
| Crossbow | 100 | Renowned Marksmen | governor | 0.3 | all | 30% security provided by ranged troops in the garrison of the governed settlement. |
| Crossbow | 200 | Long Shots | governor | 1 | all | 1 daily militia recruitment in the governed settlement. |
| Crossbow | 200 | Steady | governor | 0.05 | all | 5% tariff gain in the governed settlement. |
| Crossbow | 225 | Pavise | governor | 0.3 | all | 30% accuracy to ballistas in the governed settlement. |
| Engineering | 50 | Dungeon Architect | governor | -0.25 | all | -25% escape chance to prisoners in dungeons of governed settlements. |
| Engineering | 50 | Siegeworks | governor | 1 | all | 1 prebuilt catapult to the settlement when a siege starts in the governed settlement. |
| Engineering | 75 | Carpenters | governor | 0.12 | all | 12% build speed for projects in the governed town. |
| Engineering | 75 | Military Planner | governor | 0.25 | all | 25% build speed for projects in the governed castle. |
| Engineering | 100 | Dreadful Besieger | governor | 0.1 | all | 10% accuracy to your siege engines during siege bombardments in the governed settlement. |
| Engineering | 125 | Foreman | governor | 100 | all | 100 prosperity when a project is finished in the governed settlement. |
| Engineering | 125 | Salvager | governor | 0.001 | all | 0.1% siege engine build speed increase for each militia. |
| Engineering | 150 | Siege Engineer | governor | 0.3 | all | 30% hit points to defensive siege engines in the governed settlement. |
| Engineering | 150 | Stonecutters | governor | 0.3 | all | 30% build speed for fortifications, aqueducts and barrack projects in the governed settlement. |
| Engineering | 175 | Battlements | governor | 100 | all | 100 maximum food reserve limits in the governed settlement. |
| Engineering | 200 | Apprenticeship | governor | 0.01 | all | 1% prosperity gain for each unique project in the governed settlement. |
| Engineering | 200 | Engineering Guilds | governor | 0.25 | all | 25% wall hit points in the governed settlement. |
| Engineering | 250 | Architectural Commissions | governor | 20 | all | 20 gold per day for continuous projects in the governed settlement. |
| Engineering | 250 | Clockwork | governor | 0.2 | all | 20% effect from boosting projects in the governed town. |
| Leadership | 25 | Raise The Meek | governor | 3 | all | 3 experience per day to each troop in garrison in the governed settlement. |
| Leadership | 75 | Authority | governor | 0.2 | all | 20% security bonus from the town garrison in the governing settlement. |
| Leadership | 75 | Heroic Leader | governor | 1 | all | 1 daily loyalty in the governed settlement. |
| Leadership | 150 | Citizen Militia | governor | 0.2 | all | 20% rate of militias will spawn as veteran troops in the governed settlement. |
| Leadership | 150 | Veteran's Respect | governor | 20 | all | 20 garrison size in the governed settlement. |
| Medicine | 50 | Triage Tent | governor | -0.05 | all | -5% food consumption for besieged governed settlement. |
| Medicine | 150 | Bush Doctor | governor | 0.2 | all | 20% hearth growth in villages bound to the governed settlement. |
| Medicine | 150 | Pristine Streets | governor | 1 | all | 1 settlement prosperity every day in governed settlements. |
| Medicine | 175 | Perfect Health | governor | 0.1 | all | 10% animal production rate in villages bound to the governed settlement. |
| Medicine | 200 | Clean Infrastructure | governor | 1 | all | 1 prosperity bonus from civilian projects in the governed settlement. |
| Medicine | 200 | Clean Infrastructure | governor | 0.3 | all | 30% recovery rate from raids in villages bound to the governed settlement. |
| Medicine | 200 | Physician of People | governor | 1 | all | 1 loyalty per day in the governed settlement. |
| Medicine | 250 | Battle Hardened | governor | -0.25 | all | -25% siege attrition loss in the governed settlement. |
| Medicine | 250 | Helping Hands | governor | -0.5 | all | -50% prosperity loss from starvation. |
| One Handed | 50 | Swift Strike | governor | 1 | all | 1 daily militia recruitment in the governed settlement. |
| One Handed | 50 | To Be Blunt | governor | 0.5 | all | 0.5 daily security to governed settlement. |
| One Handed | 150 | Corps-a-corps | governor | 30 | all | 30 garrison limit in the governed settlement. |
| One Handed | 150 | Military Tradition | governor | -0.05 | all | -5% garrison wages in the governed settlement. |
| One Handed | 175 | Stand United | governor | 0.3 | all | 30% security provided by troops in the garrison of the governed settlement. |
| Polearm | 50 | Keep at Bay | governor | 1 | all | 1 militia recruitment in the governed settlement. |
| Polearm | 150 | Guards | governor | 0.2 | all | 20% experience gain to garrisoned cavalry in the governed settlement. |
| Polearm | 150 | Skewer | governor | 1 | all | 1 daily security in the governed settlement. |
| Polearm | 175 | Standard Bearer | governor | -0.2 | all | -20% wages to garrisoned infantry in the governed settlement. |
| Polearm | 200 | Drills | governor | 1 | all | 100% rate of militias will spawn as veteran troops in the governed settlement. |
| Riding | 50 | Well Strapped | governor | 0.5 | all | 0.5 daily loyalty to the governed settlement. |
| Riding | 125 | Relief Force | governor | 0.2 | all | 20% security provided by mounted troops in the governed settlement. |
| Riding | 175 | Breeder | governor | 0.05 | all | 5% production rate to villages bound to the governed settlement. |
| Riding | 175 | Shepherd | governor | 0.15 | all | 15% chance of producing tier 2 horses in villages bound to the governed settlement. |
| Riding | 225 | Cavalry Tactics | governor | -0.5 | all | -50% wages of mounted troops in the governed settlement. |
| Riding | 225 | Mounted Patrols | governor | -0.5 | all | -50% escape chance to prisoners in the governed settlement. |
| Roguery | 25 | Sweet Talker | governor | -0.2 | all | -20% prisoner escape chance in the governed settlement. |
| Roguery | 75 | Know-How | governor | 1 | all | 1 security per day in the governed settlement. |
| Roguery | 125 | Scarface | governor | 0.05 | all | 5% chance per day to increase relation with a notable by 1 in the governed settlement. |
| Roguery | 125 | White Lies | governor | 0.02 | all | 2% chance to get 1 relation per day with a random notable in the governed settlement. |
| Roguery | 175 | One of the Family | governor | 1 | all | 1 recruitment slot when recruiting from gang leaders. |
| Roguery | 175 | Salt the Earth | governor | 0.05 | all | 5% tariff revenue in the governed settlement. |
| Roguery | 225 | Arms Dealer | governor | 2 | all | 200% militia per day in the besieged governed settlement. |
| Roguery | 225 | Dirty Fighting | governor | 2 | all | 2 random food item will be smuggled to the besieged governed settlement. |
| Scouting | 75 | Desert Born | governor | 0.025 | all | 2.5% tax income from the governed settlement. |
| Scouting | 75 | Forest Kin | governor | 0.1 | all | 10% tax income from villages bound to the governed settlement. |
| Scouting | 200 | Village Network | governor | 0.1 | all | 10% villager party size of villages bound to the governed settlement. |
| Steward | 50 | Drill Sergeant | governor | -0.05 | all | -5% garrison wages in the governed settlement. |
| Steward | 50 | Seven Veterans | governor | 0.1 | all | 10% rate of militias will spawn as veteran troops in the governed settlement. |
| Steward | 75 | Stiff Upper Lip | governor | -0.2 | all | -20% garrison wages in the governed castle. |
| Steward | 125 | Giving Hands | governor | 0.1 | all | 10% tariff income in the governed settlement. |
| Steward | 125 | Logistician | governor | 0.1 | all | 10% tax income. |
| Steward | 150 | Aid Corps | governor | 0.2 | all | 20% hearth growth in villages bound to the governed settlement. |
| Steward | 150 | Relocation | governor | 0.2 | all | 20% effect from boosting projects in the governed settlement. |
| Steward | 175 | Gourmet | governor | -0.1 | all | -10% garrison food consumption during sieges in the governed settlement. |
| Steward | 200 | Contractors | governor | 0.1 | all | 10% town project effects in the governed settlement. |
| Steward | 200 | Forced Labor | governor | 0.01 | all | 1% construction speed per every 3 prisoners. |
| Steward | 250 | Master of Planning | governor | 0.2 | all | 20% effectiveness to continuous projects in the governed settlement. |
| Steward | 250 | Master of Warcraft | governor | -0.05 | all | -5% food consumption of town population in the governed settlement. |
| Steward | 275 | Price of Loyalty | governor | 0.005 | all | 0.5% tax income for each skill point above 200 in the governed settlement |
| Tactics | 150 | On The March | governor | 0.2 | all | 20% fortification bonus to the governed settlement |
| Tactics | 175 | Make Them Pay | governor | 0.25 | all | 25% damage to besieging siege engines. |
| Tactics | 175 | Pick Them Off The Walls | governor | 0.25 | all | 25% chance for dealing double damage to besieging troops in siege bombardment of the governed settlement. |
| Tactics | 250 | Gens d'armes | governor | 1 | all | 1 daily security in the governed settlement. |
| Throwing | 150 | Focus | governor | 1 | all | 1 daily security in the governed settlement. |
| Throwing | 175 | Slinging Competitions | governor | 1 | all | 1 militia recruitment in the governed settlement. |
| Trade | 100 | Toll Gates | governor | 30 | all | 30 gold for each caravan visiting the governed settlement. |
| Trade | 100 | Traveling Rumors | governor | 20 | all | 20 gold for each villager party visiting the governed settlement. |
| Trade | 150 | Content Trades | governor | 0.1 | all | 10% tariff income in the governed settlement. |
| Trade | 150 | Mercenary Connections | governor | 0.25 | all | 25% workshop production rate. |
| Trade | 200 | Granary Accountant | governor | 0.2 | all | 20% production rate to grain, olives, fish, date in villages bound to the governed settlement. |
| Trade | 200 | Tradeyard Foreman | governor | 0.2 | all | 20% production rate to clay, iron, silk and silver in villages bound to the governed settlement. |
| Trade | 225 | Self-made Man | governor | 0.3 | all | 30% build speed for marketplace, kiln and aqueduct projects. |
| Trade | 250 | Spring of Gold | governor | 0.2 | all | 20% effect from boosting projects in the governed settlement. |
| Trade | 275 | Trickle Down | governor | 2 | all | 2 daily prosperity while building a project in the governed settlement. |
| Two Handed | 125 | Berserker | governor | -0.1 | all | -10% garrison wages in the governed settlement. |
| Two Handed | 125 | Confidence | governor | 0.3 | all | 30% build speed to military projects in the governed settlement. |
| Two Handed | 150 | Projectile Deflection | governor | 0.1 | all | 10% experience to garrison troops in the governed settlement. |

### Medicine and Healing Rate Perks

Perks from the Medicine skill or perks that boost healing rate/survival factors.

Rows: 45

| Skill | Level | Perk | Role | Bonus | Scope | Effect |
| --- | ---: | --- | --- | ---: | --- | --- |
| Athletics | 150 | A Good Days Rest | party leader | 0.1 | all | 10% hit point regeneration while waiting in settlements. |
| Athletics | 150 | Walk It Off | party leader | 0.1 | all | 10% hit point regeneration while traveling. |
| Medicine | 25 | Preventive Medicine | personal | 5 | all | 5 hit points. |
| Medicine | 25 | Preventive Medicine | personal | 0.3 | all | 30% recovery of lost hit points after each battle. |
| Medicine | 25 | Self Medication | personal | 0.3 | all | 30% healing rate. |
| Medicine | 25 | Self Medication | personal | 0.02 | all | 2% combat movement speed. |
| Medicine | 50 | Triage Tent | surgeon | 0.3 | all | 30% healing rate when stationary on the campaign map. |
| Medicine | 50 | Triage Tent | governor | -0.05 | all | -5% food consumption for besieged governed settlement. |
| Medicine | 50 | Walk It Off | surgeon | 0.15 | all | 15% healing rate when moving on the campaign map. |
| Medicine | 50 | Walk It Off | personal | 10 | all | 10 hit points recovery after each offensive battle. |
| Medicine | 75 | Doctor's Oath | surgeon | 0 | all | Your medicine skill partially applies to enemy casualties, increasing potential prisoners. |
| Medicine | 75 | Doctor's Oath | personal | 5 | all | 5 hit points. |
| Medicine | 75 | Sledges | surgeon | -0.5 | all | -50% party speed penalty from the wounded. |
| Medicine | 75 | Sledges | party leader | 15 | all | 15 hit points to mounts in your party. |
| Medicine | 100 | Best Medicine | surgeon | 0.15 | all | 15% healing rate while party morale is above 70. |
| Medicine | 100 | Best Medicine | personal | 1 | all | 1 relationship per day with a random notable over age 40 when party is in a town. |
| Medicine | 100 | Good Lodging | surgeon | 0.2 | all | 20% healing rate while resting in settlements. |
| Medicine | 100 | Good Lodging | personal | 1 | all | 1 relationship per day with a random noble over age 40 when party is in a town. |
| Medicine | 125 | Siege Medic | surgeon | 0.5 | all | 50% chance of troops getting wounded instead of getting killed during siege bombardment. |
| Medicine | 125 | Siege Medic | surgeon | 0.3 | all | 30% chance to recover from lethal wounds during siege bombardment. |
| Medicine | 125 | Veterinarian | surgeon | 0.3 | all | 30% daily chance to recover a lame horse. |
| Medicine | 125 | Veterinarian | surgeon | 0.5 | all | 50% chance to recover mounts of dead cavalry troops in battles. |
| Medicine | 150 | Bush Doctor | governor | 0.2 | all | 20% hearth growth in villages bound to the governed settlement. |
| Medicine | 150 | Bush Doctor | surgeon | 0.2 | all | 20% party healing rate while waiting in villages. |
| Medicine | 150 | Pristine Streets | governor | 1 | all | 1 settlement prosperity every day in governed settlements. |
| Medicine | 150 | Pristine Streets | surgeon | 0.2 | all | 20% party healing rate while waiting in towns. |
| Medicine | 175 | Health Advice | clan leader | 0 | all | Chance of recovery from death due to old age for every clan member. |
| Medicine | 175 | Health Advice | surgeon | 0 | all | Wounded troops do not decrease morale in battles. |
| Medicine | 175 | Perfect Health | surgeon | 0.05 | all | 5% recovery rate for each type of food in party inventory. |
| Medicine | 175 | Perfect Health | governor | 0.1 | all | 10% animal production rate in villages bound to the governed settlement. |
| Medicine | 200 | Clean Infrastructure | governor | 1 | all | 1 prosperity bonus from civilian projects in the governed settlement. |
| Medicine | 200 | Clean Infrastructure | governor | 0.3 | all | 30% recovery rate from raids in villages bound to the governed settlement. |
| Medicine | 200 | Physician of People | governor | 1 | all | 1 loyalty per day in the governed settlement. |
| Medicine | 200 | Physician of People | surgeon | 0.3 | all | 30% chance to recover from lethal wounds for tier 1 and 2 troops |
| Medicine | 225 | Cheat Death | personal | 0 | all | Cheat death due to old age once. |
| Medicine | 225 | Cheat Death | surgeon | -0.5 | all | -50% chance to die when you fall unconscious in battle. |
| Medicine | 225 | Fortitude Tonic | party leader | 10 | all | 10 hit points to other heroes in your party. |
| Medicine | 225 | Fortitude Tonic | personal | 5 | all | 5 hit points. |
| Medicine | 250 | Battle Hardened | surgeon | 25 | all | 25 experience to wounded units at the end of the battle. |
| Medicine | 250 | Battle Hardened | governor | -0.25 | all | -25% siege attrition loss in the governed settlement. |
| Medicine | 250 | Helping Hands | surgeon | 0.02 | all | 2% troop recovery rate for every 10 troop in your party. |
| Medicine | 250 | Helping Hands | governor | -0.5 | all | -50% prosperity loss from starvation. |
| Medicine | 275 | Minister of Health | personal | 1 | all | 1 hit point to troops for every skill point above 250. |
| Roguery | 75 | In Best Light | clan leader | 0.2 | all | 20% faster recovery from raids for your villages. |
| Scouting | 250 | Rearguard | party leader | 0.2 | all | 20% wounded troop recovery speed while in an army. |

### Party Leader and Quartermaster Perks

Perks that apply to a Party Leader or Quartermaster role to manage party size, speed, wages, and limits.

Rows: 183

| Skill | Level | Perk | Role | Bonus | Scope | Effect |
| --- | ---: | --- | --- | ---: | --- | --- |
| Athletics | 25 | Well Built | party leader | 5 | all | 5 hit points to foot troops in your party. |
| Athletics | 75 | Imposing Stature | party leader | 5 | all | 5 party size. |
| Athletics | 75 | Stamina | party leader | 5 | all | 5 prisoner limit and -10% escape chance to your prisoners. |
| Athletics | 150 | A Good Days Rest | party leader | 0.1 | all | 10% hit point regeneration while waiting in settlements. |
| Athletics | 150 | A Good Days Rest | party leader | 10 | all | 10 daily experience to foot troops while waiting in settlements. |
| Athletics | 150 | Walk It Off | party leader | 0.1 | all | 10% hit point regeneration while traveling. |
| Athletics | 150 | Walk It Off | party leader | 3 | all | 3 daily experience to foot troops while traveling. |
| Athletics | 175 | Energetic | party leader | -0.2 | all | -20% overburdened speed penalty. |
| Athletics | 200 | Strong | party leader | 0.05 | all | 5% party speed by foot troops in your party. |
| Athletics | 250 | Spartan | party leader | -0.2 | all | -20% food consumption in your party. |
| Bow | 100 | Merry Men | party leader | 5 | all | 5 party size. |
| Bow | 125 | Trainer | party leader | 6 | all | Daily Bow skill experience bonus to the party member with the lowest bow skill. |
| Bow | 125 | Trainer | party leader | 3 | all | 3 daily experience to archers in your party. |
| Bow | 175 | Eagle Eye | party leader | 0.1 | all | 10% visual range on the campaign map. |
| Bow | 200 | Bulls Eye | party leader | 0.1 | ranged | 10% bonus experience to ranged troops in your party after every battle. |
| Bow | 200 | Renowned Archer | party leader | 0.1 | all | 10% starting battle morale to ranged troops in your party. |
| Bow | 200 | Renowned Archer | party leader | -0.3 | all | -30% recruitment and upgrade cost to ranged troops. |
| Bow | 225 | Deep Quivers | party leader | 1 | all | 1 extra arrow per quiver to troops in your party. |
| Charm | 25 | Self Promoter | party leader | 1 | all | 1 morale while defending in a besieged settlement. |
| Charm | 50 | Oratory | party leader | 1 | all | 1 relationship with a random notable of your kingdom when an enemy lord is defeated. |
| Charm | 50 | Warlord | party leader | 1 | all | 1 relationship with a random lord of your kingdom when an enemy lord is defeated. |
| Charm | 125 | Firebrand | party leader | 1 | all | 1 recruitment slot from rural notables. |
| Charm | 225 | Parade | party leader | 0.05 | all | 5% daily chance to gain +1 relationship with a random lord in the same army. |
| Charm | 225 | Public Speaker | party leader | 0.3 | all | 30% renown gain from battles. |
| Crossbow | 25 | Marksmen | party leader | 0.1 | all | 10% starting battle morale to ranged troops in your party. |
| Crossbow | 25 | Piercer | party leader | -0.2 | all | -20% recruitment cost of ranged troops. |
| Crossbow | 100 | Peasant Leader | party leader | 0.1 | all | 10% battle morale to tier 1 to 3 troops |
| Crossbow | 100 | Renowned Marksmen | party leader | 2 | all | 2 daily experience to ranged troops in your party. |
| Crossbow | 125 | Fletcher | party leader | 2 | all | 2 bolts per quiver to troops in your party. |
| Crossbow | 175 | Mounted Crossbowman | party leader | 0.05 | all | 5% experience gained to ranged troops in your party. |
| Crossbow | 250 | Picked Shots | party leader | -0.5 | all | -50% wages of tier 4+ ranged troops. |
| Crossbow | 250 | Picked Shots | party leader | 5 | all | 5 hit points to ranged troops in your party. |
| Crossbow | 250 | Terror | party leader | 0.2 | all | 20% chance of increasing the siege bombardment casualties per hit by 1. |
| Leadership | 25 | Combat Tips | party leader | 2 | all | 2 experience per day to all troops in party. |
| Leadership | 25 | Combat Tips | party leader | 1 | all | 1 to troop tiers when recruiting from same culture. |
| Leadership | 25 | Raise The Meek | party leader | 4 | all | 4 experience per day to tier 1 and 2 troops. |
| Leadership | 50 | Fervent Attacker | party leader | 4 | all | 4 starting battle morale when attacking. |
| Leadership | 50 | Fervent Attacker | party leader | 0.5 | all | 50% recruitment rate of tier 1, 2 and 3 prisoners. |
| Leadership | 50 | Stout Defender | party leader | 8 | all | 8 starting battle morale when defending. |
| Leadership | 50 | Stout Defender | party leader | 0.5 | all | 50% recruitment rate of tier 4+ prisoners. |
| Leadership | 75 | Authority | party leader | 5 | all | 5 party size limit. |
| Leadership | 100 | Loyalty and Honor | party leader | 3 | all | Tier 3+ troops in your party no longer retreat due to low morale |
| Leadership | 100 | Loyalty and Honor | party leader | 0.3 | all | 30% faster non-bandit prisoner recruitment. |
| Leadership | 125 | Leader of the Masses | party leader | 0.05 | all | 5% experience from battles shared with the troops in your party. |
| Leadership | 125 | Presence | party leader | 0 | all | No morale penalty for recruiting prisoners of your faction. |
| Leadership | 150 | Citizen Militia | party leader | 0.1 | all | 10% morale from victories. |
| Leadership | 150 | Veteran's Respect | party leader | 0 | all | Bandits can be converted into regular troops. |
| Leadership | 175 | Uplifting Spirit | party leader | 10 | all | 10 battle morale in siege battles. |
| Leadership | 175 | Uplifting Spirit | party leader | 10 | all | 10 party size limit. |
| Leadership | 200 | Lead by Example | party leader | 0.5 | all | 50% recruitment rate for infantry prisoners. |
| Leadership | 200 | Lead by Example | party leader | 0.1 | all | 10% shared experience for cavalry troops. |
| Leadership | 200 | Trusted Commander | party leader | 0.5 | all | 50% recruitment rate for ranged prisoners. |
| Leadership | 200 | Trusted Commander | party leader | 0.2 | all | 20% experience for troops, when they are sent to confront the enemy. |
| Leadership | 225 | Great Leader | party leader | 5 | all | 5 battle morale to troops that are of same culture as you. |
| Leadership | 225 | Make a Difference | party leader | 0.1 | all | 10% shared experience for archers. |
| Leadership | 250 | Talent Magnet | party leader | 10 | all | 10 party size limit. |
| Leadership | 250 | We Pledge our Swords | party leader | 1 | all | 1 battle morale at the beginning of the battle for each tier 6 troop in the party up to 10 morale. |
| Leadership | 275 | Ultimate Leader | party leader | 1 | all | 1 party size for each leadership point above 250. |
| Medicine | 75 | Sledges | party leader | 15 | all | 15 hit points to mounts in your party. |
| Medicine | 225 | Fortitude Tonic | party leader | 10 | all | 10 hit points to other heroes in your party. |
| One Handed | 100 | Trainer | party leader | 0.05 | all | 5% experience to melee troops in your party after every battle. |
| One Handed | 150 | Corps-a-corps | party leader | 0.1 | all | 10% of the total experience gained as a bonus to infantry after battles. |
| One Handed | 150 | Military Tradition | party leader | 2 | all | 2 daily experience to infantry in your party. |
| One Handed | 175 | Lead by example | party leader | 0.05 | all | 5% experience to troops in your party after battle. |
| One Handed | 175 | Lead by example | party leader | 5 | all | 5 starting battle morale to troops in your party. |
| One Handed | 175 | Stand United | party leader | 8 | all | 8 starting battle morale to troops in your party if you are outnumbered. |
| One Handed | 225 | Unwavering Defense | party leader | 10 | all | 10 hit points to infantry in your party. |
| One Handed | 250 | Chink in the Armor | party leader | -0.2 | all | -20% recruitment cost of infantry. |
| One Handed | 250 | Prestige | party leader | 15 | all | 15 party limit. |
| Polearm | 100 | Hard Knock | party leader | 3 | all | 3 hit points to infantry in your party. |
| Polearm | 175 | Phalanx | party leader | 30 | all | 30 melee weapon skills to troops in your party while in shield wall formation. |
| Polearm | 200 | Drills | party leader | 0.1 | all | 0.1 bonus daily experience to troops in your party. |
| Polearm | 200 | Hardy Frontline | party leader | 5 | all | 5 hit points to troops in your party. |
| Polearm | 200 | Hardy Frontline | party leader | -0.2 | all | -20% recruitment cost of infantry. |
| Riding | 50 | Veterinary | party leader | 0.1 | all | 10% hit points to mounts of troops in your party. |
| Riding | 75 | Deeper Sacks | party leader | 0.2 | all | 20% carrying capacity for pack animals in your party. |
| Riding | 75 | Deeper Sacks | party leader | -0.1 | all | -10% trade penalty for mounts. |
| Riding | 75 | Nomadic Traditions | party leader | 0.3 | all | 30% party speed bonus from footmen on horses. |
| Riding | 100 | Sweeping Wind | party leader | 0.02 | all | 2% party speed. |
| Riding | 125 | Relief Force | party leader | 10 | all | 10 starting battle morale when you join an ongoing battle of your allies. |
| Riding | 175 | Breeder | party leader | 0.01 | all | 1% daily chance of animals in your party reproducing. |
| Riding | 175 | Shepherd | party leader | -0.5 | all | -50% herding speed penalty. |
| Riding | 225 | Mounted Patrols | party leader | -0.5 | all | -50% escape chance to prisoners in your party. |
| Roguery | 25 | No Rest for the Wicked | party leader | 0.2 | all | 20% experience gain for bandits in your party. |
| Roguery | 25 | No Rest for the Wicked | party leader | 0.05 | all | 5% raid speed. |
| Roguery | 25 | Sweet Talker | party leader | 0.2 | all | 20% chance for convincing bandits to leave in peace with barter. |
| Roguery | 50 | Two Faced | party leader | 0 | all | No morale loss from converting bandit prisoners. |
| Roguery | 75 | In Best Light | party leader | 1 | all | 1 extra troop from village notables when successfully forced for volunteers. |
| Roguery | 75 | Know-How | party leader | 0.05 | all | 5% more loot from defeated villagers and caravans. |
| Roguery | 100 | Manhunter | party leader | 10 | all | 10 prisoner limit. |
| Roguery | 100 | Promises | party leader | -0.5 | all | -50% food consumption for bandit units in your party. |
| Roguery | 100 | Promises | party leader | 0.3 | all | 30% recruitment rate for bandit prisoners in your party. |
| Roguery | 150 | Partners in Crime | party leader | 0 | all | Surrendering bandit parties can be recruited. |
| Roguery | 150 | Smuggler Connections | party leader | -0.5 | all | -50% trade penalty when you are trading with a faction you have crime rating against. |
| Roguery | 175 | One of the Family | party leader | 10 | all | 10 bonus Vigor and Control skills to bandit units in your party |
| Roguery | 175 | Salt the Earth | party leader | 0.2 | all | 20% more loot when villagers comply to your hostile actions. |
| Roguery | 200 | Ransom Broker | party leader | 0.25 | all | 25% better deals for heroes from ransom brokers. |
| Roguery | 200 | Ransom Broker | party leader | -0.3 | all | -30% escape chance for hero prisoners. |
| Roguery | 225 | Arms Dealer | party leader | -0.2 | all | -20% sell price penalty for weapons. |
| Scouting | 50 | Pathfinder | party leader | 0.5 | all | 50% daily chance to increase relation with a notable by 1 when you enter a town. |
| Scouting | 50 | Water Diviner | party leader | 0.5 | all | 50% daily chance to increase relation with a notable by 1 when you enter a village. |
| Scouting | 100 | Forced March | party leader | 2 | all | 2 experience per day to all troops while traveling with party morale higher than 75. |
| Scouting | 100 | Unburdened | party leader | 2 | all | 2 experience per day to all troops when traveling while overburdened. |
| Scouting | 150 | Mounted Scouts | party leader | 5 | all | 5 party size limit. |
| Scouting | 150 | Patrols | party leader | 0.1 | all | 10% advantage against bandits when troops are sent to confront the enemy. |
| Scouting | 175 | Beast Whisperer | party leader | 0.1 | all | 10% carrying capacity for pack animals in your party. |
| Scouting | 175 | Foragers | party leader | -0.15 | all | -15% disorganized state duration. |
| Scouting | 200 | Rumor Network | party leader | -0.05 | all | -5% trade penalty within cities of your own kingdom. |
| Scouting | 200 | Village Network | party leader | -0.1 | all | -10% trade penalty with villages of your own culture. |
| Scouting | 225 | Keen Sight | party leader | -0.5 | all | -50% chance of prisoner lords escaping from your party. |
| Scouting | 225 | Vantage Point | party leader | 10 | all | 10 prisoner limit. |
| Scouting | 250 | Rearguard | party leader | 0.2 | all | 20% wounded troop recovery speed while in an army. |
| Scouting | 250 | Rearguard | party leader | 0.1 | all | 10% damage by your troops when defending at your siege camp. |
| Scouting | 250 | Vanguard | party leader | 0.05 | all | 5% damage by your troops when they are sent as attackers. |
| Scouting | 250 | Vanguard | party leader | 0.1 | all | 10% damage by your troops when they are sent to sally out. |
| Smithing | 175 | Artisan Smith | party leader | -0.5 | all | -50% trade penalty when selling smithing weapons. |
| Steward | 25 | Frugal | quartermaster | -0.05 | all | -5% wages in your party. |
| Steward | 25 | Frugal | party leader | -0.15 | all | -15% recruitment costs. |
| Steward | 25 | Warrior's Diet | quartermaster | -0.1 | all | -10% food consumption in your party. |
| Steward | 25 | Warrior's Diet | party leader | 0 | all | No morale penalty from having single type of food. |
| Steward | 50 | Drill Sergeant | quartermaster | 2 | all | 2 daily experience to troops in your party. |
| Steward | 50 | Seven Veterans | quartermaster | 4 | all | 4 daily experience for tier 4+ troops in your party. |
| Steward | 75 | Stiff Upper Lip | quartermaster | -0.1 | all | -10% food consumption in your party while it is part of an army. |
| Steward | 75 | Sweatshops | quartermaster | 0.2 | all | 20% siege engine build rate in your party. |
| Steward | 100 | Efficient Campaigner | party leader | 1 | all | 1 extra food for each food taken during village raids for your party. |
| Steward | 100 | Efficient Campaigner | quartermaster | -0.25 | all | -25% troop wages in your party while it is part of an army. |
| Steward | 100 | Paid in Promise | party leader | -0.25 | all | -25% companion wages and recruitment fees. |
| Steward | 100 | Paid in Promise | quartermaster | 0 | all | Discarded armors are donated to troops for increased experience. |
| Steward | 125 | Giving Hands | quartermaster | 0 | all | Discarded weapons are donated to troops for increased experience. |
| Steward | 125 | Logistician | quartermaster | 4 | all | 4 party morale when number of mounts is greater than number of foot troops in your party. |
| Steward | 150 | Aid Corps | quartermaster | 0 | all | Wounded troops in your party are no longer paid wages. |
| Steward | 150 | Relocation | quartermaster | 0.25 | all | 25% influence gain from donating troops. |
| Steward | 175 | Gourmet | quartermaster | 1 | all | Double the morale bonus from having diverse food in your party. |
| Steward | 175 | Sound Reserves | quartermaster | -0.1 | all | -10% troop upgrade costs. |
| Steward | 175 | Sound Reserves | quartermaster | -0.1 | all | -10% food consumption during sieges in your party. |
| Steward | 200 | Contractors | quartermaster | -0.25 | all | -25% wages and upgrade costs of the mercenary troops in your party. |
| Steward | 200 | Forced Labor | quartermaster | 0 | all | Prisoners in your party provide carry capacity as if they are standard troops. |
| Steward | 225 | Arenicos' Horses | quartermaster | 0.1 | all | 10% carrying capacity for troops in your party. |
| Steward | 225 | Arenicos' Mules | quartermaster | 0.2 | all | 20% carrying capacity for pack animals in your party. |
| Steward | 225 | Arenicos' Mules | quartermaster | -0.2 | all | -20% trade penalty for trading pack animals. |
| Steward | 250 | Master of Planning | quartermaster | -0.4 | all | -40% food consumption while your party is in a siege camp. |
| Steward | 250 | Master of Warcraft | quartermaster | -0.25 | all | -25% troop wages while your party is in a siege camp. |
| Steward | 275 | Price of Loyalty | quartermaster | -0.005 | all | -0.5% to food consumption, wages and combat related morale loss for each steward point above 250 in your party. |
| Tactics | 25 | Loose Formations | party leader | -0.1 | all | -10% damage to your infantry from ranged troops when troops are sent to confront the enemy. |
| Tactics | 25 | Tight Formations | party leader | 0.1 | all | 10% damage by your infantry to cavalry when troops are sent to confront the enemy. |
| Tactics | 50 | Decisive Battle | party leader | 0.05 | all | 5% damage in plains, steppes and deserts when your troops are sent to confront the enemy. |
| Tactics | 50 | Extended Skirmish | party leader | 0.1 | all | 10% damage in snowy and forest terrains when troops are sent to confront the enemy. |
| Tactics | 75 | Horde Leader | party leader | 10 | all | 10 party size. |
| Tactics | 75 | Small Unit Tactics | party leader | 1 | all | 1 troop for the hideout crew |
| Tactics | 100 | Coaching | party leader | 0.03 | all | 3% damage when your troops are sent to confront the enemy. |
| Tactics | 100 | Law Keeper | party leader | 0.1 | all | 10% damage against bandits when your troops are sent to confront the enemy. |
| Tactics | 125 | Improviser | party leader | -0.25 | all | -25% loss of troops when breaking into or out of a settlement under siege. |
| Tactics | 125 | Swift Regroup | party leader | -0.5 | all | -50% troops left behind when escaping from battles. |
| Tactics | 200 | Elite Reserves | party leader | -0.2 | all | -20% less damage to tier 3+ units when troops are sent to confront the enemy. |
| Tactics | 200 | Encirclement | party leader | 0.05 | all | 5% damage to outnumbered enemies when troops are sent to confront the enemy. |
| Tactics | 225 | Pre Battle Maneuvers | party leader | 0.01 | all | 1% damage per 100 skill difference with the enemy when troops are sent to confront the enemy. |
| Tactics | 250 | Counter Offensive | party leader | 0.1 | all | 10% damage when troops are sent to confront the attacking enemy in a field battle. |
| Tactics | 250 | Counter Offensive | party leader | 0.1 | all | 10% damage when troops are sent to confront the enemy while outnumbered. |
| Throwing | 75 | Well Prepared | party leader | 1 | all | 1 ammunition for throwing weapons to troops in your party. |
| Throwing | 125 | Saddlebags | party leader | 1 | all | 1 daily experience to infantry troops in your party. |
| Throwing | 150 | Last Hit | party leader | 5 | all | 5 starting battle morale to troops in your party. |
| Throwing | 175 | Head Hunter | party leader | -0.2 | all | -20% recruitment cost of tier 2+ troops. |
| Throwing | 200 | Resourceful | party leader | 0.1 | all | 10% experience from battles to troops in your party equipped with throwing weapons. |
| Throwing | 225 | Long Reach | party leader | 0.2 | all | 20% morale and renown gained from battles won. |
| Trade | 25 | Appraiser | party leader | -0.15 | all | -15% price penalty while selling equipment. |
| Trade | 25 | Whole Seller | party leader | -0.15 | all | -15% price penalty while selling trade goods. |
| Trade | 50 | Caravan Master | quartermaster | 0.3 | all | 30% carrying capacity for your party. |
| Trade | 75 | Distributed Goods | quartermaster | -0.15 | all | -15% price penalty while buying from villages. |
| Trade | 75 | Local Connection | quartermaster | -0.15 | all | -15% price penalty while selling animals. |
| Trade | 125 | Artisan Community | quartermaster | 1 | all | 1 recruitment slot when recruiting from merchant notables. |
| Trade | 125 | Great Investor | quartermaster | -0.3 | all | -30% companion recruitment cost. |
| Trade | 150 | Content Trades | party leader | -0.5 | all | -50% wages paid while waiting in settlements. |
| Trade | 150 | Mercenary Connections | party leader | -0.25 | all | -25% mercenary troop wages in your party. |
| Trade | 175 | Insurance Plans | quartermaster | -0.25 | all | -25% price penalty while buying food items. |
| Trade | 175 | Rapid Development | quartermaster | -0.25 | all | -25% price penalty while buying clay, iron, silk and silver. |
| Trade | 225 | Sword For Barter | quartermaster | -0.15 | all | -15% caravan guard wages. |
| Trade | 250 | Silver Tongue | quartermaster | 0.15 | all | 15% better trade deals from caravans and villagers |
| Trade | 275 | Trickle Down | party leader | 1 | all | 1 relationship with merchants if 10.000 or more denars are spent on a single deal. |
| Two Handed | 75 | Baptised in Blood | party leader | 0.05 | all | 5% experience to melee troops in your party after every battle. |
| Two Handed | 75 | Show of Strength | party leader | -0.2 | all | -20% recruitment cost of infantry. |
| Two Handed | 175 | Hope | party leader | 5 | all | 5 party limit. |
| Two Handed | 175 | Terror | party leader | 10 | all | 10 prisoner limit. |
| Two Handed | 200 | Thick Hides | party leader | 5 | all | 5 hit points to troops in your party. |

### Personal Combat Payoff Perks

Perks with a Personal role that affect the main hero's combat stats.

Rows: 141

| Skill | Level | Perk | Role | Bonus | Scope | Effect |
| --- | ---: | --- | --- | ---: | --- | --- |
| Athletics | 25 | Morning Exercise | personal | 0.03 | all | 3% combat movement speed. |
| Athletics | 25 | Well Built | personal | 5 | all | 5 hit points. |
| Athletics | 50 | Fury | personal | 0.1 | all | 10% weapon handling while on foot. |
| Athletics | 100 | Powerful | personal | 0.04 | all | 4% damage with melee weapons. |
| Athletics | 100 | Sprint | personal | 0.05 | all | 5% combat movement speed when you have no shields and no ranged weapons equipped. |
| Athletics | 125 | Braced | personal | -0.4 | all | -40% charge damage taken. |
| Athletics | 125 | Surging Blow | personal | 0.3 | all | 30% damage bonus from speed while on foot. |
| Athletics | 225 | Strong Arms | personal | 0.05 | all | 5% damage with throwing weapons. |
| Athletics | 225 | Strong Legs | personal | -0.5 | all | -50% fall damage taken and +100% kick damage dealt. |
| Athletics | 250 | Ignore Pain | personal | 0.1 | all | 10% armor while on foot. |
| Athletics | 250 | Spartan | personal | 0.5 | all | 50% resistance to getting staggered while on foot. |
| Athletics | 275 | Mighty Blow | personal | 0.05 | all | You stun your enemies longer after they block your attack. |
| Athletics | 275 | Mighty Blow | personal | 1 | all | 1 hit points for every skill point above 250. |
| Bow | 25 | Bow Control | personal | -0.3 | all | -30% accuracy penalty while moving. |
| Bow | 25 | Dead Aim | personal | 0.3 | all | 30% headshot damage with bows. |
| Bow | 50 | Bodkin | personal | 0.1 | all | 10% armor penetration with bows. |
| Bow | 50 | Nocking Point | personal | -0.5 | all | -50% movement speed penalty while reloading. |
| Bow | 75 | Quick Adjustments | personal | -0.5 | all | -50% accuracy penalty while rotating. |
| Bow | 75 | Rapid Fire | personal | 0.25 | all | 25% reload speed with bows. |
| Bow | 100 | Mounted Archery | personal | -0.3 | all | -30% accuracy penalty using bows while mounted. |
| Bow | 125 | Strong bows | personal | 0.08 | all | 8% damage with bows. |
| Bow | 150 | Discipline | personal | 0.5 | all | 50% aiming duration without losing accuracy. |
| Bow | 150 | Hunter Clan | personal | 0.3 | all | 30% damage with bows to mounts. |
| Bow | 175 | Eagle Eye | personal | 0.5 | all | 50% zoom with bows. |
| Bow | 175 | Skirmish Phase Master | personal | -0.1 | all | -10% damage taken from projectiles. |
| Bow | 225 | Deep Quivers | personal | 3 | all | 3 extra arrows per quiver. |
| Bow | 250 | Quick Draw | personal | 0.25 | all | 25% aiming speed with bows. |
| Bow | 250 | Ranger's Swiftness | personal | 0 | all | Equipped bows do not slow you down. |
| Bow | 275 | Deadshot | personal | 0.002 | all | 0.2% reload speed with bows for every skill point above 200. |
| Bow | 275 | Deadshot | personal | 0.005 | all | 0.5% damage with bows for every skill point above 200. |
| Crossbow | 25 | Marksmen | personal | 0.25 | all | 25% faster aiming with crossbows. |
| Crossbow | 25 | Piercer | personal | 20 | all | Your crossbow attacks ignore armors below 20. |
| Crossbow | 50 | Unhorser | personal | 0.4 | all | 40% crossbow damage to mounts. |
| Crossbow | 50 | Wind Winder | personal | 0.25 | all | 25% reload speed with crossbows. |
| Crossbow | 75 | Donkey's Swiftness | personal | -0.3 | all | -30% accuracy loss while moving. |
| Crossbow | 75 | Sheriff | personal | 0.5 | all | 50% headshot damage with crossbows. |
| Crossbow | 125 | Fletcher | personal | 4 | all | 4 bolts per quiver. |
| Crossbow | 125 | Puncture | personal | 0.1 | all | 10% armor penetration with crossbows. |
| Crossbow | 150 | Deft Hands | personal | 0.5 | all | 50% resistance to getting staggered while reloading your crossbow. |
| Crossbow | 150 | Loose and Move | personal | 0 | all | Equipped crossbows do not slow you down. |
| Crossbow | 175 | Counter Fire | personal | -0.1 | all | -10% projectile damage taken while equipped with a crossbow. |
| Crossbow | 200 | Long Shots | personal | 1 | all | 100% more zoom with crossbows. |
| Crossbow | 200 | Steady | personal | -0.5 | all | -50% accuracy penalty with crossbows while mounted. |
| Crossbow | 225 | Hammer Bolts | personal | 0.5 | all | Crossbows can now dismount and ignore 50% dismount resistance on attacks against cavalry. |
| Crossbow | 225 | Pavise | personal | 0.75 | all | 75% chance of blocking projectiles from behind with a shield on your back. |
| Crossbow | 275 | Mighty Pull | personal | 0.002 | all | 0.2% reload speed with crossbows for every skill point above 200. |
| Crossbow | 275 | Mighty Pull | personal | 0.005 | all | 0.5% damage with crossbows for every skill point above 200. |
| Engineering | 25 | Scaffolds | personal | 0.3 | all | 30% shield hitpoints. |
| Engineering | 25 | Torsion Engines | personal | 3 | all | 3 damage to equipped crossbows. |
| Medicine | 25 | Preventive Medicine | personal | 5 | all | 5 hit points. |
| Medicine | 25 | Preventive Medicine | personal | 0.3 | all | 30% recovery of lost hit points after each battle. |
| Medicine | 25 | Self Medication | personal | 0.02 | all | 2% combat movement speed. |
| Medicine | 50 | Walk It Off | personal | 10 | all | 10 hit points recovery after each offensive battle. |
| Medicine | 75 | Doctor's Oath | personal | 5 | all | 5 hit points. |
| Medicine | 225 | Fortitude Tonic | personal | 5 | all | 5 hit points. |
| One Handed | 25 | Basher | personal | 0.5 | all | 50% damage and longer stun duration with shield bashes. |
| One Handed | 25 | Wrapped Handles | personal | 0.2 | all | 20% handling to one handed weapons. |
| One Handed | 50 | Swift Strike | personal | 0.02 | all | 2% swing speed with one handed weapons. |
| One Handed | 50 | To Be Blunt | personal | 0.05 | all | 5% damage with one handed axes and maces. |
| One Handed | 75 | Cavalry | personal | 0.05 | all | 5% damage with one handed weapons while mounted. |
| One Handed | 75 | Shield Bearer | personal | 0 | all | Removed movement speed penalty of wielding shields. |
| One Handed | 100 | Duelist | personal | 0.2 | all | 20% damage while wielding a one handed weapon without a shield. |
| One Handed | 100 | Trainer | personal | 2 | all | 2 hit points. |
| One Handed | 125 | Arrow Catcher | personal | 0.01 | all | Larger shield protection area against projectiles. |
| One Handed | 125 | Shieldwall | personal | -0.2 | all | -20% damage to your shield while blocking in wrong direction. |
| One Handed | 200 | Fleet of Foot | personal | 0.04 | all | 4% combat movement speed. |
| One Handed | 200 | Steel Core Shields | personal | -0.1 | all | -10% damage to your shields. |
| One Handed | 225 | Deadly Purpose | personal | 0.05 | all | 5% damage with one handed weapons. |
| One Handed | 225 | Unwavering Defense | personal | 5 | all | 5 hit points. |
| One Handed | 250 | Chink in the Armor | personal | 0.1 | all | 10% armor penetration with melee attacks. |
| One Handed | 250 | Prestige | personal | 0.5 | all | 50% damage against shields with one handed weapons. |
| One Handed | 275 | Way of the Sword | personal | 0.002 | all | 0.2% attack speed with one handed weapons for every skill point above 250. |
| One Handed | 275 | Way of the Sword | personal | 0.005 | all | 0.5% damage with one handed weapons for every skill point above 250. |
| Polearm | 25 | Cavalry | personal | 0.02 | all | 2% damage with polearms while mounted. |
| Polearm | 25 | Pikeman | personal | 0.02 | all | 2% damage with polearms on foot. |
| Polearm | 50 | Braced | personal | 0.25 | all | Polearms that can dismount ignore 25% dismount resistance on attacks against cavalry. |
| Polearm | 50 | Keep at Bay | personal | 0.3 | all | Polearms ignore 30% knockback resistance on thrust attacks against footmen. |
| Polearm | 75 | Clean Thrust | personal | 0.1 | all | 10% thrust damage with polearms. |
| Polearm | 75 | Swift Swing | personal | 0.05 | all | 5% swing speed with polearms. |
| Polearm | 100 | Footwork | personal | 0.02 | all | 2% combat movement speed with polearms. |
| Polearm | 100 | Hard Knock | personal | 0.25 | all | Polearms that can knockdown ignore 25% knockdown resistance on thrust attacks. |
| Polearm | 125 | Lancer | personal | 0.2 | all | 20% damage bonus from speed with polearms while mounted. |
| Polearm | 125 | Steed Killer | personal | 0.7 | all | 70% damage to mounts with polearms. |
| Polearm | 150 | Guards | personal | 0.5 | all | 50% damage when you hit an enemy in the head with a polearm. |
| Polearm | 225 | Sure Footed | personal | -0.4 | all | -40% charge damage taken. |
| Polearm | 225 | Unstoppable Force | personal | 3 | all | Triple couch lance damage against shields. |
| Polearm | 250 | Counterweight | personal | 0.15 | all | 15% handling of swingable polearms. |
| Polearm | 250 | Sharpen the Tip | personal | 0.05 | all | 5% damage with thrust attacks made with polearms. |
| Polearm | 275 | Way of the Spear | personal | 0.002 | all | 0.2% attack speed with polearms for every skill point above 250. |
| Polearm | 275 | Way of the Spear | personal | 0.005 | all | 0.5% damage with polearms for every skill point above 250. |
| Riding | 25 | Full Speed | personal | 0.2 | all | 20% charge damage dealt. |
| Riding | 50 | Veterinary | personal | 0.2 | all | 20% hit points to your mount. |
| Riding | 100 | Sagittarius | personal | -0.15 | all | -15% accuracy penalty while mounted. |
| Riding | 150 | Horse Archer | personal | 0.1 | all | 10% ranged damage while mounted. |
| Riding | 150 | Mounted Warrior | personal | 0.05 | all | 5% mounted melee damage. |
| Riding | 200 | Annoying Buzz | personal | 0.2 | all | 20% battle morale penalty to enemies with mounted ranged kills. |
| Riding | 200 | Thunderous Charge | personal | 0.2 | all | 20% battle morale penalty to enemies with mounted melee kills. |
| Riding | 250 | Dauntless Steed | personal | 0.5 | all | 50% resistance to getting staggered while mounted. |
| Riding | 250 | Tough Steed | personal | 0.2 | all | 20% armor to your mount. |
| Roguery | 200 | Carver | personal | 0.1 | all | 10% damage with civilian weapons. |
| Roguery | 225 | Dirty Fighting | personal | 0.5 | all | 50% stun duration for kicking. |
| Roguery | 250 | Dash and Slash | personal | 0.5 | all | 50% damage bonus from speed while on foot. |
| Roguery | 250 | Fleet Footed | personal | 0.1 | all | 10% combat movement speed while no weapons or shields are equipped. |
| Smithing | 250 | Sharpened Edge | personal | 0.02 | all | 2% swing damage of crafted weapons. |
| Smithing | 250 | Sharpened Tip | personal | 0.02 | all | 2% thrust damage of crafted weapons. |
| Throwing | 25 | Quick Draw | personal | 0.2 | all | 20% draw speed with throwing weapons. |
| Throwing | 25 | Shield Breaker | personal | 0.4 | all | 40% damage to shields with throwing weapons. |
| Throwing | 50 | Flexible Fighter | personal | 0.1 | all | 10% damage while using throwing weapons as melee. |
| Throwing | 50 | Hunter | personal | 0.4 | all | 40% damage to mounts with throwing weapons. |
| Throwing | 75 | Mounted Skirmisher | personal | -0.2 | all | -20% accuracy penalty with throwing weapons while mounted. |
| Throwing | 75 | Well Prepared | personal | 1 | all | 1 ammunition for throwing weapons. |
| Throwing | 100 | Knock Off | personal | 0.25 | all | Thrown weapons can now dismount and ignore 25% dismount resistance on attacks against cavalry. |
| Throwing | 100 | Running Throw | personal | 0.25 | all | 25% damage bonus from speed with throwing weapons. |
| Throwing | 125 | Saddlebags | personal | 2 | all | 2 ammunition for throwing weapons when you start a battle mounted. |
| Throwing | 125 | Skirmisher | personal | -0.1 | all | -10% damage taken by ranged attacks while holding a throwing weapon. |
| Throwing | 150 | Focus | personal | 0.25 | all | 25% zoom with throwing weapons. |
| Throwing | 150 | Last Hit | personal | 0.5 | all | 50% damage to enemies with less than half of their hit points left. |
| Throwing | 175 | Head Hunter | personal | 0.5 | all | 50% headshot damage with thrown weapons. |
| Throwing | 175 | Slinging Competitions | personal | -0.2 | all | Sling weapons can penetrate head armor. |
| Throwing | 200 | Resourceful | personal | 2 | all | 2 ammunition for throwing weapons. |
| Throwing | 200 | Splinters | personal | 3 | all | Triple damage against shields with throwing axes. |
| Throwing | 225 | Perfect Technique | personal | 0.25 | all | 25% travel speed to your throwing weapons. |
| Throwing | 250 | Weak Spot | personal | 0.3 | all | 30% armor penetration with throwing weapons. |
| Throwing | 275 | Unstoppable Force | personal | 0.002 | all | 0.2% travel speed to your throwing weapons for every skill point above 200. |
| Throwing | 275 | Unstoppable Force | personal | 0.005 | all | 0.5% damage with throwing weapons for every skill point above 200. |
| Two Handed | 25 | Strong Grip | personal | 0.1 | all | 10% handling to two handed weapons. |
| Two Handed | 25 | Wood Chopper | personal | 0.3 | all | 30% damage to shields with two handed weapons. |
| Two Handed | 50 | Head Basher | personal | 0.1 | all | 10% damage with two handed axes and maces. |
| Two Handed | 50 | On the Edge | personal | 0.03 | all | 3% swing speed with two handed weapons. |
| Two Handed | 75 | Show of Strength | personal | 0.3 | all | Two handed weapons that can knockdown ignore 30% knockdown resistance on swing attacks. |
| Two Handed | 100 | Beast Slayer | personal | 0.5 | all | 50% damage to mounts with two handed weapons. |
| Two Handed | 100 | Shield breaker | personal | 0.4 | all | 40% damage to shields with two handed weapons. |
| Two Handed | 125 | Berserker | personal | 0.2 | all | 20% damage with two handed weapons while you have less than half of your hit points. |
| Two Handed | 125 | Confidence | personal | 0.15 | all | 15% damage with two handed weapons while you have more than 90% of your hit points. |
| Two Handed | 150 | Projectile Deflection | personal | 0 | all | You can deflect projectiles with two handed swords by blocking. |
| Two Handed | 200 | Reckless Charge | personal | 0.2 | all | 20% damage bonus from speed with two handed weapons while on foot. |
| Two Handed | 200 | Thick Hides | personal | 5 | all | 5 hit points. |
| Two Handed | 225 | Blade Master | personal | 0.1 | all | 10% damage with two handed weapons. |
| Two Handed | 225 | Vandal | personal | 0.25 | all | 25% armor penetration with your attacks. |
| Two Handed | 250 | Way Of The Great Axe | personal | 0.002 | all | 0.2% attack speed with two handed weapons for every skill point above 250. |
| Two Handed | 250 | Way Of The Great Axe | personal | 0.005 | all | 0.5% damage with two handed weapons for every skill point above 250. |

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

### Trade and Gold Economy Perks

Perks that affect prices, trade penalties, workshops, caravans, and gold accumulation.

Rows: 86

| Skill | Level | Perk | Role | Bonus | Scope | Effect |
| --- | ---: | --- | --- | ---: | --- | --- |
| Bow | 150 | Hunter Clan | governor | -0.15 | all | -15% garrison wages in the governed castle. |
| Bow | 200 | Renowned Archer | party leader | -0.3 | all | -30% recruitment and upgrade cost to ranged troops. |
| Charm | 150 | Effort For The People | personal | -0.25 | all | -25% barter penalty with lords of same culture. |
| Charm | 150 | Slick Negotiator | personal | -0.2 | all | -20% hiring costs of mercenary troops. |
| Charm | 150 | Slick Negotiator | personal | -0.1 | all | -10% barter penalty with lords of different cultures. |
| Crossbow | 25 | Piercer | party leader | -0.2 | all | -20% recruitment cost of ranged troops. |
| Crossbow | 100 | Peasant Leader | governor | -0.2 | all | -20% garrisoned ranged troop wages in the governed settlement. |
| Crossbow | 250 | Picked Shots | party leader | -0.5 | all | -50% wages of tier 4+ ranged troops. |
| Engineering | 225 | Metallurgy | engineer | 0.3 | all | 30% chance to remove negative modifiers on looted items. |
| One Handed | 150 | Military Tradition | governor | -0.05 | all | -5% garrison wages in the governed settlement. |
| One Handed | 250 | Chink in the Armor | party leader | -0.2 | all | -20% recruitment cost of infantry. |
| Polearm | 175 | Standard Bearer | governor | -0.2 | all | -20% wages to garrisoned infantry in the governed settlement. |
| Polearm | 200 | Hardy Frontline | party leader | -0.2 | all | -20% recruitment cost of infantry. |
| Riding | 75 | Deeper Sacks | party leader | -0.1 | all | -10% trade penalty for mounts. |
| Riding | 225 | Cavalry Tactics | governor | -0.5 | all | -50% wages of mounted troops in the governed settlement. |
| Roguery | 50 | Deep Pockets | personal | -0.2 | all | -20% bandit troop wages. |
| Roguery | 75 | Know-How | party leader | 0.05 | all | 5% more loot from defeated villagers and caravans. |
| Roguery | 100 | Manhunter | personal | 0.2 | all | 20% better deals with ransom broker for regular troops. |
| Roguery | 150 | Smuggler Connections | party leader | -0.5 | all | -50% trade penalty when you are trading with a faction you have crime rating against. |
| Roguery | 175 | Salt the Earth | party leader | 0.2 | all | 20% more loot when villagers comply to your hostile actions. |
| Roguery | 200 | Ransom Broker | party leader | 0.25 | all | 25% better deals for heroes from ransom brokers. |
| Roguery | 225 | Arms Dealer | party leader | -0.2 | all | -20% sell price penalty for weapons. |
| Roguery | 275 | Rogue Extraordinaire | personal | 0.01 | all | 1% loot amount for every skill point above 200. |
| Scouting | 200 | Rumor Network | party leader | -0.05 | all | -5% trade penalty within cities of your own kingdom. |
| Scouting | 200 | Village Network | party leader | -0.1 | all | -10% trade penalty with villages of your own culture. |
| Smithing | 175 | Artisan Smith | party leader | -0.5 | all | -50% trade penalty when selling smithing weapons. |
| Steward | 25 | Frugal | quartermaster | -0.05 | all | -5% wages in your party. |
| Steward | 25 | Frugal | party leader | -0.15 | all | -15% recruitment costs. |
| Steward | 50 | Drill Sergeant | governor | -0.05 | all | -5% garrison wages in the governed settlement. |
| Steward | 75 | Stiff Upper Lip | governor | -0.2 | all | -20% garrison wages in the governed castle. |
| Steward | 100 | Efficient Campaigner | quartermaster | -0.25 | all | -25% troop wages in your party while it is part of an army. |
| Steward | 100 | Paid in Promise | party leader | -0.25 | all | -25% companion wages and recruitment fees. |
| Steward | 150 | Aid Corps | quartermaster | 0 | all | Wounded troops in your party are no longer paid wages. |
| Steward | 175 | Sound Reserves | quartermaster | -0.1 | all | -10% troop upgrade costs. |
| Steward | 200 | Contractors | quartermaster | -0.25 | all | -25% wages and upgrade costs of the mercenary troops in your party. |
| Steward | 225 | Arenicos' Horses | personal | -0.2 | all | -20% trade penalty for trading mounts. |
| Steward | 225 | Arenicos' Mules | quartermaster | -0.2 | all | -20% trade penalty for trading pack animals. |
| Steward | 250 | Master of Warcraft | quartermaster | -0.25 | all | -25% troop wages while your party is in a siege camp. |
| Throwing | 175 | Head Hunter | party leader | -0.2 | all | -20% recruitment cost of tier 2+ troops. |
| Trade | 25 | Appraiser | party leader | -0.15 | all | -15% price penalty while selling equipment. |
| Trade | 25 | Appraiser | personal | 0 | all | Your profits are marked. |
| Trade | 25 | Whole Seller | party leader | -0.15 | all | -15% price penalty while selling trade goods. |
| Trade | 25 | Whole Seller | personal | 0 | all | Your profits are marked. |
| Trade | 50 | Caravan Master | quartermaster | 0.3 | all | 30% carrying capacity for your party. |
| Trade | 50 | Caravan Master | personal | 0 | all | Item prices are marked relative to the average price. |
| Trade | 50 | Market Dealer | clan leader | -0.5 | all | -50% cost of bartering for safe passage. |
| Trade | 50 | Market Dealer | personal | 0 | all | Item prices are marked relative to the average price. |
| Trade | 75 | Distributed Goods | personal | 2 | all | Double the relationship gain by resolved issues with artisans. |
| Trade | 75 | Distributed Goods | quartermaster | -0.15 | all | -15% price penalty while buying from villages. |
| Trade | 75 | Local Connection | personal | 2 | all | Double the relationship gain by resolved issues with merchants. |
| Trade | 75 | Local Connection | quartermaster | -0.15 | all | -15% price penalty while selling animals. |
| Trade | 100 | Toll Gates | personal | 0 | all | Your workshops gather trade rumors. |
| Trade | 100 | Toll Gates | governor | 30 | all | 30 gold for each caravan visiting the governed settlement. |
| Trade | 100 | Traveling Rumors | personal | 0 | all | Your caravans gather trade rumors. |
| Trade | 100 | Traveling Rumors | governor | 20 | all | 20 gold for each villager party visiting the governed settlement. |
| Trade | 125 | Artisan Community | clan leader | 1 | all | 1 daily renown from every profiting workshop. |
| Trade | 125 | Artisan Community | quartermaster | 1 | all | 1 recruitment slot when recruiting from merchant notables. |
| Trade | 125 | Great Investor | clan leader | 1 | all | 1 daily renown from every profiting caravan. |
| Trade | 125 | Great Investor | quartermaster | -0.3 | all | -30% companion recruitment cost. |
| Trade | 150 | Content Trades | governor | 0.1 | all | 10% tariff income in the governed settlement. |
| Trade | 150 | Content Trades | party leader | -0.5 | all | -50% wages paid while waiting in settlements. |
| Trade | 150 | Mercenary Connections | governor | 0.25 | all | 25% workshop production rate. |
| Trade | 150 | Mercenary Connections | party leader | -0.25 | all | -25% mercenary troop wages in your party. |
| Trade | 175 | Insurance Plans | clan leader | 5000 | all | 5000 denar return when one of your caravans is destroyed. |
| Trade | 175 | Insurance Plans | quartermaster | -0.25 | all | -25% price penalty while buying food items. |
| Trade | 175 | Rapid Development | clan leader | 5000 | all | 5000 denar return for each workshop when workshop's town is captured by an enemy. |
| Trade | 175 | Rapid Development | quartermaster | -0.25 | all | -25% price penalty while buying clay, iron, silk and silver. |
| Trade | 200 | Granary Accountant | personal | -0.2 | all | -20% price penalty while selling food items. |
| Trade | 200 | Granary Accountant | governor | 0.2 | all | 20% production rate to grain, olives, fish, date in villages bound to the governed settlement. |
| Trade | 200 | Tradeyard Foreman | personal | -0.2 | all | -20% price penalty while selling pottery, tools, silk and jewelry. |
| Trade | 200 | Tradeyard Foreman | governor | 0.2 | all | 20% production rate to clay, iron, silk and silver in villages bound to the governed settlement. |
| Trade | 225 | Self-made Man | personal | -0.5 | all | -50% barter penalty for items. |
| Trade | 225 | Self-made Man | governor | 0.3 | all | 30% build speed for marketplace, kiln and aqueduct projects. |
| Trade | 225 | Sword For Barter | personal | -0.2 | all | -20% hiring costs of mercenary troops. |
| Trade | 225 | Sword For Barter | quartermaster | -0.15 | all | -15% caravan guard wages. |
| Trade | 250 | Silver Tongue | personal | -0.15 | all | -15% gold required while persuading lords to defect to your faction. |
| Trade | 250 | Silver Tongue | quartermaster | 0.15 | all | 15% better trade deals from caravans and villagers |
| Trade | 250 | Spring of Gold | clan leader | 0.001 | all | 0.1% denars of interest income per day based on your current denars up to 1000 denars. |
| Trade | 250 | Spring of Gold | governor | 0.2 | all | 20% effect from boosting projects in the governed settlement. |
| Trade | 275 | Man of Means | clan leader | -0.2 | all | -20% costs of recruiting minor faction clans into your clan. |
| Trade | 275 | Man of Means | personal | -0.3 | all | -30% ransom cost for your freedom. |
| Trade | 275 | Trickle Down | party leader | 1 | all | 1 relationship with merchants if 10.000 or more denars are spent on a single deal. |
| Trade | 275 | Trickle Down | governor | 2 | all | 2 daily prosperity while building a project in the governed settlement. |
| Trade | 300 | Everything Has a Price | personal | 0 | all | You can now trade settlements in barter. |
| Two Handed | 75 | Show of Strength | party leader | -0.2 | all | -20% recruitment cost of infantry. |
| Two Handed | 125 | Berserker | governor | -0.1 | all | -10% garrison wages in the governed settlement. |

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
