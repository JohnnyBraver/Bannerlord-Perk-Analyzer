---
skill: "Tactics"
attribute: "Cunning"
game_version: "1.4.5"
---

# Tactics Perks

| Level | Perk | Slot | Role | Effect | Type | Subtype | Triggers | Tags | Target Version | Curation/Status | ID |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | Loose Formations | primary | party leader | -10% damage to your infantry from ranged troops when troops are sent to confront the enemy. | troop combat | damage resistance | simulation, party composition |  | 1.4.5 | OK | TacticsLooseFormations |
| 25 | Loose Formations | secondary | captain | -25% morale penalty when troops in your formation use line, loose, circle or scatter formations. | troop combat | morale |  |  | 1.4.5 | Review: Formation-type condition is not represented by current trigger_condition taxonomy. | TacticsLooseFormations |
| 25 | Tight Formations | primary | party leader | 10% damage by your infantry to cavalry when troops are sent to confront the enemy. | troop combat | damage increase | simulation, party composition | mounts | 1.4.5 | OK | TacticsTightFormations |
| 25 | Tight Formations | secondary | captain | -25% morale penalty when troops in your formation use shield wall, square, skein, column formations. | troop combat | morale |  |  | 1.4.5 | Review: Formation-type condition is not represented by current trigger_condition taxonomy. | TacticsTightFormations |
| 50 | Decisive Battle | primary | party leader | 5% damage in plains, steppes and deserts when your troops are sent to confront the enemy. | troop combat | damage increase | simulation, terrain |  | 1.4.5 | OK | TacticsDecisiveBattle |
| 50 | Decisive Battle | secondary | captain | 5% movement speed to troops in your formation in plains, steppes and deserts. | troop combat | movement speed | terrain |  | 1.4.5 | OK | TacticsDecisiveBattle |
| 50 | Extended Skirmish | primary | party leader | 10% damage in snowy and forest terrains when troops are sent to confront the enemy. | troop combat | damage increase | simulation, terrain |  | 1.4.5 | OK | TacticsExtendedSkirmish |
| 50 | Extended Skirmish | secondary | captain | 2% movement speed to troops in your formation in snowy and forest terrains. | troop combat | movement speed | terrain |  | 1.4.5 | OK | TacticsExtendedSkirmish |
| 75 | Horde Leader | primary | party leader | 10 party size. | party management | party size |  |  | 1.4.5 | OK | TacticsHordeLeader |
| 75 | Horde Leader | secondary | army leader | -5% army cohesion loss to commanded armies. | army management | cohesion |  |  | 1.4.5 | OK | TacticsHordeLeader |
| 75 | Small Unit Tactics | primary | party leader | 1 troop for the hideout crew | party management | party size |  |  | 1.4.5 | OK | TacticsSmallUnitTactics |
| 75 | Small Unit Tactics | secondary | captain | 5% movement speed to troops in your formation when there are less than 15 soldiers. | troop combat | movement speed |  |  | 1.4.5 | Review: Formation-size condition is not represented by current trigger_condition taxonomy. | TacticsSmallUnitTactics |
| 100 | Coaching | primary | party leader | 3% damage when your troops are sent to confront the enemy. | troop combat | damage increase | simulation |  | 1.4.5 | OK | TacticsCoaching |
| 100 | Coaching | secondary | captain | 1% damage by troops in your formation. | troop combat | damage increase |  |  | 1.4.5 | OK | TacticsCoaching |
| 100 | Law Keeper | primary | party leader | 10% damage against bandits when your troops are sent to confront the enemy. | troop combat | damage increase | simulation | bandits | 1.4.5 | OK | TacticsLawkeeper |
| 100 | Law Keeper | secondary | captain | 4% damage against bandits by troops in your formation. | troop combat | damage increase |  | bandits | 1.4.5 | OK | TacticsLawkeeper |
| 125 | Improviser | primary | player | No morale penalty for disorganized state in battles, in sally out or when being attacked. | party management | morale | during siege, defending |  | 1.4.5 | Review: Effect removes morale penalty from disorganized state; battle escape is only an indirect source of the state. | TacticsImproviser |
| 125 | Improviser | secondary | party leader | -25% loss of troops when breaking into or out of a settlement under siege. | battle escape |  | during siege |  | 1.4.5 | OK | TacticsImproviser |
| 125 | Swift Regroup | primary | player | -15% disorganized state duration when a raid or siege is broken. | battle escape |  | during siege |  | 1.4.5 | OK | TacticsSwiftRegroup |
| 125 | Swift Regroup | secondary | party leader | -50% troops left behind when escaping from battles. | battle escape |  | after battle |  | 1.4.5 | OK | TacticsSwiftRegroup |
| 150 | Call To Arms | primary | army leader | 10% movement speed to parties called to your army. | movement | movement speed |  |  | 1.4.5 | OK | TacticsCallToArms |
| 150 | Call To Arms | secondary | army leader | -15% influence required to call parties to your army | army management | influence cost |  |  | 1.4.5 | OK | TacticsCallToArms |
| 150 | On The March | primary | army leader | -20% fortification bonus to enemies when troops are sent to confront the enemy. | simulation bonus | fortification bonus | simulation | defense, fortifications | 1.4.5 | OK | TacticsOnTheMarch |
| 150 | On The March | secondary | governor | 20% fortification bonus to the governed settlement | settlement defense | fortification bonus | governed settlement | defense, fortifications | 1.4.5 | OK | TacticsOnTheMarch |
| 175 | Make Them Pay | primary | engineer | 25% damage to defender siege engines. | damage increase | siege engines | during siege |  | 1.4.5 | OK | TacticsMakeThemPay |
| 175 | Make Them Pay | secondary | governor | 25% damage to besieging siege engines. | settlement defense | siege engines | during siege, governed settlement | defense | 1.4.5 | OK | TacticsMakeThemPay |
| 175 | Pick Them Off The Walls | primary | engineer | 25% chance for dealing double damage to siege defender troops in siege bombardment | damage increase | siege engines | during siege |  | 1.4.5 | OK | TacticsPickThemOfTheWalls |
| 175 | Pick Them Off The Walls | secondary | governor | 25% chance for dealing double damage to besieging troops in siege bombardment of the governed settlement. | settlement defense | siege engines | during siege, governed settlement | defense | 1.4.5 | OK | TacticsPickThemOfTheWalls |
| 200 | Elite Reserves | primary | party leader | -20% less damage to tier 3+ units when troops are sent to confront the enemy. | troop combat | damage resistance | simulation, party composition |  | 1.4.5 | OK | TacticsEliteReserves |
| 200 | Elite Reserves | secondary | captain | -5% damage taken by troops in your formation. | troop combat | damage resistance |  |  | 1.4.5 | OK | TacticsEliteReserves |
| 200 | Encirclement | primary | party leader | 5% damage to outnumbered enemies when troops are sent to confront the enemy. | troop combat | damage increase | simulation |  | 1.4.5 | Review: Outnumbered condition is not represented by current trigger_condition taxonomy. | TacticsEncirclement |
| 200 | Encirclement | secondary | army leader | -10% influence cost to boost army cohesion. | army management | influence cost |  |  | 1.4.5 | OK | TacticsEncirclement |
| 225 | Besieged | primary | player | 10% damage while besieged when troops are sent to confront the enemy. | personal combat | damage increase | during siege, simulation |  | 1.4.5 | OK | TacticsBesieged |
| 225 | Besieged | secondary | personal | 50% influence gain from winning sieges. | army management | influence | during siege, after battle |  | 1.4.5 | OK | TacticsBesieged |
| 225 | Pre Battle Maneuvers | primary | player | 25% influence gain from winning battles. | army management | influence | after battle |  | 1.4.5 | OK | TacticsPreBattleManeuvers |
| 225 | Pre Battle Maneuvers | secondary | party leader | 1% damage per 100 skill difference with the enemy when troops are sent to confront the enemy. | troop combat | damage increase | simulation |  | 1.4.5 | OK | TacticsPreBattleManeuvers |
| 250 | Counter Offensive | primary | party leader | 10% damage when troops are sent to confront the attacking enemy in a field battle. | troop combat | damage increase | simulation, defending |  | 1.4.5 | OK | TacticsCounteroffensive |
| 250 | Counter Offensive | secondary | party leader | 10% damage when troops are sent to confront the enemy while outnumbered. | troop combat | damage increase | simulation |  | 1.4.5 | Review: Outnumbered condition is not represented by current trigger_condition taxonomy. | TacticsCounteroffensive |
| 250 | Gens d'armes | primary | captain | 2% damage to infantry by cavalry troops in your formation. | troop combat | damage increase | party composition | mounts | 1.4.5 | OK | TacticsGensdarmes |
| 250 | Gens d'armes | secondary | governor | 1 daily security in the governed settlement. | settlement defense | security | governed settlement | defense | 1.4.5 | OK | TacticsGensdarmes |
| 275 | Tactical Mastery | primary | army leader | 0.5% damage for every skill point above 200 tactics skill when troops are sent to confront the enemy. | troop combat | damage increase | simulation, over skill cap |  | 1.4.5 | OK | TacticsTacticalMastery |
