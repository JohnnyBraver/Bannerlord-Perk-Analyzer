# Perk Investment Costs

Generated: 2026-05-31T20:49:49.583422+03:00

This report assigns a point-budget cost to every perk tier and starts the pragmatic review of perks above the focus-only line.

## Assumptions

- Baseline is `2` attribute and `0` focus in every skill.
- Focus-only means up to `5` focus with no purchased attribute points; that reaches skill `218`.
- Main cost is additive opportunity cost: `focus points spent + purchased attribute points * 4`.
- Raw allocation is also kept as `focus points spent + purchased attribute points`, because `3 attr / 5 focus` really means `1 attr + 5 focus` above the baseline.
- Level gate is still reported separately as `max(focus points spent, purchased attribute points * 4)`, but it is no longer the rating cost.
- Attribute points are broader than focus points. A Vigor point helps One Handed, Two Handed, and Polearm together, so build-level cost should count that attribute point once and share it across the pushed skills.
- Endurance-assisted rows use the planner's stretch mode for Athletics/Smithing permanent attribute perks. Treat them as build-context hints, not a default recommendation.

## Investment Categories

| Category | Meaning |
| --- | --- |
| Low | Focus-only from the practical 2-attribute floor. Covers every perk at or below level 200. |
| Medium | Requires attribute points, but the cheapest split stays at 3-5 attribute. Covers levels 225 and 250. |
| High | Requires pushing beyond 5 attribute. Covers level 275 perks and max-skill planning. |

## Tier Cost Reference

| Target | Category | Cheapest Split | Raw Allocation | Weighted Cost | Level Gate | Limit | Peak Learning Range |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 25 | low | 2 attr / 1 focus | 0 attr + 1 focus | 1 | 1 | 58 | 40 |
| 50 | low | 2 attr / 1 focus | 0 attr + 1 focus | 1 | 1 | 58 | 40 |
| 75 | low | 2 attr / 2 focus | 0 attr + 2 focus | 2 | 2 | 98 | 70 |
| 100 | low | 2 attr / 3 focus | 0 attr + 3 focus | 3 | 3 | 138 | 100 |
| 125 | low | 2 attr / 3 focus | 0 attr + 3 focus | 3 | 3 | 138 | 100 |
| 150 | low | 2 attr / 4 focus | 0 attr + 4 focus | 4 | 4 | 178 | 130 |
| 175 | low | 2 attr / 4 focus | 0 attr + 4 focus | 4 | 4 | 178 | 130 |
| 200 | low | 2 attr / 5 focus | 0 attr + 5 focus | 5 | 5 | 218 | 160 |
| 225 | medium | 3 attr / 5 focus | 1 attr + 5 focus | 9 | 5 | 232 | 170 |
| 250 | medium | 5 attr / 5 focus | 3 attr + 5 focus | 17 | 12 | 260 | 190 |
| 275 | high | 7 attr / 5 focus | 5 attr + 5 focus | 25 | 20 | 288 | 210 |
| 300 | high | 8 attr / 5 focus | 6 attr + 5 focus | 29 | 24 | 302 | 220 |
| max skill | high | 10 attr / 5 focus | 8 attr + 5 focus | 37 | 32 | 330 | 240 |

## Shared Attribute Examples

If several skills under the same attribute are pushed together, the attribute cost is paid once and the focus costs remain per skill.

| Attribute | Target | Skills | Shared Raw Allocation | Shared Weighted Cost | Isolated Weighted Cost | Savings | Per-Skill Weighted Cost |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: |
| Vigor | 225 | One Handed, Polearm, Two Handed | 1 attr + 15 focus | 19 | 27 | 8 | 6.333333 |
| Vigor | 250 | One Handed, Polearm, Two Handed | 3 attr + 15 focus | 27 | 51 | 24 | 9 |
| Vigor | 275 | One Handed, Polearm, Two Handed | 5 attr + 15 focus | 35 | 75 | 40 | 11.666667 |
| Control | 225 | Bow, Crossbow, Throwing | 1 attr + 15 focus | 19 | 27 | 8 | 6.333333 |
| Control | 250 | Bow, Crossbow, Throwing | 3 attr + 15 focus | 27 | 51 | 24 | 9 |
| Control | 275 | Bow, Crossbow, Throwing | 5 attr + 15 focus | 35 | 75 | 40 | 11.666667 |
| Endurance | 225 | Athletics, Riding, Smithing | 1 attr + 15 focus | 19 | 27 | 8 | 6.333333 |
| Endurance | 250 | Athletics, Riding, Smithing | 3 attr + 15 focus | 27 | 51 | 24 | 9 |
| Endurance | 275 | Athletics, Riding, Smithing | 5 attr + 15 focus | 35 | 75 | 40 | 11.666667 |
| Cunning | 225 | Roguery, Scouting, Tactics | 1 attr + 15 focus | 19 | 27 | 8 | 6.333333 |
| Cunning | 250 | Roguery, Scouting, Tactics | 3 attr + 15 focus | 27 | 51 | 24 | 9 |
| Cunning | 275 | Roguery, Scouting, Tactics | 5 attr + 15 focus | 35 | 75 | 40 | 11.666667 |
| Social | 225 | Charm, Leadership, Trade | 1 attr + 15 focus | 19 | 27 | 8 | 6.333333 |
| Social | 250 | Charm, Leadership, Trade | 3 attr + 15 focus | 27 | 51 | 24 | 9 |
| Social | 275 | Charm, Leadership, Trade | 5 attr + 15 focus | 35 | 75 | 40 | 11.666667 |
| Intelligence | 225 | Engineering, Medicine, Steward | 1 attr + 15 focus | 19 | 27 | 8 | 6.333333 |
| Intelligence | 250 | Engineering, Medicine, Steward | 3 attr + 15 focus | 27 | 51 | 24 | 9 |
| Intelligence | 275 | Engineering, Medicine, Steward | 5 attr + 15 focus | 35 | 75 | 40 | 11.666667 |

## Distribution

| Category | Perks | Share |
| --- | ---: | ---: |
| low | 285 | 76.2% |
| medium | 70 | 18.7% |
| high | 19 | 5.1% |

## Skills Above Focus-Only

These are the perk bands that require attribute investment under the baseline model.

| Attribute | Skill | Perks Above 200 | Main Extracted Effect Buckets |
| --- | --- | ---: | --- |
| Endurance | Athletics | 5 | food consumption (2), armor increase (2), stagger bonus (2), damage increase (1), skill bonus (1), fall (1) |
| Control | Bow | 5 | ammo capacity (2), unique (1), skill bonus (1), ranged accuracy (1), settlement income (1), movement speed (1) |
| Social | Charm | 4 | relationship (2), loyalty (1), renown (1), project effect (1), companion limit (1), influence (1) |
| Control | Crossbow | 5 | damage increase (2), dismount (1), projectile protection (1), ranged accuracy (1), wages (1), hit points (1) |
| Intelligence | Engineering | 5 | siege engines (3), siege camp speed (1), melee (1), loot bonus (1), armor increase (1), settlement income (1) |
| Social | Leadership | 5 | morale (4), party size (2), troop xp (1), clan party limit (1), companion limit (1) |
| Intelligence | Medicine | 5 | hit points (3), death avoidance (2), troop xp (1), damage resistance (1), regen bonus (1), prosperity (1) |
| Vigor | One Handed | 5 | damage increase (2), hit points (2), melee (1), armor penetration (1), recruitment cost (1), shields (1) |
| Vigor | Polearm | 5 | damage increase (3), charge (2), shields (1), speed bonus (1), weapon handling (1), skill bonus (1) |
| Endurance | Riding | 5 | armor increase (3), prisoners (2), recruitment bonus (1), wages (1), stagger bonus (1), mount performance (1) |
| Cunning | Roguery | 5 | trade penalty reduction (1), militia gain (1), stagger bonus (1), food reserve (1), speed bonus (1), damage increase (1) |
| Cunning | Scouting | 5 | damage increase (3), party vision (2), prisoners (2), regen bonus (1), party speed (1) |
| Endurance | Smithing | 5 | melee (2), attribute point (1), focus point (1), crafting quality (1) |
| Intelligence | Steward | 5 | carrying capacity (2), trade penalty reduction (2), food consumption (2), project effect (1), wages (1), morale damage (1) |
| Cunning | Tactics | 5 | damage increase (6), influence (2), security (1) |
| Control | Throwing | 5 | projectile speed (3), damage increase (2), armor penetration (2), utility (1), morale (1), shields (1) |
| Social | Trade | 7 | recruitment cost (2), trade penalty reduction (2), barter (1), build speed (1), wages (1), persuasion cost (1) |
| Vigor | Two Handed | 3 | damage increase (3), attack speed (2), armor penetration (1) |

## Endurance Stretch Snapshot

Single-skill targets rarely justify Endurance detours on additive cost alone. The value is mostly build-wide: free Vigor/Control/Endurance points get much better when several skills in those attributes are being pushed together.

| Target | No Endurance Weighted Cost | Stretch Weighted Cost | Delta | Level Gate Delta | Stretch Plan |
| --- | ---: | ---: | ---: | ---: | --- |
| Athletics:225 | 9 | 5 | -4 | +0 | Athletics 175 |
| Bow:225 | 9 | 9 | +0 | +0 | no endurance bonuses |
| Crossbow:225 | 9 | 9 | +0 | +0 | no endurance bonuses |
| One Handed:225 | 9 | 9 | +0 | +0 | no endurance bonuses |
| Polearm:225 | 9 | 9 | +0 | +0 | no endurance bonuses |
| Riding:225 | 9 | 9 | +0 | +0 | no endurance bonuses |
| Smithing:225 | 9 | 9 | +0 | +0 | no endurance bonuses |
| Throwing:225 | 9 | 9 | +0 | +0 | no endurance bonuses |
| Two Handed:225 | 9 | 9 | +0 | +0 | no endurance bonuses |
| Athletics:250 | 17 | 13 | -4 | -4 | Athletics 175 |
| Bow:250 | 17 | 17 | +0 | +0 | no endurance bonuses |
| Crossbow:250 | 17 | 17 | +0 | +0 | no endurance bonuses |
| One Handed:250 | 17 | 17 | +0 | +0 | no endurance bonuses |
| Polearm:250 | 17 | 17 | +0 | +0 | no endurance bonuses |
| Riding:250 | 17 | 17 | +0 | +0 | no endurance bonuses |
| Smithing:250 | 17 | 13 | -4 | -4 | Smithing 225 stretch |
| Throwing:250 | 17 | 17 | +0 | +0 | no endurance bonuses |
| Two Handed:250 | 17 | 17 | +0 | +0 | no endurance bonuses |
| Athletics:275 | 25 | 21 | -4 | -4 | Athletics 175 |
| Bow:275 | 25 | 25 | +0 | +0 | no endurance bonuses |
| Crossbow:275 | 25 | 25 | +0 | +0 | no endurance bonuses |
| One Handed:275 | 25 | 25 | +0 | +0 | no endurance bonuses |
| Polearm:275 | 25 | 25 | +0 | +0 | no endurance bonuses |
| Riding:275 | 25 | 24 | -1 | -4 | Athletics 175 |
| Smithing:275 | 25 | 20 | -5 | -8 | Athletics 175 + Smithing 225 stretch |
| Throwing:275 | 25 | 25 | +0 | +0 | no endurance bonuses |

## Above Focus-Only Perks

| Attribute | Skill | Level | Category | Raw Allocation | Weighted Cost | Level Gate | Perk | Effects | Math Notes |
| --- | --- | ---: | --- | --- | ---: | ---: | --- | --- | --- |
| Control | Bow | 225 | medium | 1 attr + 5 focus | 9 | 5 | Deep Quivers | personal: 3 extra arrows per quiver. / party leader: 1 extra arrow per quiver to troops in your party. |  |
| Control | Bow | 225 | medium | 1 attr + 5 focus | 9 | 5 | Horse Master | personal: You can now use all bows on horseback. / captain: 30 bow skill to horse archers in your formation |  |
| Control | Bow | 250 | medium | 3 attr + 5 focus | 17 | 12 | Quick Draw | personal: 25% aiming speed with bows. / governor: 5% tax gain in the governed settlement. | 25% over 17 weighted cost (1.470588% per cost) / 5% over 17 weighted cost (0.294118% per cost) |
| Control | Bow | 250 | medium | 3 attr + 5 focus | 17 | 12 | Ranger's Swiftness | personal: Equipped bows do not slow you down. / governor: 20% security provided by archers in the governed settlement. | 20% over 17 weighted cost (1.176471% per cost) |
| Control | Bow | 275 | high | 5 attr + 5 focus | 25 | 20 | Deadshot | personal: 0.2% reload speed with bows for every skill point above 200. / personal: 0.5% damage with bows for every skill point above 200. | small high-tier numeric effect (0.2%, 0.008% per weighted cost) / small high-tier numeric effect (0.5%, 0.02% per weighted cost) |
| Control | Crossbow | 225 | medium | 1 attr + 5 focus | 9 | 5 | Hammer Bolts | personal: Crossbows can now dismount and ignore 50% dismount resistance on attacks against cavalry. / captain: 10% damage with crossbows by troops in your formation. | 50% over 9 weighted cost (5.555556% per cost) / 10% over 9 weighted cost (1.111111% per cost) |
| Control | Crossbow | 225 | medium | 1 attr + 5 focus | 9 | 5 | Pavise | personal: 75% chance of blocking projectiles from behind with a shield on your back. / governor: 30% accuracy to ballistas in the governed settlement. | 75% over 9 weighted cost (8.333333% per cost) / 30% over 9 weighted cost (3.333333% per cost) |
| Control | Crossbow | 250 | medium | 3 attr + 5 focus | 17 | 12 | Picked Shots | party leader: -50% wages of tier 4+ ranged troops. / party leader: 5 hit points to ranged troops in your party. | -50% over 17 weighted cost (2.941176% per cost) |
| Control | Crossbow | 250 | medium | 3 attr + 5 focus | 17 | 12 | Terror | party leader: 20% chance of increasing the siege bombardment casualties per hit by 1. / captain: 25% morale loss to enemy due to crossbow kills by troops in your formation. | 20% over 17 weighted cost (1.176471% per cost) / 25% over 17 weighted cost (1.470588% per cost) |
| Control | Crossbow | 275 | high | 5 attr + 5 focus | 25 | 20 | Mighty Pull | personal: 0.2% reload speed with crossbows for every skill point above 200. / personal: 0.5% damage with crossbows for every skill point above 200. | small high-tier numeric effect (0.2%, 0.008% per weighted cost) / small high-tier numeric effect (0.5%, 0.02% per weighted cost) |
| Control | Throwing | 225 | medium | 1 attr + 5 focus | 9 | 5 | Long Reach | personal: You can pick up items from the ground while mounted. / party leader: 20% morale and renown gained from battles won. | 20% over 9 weighted cost (2.222222% per cost) |
| Control | Throwing | 225 | medium | 1 attr + 5 focus | 9 | 5 | Perfect Technique | personal: 25% travel speed to your throwing weapons. / captain: 10% travel speed to throwing weapons of troops in your formation. | 25% over 9 weighted cost (2.777778% per cost) / 10% over 9 weighted cost (1.111111% per cost) |
| Control | Throwing | 250 | medium | 3 attr + 5 focus | 17 | 12 | Impale | personal: Javelins you throw can penetrate shields. / captain: 10% damage with throwing weapons by troops in your formation. | 10% over 17 weighted cost (0.588235% per cost) |
| Control | Throwing | 250 | medium | 3 attr + 5 focus | 17 | 12 | Weak Spot | personal: 30% armor penetration with throwing weapons. / captain: 10% armor penetration with throwing weapons by troops in your formation. | 30% over 17 weighted cost (1.764706% per cost) / 10% over 17 weighted cost (0.588235% per cost) |
| Control | Throwing | 275 | high | 5 attr + 5 focus | 25 | 20 | Unstoppable Force | personal: 0.2% travel speed to your throwing weapons for every skill point above 200. / personal: 0.5% damage with throwing weapons for every skill point above 200. | small high-tier numeric effect (0.2%, 0.008% per weighted cost) / small high-tier numeric effect (0.5%, 0.02% per weighted cost) |
| Cunning | Roguery | 225 | medium | 1 attr + 5 focus | 9 | 5 | Arms Dealer | party leader: -20% sell price penalty for weapons. / governor: 200% militia per day in the besieged governed settlement. | -20% over 9 weighted cost (2.222222% per cost) / 200% over 9 weighted cost (22.222222% per cost) |
| Cunning | Roguery | 225 | medium | 1 attr + 5 focus | 9 | 5 | Dirty Fighting | personal: 50% stun duration for kicking. / governor: 2 random food item will be smuggled to the besieged governed settlement. | 50% over 9 weighted cost (5.555556% per cost) |
| Cunning | Roguery | 250 | medium | 3 attr + 5 focus | 17 | 12 | Dash and Slash | personal: 50% damage bonus from speed while on foot. / captain: 2% two handed weapon damage by troops in your formation. | 50% over 17 weighted cost (2.941176% per cost) / small attribute-gated numeric effect (2%, 0.117647% per weighted cost) |
| Cunning | Roguery | 250 | medium | 3 attr + 5 focus | 17 | 12 | Fleet Footed | personal: 10% combat movement speed while no weapons or shields are equipped. / personal: 30% escape chance when imprisoned by mobile parties. | 10% over 17 weighted cost (0.588235% per cost) / 30% over 17 weighted cost (1.764706% per cost) |
| Cunning | Roguery | 275 | high | 5 attr + 5 focus | 25 | 20 | Rogue Extraordinaire | personal: 1% loot amount for every skill point above 200. | small high-tier numeric effect (1%, 0.04% per weighted cost) |
| Cunning | Scouting | 225 | medium | 1 attr + 5 focus | 9 | 5 | Keen Sight | scout: -50% sight penalty for traveling in forests. / party leader: -50% chance of prisoner lords escaping from your party. | -50% over 9 weighted cost (5.555556% per cost) / -50% over 9 weighted cost (5.555556% per cost) |
| Cunning | Scouting | 225 | medium | 1 attr + 5 focus | 9 | 5 | Vantage Point | scout: 25% sight range when stationary for at least an hour. / party leader: 10 prisoner limit. | 25% over 9 weighted cost (2.777778% per cost) |
| Cunning | Scouting | 250 | medium | 3 attr + 5 focus | 17 | 12 | Rearguard | party leader: 20% wounded troop recovery speed while in an army. / party leader: 10% damage by your troops when defending at your siege camp. | 20% over 17 weighted cost (1.176471% per cost) / 10% over 17 weighted cost (0.588235% per cost) |
| Cunning | Scouting | 250 | medium | 3 attr + 5 focus | 17 | 12 | Vanguard | party leader: 5% damage by your troops when they are sent as attackers. / party leader: 10% damage by your troops when they are sent to sally out. | 5% over 17 weighted cost (0.294118% per cost) / 10% over 17 weighted cost (0.588235% per cost) |
| Cunning | Scouting | 275 | high | 5 attr + 5 focus | 25 | 20 | Uncanny Insight | scout: 0.1% party speed for every skill point above 200 scouting skill. | small high-tier numeric effect (0.1%, 0.004% per weighted cost) |
| Cunning | Tactics | 225 | medium | 1 attr + 5 focus | 9 | 5 | Besieged | player: 10% damage while besieged when troops are sent to confront the enemy. / personal: 50% influence gain from winning sieges. | 10% over 9 weighted cost (1.111111% per cost) / 50% over 9 weighted cost (5.555556% per cost) |
| Cunning | Tactics | 225 | medium | 1 attr + 5 focus | 9 | 5 | Pre Battle Maneuvers | player: 25% influence gain from winning battles. / party leader: 1% damage per 100 skill difference with the enemy when troops are sent to confront the enemy. | 25% over 9 weighted cost (2.777778% per cost) / small attribute-gated numeric effect (1%, 0.111111% per weighted cost) |
| Cunning | Tactics | 250 | medium | 3 attr + 5 focus | 17 | 12 | Counter Offensive | party leader: 10% damage when troops are sent to confront the attacking enemy in a field battle. / party leader: 10% damage when troops are sent to confront the enemy while outnumbered. | 10% over 17 weighted cost (0.588235% per cost) / 10% over 17 weighted cost (0.588235% per cost) |
| Cunning | Tactics | 250 | medium | 3 attr + 5 focus | 17 | 12 | Gens d'armes | captain: 2% damage to infantry by cavalry troops in your formation. / governor: 1 daily security in the governed settlement. | small attribute-gated numeric effect (2%, 0.117647% per weighted cost) |
| Cunning | Tactics | 275 | high | 5 attr + 5 focus | 25 | 20 | Tactical Mastery | army leader: 0.5% damage for every skill point above 200 tactics skill when troops are sent to confront the enemy. | small high-tier numeric effect (0.5%, 0.02% per weighted cost) |
| Endurance | Athletics | 225 | medium | 1 attr + 5 focus | 9 | 5 | Strong Arms | personal: 5% damage with throwing weapons. / captain: 20 throwing skill to troops in your formation. | 5% over 9 weighted cost (0.555556% per cost) |
| Endurance | Athletics | 225 | medium | 1 attr + 5 focus | 9 | 5 | Strong Legs | personal: -50% fall damage taken and +100% kick damage dealt. / governor: -20% food consumption in the governed settlement while under siege. | -50% over 9 weighted cost (5.555556% per cost) / -20% over 9 weighted cost (2.222222% per cost) |
| Endurance | Athletics | 250 | medium | 3 attr + 5 focus | 17 | 12 | Ignore Pain | personal: 10% armor while on foot. / captain: 5 armor to all equipped armor pieces of foot troops in your formation. | 10% over 17 weighted cost (0.588235% per cost) |
| Endurance | Athletics | 250 | medium | 3 attr + 5 focus | 17 | 12 | Spartan | personal: 50% resistance to getting staggered while on foot. / party leader: -20% food consumption in your party. | 50% over 17 weighted cost (2.941176% per cost) / -20% over 17 weighted cost (1.176471% per cost) |
| Endurance | Athletics | 275 | high | 5 attr + 5 focus | 25 | 20 | Mighty Blow | personal: You stun your enemies longer after they block your attack. / personal: 1 hit points for every skill point above 250. | small high-tier numeric effect (5%, 0.2% per weighted cost) |
| Endurance | Riding | 225 | medium | 1 attr + 5 focus | 9 | 5 | Cavalry Tactics | clan leader: 30% volunteering rate of cavalry troops in the settlements governed by your clan. / governor: -50% wages of mounted troops in the governed settlement. | 30% over 9 weighted cost (3.333333% per cost) / -50% over 9 weighted cost (5.555556% per cost) |
| Endurance | Riding | 225 | medium | 1 attr + 5 focus | 9 | 5 | Mounted Patrols | party leader: -50% escape chance to prisoners in your party. / governor: -50% escape chance to prisoners in the governed settlement. | -50% over 9 weighted cost (5.555556% per cost) / -50% over 9 weighted cost (5.555556% per cost) |
| Endurance | Riding | 250 | medium | 3 attr + 5 focus | 17 | 12 | Dauntless Steed | personal: 50% resistance to getting staggered while mounted. / captain: 5 armor to all equipped armor pieces of mounted troops in your formation. | 50% over 17 weighted cost (2.941176% per cost) |
| Endurance | Riding | 250 | medium | 3 attr + 5 focus | 17 | 12 | Tough Steed | personal: 20% armor to your mount. / captain: 10 armor to mounts of troops in your formation. | 20% over 17 weighted cost (1.176471% per cost) |
| Endurance | Riding | 275 | high | 5 attr + 5 focus | 25 | 20 | The Way Of The Saddle | personal: 0.3 charge damage and maneuvering for every skill point above 250. |  |
| Endurance | Smithing | 225 | medium | 1 attr + 5 focus | 9 | 5 | Enduring Smith | personal: 1 Endurance attribute. |  |
| Endurance | Smithing | 225 | medium | 1 attr + 5 focus | 9 | 5 | Fencer Smith | personal: 1 Focus Point to One Handed and Two Handed. |  |
| Endurance | Smithing | 250 | medium | 3 attr + 5 focus | 17 | 12 | Sharpened Edge | personal: 2% swing damage of crafted weapons. | small attribute-gated numeric effect (2%, 0.117647% per weighted cost) |
| Endurance | Smithing | 250 | medium | 3 attr + 5 focus | 17 | 12 | Sharpened Tip | personal: 2% thrust damage of crafted weapons. | small attribute-gated numeric effect (2%, 0.117647% per weighted cost) |
| Endurance | Smithing | 275 | high | 5 attr + 5 focus | 25 | 20 | Legendary Smith | personal: 5% greater chance of creating Legendary weapons, chance increases by 1% for every 5 skill points above 275. | small high-tier numeric effect (5%, 0.2% per weighted cost) |
| Intelligence | Engineering | 225 | medium | 1 attr + 5 focus | 9 | 5 | Improved Tools | engineer: 20% siege camp preparation speed. / captain: 5% melee damage by troops in your formation. | 20% over 9 weighted cost (2.222222% per cost) / 5% over 9 weighted cost (0.555556% per cost) |
| Intelligence | Engineering | 225 | medium | 1 attr + 5 focus | 9 | 5 | Metallurgy | engineer: 30% chance to remove negative modifiers on looted items. / captain: 5 armor to all equipped armor pieces of troops in your formation. | 30% over 9 weighted cost (3.333333% per cost) |
| Intelligence | Engineering | 250 | medium | 3 attr + 5 focus | 17 | 12 | Architectural Commissions | engineer: 25% reload speed to mangonels and trebuchets in siege bombardment. / governor: 20 gold per day for continuous projects in the governed settlement. | 25% over 17 weighted cost (1.470588% per cost) |
| Intelligence | Engineering | 250 | medium | 3 attr + 5 focus | 17 | 12 | Clockwork | engineer: 25% reload speed to ballistas during siege bombardment. / governor: 20% effect from boosting projects in the governed town. | 25% over 17 weighted cost (1.470588% per cost) / 20% over 17 weighted cost (1.176471% per cost) |
| Intelligence | Engineering | 275 | high | 5 attr + 5 focus | 25 | 20 | Masterwork | engineer: 1% damage for each engineering skill point over 250 for siege engines in siege bombardment. | small high-tier numeric effect (1%, 0.04% per weighted cost) |
| Intelligence | Medicine | 225 | medium | 1 attr + 5 focus | 9 | 5 | Cheat Death | personal: Cheat death due to old age once. / surgeon: -50% chance to die when you fall unconscious in battle. | -50% over 9 weighted cost (5.555556% per cost) |
| Intelligence | Medicine | 225 | medium | 1 attr + 5 focus | 9 | 5 | Fortitude Tonic | party leader: 10 hit points to other heroes in your party. / personal: 5 hit points. |  |
| Intelligence | Medicine | 250 | medium | 3 attr + 5 focus | 17 | 12 | Battle Hardened | surgeon: 25 experience to wounded units at the end of the battle. / governor: -25% siege attrition loss in the governed settlement. | -25% over 17 weighted cost (1.470588% per cost) |
| Intelligence | Medicine | 250 | medium | 3 attr + 5 focus | 17 | 12 | Helping Hands | surgeon: 2% troop recovery rate for every 10 troop in your party. / governor: -50% prosperity loss from starvation. | small attribute-gated numeric effect (2%, 0.117647% per weighted cost) / -50% over 17 weighted cost (2.941176% per cost) |
| Intelligence | Medicine | 275 | high | 5 attr + 5 focus | 25 | 20 | Minister of Health | personal: 1 hit point to troops for every skill point above 250. |  |
| Intelligence | Steward | 225 | medium | 1 attr + 5 focus | 9 | 5 | Arenicos' Horses | quartermaster: 10% carrying capacity for troops in your party. / personal: -20% trade penalty for trading mounts. | 10% over 9 weighted cost (1.111111% per cost) / -20% over 9 weighted cost (2.222222% per cost) |
| Intelligence | Steward | 225 | medium | 1 attr + 5 focus | 9 | 5 | Arenicos' Mules | quartermaster: 20% carrying capacity for pack animals in your party. / quartermaster: -20% trade penalty for trading pack animals. | 20% over 9 weighted cost (2.222222% per cost) / -20% over 9 weighted cost (2.222222% per cost) |
| Intelligence | Steward | 250 | medium | 3 attr + 5 focus | 17 | 12 | Master of Planning | quartermaster: -40% food consumption while your party is in a siege camp. / governor: 20% effectiveness to continuous projects in the governed settlement. | -40% over 17 weighted cost (2.352941% per cost) / 20% over 17 weighted cost (1.176471% per cost) |
| Intelligence | Steward | 250 | medium | 3 attr + 5 focus | 17 | 12 | Master of Warcraft | quartermaster: -25% troop wages while your party is in a siege camp. / governor: -5% food consumption of town population in the governed settlement. | -25% over 17 weighted cost (1.470588% per cost) / -5% over 17 weighted cost (0.294118% per cost) |
| Intelligence | Steward | 275 | high | 5 attr + 5 focus | 25 | 20 | Price of Loyalty | quartermaster: -0.5% to food consumption, wages and combat related morale loss for each steward point above 250 in your party. / governor: 0.5% tax income for each skill point above 200 in the governed settlement | small high-tier numeric effect (-0.5%, 0.02% per weighted cost) / small high-tier numeric effect (0.5%, 0.02% per weighted cost) |
| Social | Charm | 225 | medium | 1 attr + 5 focus | 9 | 5 | Parade | personal: 5 loyalty bonus to settlement while waiting in the settlement. / party leader: 5% daily chance to gain +1 relationship with a random lord in the same army. | 5% over 9 weighted cost (0.555556% per cost) |
| Social | Charm | 225 | medium | 1 attr + 5 focus | 9 | 5 | Public Speaker | party leader: 30% renown gain from battles. / governor: 10% effect from forums, marketplaces and festivals. | 30% over 9 weighted cost (3.333333% per cost) / 10% over 9 weighted cost (1.111111% per cost) |
| Social | Charm | 250 | medium | 3 attr + 5 focus | 17 | 12 | Camaraderie | personal: Double the relation gain for helping lords in battle. / clan leader: 1 companion limit | 200% over 17 weighted cost (11.764706% per cost) |
| Social | Charm | 275 | high | 5 attr + 5 focus | 25 | 20 | Immortal Charm | personal: 5 influence per day. |  |
| Social | Leadership | 225 | medium | 1 attr + 5 focus | 9 | 5 | Great Leader | army leader: 5 battle morale to troops at the beginning of a battle. / party leader: 5 battle morale to troops that are of same culture as you. |  |
| Social | Leadership | 225 | medium | 1 attr + 5 focus | 9 | 5 | Make a Difference | personal: 100% battle morale to troops when you kill an enemy in battle. / party leader: 10% shared experience for archers. | 100% over 9 weighted cost (11.111111% per cost) / 10% over 9 weighted cost (1.111111% per cost) |
| Social | Leadership | 250 | medium | 3 attr + 5 focus | 17 | 12 | Talent Magnet | party leader: 10 party size limit. / clan leader: 1 clan party limit. |  |
| Social | Leadership | 250 | medium | 3 attr + 5 focus | 17 | 12 | We Pledge our Swords | personal: 1 companion limit. / party leader: 1 battle morale at the beginning of the battle for each tier 6 troop in the party up to 10 morale. |  |
| Social | Leadership | 275 | high | 5 attr + 5 focus | 25 | 20 | Ultimate Leader | party leader: 1 party size for each leadership point above 250. |  |
| Social | Trade | 225 | medium | 1 attr + 5 focus | 9 | 5 | Self-made Man | personal: -50% barter penalty for items. / governor: 30% build speed for marketplace, kiln and aqueduct projects. | -50% over 9 weighted cost (5.555556% per cost) / 30% over 9 weighted cost (3.333333% per cost) |
| Social | Trade | 225 | medium | 1 attr + 5 focus | 9 | 5 | Sword For Barter | personal: -20% hiring costs of mercenary troops. / quartermaster: -15% caravan guard wages. | -20% over 9 weighted cost (2.222222% per cost) / -15% over 9 weighted cost (1.666667% per cost) |
| Social | Trade | 250 | medium | 3 attr + 5 focus | 17 | 12 | Silver Tongue | personal: -15% gold required while persuading lords to defect to your faction. / quartermaster: 15% better trade deals from caravans and villagers | -15% over 17 weighted cost (0.882353% per cost) / 15% over 17 weighted cost (0.882353% per cost) |
| Social | Trade | 250 | medium | 3 attr + 5 focus | 17 | 12 | Spring of Gold | clan leader: 0.1% denars of interest income per day based on your current denars up to 1000 denars. / governor: 20% effect from boosting projects in the governed settlement. | small attribute-gated numeric effect (0.1%, 0.005882% per weighted cost) / 20% over 17 weighted cost (1.176471% per cost) |
| Social | Trade | 275 | high | 5 attr + 5 focus | 25 | 20 | Man of Means | clan leader: -20% costs of recruiting minor faction clans into your clan. / personal: -30% ransom cost for your freedom. | -20% over 25 weighted cost (0.8% per cost) / -30% over 25 weighted cost (1.2% per cost) |
| Social | Trade | 275 | high | 5 attr + 5 focus | 25 | 20 | Trickle Down | party leader: 1 relationship with merchants if 10.000 or more denars are spent on a single deal. / governor: 2 daily prosperity while building a project in the governed settlement. |  |
| Social | Trade | 300 | high | 6 attr + 5 focus | 29 | 24 | Everything Has a Price | personal: You can now trade settlements in barter. |  |
| Vigor | One Handed | 225 | medium | 1 attr + 5 focus | 9 | 5 | Deadly Purpose | personal: 5% damage with one handed weapons. / captain: 10% melee weapon damage by infantry in your formation. | 5% over 9 weighted cost (0.555556% per cost) / 10% over 9 weighted cost (1.111111% per cost) |
| Vigor | One Handed | 225 | medium | 1 attr + 5 focus | 9 | 5 | Unwavering Defense | personal: 5 hit points. / party leader: 10 hit points to infantry in your party. |  |
| Vigor | One Handed | 250 | medium | 3 attr + 5 focus | 17 | 12 | Chink in the Armor | personal: 10% armor penetration with melee attacks. / party leader: -20% recruitment cost of infantry. | 10% over 17 weighted cost (0.588235% per cost) / -20% over 17 weighted cost (1.176471% per cost) |
| Vigor | One Handed | 250 | medium | 3 attr + 5 focus | 17 | 12 | Prestige | personal: 50% damage against shields with one handed weapons. / party leader: 15 party limit. | 50% over 17 weighted cost (2.941176% per cost) |
| Vigor | One Handed | 275 | high | 5 attr + 5 focus | 25 | 20 | Way of the Sword | personal: 0.2% attack speed with one handed weapons for every skill point above 250. / personal: 0.5% damage with one handed weapons for every skill point above 250. | small high-tier numeric effect (0.2%, 0.008% per weighted cost) / small high-tier numeric effect (0.5%, 0.02% per weighted cost) |
| Vigor | Polearm | 225 | medium | 1 attr + 5 focus | 9 | 5 | Sure Footed | personal: -40% charge damage taken. / captain: -30% charge damage taken by troops in your formation. | -40% over 9 weighted cost (4.444444% per cost) / -30% over 9 weighted cost (3.333333% per cost) |
| Vigor | Polearm | 225 | medium | 1 attr + 5 focus | 9 | 5 | Unstoppable Force | personal: Triple couch lance damage against shields. / captain: 30% damage bonus from speed with polearms to cavalry in your formation. | 300% over 9 weighted cost (33.333333% per cost) / 30% over 9 weighted cost (3.333333% per cost) |
| Vigor | Polearm | 250 | medium | 3 attr + 5 focus | 17 | 12 | Counterweight | personal: 15% handling of swingable polearms. / captain: 20 polearm skill to troops in your formation. | 15% over 17 weighted cost (0.882353% per cost) |
| Vigor | Polearm | 250 | medium | 3 attr + 5 focus | 17 | 12 | Sharpen the Tip | personal: 5% damage with thrust attacks made with polearms. / captain: 5% damage with thrust attacks by infantry troops in your formation. | 5% over 17 weighted cost (0.294118% per cost) / 5% over 17 weighted cost (0.294118% per cost) |
| Vigor | Polearm | 275 | high | 5 attr + 5 focus | 25 | 20 | Way of the Spear | personal: 0.2% attack speed with polearms for every skill point above 250. / personal: 0.5% damage with polearms for every skill point above 250. | small high-tier numeric effect (0.2%, 0.008% per weighted cost) / small high-tier numeric effect (0.5%, 0.02% per weighted cost) |
| Vigor | Two Handed | 225 | medium | 1 attr + 5 focus | 9 | 5 | Blade Master | personal: 10% damage with two handed weapons. / captain: 2% attack speed to infantry in your formation. | 10% over 9 weighted cost (1.111111% per cost) / small attribute-gated numeric effect (2%, 0.222222% per weighted cost) |
| Vigor | Two Handed | 225 | medium | 1 attr + 5 focus | 9 | 5 | Vandal | personal: 25% armor penetration with your attacks. / captain: 20% damage against destructible objects by troops in your formation. | 25% over 9 weighted cost (2.777778% per cost) / 20% over 9 weighted cost (2.222222% per cost) |
| Vigor | Two Handed | 250 | medium | 3 attr + 5 focus | 17 | 12 | Way Of The Great Axe | personal: 0.2% attack speed with two handed weapons for every skill point above 250. / personal: 0.5% damage with two handed weapons for every skill point above 250. | small attribute-gated numeric effect (0.2%, 0.011765% per weighted cost) / small attribute-gated numeric effect (0.5%, 0.029412% per weighted cost) |

## Outputs

- JSON: `Data\generated\perk-investment-costs.json`
- Report: `Data\generated\reports\perk-investment-costs.md`
