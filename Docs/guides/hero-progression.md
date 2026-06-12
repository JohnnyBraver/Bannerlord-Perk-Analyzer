# Hero Progression Guide



---

## 1. XP and Character Level Mechanics

Bannerlord tracks character progression on two separate ledgers every time a skill-related action occurs. 

### The Dual-Ledger System
Whenever a character exercises a skill, the game processes the raw experience points ($XP$) into two destinations:
1. **Character Total XP**: Raw $XP$ is rounded and added directly to the main character level pool (through `GainRawXp`). This is only done if the event is focus-affected (`isAffectedByFocusFactor = true`).
2. **Skill Stored XP**: The experience that increases the specific skill level. It is modified by multipliers:
   $$\text{Skill XP Added} = \text{Raw XP} \times \text{Generic XP Multiplier} \times \text{Learning Rate}$$

> [!IMPORTANT]
> Because learning rates, focus points, and attributes only apply to the **Skill Stored XP** ledger, they do not increase the rate at which you gain main character levels. A high learning rate makes your skills grow faster, but not your main character level. Conversely, exercising a skill that has hit its learning limit (0 learning rate) will still feed your main character level as long as the event is focus-affected.

### Character Level Thresholds
The experience required to level up your main character level is cumulative and grows quadratically. The cumulative raw-XP threshold for each level is calculated as follows:
- Level 1 threshold = 1
- Level 2 threshold = 1,001
- For each subsequent level:
  $$\text{Next Level Delta} = \text{Current Level Delta} + 1000 + \lfloor\text{Current Level Delta} / 5\rfloor$$
  $$\text{Next Threshold} = \text{Previous Threshold} + \text{Next Level Delta}$$

Here are sample thresholds for main character levels:

| Character Level | Cumulative Raw XP Required | XP Needed From Previous Level |
| :--- | ---: | ---: |
| **2** | 1,001 | 1,000 |
| **5** | 12,209 | 5,368 |
| **10** | 79,784 | 20,795 |
| **15** | 285,123 | 59,183 |
| **20** | 833,261 | 154,704 |
| **25** | 2,234,392 | 392,390 |
| **30** | 5,758,047 | 983,831 |
| **40** | 36,510,511 | 6,117,572 |
| **50** | 227,181,147 | 37,904,341 |
| **62** | 2,027,685,990 | 337,998,478 |

> [!TIP]
> Since main levels are driven by raw XP before learning rates are applied, big raw-XP eventsג€”such as high-damage melee hits, long-distance headshots, and expensive crafting itemsג€”are the fastest ways to level up your main character.

---

## 2. Combat and Activity XP Formulas

### Combat Hit XP
Melee and ranged combat experience starts from the base hit formula:
$$\text{Base XP} = 0.4 \times (\text{Attacker Power} + 0.5) \times (\text{Target Power} + 0.5) \times \text{Effective Damage} \times \text{Mission Multiplier}$$

* **Target Power**: The internal strength value of the defender's troop tier. Fighting higher-tier units yields significantly more experience.
* **Effective Damage**: 
  - On non-fatal hits: The actual damage dealt (capped at target's remaining HP).
  - On fatal hits: $\text{Damage Dealt (up to max HP)} + \text{Target Max HP}$.
  - Stacking lethal hits is highly rewarded; a one-shot kill on a full-health target counts as double the target's HP in the formula.

#### Mission Multipliers
The type of combat scenario heavily scales the experience awarded:
- **Battle (Campaign Field Battles)**: $1.0\times$
- **Simulation Battle (Autoresolve)**: $0.9\times$
- **Tournament**: $0.33\times$
- **Practice Fight**: $0.0625\times$

### Ranged Shot Difficulty
Ranged attacks apply a multiplier based on the difficulty of the shot:
$$\text{Raw Difficulty} = 0.3 \times \frac{\text{Distance} + 4}{4} \times \frac{4 + \text{Lateral Motion} \times \text{Relative Speed}}{4}$$
$$\text{Shot Difficulty} = \text{Clamp}(\text{Raw Difficulty}, 1, 12)$$

* **Relative Speed**: Target speed relative to attacker.
* **Lateral Motion**: Perpendicular component of movement against the shot line.
* **Headshot Bonus**: Headshots multiply the clamped difficulty by $1.2\times$ (capping at $14.4$).

This difficulty is converted into an XP factor:
$$\text{Shot Difficulty Factor} = \text{Lerp}\left(0, 2, \frac{\text{Clamp}(\text{Shot Difficulty}, 1, 14.4) - 1}{13.4}\right)$$
$$\text{Final Ranged XP} = \text{Base XP} \times (1 + \text{Skill Factor} \times \text{Shot Difficulty Factor})$$
* **Skill Factor**: $0.5$ for Bow, and $1.0$ for Crossbow/Throwing.

### Mounted Riding XP
Riding experience is gained alongside hit experience when mounted:
$$\text{Riding XP} = \text{Base XP} \times (1 + \text{Horse Difficulty} \times 0.02)$$

### Non-Combat XP Ratios
* **Smithing**: Driven entirely by the market value of the output item:
  - Smelting and Free Build: $\text{XP} = 0.02 \times \text{Item Market Value}$
  - Crafting Orders: $\text{XP} = 0.10 \times \text{Item Market Value}$ (Five times faster)
  - Refining: $\text{XP} = 0.30 \times \text{Produced Material Value} \times \text{Count}$
* **Troop Training (Steward/Leadership)**: Daily flat values from training perks.

---

## 3. Passive and Semi-Passive XP Channels

Passive and semi-passive XP channels run continuously in the background as you travel, rest, or manage your clan's assets.

### Stewardship - Food Consumption
Steward XP is awarded daily to the party's assigned **Quartermaster** based on food consumption and variety.
$$\text{Steward XP} = \text{Round}(\text{Daily Food Consumption} \times 100) \times \frac{\text{Food Variety} - 2}{3}$$
* **Prerequisites**: The party must have an active Quartermaster, must not be starving, and must carry **strictly more than 3 unique food types** ($\text{Food Variety} > 3$). If variety is 3 or less, Steward XP is $0$.
> [!WARNING]
> **The Food Upkeep XP Trap**: Perks that reduce party food consumption (such as Steward 25 `Warrior's Diet` or other consumption discounts) directly reduce the daily food consumption rate. Because Steward XP scales on the volume of food consumed, **food upkeep reductions directly slow down your Steward XP gain**.
* **Calradic Diet**: There are exactly 9 unique consumable food items in Bannerlord: *Grain, Fish, Meat, Butter, Cheese, Grapes, Olives, Dates, and Beer*. Stacking all 9 types applies a $2.33\times$ multiplier to the XP pulse, while carrying only 4 types reduces the multiplier to $0.67\times$.

### Stewardship - Town/Castle Governance
Companions or family members assigned as governors of town or castle fiefs earn Steward XP daily.
$$\text{Steward XP} = \text{Prosperity Change} \times 30$$
* **Prosperity Constraint**: Steward XP is only awarded when the settlement's daily prosperity growth is positive ($\Delta P > 0$). Negative or stagnant growth yields $0$ Steward XP.
* **Governor Restriction**: **The player character cannot govern settlements**. Therefore, this governance XP pathway is only available for training companions and family members.

### Scouting - Campaign Map Traversal
Scouting XP is awarded in periodic pulses as your party moves across the campaign map.
$$\text{Scouting XP} = \text{Speed} \times \left(1.0 + \text{PartySize}^{0.66}\right) \times \text{TerrainMultiplier}$$
* **Prerequisites**: Party movement speed must be strictly greater than $1.0$, and the calculated XP pulse must be **$\ge 5.0$** to be awarded. Pulses below $5.0$ are discarded.
* **Terrain Multiplier**:
  - **0.25** for difficult terrains (Forest, Snow, Desert, Mountain).
  - **0.15** for normal terrains (Plains, Steppes).
> [!IMPORTANT]
> **The Small Party Scouting Penalty**: Because of the $5.0$ XP minimum threshold, tiny parties (especially solo heroes) on clean terrain often receive **zero Scouting XP** because their pulse values fail to reach $5.0$. Larger parties scale the pulse value, making Scouting much easier to train. Caravan parties also have their final Scouting XP halved ($0.5\times$).

### Medicine - Passive Healing (Town Resting)
Passive healing of wounded troops in your party yields Medicine XP.
* **The Town Resting Multiplier**: Waiting inside a **Town** (non-castle settlement) multiplies the passive healing Medicine XP by **$2.0\times$**. Resting in castles or in the open field (by camping/waiting) awards only the base $1.0\times$ rate.

### Medicine - Doctor's Oath (Combat Wounding)
The Medicine 75 perk `Doctor's Oath` applies your Surgeon survival calculations to enemy casualties as well as your own.
* **XP Harvesting**: Because you wound rather than kill a massive portion of enemy armies, you heal them post-battle. Every check triggers `OnSurgeryApplied`, awarding:
  - **$+10 \times \text{Troop Tier}$** XP per enemy saved (wounded).
  - **$+5 \times \text{Troop Tier}$** XP per enemy killed.
  This turns combat into a massive accelerator for Medicine XP.

### Athletics - Campaign Foot Travel
Traveling on the campaign map on foot (without a mount equipped in your character's active horse slot) awards passive Athletics XP:
$$\text{Athletics XP} = 1 + \text{RoundRandomized}(\text{Speed} \times 0.2)$$

> [!TIP]
> **Stealth/Crouching Kills XP Boost**: Performing kills while sneaking (crouched) in active missions awards a massive multiplier of XP to **Athletics** and **One-Handed** combat skills. This is commonly exploited in the repeatable stealth training tutorial early in the campaign to power-level these skills quickly by repeatedly executing guards and retreating/resetting the scenario before completion.

### Riding - Campaign Map Quirk
> [!NOTE]
> **Riding Map Travel Quirk**: Riding on the campaign map while mounted awards exactly **$0$ Riding XP**. Unlike Athletics, there is no map travel XP hook in the Riding code; Riding XP can only be earned in active combat missions or tournaments (by hitting targets while mounted or moving at high speed).

---

## 4. Learning Limits and Point Budgets

Attributes and focus points determine where your learning rate falls to zero.

### The Math of Limits
Every skill in Bannerlord uses the exact same formulas to resolve learning limits:
$$\text{Skill Limit} = 4 + 14 \times (\text{Attribute} - 1) + 40 \times \text{Focus}$$
$$\text{Peak Learning Range} = 10 \times (\text{Attribute} - 1) + 30 \times \text{Focus}$$

* **Skill Limit**: The exact skill level where your learning rate reaches $0.00$. You cannot raise a skill past this number.
* **Peak Learning Range**: The skill level where the over-limit penalty begins. Past this point, your learning rate starts decaying.

### The Skill Limit Grid
The table below displays the maximum skill level attainable for any combination of Attribute (1ג€“10) and Focus Points (0ג€“5). The format is **Limit (Peak Learning Range)**:

| Attribute | Focus 0 | Focus 1 | Focus 2 | Focus 3 | Focus 4 | Focus 5 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 4 (0) | 44 (30) | 84 (60) | 124 (90) | 164 (120) | 204 (150) |
| **2** | 18 (10) | 58 (40) | 98 (70) | 138 (100) | 178 (130) | 218 (160) |
| **3** | 32 (20) | 72 (50) | 112 (80) | 152 (110) | 192 (140) | 232 (170) |
| **4** | 46 (30) | 86 (60) | 126 (90) | 166 (120) | 206 (150) | 246 (180) |
| **5** | 60 (40) | 100 (70) | 140 (100) | 180 (130) | 220 (160) | 260 (190) |
| **6** | 74 (50) | 114 (80) | 154 (110) | 194 (140) | 234 (170) | 274 (200) |
| **7** | 88 (60) | 128 (90) | 168 (120) | 208 (150) | 248 (180) | **288 (210)** |
| **8** | 102 (70) | 142 (100) | 182 (130) | 222 (160) | 262 (190) | **302 (220)** |
| **9** | 116 (80) | 156 (110) | 196 (140) | 236 (170) | **276 (200)** | **316 (230)** |
| **10** | 130 (90) | 170 (120) | 210 (150) | 250 (180) | **290 (210)** | **330 (240)** |

* **Bold cells** indicate build combinations capable of unlocking the final level 275 perk tier ($\text{Limit} \ge 275$).

### Minimum Target Splits
To reach specific perk tiers with the minimum point waste, use these optimized splits:
- **Level 25**: 2 Attribute + 1 Focus
- **Level 50**: 2 Attribute + 1 Focus
- **Level 75**: 2 Attribute + 2 Focus
- **Level 100**: 2 Attribute + 3 Focus
- **Level 125**: 2 Attribute + 3 Focus
- **Level 150**: 2 Attribute + 4 Focus
- **Level 175**: 2 Attribute + 4 Focus
- **Level 200**: 2 Attribute + 5 Focus
- **Level 225**: 3 Attribute + 5 Focus
- **Level 250**: 5 Attribute + 5 Focus
- **Level 275**: 7 Attribute + 5 Focus
- **Level 300**: 8 Attribute + 5 Focus
- **Level 330**: 10 Attribute + 5 Focus

### Alternative Splits (Attribute and Focus Trade-offs)
In multi-skill builds, you may have high attributes that allow you to reach your target perk level with fewer focus points. Below are all combinations that satisfy each skill target tier:

* **Level 25**: 2 Attribute + 1 Focus | 3 Attribute + 0 Focus
* **Level 50**: 2 Attribute + 1 Focus | 5 Attribute + 0 Focus
* **Level 75**: 2 Attribute + 2 Focus | 4 Attribute + 1 Focus | 7 Attribute + 0 Focus
* **Level 100**: 2 Attribute + 3 Focus | 3 Attribute + 2 Focus | 5 Attribute + 1 Focus | 8 Attribute + 0 Focus
* **Level 125**: 2 Attribute + 3 Focus | 4 Attribute + 2 Focus | 7 Attribute + 1 Focus | 10 Attribute + 0 Focus
* **Level 150**: 2 Attribute + 4 Focus | 3 Attribute + 3 Focus | 6 Attribute + 2 Focus | 9 Attribute + 1 Focus
* **Level 175**: 2 Attribute + 4 Focus | 5 Attribute + 3 Focus | 8 Attribute + 2 Focus
* **Level 200**: 2 Attribute + 5 Focus | 4 Attribute + 4 Focus | 7 Attribute + 3 Focus | 10 Attribute + 2 Focus
* **Level 225**: 3 Attribute + 5 Focus | 6 Attribute + 4 Focus | 9 Attribute + 3 Focus
* **Level 250**: 5 Attribute + 5 Focus | 8 Attribute + 4 Focus | 10 Attribute + 3 Focus
* **Level 275**: 7 Attribute + 5 Focus | 9 Attribute + 4 Focus
* **Level 300**: 8 Attribute + 5 Focus
* **Level 330**: 10 Attribute + 5 Focus

### Player Point Budget & Cost Model
Every character level up gives you 1 Focus Point. Every 4 character levels give you 1 Attribute Point. 
To evaluate builds, we use a **Weighted Opportunity Cost Formula**:
$$\text{Weighted Cost} = \text{Focus Points Spent} + (\text{Purchased Attribute Points} \times 4)$$

> [!TIP]
> Attribute points are highly efficient when shared. For example, spending 1 point to raise Cunning from 2 to 3 costs 4 weighted points, but it simultaneously increases the skill limit of Scouting, Tactics, and Roguery by 14 points each. Plan your builds around attribute groups rather than single skills.

---

## 5. Early Splash Perks (Low Investment)

At the baseline of **2 Attribute and 1 Focus Point**, any skill will reach a limit of **58**. This is a highly efficient way to grab the first two perk tiers (level 25 and 50) of multiple skills.

### High-Value Utility Splashes
1. **Trade (Level 50)**:
   - **Level 25**: `Appraiser` or `Whole Seller` (Profits are highlighted green/red in the trade UI; Appraiser reduces equipment trade penalty, Whole Seller reduces trade goods penalty).
   - **Level 50**: `Caravan Master` (Marks item prices relative to average; gives Quartermaster $+30\%$ party carrying capacity).
   - *Result*: Dramatically reduces friction when buying food, selling combat loot, or trading.
2. **Medicine (Level 50)**:
   - **Level 25**: `Preventive Medicine` ($+5$ personal HP and heals $30\%$ of lost HP immediately after battle).
   - **Level 50**: `Walk It Off` ($+15\%$ healing rate while moving on map; heals $+10$ personal HP after offensive battles).
   - *Result*: Massive personal survivability and minimal downtime when roaming and fighting.
3. **Steward (Level 50)**:
   - **Level 25**: `Warrior's Diet` (Reduces food consumption by $10\%$ and removes morale penalties from single-food parties).
   - **Level 50**: `Drill Sergeant` (Adds $+2$ daily experience to all troops in your party).
4. **Scouting (Level 50)**:
   - **Level 25**: `Day Traveler` ($+2\%$ daytime map speed).
   - **Level 50**: `Pathfinder` ($+2\%$ travel speed on steppes and plains; chance to gain relation with a notable when entering towns).
   - **Level 50**: `Water Diviner` ($+10\%$ sight range on steppes and plains; chance to gain relation with a notable when entering villages).
5. **Leadership (Level 50)**:
   - **Level 25**: `Combat Tips` ($+2$ daily experience to all troops in your party).
   - **Level 25**: `Raise The Meek` ($+4$ daily experience to Tier 1-2 troops, or $+3$ daily XP to garrison troops as governor).
6. **Athletics (Level 50)**:
   - **Level 25**: `Well Built` ($+5$ personal HP and $+5$ HP to foot troops in party).
   - **Level 50**: `Form Fitting Armor` (Reduces equipped armor weight by $15\%$, improving combat movement speed).
7. **Riding (Level 50)**:
   - **Level 25**: `Nimble Steed` (Increases mount maneuverability by $10\%$).
   - **Level 50**: `Well Strapped` (Reduces mount lameness/death chance by $50\%$ from fall damage).

---

## 6. Combat Tree Highlights



### Direct Skill Passive Scaling
Even before perks are unlocked, raising your weapon skill levels provides passive bonuses:

| Weapon Skill | Passive Benefit per Level | Passives at +80 Skill Level |
| :--- | :--- | :--- |
| **One Handed** | $+0.07\%$ Weapon Speed, $+0.15\%$ Damage | $+5.6\%$ Speed, $+12.0\%$ Damage |
| **Two Handed** | $+0.06\%$ Weapon Speed, $+0.16\%$ Damage | $+4.8\%$ Speed, $+12.8\%$ Damage |
| **Polearm** | $+0.06\%$ Weapon Speed, $+0.07\%$ Damage | $+4.8\%$ Speed, $+5.6\%$ Damage |
| **Bow** | $+0.11\%$ Damage, $+0.09\%$ Accuracy | $+8.8\%$ Damage, $+7.2\%$ Accuracy |
| **Crossbow** | $+0.07\%$ Reload Speed, $+0.05\%$ Accuracy | $+5.6\%$ Reload, $+4.0\%$ Accuracy |
| **Throwing** | $+0.07\%$ Draw Speed, $+0.06\%$ Damage, $+0.06\%$ Accuracy | $+5.6\%$ Draw, $+4.8\%$ Damage, $+4.8\%$ Accuracy |

---

### Melee Tree Highlights (Vigor)

#### One Handed
* **Level 25** - `Wrapped Handles`: $+20\%$ handling (weapon swing recovery). Highly noticeable.
* **Level 50** - `Swift Strike`: $+2\%$ one-handed swing speed.
* **Level 75** - `Shield Bearer`: Removes the movement speed penalty from equipped shields.
* **Level 100** - `Duelist`: $+20\%$ melee damage when fighting without a shield. Great for high-damage dueling.
* **Level 200** - `Fleet of Foot`: $+4\%$ combat movement speed, or $+4\%$ movement speed to infantry in your formation.
* **Level 225** - `Deadly Purpose`: $+5\%$ one-handed weapon damage, or $+10\%$ melee weapon damage by infantry in your formation.
* **Level 250** - `Chink in the Armor`: $+10\%$ melee armor penetration. Strongly improves damage against heavy units.
* **Level 250** - `Prestige`: $+50\%$ damage against shields with one-handed weapons, or $+15$ party limit.
* **Level 275** - `Way of the Sword`: At 330 skill, yields $+16\%$ attack speed and $+40\%$ One Handed damage.

#### Two Handed
* **Level 25** - `Strong Grip`: $+10\%$ personal weapon handling, or $+30$ Two Handed skill to infantry in your formation.
* **Level 25** - `Wood Chopper`: $+30\%$ personal shield damage, or $+15\%$ shield damage by troops in your formation.
* **Level 50** - `Head Basher`: $+10\%$ blunt damage with two-handed weapons.
* **Level 50** - `On the Edge`: $+3\%$ personal two-handed swing speed, or $+2\%$ infantry swing speed.
* **Level 75** - `Show of Strength`: Two-handed weapons that can knock down ignore $30\%$ knockdown resistance on swing attacks.
* **Level 100** - `Beast Slayer`: $+50\%$ damage against mounts.
* **Level 125** - `Berserker`: Deal $+20\%$ damage when below $50\%$ health.
* **Level 125** - `Confidence`: $+15\%$ damage when your character HP is above $90\%$.
* **Level 150** - `Projectile Deflection`: Allows blocking projectiles with two-handed swords. Defining defensive tool, but it requires a higher investment than the level 100 utility tier.
* **Level 175** - `Hope`: Friendly troop morale effect from your two-handed kills, or $+5$ party size.
* **Level 175** - `Terror`: Enemy morale effect from your two-handed kills, or $+10$ prisoner capacity.
* **Level 200** - `Reckless Charge`: $+20\%$ personal speed-damage bonus on foot, or $+2\%$ infantry damage and movement speed.
* **Level 200** - `Thick Hides`: $+5$ personal HP, or $+5$ HP to troops in your party.
* **Level 225** - `Vandal`: $+25\%$ personal armor penetration, or $+20\%$ damage to destructible objects by troops in your formation.
* **Level 225** - `Blade Master`: $+10\%$ personal two-handed damage, or $+2\%$ attack speed to infantry in your formation.
* **Level 250** - `Way Of The Great Axe`: *Note: the scaling formula only starts above 250.* At 330 skill, yields $+16\%$ speed and $+40\%$ damage.

#### Polearm
* **Level 25** - `Pikeman`: $+2\%$ polearm damage on foot, or $+2\%$ infantry polearm damage in your formation.
* **Level 50** - `Keep at Bay`: Polearm thrusts have a chance to push back enemies.
* **Level 75** - `Clean Thrust`: $+10\%$ thrust damage. Paired with `Guards` ($+50\%$ headshot damage) makes spear thrusts lethal.
* **Level 75** - `Swift Swing`: $+5\%$ swing speed. Mandatory for swingable polearms (glaives/menavlions).
* **Level 100** - `Footwork`: $+2\%$ combat speed while holding a polearm, or $+2\%$ movement speed to infantry in your formation.
* **Level 125** - `Lancer`: $+20\%$ mounted speed-damage bonus with polearms.
* **Level 125** - `Steed Killer`: Dismounts enemies on successful thrust attacks.
* **Level 150** - `Skewer`: $30\%$ chance to keep couch lance active after hitting.
* **Level 175** - `Phalanx`: $+30$ melee weapon skills to troops in your party while in shield wall formation, or $+3\%$ polearm damage by troops in your formation.
* **Level 175** - `Standard Bearer`: Increases party morale in battles.
* **Level 250** - `Counterweight`: $+15\%$ handling with swingable polearms, or $+20$ Polearm skill to troops in your formation.
* **Level 250** - `Sharpen the Tip`: $+5\%$ thrust damage, or $+5\%$ thrust damage by infantry in your formation.
* **Level 275** - `Way of the Spear`: Pushes limits of polearm combat stats.

---

### Ranged Tree Highlights (Control)

#### Bow
* **Level 25** - `Bow Control`: Reduces movement accuracy penalty by $30\%$.
* **Level 25** - `Dead Aim`: $+30\%$ headshot damage.
* **Level 50** - `Bodkin`: $+10\%$ personal armor penetration with bows, or $+5\%$ bow armor penetration by troops in your formation.
* **Level 50** - `Nocking Point`: Reloading bows slows you $50\%$ less, or archers in your formation gain $+3\%$ movement speed.
* **Level 75** - `Quick Adjustments`: Removes the accuracy penalty from turning.
* **Level 75** - `Rapid Fire`: $+25\%$ reload speed. Clear DPS increase.
* **Level 125** - `Strong bows`: Bow shots deal $+8\%$ more damage.
* **Level 150** - `Discipline`: You can aim $50\%$ longer without losing accuracy, or gain $+1$ loyalty per day as governor.
* **Level 175** - `Eagle Eye`: Zoom factor increased by $+50\%$.
* **Level 200** - `Renowned Archer`: $+10\%$ starting battle morale to ranged troops, or $-30\%$ recruitment and upgrade costs for ranged troops.
* **Level 225** - `Horse Master`: Allows utilizing all bows on horseback (otherwise restricted).
* **Level 225** - `Deep Quivers`: Adds $+3$ arrows per quiver.
* **Level 250** - `Quick Draw`: Bow draw speed increased by $+25\%$.
* **Level 250** - `Ranger's Swiftness`: Equipped bows no longer slow you down, or archers provide $+20\%$ security as governor.
* **Level 275** - `Deadshot`: Starts scaling at 200 skill. At 330 skill, yields $+26\%$ reload speed and $+65\%$ bow damage.

#### Crossbow
* **Level 25** - `Piercer`: Ignores enemy armor below 20. Highly lethal early game.
* **Level 50** - `Wind Winder`: $+25\%$ reload speed.
* **Level 50** - `Unhorser`: Crossbow shots deal $+40\%$ damage against mounts.
* **Level 75** - `Donkey's Swiftness`: Moving accuracy loss with crossbows is reduced by $30\%$, or troops in your formation gain $+30$ Crossbow skill.
* **Level 75** - `Sheriff`: $+50\%$ headshot damage with crossbows, or $+10\%$ crossbow damage to infantry by troops in your formation.
* **Level 100** - `Peasant Leader`: Tier 1-3 troops gain $+10\%$ battle morale, or garrisoned ranged troop wages are reduced by $20\%$.
* **Level 125** - `Fletcher`: Adds $+4$ bolts per quiver.
* **Level 125** - `Puncture`: Crossbow shots gain $+10\%$ armor penetration, or troops in your formation gain $+5\%$ crossbow armor penetration.
* **Level 150** - `Deft Hands`: $+50\%$ resistance to being staggered while reloading a crossbow, including troops in your formation.
* **Level 150** - `Loose and Move`: Equipped crossbows no longer slow you down, or ranged troops in your formation gain $+5\%$ movement speed.
* **Level 175** - `Mounted Crossbowman`: Allows reloading all crossbows on horseback, or gives $+5\%$ XP to ranged troops.
* **Level 200** - `Long Shots`: $+100\%$ zoom with crossbows, or $+1$ daily militia recruitment as governor.
* **Level 225** - `Pavise`: $75\%$ chance to block projectiles from behind with a shield on your back, or $+30\%$ ballista accuracy as governor.
* **Level 225** - `Hammer Bolts`: Crossbows can dismount cavalry and ignore $50\%$ dismount resistance, or troops in your formation gain $+10\%$ crossbow damage.
* **Level 250** - `Terror`: Off-bucket utility: siege bombardment hits have a $20\%$ chance to add a casualty, or enemy morale loss from formation crossbow kills is increased by $25\%$.
* **Level 275** - `Mighty Pull`: At 330 skill, yields $+26\%$ reload speed and $+65\%$ crossbow damage.

#### Throwing
* **Level 25** - `Shield Breaker`: $+40\%$ damage to shields.
* **Level 50** - `Flexible Fighter`: $+10\%$ damage with throwing weapons on foot.
* **Level 75** - `Mounted Skirmisher`: Accuracy penalty while mounted reduced by $-20\%$.
* **Level 75** - `Well Prepared`: $+1$ throwing weapon per quiver, and $+1$ throwing ammunition to troops in your party.
* **Level 100** - `Knock Off`: Thrown weapons can dismount cavalry and ignore $25\%$ dismount resistance, or troops in your formation deal $+5\%$ throwing damage to cavalry.
* **Level 100** - `Running Throw`: Throwing damage gains $+25\%$ speed bonus, or troops in your formation gain $+30$ Throwing skill.
* **Level 150** - `Last Hit`: $+50\%$ damage when target is below half health, or $+5$ starting battle morale to troops in your party.
* **Level 175** - `Slinging Competitions`: Sling weapons can penetrate head armor, or $+1$ militia recruitment as governor.
* **Level 200** - `Splinters`: Throwing axes deal triple damage against shields, or troops in your formation deal $+50\%$ throwing weapon damage to shields.
* **Level 225** - `Long Reach`: Throwing weapon range increased by $+20\%$.
* **Level 225** - `Perfect Technique`: Throwing weapon travel speed increases by $+25\%$, or by $+10\%$ for troops in your formation.
* **Level 250** - `Impale`: Javelins break and penetrate shields, hitting the defender. Extremely powerful.
* **Level 250** - `Weak Spot`: $+30\%$ armor penetration.
* **Level 275** - `Unstoppable Force`: Throwing hits knock back foot soldiers.

---

### Combat Support Trees

#### Athletics
* **Level 25** - `Morning Exercise`: $+3\%$ combat movement speed.
* **Level 50** - `Fury`: $+10\%$ weapon handling while on foot, or $+10\%$ weapon handling to foot troops in your formation.
* **Level 75** - `Imposing Stature`: Persuasion chance $+30\%$, or $+5$ party size.
* **Level 100** - `Sprint`: $+5\%$ combat movement speed when carrying no shields or ranged weapons, or $+3\%$ movement speed to infantry in your formation.
* **Level 100** - `Powerful`: $+4\%$ melee weapon damage.
* **Level 125** - `Surging Blow`: $+30\%$ speed-damage bonus while on foot, or the same speed-damage bonus to troops in your formation.
* **Level 150** - `A Good Days Rest`: $+10\%$ hit point regeneration while waiting in settlements; the party-leader side gives $+10$ daily XP to foot troops while waiting.
* **Level 225** - `Strong Arms`: Throwing weapons deal $+5\%$ damage, or troops in your formation gain $+20$ Throwing skill.
* **Level 250** - `Ignore Pain`: $+10\%$ armor while on foot, or $+5$ armor to foot troops in your formation.
* **Level 250** - `Spartan`: $+50\%$ stagger resistance while on foot, or $-20\%$ party food consumption.
* **Level 275** - `Mighty Blow`: At 330 skill, yields $+80$ personal HP, making you exceptionally durable.

#### Riding
* **Level 25** - `Full Speed`: $+20\%$ charge damage.
* **Level 100** - `Sagittarius`: Mounted ranged accuracy penalty reduced by $-15\%$.
* **Level 125** - `Relief Force`: $+10$ starting battle morale when joining an ongoing allied battle, or $+20\%$ security from mounted troops as governor.
* **Level 150** - `Horse Archer`: Mounted bow damage $+10\%$.
* **Level 150** - `Mounted Warrior`: $+5\%$ mounted melee damage.
* **Level 175** - `Breeder`: Pack animals/mounts reproduce slowly in your inventory.
* **Level 200** - `Annoying Buzz`: Mounted ranged kills apply a battle morale penalty to enemies.
* **Level 200** - `Thunderous Charge`: Mounted melee kills apply a battle morale penalty to enemies.
* **Level 225** - `Cavalry Tactics`: $+30\%$ cavalry volunteering rate in settlements governed by your clan, or $-50\%$ wages of mounted troops in a governed settlement.
* **Level 225** - `Mounted Patrols`: Adds a $-0.50$ factor to prisoner escape chance. Role-dependent:
  * **Party leader (primary slot)**: Applied via `AddPerkBonusForParty` — reduces hero escape chance from your mobile party.
  * **Governor (secondary slot)**: Applied via `AddFactor` — reduces hero escape chance from your governed town or castle.
  * All escape-chance factors from perks share a single `SumOfFactors` pool: `Result = Base × (1 + SumOfFactors)`. Combined with `Keen Sight` (−0.50) the pool reaches −1.00 → **0% escape** (clamped). See [Prisoner Escape Mechanics](military-and-troop-tactics.md#prisoner-escape-mechanics) for full stacking details.
* **Level 250** - `Tough Steed` & `Dauntless Steed`: Provides $+20\%$ armor to your mount, $+10$ armor to troop mounts, $+50\%$ mounted stagger resistance, or $+5$ armor to mounted troops.
* **Level 275** - `The Way Of The Saddle`: Mount maneuverability and speed scaling.

---

## 7. Personal Non-Combat Perks



### Permanent Attribute Points
These perks are highly prized because they grant permanent points that can reshape your entire character build:

| Skill | Level | Perk | Benefit | Notes |
| :--- | ---: | :--- | :--- | :--- |
| **Smithing** | 150 | `Vigorous Smith` | $+1$ Vigor | Pushes One Handed, Two Handed, and Polearm limits. |
| **Smithing** | 150 | `Controlled Smith` | $+1$ Control | Pushes Bow, Crossbow, and Throwing limits. |
| **Athletics** | 175 | `Durable` | $+1$ Endurance | Pushes Athletics, Riding, and Smithing limits. |
| **Athletics** | 200 | `Strong` | $+1$ Vigor | Melee enabler. |
| **Athletics** | 200 | `Steady` | $+1$ Control | Ranged enabler. |
| **Smithing** | 225 | `Enduring Smith` | $+1$ Endurance | Pushes Endurance limits further. |
| **Smithing** | 225 | `Fencer Smith` | $+1$ Focus Point to One Handed and Two Handed | Stacks with Vigor attribute perks and can save one manual focus in each skill while training them. Does not help Polearm. |

> [!NOTE]
> **The Physical Attribute Rotation Strategy**:
> In vanilla Bannerlord, you can exploit the Arena Master respec mechanics to rotate physical attribute perks in Athletics (Level 175/200) and Smithing (Level 150/225). This allows your physical attributes (Vigor, Control, and Endurance) to reach 5 without ever investing hard attribute points.
> * **Physical Attribute Push**: Investing 10 focus points (5 in Athletics, 5 in Smithing) to execute this push essentially buys **6 physical attribute points** (equivalent to 24 character levels of progression) while unlocking high-value utility and survival perks.
> * **Vigor Focus Stretch**: `Fencer Smith` can be selected instead of `Enduring Smith` to give both One Handed and Two Handed an extra focus point while they are being trained. Since focus caps at 5, treat this as a temporary/manual focus refund rather than as extra room above the cap.
> * **Progression Warning**: This requires a heavy investment of 10 focus points and is only relevant if your build requires multiple high-tier combat perks.
> * **Detailed Guide**: For the step-by-step leveling walkthrough, focus point limits, and math proofs, see [The Arena Respec Rotation Trick in the Commander Guide](battanian-starts.md#the-arena-perk-respec-trick).

---

### Economy and Utility Perks

#### Trade and Disguise
* **Level 25 (Trade)** - `Appraiser`/`Whole Seller`: Mark profit values on trade screens.
* **Level 300 (Trade)** - `Everything Has a Price`: Allows trading fiefs and settlements directly in lord barters. Huge, but requires massive point investment.
* **Level 150 (Roguery)** - `Smuggler Connections`: Allows trading with town merchants and markets even while in disguise inside enemy settlements.

#### Charm and Diplomacy
* **Level 25** - `Virile`: $+30\%$ pregnancy chance to hero couples.
* **Level 50** - `Oratory`: Adds $+1$ renown and $+1$ influence for every issue resolved.
* **Level 200** - `Moral Leader` & `Natural Leader`: Reduces the number of successful arguments required during persuasion checks.
* **Level 250** - `Camaraderie`: Doubles relation gains when aiding allied lords in combat.
* **Level 275** - `Immortal Charm`: Passive $+5$ influence per day.

> [!NOTE]
> `Immortal Charm` is political/army-management utility, not a persuasion perk. Treat it as a late Social sink for kingdom-scale influence income.

---

## See Also

* [Commander Perks and Build Optimization Guide](commander-perks-and-build-optimization.md) — focus point allocation, starting origins, progression roadmaps, and perk directory for a melee commander build.
* [Battanian Character Creation and Commander Progression Guide](battanian-starts.md) — zero-waste starting background choices and level-up walkthrough.
