# Hero Progression and Build Guide

This manual covers the complete mechanics of character growth in Bannerlord: how character levels and skills gain experience, how learning rate limits shape attribute and focus choices, where to find the best low-investment perk splashes, and how to optimize personal combat and utility perks.

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
> Since main levels are driven by raw XP before learning rates are applied, big raw-XP events—such as high-damage melee hits, long-distance headshots, and expensive crafting items—are the fastest ways to level up your main character.

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
* **Healing (Medicine)**: Flat $+5$ XP per healing tick in town or camp.
* **Troop Training (Steward/Leadership)**: Daily flat values from perks.

---

## 3. Learning Limits and Point Budgets

Attributes and focus points determine where your learning rate falls to zero.

### The Math of Limits
Every skill in Bannerlord uses the exact same formulas to resolve learning limits:
$$\text{Skill Limit} = 4 + 14 \times (\text{Attribute} - 1) + 40 \times \text{Focus}$$
$$\text{Peak Learning Range} = 10 \times (\text{Attribute} - 1) + 30 \times \text{Focus}$$

* **Skill Limit**: The exact skill level where your learning rate reaches $0.00$. You cannot raise a skill past this number.
* **Peak Learning Range**: The skill level where the over-limit penalty begins. Past this point, your learning rate starts decaying.

### The Skill Limit Grid
The table below displays the maximum skill level attainable for any combination of Attribute (1–10) and Focus Points (0–5). The format is **Limit (Peak Learning Range)**:

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
- **Level 25**: 2 Attribute + 1 Focus (Limit 58)
- **Level 50**: 2 Attribute + 1 Focus (Limit 58)
- **Level 75**: 2 Attribute + 2 Focus (Limit 98)
- **Level 100**: 2 Attribute + 3 Focus (Limit 138)
- **Level 125**: 2 Attribute + 3 Focus (Limit 138)
- **Level 150**: 2 Attribute + 4 Focus (Limit 178)
- **Level 175**: 2 Attribute + 4 Focus (Limit 178)
- **Level 200**: 2 Attribute + 5 Focus (Limit 218)
- **Level 225**: 3 Attribute + 5 Focus (Limit 232)
- **Level 250**: 5 Attribute + 5 Focus (Limit 260)
- **Level 275**: 7 Attribute + 5 Focus (Limit 288)
- **Level 330**: 10 Attribute + 5 Focus (Limit 330)

### Player Point Budget & Cost Model
Every character level up gives you 1 Focus Point. Every 4 character levels give you 1 Attribute Point. 
To evaluate builds, we use a **Weighted Opportunity Cost Formula**:
$$\text{Weighted Cost} = \text{Focus Points Spent} + (\text{Purchased Attribute Points} \times 4)$$

> [!TIP]
> Attribute points are highly efficient when shared. For example, spending 1 point to raise Cunning from 2 to 3 costs 4 weighted points, but it simultaneously increases the skill limit of Scouting, Tactics, and Roguery by 14 points each. Plan your builds around attribute groups rather than single skills.

---

## 4. Early Splash Perks (Low Investment)

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
   - **Level 50**: `Pathfinder` ($+2\%$ daytime map speed; chance to gain relations with local notables when entering towns).
   - **Level 50**: `Water Diviner` ($+5\%$ map speed on marshes and river crossings).
5. **Leadership (Level 50)**:
   - **Level 25**: `Combat Tips` ($+2$ daily experience to all troops in your party).
   - **Level 50**: `Raise The Meek` ($+30\%$ prisoner recruitment speed; doubles training rate for Tier 1-3 troops).
6. **Athletics (Level 50)**:
   - **Level 25**: `Well Built` ($+5$ personal HP and $+5$ HP to foot troops in party).
   - **Level 50**: `Form Fitting Armor` (Reduces equipped armor weight by $15\%$, improving combat movement speed).
7. **Riding (Level 50)**:
   - **Level 25**: `Nimble Steed` (Increases mount maneuverability by $10\%$).
   - **Level 50**: `Well Strapped` (Reduces mount lameness/death chance by $50\%$ from fall damage).

---

## 5. Personal Combat Perks

Personal combat perks improve the main hero's combat performance in live battle. 

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
* **Level 50** - `Shield Bearer`: Removes the movement speed penalty from equipped shields.
* **Level 50** - `Swift Strike`: $+5\%$ one-handed attack speed.
* **Level 150** - `Duelist`: $+20\%$ melee damage when fighting without a shield. Great for high-damage dueling.
* **Level 200** - `Fleet of Foot`: $+5\%$ combat movement speed when holding a one-handed weapon.
* **Level 225** - `Deadly Purpose`: $+10\%$ one-handed weapon damage.
* **Level 250** - `Chink in the Armor`: $+10\%$ melee armor penetration. Strongly improves damage against heavy units.
* **Level 250** - `Prestige`: $+50\%$ renown from battles where you personally fight.
* **Level 275** - `Way of the Sword`: At 330 skill, yields $+16\%$ attack speed and $+40\%$ One Handed damage.

#### Two Handed
* **Level 25** - `Strong Grip`: $+10\%$ weapon handling.
* **Level 25** - `Wood Chopper`: $+15\%$ damage to shields.
* **Level 50** - `Head Basher`: $+10\%$ blunt damage with two-handed weapons.
* **Level 50** - `On the Edge`: $+5\%$ two-handed weapon swing speed.
* **Level 75** - `Show of Strength`: Melee strikes have a $+30\%$ chance to knock down foot soldiers.
* **Level 100** - `Projectile Deflection`: Allows blocking arrows and bolts with two-handed swords. Defining defensive tool.
* **Level 100** - `Beast Slayer`: $+50\%$ damage against mounts.
* **Level 125** - `Berserker`: Deal $+20\%$ damage when below $50\%$ health.
* **Level 125** - `Confidence`: $+10\%$ damage when your character HP is above $90\%$.
* **Level 175** - `Hope`: $+1$ daily influence per town under own clan control / $+10\%$ party morale.
* **Level 200** - `Reckless Charge`: $+20\%$ damage when charging on foot.
* **Level 225** - `Vandal`: Triple damage to wooden structures (shields/gates) and $+10\%$ armor penetration.
* **Level 225** - `Blade Master`: $+10\%$ two-handed weapon speed.
* **Level 250** - `Way Of The Great Axe`: *Note: the scaling formula only starts above 250.* At 330 skill, yields $+16\%$ speed and $+40\%$ damage.

#### Polearm
* **Level 25** - `Pikeman`: $+50\%$ damage against mounts.
* **Level 50** - `Clean Thrust`: $+10\%$ thrust damage. Paired with `Guards` ($+50\%$ headshot damage) makes spear thrusts lethal.
* **Level 50** - `Keep at Bay`: Polearm thrusts have a chance to push back enemies.
* **Level 75** - `Swift Swing`: $+5\%$ swing speed. Mandatory for swingable polearms (glaives/menavlions).
* **Level 100** - `Footwork`: $+5\%$ combat speed while holding a polearm.
* **Level 125** - `Steed Killer`: Dismounts enemies on successful thrust attacks.
* **Level 150** - `Skewer`: $30\%$ chance to keep couch lance active after hitting.
* **Level 175** - `Phalanx`: Infantry in your formation have $+5\%$ melee speed.
* **Level 175** - `Standard Bearer`: Increases party morale in battles.
* **Level 200** - `Lancer`: $+20\%$ speed-damage bonus while mounted.
* **Level 250** - `Counterweight`: $+10\%$ swing damage.
* **Level 250** - `Sharpen the Tip`: $+10\%$ thrust damage.
* **Level 275** - `Way of the Spear`: Pushes limits of polearm combat stats.

---

### Ranged Tree Highlights (Control)

#### Bow
* **Level 25** - `Bow Control`: Reduces movement accuracy penalty by $30\%$.
* **Level 50** - `Dead Aim`: $+30\%$ headshot damage.
* **Level 50** - `Bodkin`: $+20\%$ armor penetration with bows.
* **Level 50** - `Nocking Point`: $+10\%$ bow reload speed.
* **Level 75** - `Quick Adjustments`: Removes the accuracy penalty from turning.
* **Level 100** - `Rapid Fire`: $+25\%$ reload speed. Clear DPS increase.
* **Level 125** - `Strong bows`: Bow shots deal $+8\%$ more damage.
* **Level 150** - `Discipline`: Under command of the captain, archers have $+10\%$ accuracy.
* **Level 175** - `Eagle Eye`: Zoom factor increased by $+50\%$.
* **Level 200** - `Renowned Archer`: Battle renown increased by $+20\%$.
* **Level 225** - `Horse Master`: Allows utilizing all bows on horseback (otherwise restricted).
* **Level 225** - `Deep Quivers`: Adds $+3$ arrows per quiver.
* **Level 250** - `Quick Draw`: Bow draw speed increased by $+25\%$.
* **Level 250** - `Ranger's Swiftness`: Combat movement speed increased by $+10\%$ when holding a bow.
* **Level 275** - `Deadshot`: Starts scaling at 200 skill. At 330 skill, yields $+26\%$ reload speed and $+65\%$ bow damage.

#### Crossbow
* **Level 25** - `Piercer`: Ignores enemy armor below 20. Highly lethal early game.
* **Level 50** - `Wind Winder`: $+25\%$ reload speed.
* **Level 50** - `Unhorser`: Crossbow shots deal $+40\%$ damage against mounts.
* **Level 75** - `Donkey's Swiftness`: Combat movement speed increased by $+5\%$ when holding a crossbow.
* **Level 75** - `Sheriff`: Earn $+10\%$ renown from battles.
* **Level 100** - `Peasant Leader`: High tier troops have $+5\%$ damage in autocalc.
* **Level 125** - `Mounted Crossbowman`: Allows reloading all crossbows on horseback.
* **Level 125** - `Fletcher`: Adds $+4$ bolts per quiver.
* **Level 125** - `Puncture`: Crossbow shots ignore target armor below 10.
* **Level 150** - `Deft Hands`: Reload speed $+15\%$ while moving.
* **Level 150** - `Loose and Move`: Accuracy penalty while moving reduced by $-30\%$.
* **Level 200** - `Long Shots`: Range-based damage decay reduced by $-50\%$.
* **Level 225** - `Pavise`: $75\%$ chance to block projectiles from behind with an equipped shield on your back while reloading.
* **Level 225** - `Hammer Bolts`: Crossbow hits have a $+25\%$ chance to stagger enemies.
* **Level 250** - `Terror`: Increases enemy morale loss from your kills by $+10\%$.
* **Level 275** - `Mighty Pull`: At 330 skill, yields $+26\%$ reload speed and $+65\%$ crossbow damage.

#### Throwing
* **Level 25** - `Shield Breaker`: $+40\%$ damage to shields.
* **Level 50** - `Flexible Fighter`: $+10\%$ damage with throwing weapons on foot.
* **Level 75** - `Mounted Skirmisher`: Accuracy penalty while mounted reduced by $-20\%$.
* **Level 100** - `Well Prepared`: $+2$ throwing weapons per quiver.
* **Level 100** - `Knock Off`: Throwing hits have a chance to disarm shields.
* **Level 100** - `Running Throw`: Throwing damage scales with running speed (up to $+15\%$).
* **Level 150** - `Last Hit`: $+20\%$ damage when target is below $50\%$ health.
* **Level 175** - `Slinging Competitions`: Renown from battles $+10\%$.
* **Level 200** - `Splinters`: Throwing axes and knives deal $+100\%$ damage to shields.
* **Level 225** - `Impale`: Javelins break and penetrate shields, hitting the defender. Extremely powerful.
* **Level 225** - `Long Reach`: Throwing weapon range increased by $+20\%$.
* **Level 225** - `Perfect Technique`: Throwing velocity increased by $+15\%$.
* **Level 250** - `Weak Spot`: $+30\%$ armor penetration.
* **Level 275** - `Unstoppable Force`: Throwing hits knock back foot soldiers.

---

### Combat Support Trees

#### Athletics
* **Level 25** - `Morning Exercise`: $+3\%$ combat movement speed.
* **Level 50** - `Fury`: $+10\%$ attack speed when HP is below $50\%$.
* **Level 75** - `Powerful`: $+4\%$ melee weapon damage.
* **Level 75** - `Imposing Stature`: Persuasion chance $+10\%$.
* **Level 100** - `Sprint`: $+10\%$ combat running speed.
* **Level 125** - `Surging Blow`: Melee damage $+5\%$ when on foot.
* **Level 150** - `A Good Days Rest`: Town resting recovery speed $+20\%$.
* **Level 175** - `Ignore Pain`: $+10\%$ armor while on foot.
* **Level 225** - `Strong Arms`: Throwing weapons deal $+10\%$ damage.
* **Level 250** - `Spartan`: Reduces campaign party wages by $-5\%$.
* **Level 275** - `Mighty Blow`: At 330 skill, yields $+80$ personal HP, making you exceptionally durable.

#### Riding
* **Level 25** - `Full Speed`: $+20\%$ charge damage.
* **Level 100** - `Sagittarius`: Mounted ranged accuracy penalty reduced by $-15\%$.
* **Level 125** - `Relief Force`: Speed on campaign map when traveling with mount $+3\%$.
* **Level 150** - `Horse Archer`: Mounted bow damage $+10\%$.
* **Level 175** - `Breeder`: Pack animals/mounts reproduce slowly in your inventory.
* **Level 200** - `Mounted Warrior`: $+5\%$ mounted melee damage.
* **Level 200** - `Annoying Buzz`: Horse archers in your formation have $+10\%$ accuracy.
* **Level 200** - `Thunderous Charge`: Mount charge damage increased by $+30\%$.
* **Level 225** - `Cavalry Tactics`: Cavalry in your formation have $+5\%$ mount speed.
* **Level 225** - `Mounted Patrols`: Prisoner escape chance reduced by $-50\%$.
* **Level 250** - `Tough Steed` & `Dauntless Steed`: Provides $+20\%$ mount HP and $+50\%$ mount stagger resistance.
* **Level 275** - `The Way Of The Saddle`: Mount maneuverability and speed scaling.

---

## 6. Personal Non-Combat Perks

These perks are focused on character attribute growth, economic trade benefits, and diplomacy utilities.

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
| **Smithing** | 225 | `Fencer Smith` | $+1$ Focus Point | Grants 1 focus point split between One Handed and Two Handed. |

> [!TIP]
> **Respec Stretch**: You can temporarily allocate points to reach the Smithing 150/225 or Athletics 175/200 thresholds, take the permanent attribute perk, and later respec your focus points at an Arena Master. The permanent attribute points will remain.

---

### Economy and Utility Perks

#### Trade and Disguise
* **Level 25 (Trade)** - `Appraiser`/`Whole Seller`: Mark profit values on trade screens.
* **Level 300 (Trade)** - `Everything Has a Price`: Allows trading fiefs and settlements directly in lord barters. Huge, but requires massive point investment.
* **Level 150 (Roguery)** - `Smuggler Connections`: Allows trading with town merchants and markets even while in disguise inside enemy settlements.

#### Charm and Persuasion
* **Level 25** - `Virile`: $+20\%$ pregnancy chance to hero couples.
* **Level 50** - `Oratory`: Adds $+2$ renown and $+1$ influence for every issue/quest resolved.
* **Level 200** - `Moral Leader` & `Natural Leader`: Reduces the number of successful arguments required during persuasion checks.
* **Level 250** - `Camaraderie`: Doubles relation gains when aiding allied lords in combat.
* **Level 275** - `Immortal Charm`: Passive $+5$ influence per day.

---

## 7. Optimized Starting Selections

When starting a new character, you want to align your culture, background choices, and starting skills to hit your target limits with **zero wasted attribute or focus points**. Below are two optimized starting builds for Battanian characters.

### Build A: The Intelligent Commander (Vigor & Intelligence)
* **Goal**: Maximize leadership, trade, steward, and combat spear/axe capabilities with $0$ wasted points.
* **Point Allocation**:
  - **Vigor**: 5 (Melee combat focus)
  - **Control**: 2
  - **Endurance**: 3
  - **Cunning**: 2
  - **Social**: 2
  - **Intelligence**: 6 (High steward/medicine capability)
* **Background Selection Steps**:
  1. *Parents*: Tribespeople (Vigor +1, One Handed +10, Polearm +10, Athletics +10)
  2. *Childhood*: Skill with Horses (Riding +10, Medicine +10)
  3. *Education*: Repaired Projects (Engineering +1, Crossbow +10, Tactics +10)
  4. *Youth*: Guard with Garrison (Two Handed +10, Leadership +10)
  5. *Adulthood*: Defeated Enemy (Vigor +1, One Handed +10, Tactics +10)
  6. *Escape Choice*: Underage/Young sibling enabler.

---

### Build B: The Cunning Ranger (Control & Cunning)
* **Goal**: Focus on scout speed, roguery, ranged bow accuracy, and athletics.
* **Point Allocation**:
  - **Vigor**: 2
  - **Control**: 6 (High bow/throwing capability)
  - **Endurance**: 3
  - **Cunning**: 5 (High scouting/tactics capability)
  - **Social**: 2
  - **Intelligence**: 2
* **Background Selection Steps**:
  1. *Parents*: Foresters (Control +1, Bow +10, Throwing +10, Scouting +10)
  2. *Childhood*: Attention to Detail (Tactics +10, Scouting +10)
  3. *Education*: Repaired Projects (Engineering +1, Crossbow +10, Tactics +10)
  4. *Youth*: Hearth Guard (Vigor +1, One Handed +10, Leadership +10)
  5. *Adulthood*: Defeated Enemy (Vigor +1, One Handed +10, Tactics +10)
