# Party Management Perks

This note covers perks whose main job is keeping the party moving, supplied, trainable, recruitable, and controllable. It focuses especially on party speed and troop XP, because those effects are easy to misread from the perk text alone.

For troop category wording, read this together with `troop-category-counting.md`: "archers in your party" and "ranged troops" are troop categories, not companion skill checks.

## Main Takeaways

- Party management is role-sensitive. Scout perks can come from the assigned scout, quartermaster perks from the quartermaster, surgeon perks from the surgeon, and many other effects require the party leader.
- Party speed is mostly about removing penalties. The best speed perks are often the ones that counter wounded troops, overburden, herding, forests, night travel, or bad terrain.
- Troop XP has three different flows: direct battle XP, shared XP, and passive/event XP. They should not be evaluated as one generic "training" number.
- Shared XP is capacity-based. Stacks that still need XP toward an upgrade can absorb it; stacks already capped for upgrades stop being useful sinks.
- Passive daily XP is good background pressure, but high-level battle kills and post-battle percentage perks are the faster way to grow troops.

## Party Speed

Party speed perks mostly live in Scouting, Riding, Athletics, and Medicine.

### Base Speed Formula

The extracted campaign-map speed model starts with party size, not unit tier:

```text
baseSpeed = 4 * (200 / (200 + totalMenCount))^0.4
```

Then the model adds percentage factors for cavalry, foot troops riding spare mounts, cargo, wounded, prisoners, morale, terrain, weather, perks, and other temporary states. A noble cavalryman and a low-tier cavalryman both count as mounted for the party-speed composition bonus; the model is checking mounted/foot composition, not individual troop quality.

Base speed by party size before composition bonuses:

| Men in party | Base speed |
| ---: | ---: |
| 20 | 3.850 |
| 50 | 3.658 |
| 100 | 3.401 |
| 150 | 3.198 |
| 200 | 3.031 |
| 300 | 2.773 |

### Composition Bonuses

For clean land movement, the important composition factors are:

```text
cavalryBonus = 0.30 * mountedTroops / totalMen
mountedFootmenBonus = 0.15 * mountedFootmen / totalMen
Strong = 0.05 * footTroops / totalMen
NomadicTraditions = 0.30 * mountedFootmenBonus
```

`mountedFootmen` means foot troops covered by available spare mounts. The game uses available mounts up to the number of foot troops, so extra horses beyond that do not keep increasing the mounted-footmen speed bonus.

For a 100-man party on clean terrain:

| Party setup | Factor | Speed |
| --- | ---: | ---: |
| 100 infantry, no spare mounts | 1.000 | 3.401 |
| 100 infantry, spare mounts | 1.150 | 3.911 |
| 100 infantry, spare mounts, `Strong` | 1.200 | 4.081 |
| 100 infantry, spare mounts, `Strong`, `Nomadic Traditions` | 1.245 | 4.234 |
| 100 cavalry | 1.300 | 4.421 |

So your hunch is right: infantry with enough horses and the relevant speed perks is not far behind pure cavalry. In this clean example the fully supported infantry party is about `95.8%` as fast as the all-cavalry party.

Mixed 100-man examples, assuming every foot soldier has a spare mount and the party has both `Strong` and `Nomadic Traditions`:

| Cavalry | Foot troops | Speed factor | Speed |
| ---: | ---: | ---: | ---: |
| 0 | 100 | 1.245 | 4.234 |
| 25 | 75 | 1.259 | 4.281 |
| 50 | 50 | 1.272 | 4.328 |
| 75 | 25 | 1.286 | 4.375 |
| 100 | 0 | 1.300 | 4.421 |

Bad weather narrows this even more because the model applies a weather penalty to the cavalry and mounted-footmen composition bonuses. `Strong` and the `Nomadic Traditions` add-on are not reduced in that same branch, so in bad-weather land movement the all-infantry-with-horses setup is almost equal to all cavalry.

Forests can flip the comparison. Forest terrain applies a `-30%` speed factor, but `Forest Kin` reduces that to `-15%` if at least 75% of the party is infantry. In a 100-man forest example, all cavalry is roughly `3.401`, while infantry with spare mounts, `Strong`, `Nomadic Traditions`, and `Forest Kin` is roughly `3.724`.

| Problem | Skill | Level | Perk | Role | Effect | Read |
| --- | --- | ---: | --- | --- | --- | --- |
| Day travel | Scouting | 25 | `Day Traveler` | scout | +2% travel speed during daytime | Small but always useful if the party travels mostly by day. |
| Night travel | Scouting | 25 | `Night Runner` | scout | +5% travel speed during nighttime | Larger number, but only for night movement. |
| Plains/steppes | Scouting | 50 | `Pathfinder` | scout | +2% travel speed on steppes and plains | Good general terrain coverage. |
| Deserts/dunes | Scouting | 75 | `Desert Born` | scout | +5% travel speed on deserts and dunes | Strong in Aserai-heavy routes. |
| Forest infantry | Scouting | 75 | `Forest Kin` | scout | -50% forest speed penalty if the party is at least 75% infantry | Excellent for infantry-heavy armies in forest regions. |
| High morale | Scouting | 100 | `Forced March` | scout | +2.5% travel speed when morale is above 75 | Good if food variety and victories keep morale high. |
| Overburden | Scouting | 100 | `Unburdened` | scout | -20% overburden penalty | Better if the party often hauls loot over capacity. |
| Chasing | Scouting | 125 | `Tracker` | scout | +2% travel speed while following a hostile party | Helps catch targets, not general travel. |
| High Scouting | Scouting | 275 | `Uncanny Insight` | scout | +0.1% party speed per Scouting point above 200 | +7.5% at 275, +13% at 330. Great if the scout is already extreme. |
| Wounded troops | Medicine | 75 | `Sledges` | surgeon | -50% party speed penalty from wounded | A huge comfort perk after hard battles. |
| Foot troops | Athletics | 200 | `Strong` | party leader | +5% party speed by foot troops | Good for infantry-heavy parties. |
| Overburden | Athletics | 175 | `Energetic` | party leader | -20% overburdened speed penalty | Stacks conceptually with better capacity discipline. |
| Footmen on horses | Riding | 75 | `Nomadic Traditions` | party leader | +30% party speed bonus from footmen on horses | Strong when carrying spare mounts for infantry. |
| Flat speed | Riding | 100 | `Sweeping Wind` | party leader | +2% party speed | Simple, unconditional party-leader speed. |
| Herding | Riding | 175 | `Shepherd` | party leader | -50% herding speed penalty | Very good for loot-heavy horse/animal runs. |

### Speed Build Read

The clean speed core is a real scout plus practical logistics:

- Scouting 25-125 gives the most direct campaign-map speed controls.
- Medicine 75 is easy to undervalue because it only matters after casualties, but wounded-speed penalties are painful exactly when the party is vulnerable.
- Riding 75 and Riding 175 are excellent if the party carries many horses or herd animals.
- Overburden perks help, but the better long-term answer is enough carry capacity and fewer inventory mistakes.
- High Scouting 275 is a real speed payoff, but it is a high-investment scout endpoint rather than a casual pickup.

## Troop XP Mechanics

### Direct Battle XP

The extracted battle troop XP reward uses the killed unit's internal character level:

```text
troopBattleXpReward = (killedCharacter.Level + 6)^2 / 3
```

This is not the in-game upgrade tier. Visible troop tiers normally end at tier 6; `CharacterObject.Level` is a separate game-data value used by XP, power, and other formulas. The rows below are sample character levels, not tier numbers.

| Killed unit character level | XP reward |
| ---: | ---: |
| 1 | 16 |
| 6 | 48 |
| 11 | 96 |
| 16 | 161 |
| 21 | 243 |
| 26 | 341 |

This is why fighting stronger enemies trains troops so much faster than farming very low-tier parties. The reward grows roughly quadratically with target character level.

### Shared XP

Shared XP is not handed out evenly. `PartyAddSharedXp` distributes it according to remaining upgrade capacity:

```text
sharedXpCapacity = remaining XP needed by stacks that can still upgrade
sharedXpAddedToStack = floor(max(1, remainingSharedXp * stackCapacity / remainingCapacity))
```

Practical consequences:

- A troop stack that already has enough XP to upgrade stops being a good shared-XP sink.
- Upgrading troops promptly keeps the party's XP capacity open.
- Mixed parties can absorb shared XP more smoothly than a party where every eligible stack is already capped.
- Weapon and armor donation perks feed into shared party XP, so they follow this same capacity logic.

### Upgrade Costs

Upgrade costs are tier-based:

| Target tier step | XP cost |
| ---: | ---: |
| 1 or lower | 100 |
| 2 | 300 |
| 3 | 550 |
| 4 | 900 |
| 5 | 1300 |
| 6 | 1700 |
| 7 | 2100 |

The game sums tier steps when it needs the cost from the current troop tier to the target tier.

## Troop XP Perks

### Passive Daily Training

These are the background drip-feed perks.

| Skill | Level | Perk | Role | Effect | Best target |
| --- | ---: | --- | --- | --- | --- |
| Leadership | 25 | `Combat Tips` | party leader | +2 XP per day to all troops | Broad early training. |
| Leadership | 25 | `Raise The Meek` | party leader | +4 XP per day to tier 1 and 2 troops | Better for fresh recruits. |
| Steward | 50 | `Drill Sergeant` | quartermaster | +2 XP per day to all troops | Broad quartermaster training. |
| Steward | 50 | `Seven Veterans` | quartermaster | +4 XP per day to tier 4+ troops | Better for high-tier maintenance. |
| One Handed | 150 | `Military Tradition` | party leader | +2 daily XP to infantry | Infantry parties. |
| Bow | 125 | `Trainer` | party leader | +3 daily XP to archers/ranged troops | Archer parties. |
| Crossbow | 100 | `Renowned Marksmen` | party leader | +2 daily XP to ranged troops | Ranged parties. |
| Athletics | 150 | `Walk It Off` | party leader | +3 daily XP to foot troops while traveling | Infantry-heavy travel. |
| Athletics | 150 | `A Good Days Rest` | party leader | +10 daily XP to foot troops while waiting in settlements | Strong if the party often rests in towns. |
| Scouting | 100 | `Forced March` | party leader | +2 XP per day to all troops while traveling with morale above 75 | Pairs with the speed effect. |
| Scouting | 100 | `Unburdened` | party leader | +2 XP per day to all troops while overburdened | A consolation prize for overloaded travel. |
| Throwing | 125 | `Saddlebags` | party leader | +1 daily XP to infantry | Small infantry trickle. |
| Polearm | 200 | `Drills` | party leader | +0.1 daily XP to troops | Appears bugged/no-op for party XP: the helper rounds perk XP to an integer, so `0.1` becomes `0`. Avoid unless valuing the governor militia-quality side. |

Daily training is best when it targets the troops you are actually carrying. It is not a replacement for fighting useful battles.

### Battle And Post-Battle XP Bonuses

These perks improve XP generated by battles or specific combat outcomes.

| Skill | Level | Perk | Role | Effect | Notes |
| --- | ---: | --- | --- | --- | --- |
| One Handed | 100 | `Trainer` | party leader | +5% XP to melee troops after every battle | Good early melee-party bonus. |
| Two Handed | 75 | `Baptised in Blood` | party leader | +5% XP to melee troops after every battle | Alternative melee-party bonus. |
| One Handed | 150 | `Corps-a-corps` | party leader | +10% of total XP gained as bonus XP to infantry after battles | Strong for infantry parties. |
| One Handed | 175 | `Lead by example` | party leader | +5% XP to troops after battle | Broad but later. |
| Bow | 200 | `Bulls Eye` | party leader | +10% battle XP to ranged troops | Good archer-party payoff. |
| Crossbow | 175 | `Mounted Crossbowman` | party leader | +5% XP to ranged troops | Ranged-party bonus attached to a strong personal unlock. |
| Throwing | 200 | `Resourceful` | party leader | +10% battle XP to troops equipped with throwing weapons | Applies by equipment, not by generic ranged category. |
| Roguery | 25 | `No Rest for the Wicked` | party leader | +20% XP gain for bandits | Excellent if running bandit troops. |
| Leadership | 200 | `Trusted Commander` | party leader | +20% XP when troops are sent to confront the enemy | Simulation/auto-resolve, not live battle. |
| Medicine | 250 | `Battle Hardened` | surgeon | +25 XP to wounded units at battle end | High-tier surgeon payoff. |
| Engineering | 200 | `Apprenticeship` | engineer | +5 XP to troops when a siege engine is built | Siege-specific trickle. |

The key split is live battle versus simulation. `Trusted Commander` is for "troops are sent to confront the enemy", so it belongs with simulation behavior, not normal live-battle training.

### Shared Battle XP Perks

These are Leadership perks that specifically improve shared XP from battles:

| Skill | Level | Perk | Role | Effect | Notes |
| --- | ---: | --- | --- | --- | --- |
| Leadership | 125 | `Leader of the Masses` | party leader | +5% experience from battles shared with the party | Broad shared-XP boost. |
| Leadership | 200 | `Lead by Example` | party leader | +10% shared XP for cavalry troops | Cavalry-focused shared XP. |
| Leadership | 225 | `Make a Difference` | party leader | +10% shared XP for archers | Archer-focused shared XP. |

These are strongest when the matching troop stacks still have upgrade capacity. If the cavalry or archer stack is already upgrade-ready, the value is partly wasted until it is upgraded.

### Recruitment And Donation XP

| Skill | Level | Perk | Role | Effect | Notes |
| --- | ---: | --- | --- | --- | --- |
| Leadership | 100 | `Famous Commander` | personal | +200 XP to troops on recruitment | Makes new recruits arrive closer to upgrade-ready. |
| Steward | 100 | `Paid in Promise` | quartermaster | Donated/discarded armor gives troop XP | Converts armor loot into shared training. |
| Steward | 125 | `Giving Hands` | quartermaster | Donated/discarded weapons give troop XP | Converts weapon loot into shared training. |
| Two Handed | 75 | `Baptised in Blood` | personal | +5 XP to infantry in your party for each suitable two-handed player kill | The IL applies this to every infantry troop stack on fatal suitable two-handed hits. |

Donation XP is especially interesting because it turns loot into upgrade pressure. The exact item-value/tier formula still deserves a dedicated read, but the path is connected to shared party XP distribution.

## Other Party Management Knobs

### Carrying Capacity

| Skill | Level | Perk | Role | Effect |
| --- | ---: | --- | --- | --- |
| Trade | 50 | `Caravan Master` | quartermaster | +30% carrying capacity for the party. |
| Riding | 75 | `Deeper Sacks` | party leader | +20% carrying capacity for pack animals. |
| Scouting | 175 | `Beast Whisperer` | party leader | +10% carrying capacity for pack animals. |
| Steward | 200 | `Forced Labor` | quartermaster | Prisoners provide carry capacity as standard troops. |
| Steward | 225 | `Arenicos' Horses` | quartermaster | +10% carrying capacity for troops. |
| Steward | 225 | `Arenicos' Mules` | quartermaster | +20% carrying capacity for pack animals. |

Capacity indirectly protects party speed because it prevents overburden penalties from appearing in the first place.

### Food And Morale

| Skill | Level | Perk | Role | Effect |
| --- | ---: | --- | --- | --- |
| Steward | 25 | `Warrior's Diet` | quartermaster | -10% food consumption. |
| Steward | 25 | `Warrior's Diet` | party leader | No morale penalty from having one food type. |
| Steward | 75 | `Stiff Upper Lip` | quartermaster | -10% food consumption while in an army. |
| Steward | 125 | `Logistician` | quartermaster | +4 morale when mounts outnumber foot troops. |
| Steward | 175 | `Gourmet` | quartermaster | Doubles morale bonus from diverse food. |
| Steward | 175 | `Sound Reserves` | quartermaster | -10% food consumption during sieges. |
| Steward | 250 | `Master of Planning` | quartermaster | -40% food consumption while in a siege camp. |
| Athletics | 250 | `Spartan` | party leader | -20% food consumption. |

Food management feeds speed indirectly through morale. `Forced March` wants morale above 75, so morale perks and food variety can become speed support.

### Party Size, Companions, And Clan Parties

| Skill | Level | Perk | Role | Effect |
| --- | ---: | --- | --- | --- |
| Athletics | 75 | `Imposing Stature` | party leader | +5 party size. |
| Bow | 100 | `Merry Men` | party leader | +5 party size. |
| Leadership | 75 | `Authority` | party leader | +5 party size. |
| Leadership | 175 | `Uplifting Spirit` | party leader | +10 party size. |
| Leadership | 250 | `Talent Magnet` | party leader | +10 party size. |
| Leadership | 275 | `Ultimate Leader` | party leader | +1 party size per Leadership point above 250. |
| One Handed | 250 | `Prestige` | party leader | +15 party limit. |
| Tactics | 75 | `Horde Leader` | party leader | +10 party size. |
| Charm | 250 | `Camaraderie` | clan leader | +1 companion limit. |
| Leadership | 250 | `We Pledge our Swords` | personal | +1 companion limit. |
| Leadership | 250 | `Talent Magnet` | clan leader | +1 clan party limit. |

Leadership remains the main party-size tree. The weapon-tree size perks are useful, but they are expensive if the weapon skill is not already part of the build.

### Prisoners And Recruitment

| Skill | Level | Perk | Role | Effect |
| --- | ---: | --- | --- | --- |
| Leadership | 50 | `Fervent Attacker` | party leader | +50% recruitment rate for tier 1-3 prisoners. |
| Leadership | 50 | `Stout Defender` | party leader | +50% recruitment rate for tier 4+ prisoners. |
| Leadership | 100 | `Loyalty and Honor` | party leader | +30% faster non-bandit prisoner recruitment. |
| Roguery | 100 | `Promises` | party leader | +30% bandit prisoner recruitment. |
| Leadership | 200 | `Lead by Example` | party leader | +50% infantry prisoner recruitment. |
| Leadership | 200 | `Trusted Commander` | party leader | +50% ranged prisoner recruitment. |
| Athletics | 75 | `Stamina` | party leader | +5 prisoner limit and -10% prisoner escape chance. |
| Riding | 225 | `Mounted Patrols` | party leader | -50% prisoner escape chance. |
| Scouting | 225 | `Keen Sight` | party leader | -50% chance of prisoner lords escaping. |
| Scouting | 225 | `Vantage Point` | party leader | +10 prisoner limit. |

The high-value prisoner-retention package is Riding 225 plus Scouting 225, but that is a serious investment. For normal runs, Leadership and Roguery prisoner recruitment choices matter earlier.

## Practical Training Plans

For fresh recruits:

- `Raise The Meek` is better than `Combat Tips` while the party is full of tier 1 and 2 troops.
- `Famous Commander` makes recruitment itself produce immediate upgrade pressure.
- Fight stronger enemies once the recruits can survive; battle XP is the main accelerator.

For infantry:

- Daily stack: `Military Tradition`, `Walk It Off` or `A Good Days Rest`, `Saddlebags`, and broad Leadership/Steward training.
- Battle stack: One Handed `Trainer`, Two Handed `Baptised in Blood`, `Corps-a-corps`, and player-kill `Baptised in Blood` if the main hero is a two-handed killer.

For ranged troops:

- Daily stack: Bow `Trainer`, Crossbow `Renowned Marksmen`, and broad Leadership/Steward training.
- Battle stack: Bow `Bulls Eye`, Crossbow `Mounted Crossbowman`, and Leadership `Make a Difference` for shared archer XP.

For cavalry:

- Cavalry has less passive daily support than infantry/ranged.
- Leadership `Lead by Example` is the clean shared-XP cavalry boost.
- Speed support from Riding and spare mounts tends to be part of the same build identity.

For bandit parties:

- Roguery `No Rest for the Wicked` is the central training perk.
- Roguery `Promises` and `Two Faced` help make bandit recruitment and conversion less awkward.

## Open Follow-Ups

- Decode the exact discarded weapon/armor XP formula behind `Giving Hands` and `Paid in Promise`.
- Turn the extracted campaign-map speed model into a generated report/calculator so cargo, prisoners, terrain, morale, herd penalties, wounded troops, and weather can be compared without hand math.
- Build a troop-training calculator that estimates time-to-upgrade from passive daily XP, shared XP capacity, and expected battle kills.
