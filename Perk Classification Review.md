# Perk Classification Review

Generated from local Bannerlord 1.4.5 assembly data. Rows listed here are classification heuristics that look ambiguous and should be hand-checked.

| Skill | Level | Perk | Role | Type | Subtype | Effect | Review |
|---|---:|---|---|---|---|---|---|
| Athletics | 50 | Form Fitting Armor | personal | utility |  | -15% armor weight. | Numeric utility effect may deserve a more specific perk_type. |
| Athletics | 225 | Strong Legs | personal | personal combat | fall | -50% fall damage taken and +100% kick damage dealt. | Composite effect spans multiple classification categories. |
| Charm | 50 | Oratory | personal | social | renown | 1 renown and influence for each issue resolved | Composite effect spans multiple classification categories. |
| One Handed | 25 | Basher | personal | personal combat | stagger bonus | 50% damage and longer stun duration with shield bashes. | Composite effect spans multiple classification categories. |
| One Handed | 175 | Stand United | party leader | party management | morale | 8 starting battle morale to troops in your party if you are outnumbered. | Outnumbered condition is not represented by current trigger_condition taxonomy. |
| Riding | 275 | The Way Of The Saddle | personal | movement | mount performance | 0.3 charge damage and maneuvering for every skill point above 250. | Composite effect spans multiple classification categories. |
| Steward | 100 | Paid in Promise | party leader | gold economy | recruitment cost | -25% companion wages and recruitment fees. | Composite effect spans companion wages and recruitment fees; single classification is partial. |
| Steward | 200 | Contractors | quartermaster | gold economy | wages | -25% wages and upgrade costs of the mercenary troops in your party. | Composite effect spans wages and upgrade costs for mercenary troops; single classification is partial. |
| Steward | 275 | Price of Loyalty | quartermaster | morale damage |  | -0.5% to food consumption, wages and combat related morale loss for each steward point above 250 in your party. | Composite effect spans multiple classification categories. |
| Tactics | 125 | Improviser | player | party management | morale | No morale penalty for disorganized state in battles, in sally out or when being attacked. | Effect removes morale penalty from disorganized state; battle escape is only an indirect source of the state. |
| Tactics | 200 | Encirclement | party leader | damage increase |  | 5% damage to outnumbered enemies when troops are sent to confront the enemy. | Outnumbered condition is not represented by current trigger_condition taxonomy. |
| Tactics | 250 | Counter Offensive | party leader | damage increase |  | 10% damage when troops are sent to confront the enemy while outnumbered. | Outnumbered condition is not represented by current trigger_condition taxonomy. |
| Throwing | 50 | Flexible Fighter | captain | troop combat | skill bonus | 15 Control skills of infantry, 15 Vigor skills of archers in your formation. | Troop skill bonus spans infantry Control and archer Vigor; not hero character growth. |
| Throwing | 225 | Long Reach | party leader | party management | morale | 20% morale and renown gained from battles won. | Composite effect spans multiple classification categories. |
| Trade | 275 | Man of Means | personal | gold economy | trade penalty reduction | -30% ransom cost for your freedom. | Ransom-cost reduction is not really a trade penalty; current subtype is a lossy fallback unless a ransom-cost subtype is added. |
| Two Handed | 200 | Reckless Charge | captain | troop combat | damage increase | 2% damage and movement speed to infantry in your formation. | Composite effect spans multiple classification categories. |
