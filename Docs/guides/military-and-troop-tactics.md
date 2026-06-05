# Military and Troop Tactics Manual

This manual covers the complete mechanics of campaign-map military logistics, battle simulation, troop training, live-combat AI scaling, and village raiding. It explains the exact math governing party speeds, training schedules, combat behaviors, and loot acquisition.

---

## 1. Party Speed and Campaign Logistics

Campaign-map speed is the most critical survival stat in Bannerlord. Rather than a simple average of troop stats, party speed is governed by a complex weight-and-composition model.

### Base Speed Formula
The Campaign Map Speed model starts by scaling party size, penalizing larger armies regardless of their individual troop tier:
$$\text{Base Speed} = 4 \times \left(\frac{200}{200 + \text{Total Men}}\right)^{0.4}$$

Here are the baseline speeds by party size before any composition or perk modifiers:

| Men in Party | Base Speed |
| :--- | ---: |
| **20** | 3.850 |
| **50** | 3.658 |
| **100** | 3.401 |
| **150** | 3.198 |
| **200** | 3.031 |
| **300** | 2.773 |

### Composition Bonuses
Once Base Speed is established, the game applies percentage factors for cavalry, foot troops riding spare mounts, cargo, wounded, prisoners, morale, terrain, weather, and perks. 

The primary land-movement composition formulas are:
$$\text{Cavalry Bonus} = 0.30 \times \frac{\text{Mounted Troops}}{\text{Total Men}}$$
$$\text{Mounted Footmen Bonus} = 0.15 \times \frac{\text{Mounted Footmen}}{\text{Total Men}}$$
$$\text{Strong Bonus} = 0.05 \times \frac{\text{Foot Troops}}{\text{Total Men}}$$
$$\text{Nomadic Traditions Bonus} = 0.30 \times \text{Mounted Footmen Bonus}$$

* **Mounted Footmen**: Foot troops covered by available spare mounts (horses/camels). The game assigns mounts up to the number of foot troops; extra horses beyond the foot troop count do not increase this bonus.
* **Cavalry vs. Foot**: Both noble and low-tier cavalry count equally as mounted for the composition bonus; the engine only checks the mounted/foot state, not troop quality.

#### Comparison: 100-Man Party on Clean Terrain
The following table shows the maximum potential speed for a 100-man party on flat, dry terrain under different composition setups:

| Party Setup | Speed Factor | Final Speed | % of Pure Cavalry Speed |
| :--- | :---: | :---: | ---: |
| **100 Infantry, no spare mounts** | 1.000 | 3.401 | 76.9% |
| **100 Infantry, spare mounts** | 1.150 | 3.911 | 88.5% |
| **100 Infantry, spare mounts + `Strong`** | 1.200 | 4.081 | 92.3% |
| **100 Infantry, spare mounts + `Strong` + `Nomadic Traditions`** | 1.245 | 4.234 | 95.8% |
| **100 Cavalry** | 1.300 | 4.421 | 100.0% |

> [!TIP]
> Fully supported infantry (with spare mounts and the `Strong` and `Nomadic Traditions` perks) is only $4.2\%$ slower than a pure cavalry party on clean terrain. In bad weather or dense forests, this gap closes completely or even reverses.

> [!TIP]
> **Strategic Comparison of Mount Coverage via `Logistician`**: Having many different types of ridable mounts in your inventory can make manual tracking extremely difficult. The Steward perk `Logistician` provides an exact signal. Since its morale bonus is active only when you have strictly more riding mounts than foot troops ($\text{Mounts} > \text{Foot Troops}$), having even a single mount over your foot troop count is sufficient to trigger the tooltip, making it trivial to verify that you have $100\%$ mount coverage.

> [!TIP]
> **Food Variety Morale Scaling via `Gourmet`**: Party morale is heavily boosted by carrying diverse food types. The Steward perk `Gourmet` (Level 175) doubles the morale bonus gained from food variety, making it easy to maintain party morale above $75$ to sustain the `Forced March` map speed bonus.


#### Mixed Formations Speed Grid
Below is the speed scaling for a 100-man mixed party (assuming every foot soldier is covered by a spare mount, and the party leader has both `Strong` and `Nomadic Traditions`):

| Cavalry Count | Foot Troop Count | Speed Factor | Map Speed |
| :---: | :---: | :---: | :---: |
| **0** | 100 | 1.245 | 4.234 |
| **25** | 75 | 1.259 | 4.281 |
| **50** | 50 | 1.272 | 4.328 |
| **75** | 25 | 1.286 | 4.375 |
| **100** | 0 | 1.300 | 4.421 |

### Environmental and Terrain Modifiers
* **Forest Terrain**: Forests apply a baseline $-30\%$ speed penalty. However, the Scout perk `Forest Kin` reduces this penalty to $-15\%$ if at least $75\%$ of the party is infantry. On forest terrain, an all-cavalry party is slowed to **3.401**, while an infantry party with spare mounts and forest perks moves at **3.724**—making the infantry party significantly faster.
* **Bad Weather**: Applies a penalty directly to the cavalry and mounted footmen composition bonuses. Because the `Strong` and `Nomadic Traditions` add-ons are applied in a separate branch, bad-weather land movement makes infantry with spare mounts virtually equal to all-cavalry.

### Speed, Vision, And Logistics Perks

Only some rows below directly increase campaign speed. Scouting also contains sight, prisoner, recovery, and simulation perks that sit near the speed tiers but should not be treated as speed bonuses.

| Skill | Level | Perk | Role | Effect | Practical Application |
| :--- | ---: | :--- | :--- | :--- | :--- |
| **Scouting** | 25 | `Day Traveler` | Scout | $+2\%$ daytime travel speed | Best for general, proactive search and trade routes. |
| **Scouting** | 25 | `Night Runner` | Scout | $+5\%$ nighttime travel speed | Great for escaping or catching enemies under cover of darkness. |
| **Scouting** | 50 | `Pathfinder` | Scout | $+2\%$ speed on steppes/plains | Maximizes speed in open field areas. |
| **Scouting** | 75 | `Desert Born` | Scout | $+5\%$ speed on deserts/dunes | Essential for Aserai campaigns. |
| **Scouting** | 75 | `Forest Kin` | Scout | $-50\%$ forest speed penalty | Requires $\ge 75\%$ infantry. Pivotal for Battanian forest combat. |
| **Scouting** | 100 | `Forced March` | Scout | $+2.5\%$ speed when morale $> 75$ | Highly compatible with high food variety and frequent victories. |
| **Scouting** | 100 | `Unburdened` | Scout | $-20\%$ overburden speed penalty | Keeps you moving when hauling heavy cargo. |
| **Scouting** | 125 | `Tracker` | Scout | $+2\%$ speed while following a hostile party | Helps chase down specific targets. |
| **Scouting** | 150 | `Mounted Scouts` | Scout / Party Leader | $+10\%$ sight range if party is $>50\%$ cavalry / $+5$ party size | Vision and party-size utility for mounted parties; not a speed bonus. |
| **Scouting** | 150 | `Patrols` | Scout / Party Leader | $+5$ battle morale against bandits / $+10\%$ autoresolve advantage against bandits | Bandit-fighting utility; not a prisoner-speed perk. |
| **Scouting** | 175 | `Foragers` | Scout / Party Leader | $-10\%$ food consumption in steppes and forests / $-15\%$ disorganized-state duration | Food and recovery utility; not a wounded-speed perk. |
| **Scouting** | 175 | `Beast Whisperer` | Scout | $+10\%$ cargo capacity per pack animal | Logistics enabler for massive baggage trains. |
| **Scouting** | 200 | `Village Network` | Party Leader / Governor | $-10\%$ same-culture village trade penalty / $+10\%$ villager party size | Village economy and governor utility; not an own-territory speed perk. |
| **Scouting** | 225 | `Keen Sight` | Scout / Party Leader | $-50\%$ forest sight penalty / $-50\%$ prisoner lord escape chance | Vision and prisoner control; not a terrain-speed perk. |
| **Scouting** | 225 | `Vantage Point` | Scout / Party Leader | $+25\%$ sight range when stationary / $+10$ prisoner limit | Stationary vision and prisoner capacity; not hill speed. |
| **Scouting** | 250 | `Rearguard` | Party Leader | $+20\%$ wounded troop recovery while in an army / $+10\%$ siege-camp defense damage | Recovery and siege-defense utility; not chase speed. |
| **Scouting** | 250 | `Vanguard` | Party Leader | $+5\%$ autoresolve attack damage / $+10\%$ sally-out damage | Simulation and siege attack utility; not chase speed. |
| **Scouting** | 275 | `Uncanny Insight` | Scout | $+0.1\%$ Speed per point $> 200$ | Massive late-game scaling. |
| **Medicine** | 75 | `Sledges` | Surgeon | $-50\%$ Speed penalty from wounded | Critical post-battle recovery tool. |
| **Steward** | 150 | `Aid Corps` | Quartermaster / Governor | Wounded troops no longer receive wages / $+20\%$ hearth growth in bound villages | Wage and governor-economy utility; use Medicine `Sledges` for wounded speed penalty. |
| **Athletics** | 200 | `Strong` | Party Leader | $+5\%$ Speed by foot troops | Strong choice for infantry-heavy builds. |
| **Riding** | 75 | `Nomadic Traditions` | Party Leader | $+30\%$ Mounted footmen bonus | Mandatory if you run infantry with spare mounts. |
| **Riding** | 100 | `Sweeping Wind` | Party Leader | $+2\%$ Flat travel speed | Simple, unconditional speed boost. |
| **Riding** | 175 | `Shepherd` | Party Leader | $-50\%$ Herding speed penalty | Indispensable for livestock traders. |

---

## 2. Troop XP and Upgrade Dynamics

Training recruits into elite soldiers relies on three separate experience systems: direct battle XP, shared combat XP, and passive daily training.

### Direct Battle XP Formula
When a troop kills an enemy in battle, the experience gained depends on the killed unit's internal character level, not their visible tier (tiers 1-6):
$$\text{Troop Battle XP} = \frac{(\text{Killed Character Level} + 6)^2}{3}$$

* **Character Level vs. Tier**: An elite Tier 5 unit might have a character level of 26, whereas a recruit has a level of 6.
* **Quadratic Growth**: Because the level reward scales quadratically, fighting higher-tier armies trains your troops exponentially faster than farming looters.

| Killed Character Level | XP Reward |
| :---: | ---: |
| **1** | 16 |
| **6** | 48 |
| **11** | 96 |
| **16** | 161 |
| **21** | 243 |
| **26** | 341 |
| **31** | 456 |

### Shared XP Distribution Algorithm
Shared XP (from battle victories, quests, or donation perks) is distributed dynamically based on a stack's remaining upgrade capacity:
$$\text{Shared XP Capacity} = \text{Remaining XP needed by stacks that can still upgrade}$$
$$\text{Shared XP Added to Stack} = \text{Floor}\left(\text{Max}\left(1, \text{Remaining Shared XP} \times \frac{\text{Stack Capacity}}{\text{Remaining Capacity}}\right)\right)$$

> [!NOTE]
> **Strategic Trade-offs of Delayed Promotions**:
> Because a troop stack that has accumulated enough experience to upgrade ceases to absorb Shared XP, you can strategically delay promotions to control where experience is distributed:
> * **XP Channeling to Lower Tiers**: If you leave higher-tier units (e.g., Tier 4 troops ready for Tier 5) unupgraded, their stack capacity remains $0$, and they consume $0\%$ of incoming Shared XP. This diverts $100\%$ of battle victory and item donation XP to your lower-tier Recruits and Tier 1–2 troops.
> * **Siphon Re-opening**: Conversely, if you want your higher-tier troops to keep advancing toward elite status, you must upgrade them promptly to open up new capacity (e.g., promoting them to Tier 5 immediately creates a new siphon capacity of $1,700$ XP per troop, letting them absorb Shared XP again).
> * **Milking Tier-Restricted Perks**: Passive training perks like `Raise The Meek` only benefit Tier 1–2 troops ($+4$ XP/day). Keeping Tier 2 units ready to upgrade but unupgraded allows them to continue receiving this high daily bonus. Upgrading them immediately to Tier 3 would stop this passive XP drip.
> * **Stack-Size Daily XP Scaling**: Passive training perks add XP to the stack based on its total count ($\text{Perk Value} \times \text{Troop Count}$), regardless of upgrade status. Keeping ready recruits in the stack keeps the multiplier high, allowing the remaining recruits to reach readiness much faster.

### Upgrade Costs
The experience required to upgrade a troop to the next tier:

| Target Tier Step | XP Cost |
| :---: | ---: |
| **Tier 1 or lower** | 100 |
| **Tier 2** | 300 |
| **Tier 3** | 550 |
| **Tier 4** | 900 |
| **Tier 5** | 1,300 |
| **Tier 6** | 1,700 |
| **Tier 7 (Elite Mod)** | 2,100 |

### Daily Passive Training Perks
These perks drip-feed experience to your troops at the end of each campaign day. The daily XP is calculated **per troop** in each matching stack (i.e. $\text{Daily XP Added to Stack} = \text{Perk Value} \times \text{Troop Count in Stack}$), meaning larger stacks gain XP much faster as a whole:

| Skill | Level | Perk | Role | Effect | Best Target |
| :--- | ---: | :--- | :--- | :--- | :--- |
| **Leadership** | 25 | `Combat Tips` | Party Leader | $+2$ XP/day to all troops | Broad early-game progression. |
| **Leadership** | 25 | `Raise The Meek` | Party Leader | $+4$ XP/day to Tier 1-2 troops | Fast-tracks fresh recruits. |
| **Steward** | 50 | `Drill Sergeant` | Quartermaster | $+2$ XP/day to all troops | Stacks with Leadership perks. |
| **Steward** | 50 | `Seven Veterans` | Quartermaster | $+4$ XP/day to Tier 4+ troops | Maintains elite rosters. |
| **One Handed** | 150 | `Military Tradition` | Party Leader | $+2$ XP/day to infantry | Specializes in footmen training. |
| **Bow** | 125 | `Trainer` | Party Leader | $+3$ XP/day to archers | Ranged-focused builds. |
| **Crossbow** | 100 | `Renowned Marksmen` | Party Leader | $+2$ XP/day to ranged troops | Stacks on crossbow lines. |
| **Athletics** | 150 | `Walk It Off` | Party Leader | $+3$ XP/day to foot troops moving | Excellent for active campaign mapping. |
| **Athletics** | 150 | `A Good Days Rest`| Party Leader | $+10$ XP/day to foot troops resting | Extremely strong when waiting in towns. |
| **Scouting** | 100 | `Forced March` | Party Leader | $+2$ XP/day when traveling, morale $>75$ | Reward for maintaining high party morale. |
| **Throwing** | 125 | `Saddlebags` | Party Leader | $+1$ XP/day to infantry | Minor auxiliary boost. |
| **Polearm** | 200 | `Drills` | Party Leader | $+0.1$ XP/day to troops | **BUGGED/NO-OP**: The helper rounds this value to the nearest integer, turning `0.1` into `0`. Avoid. |

### Battle and Post-Battle XP Modifiers
These perks increase the XP gained during live combat or simulation:

* **One Handed (Level 100) - `Trainer`**: $+5\%$ XP to melee troops after battles.
* **Two Handed (Level 75) - `Baptised in Blood`**: $+5\%$ XP to melee troops after battles.
* **One Handed (Level 150) - `Corps-a-corps`**: $+10\%$ of total XP gained as bonus XP to infantry after battles.
* **Leadership (Level 200) - `Lead by Example`**: $+10\%$ shared experience for cavalry troops. This is not a One Handed perk.
* **Bow (Level 200) - `Bulls Eye`**: $+10\%$ battle XP to ranged troops.
* **Crossbow (Level 175) - `Mounted Crossbowman`**: $+5\%$ XP to ranged troops.
* **Throwing (Level 200) - `Resourceful`**: $+10\%$ battle XP to troops equipped with throwing weapons.
* **Roguery (Level 25) - `No Rest for the Wicked`**: $+20\%$ XP gain for bandit troops.
* **Leadership (Level 125) - `Leader of the Masses`**: $+5\%$ experience from battles shared with troops in your party.
* **Leadership (Level 200) - `Trusted Commander`**: $+20\%$ XP when sending troops to confront the enemy (autoresolve).
* **Medicine (Level 250) - `Battle Hardened`**: $+25$ XP to wounded units at battle end. (**BUGGED/NO-OP**: This perk's battle-end effect is never called in the game logic).

### Donation and Special Training Perks
* **Steward (Level 100) - `Paid in Promise`**: Discarded/donated armor yields **Shared XP** distributed across eligible party stacks.
* **Steward (Level 125) - `Giving Hands`**: Discarded/donated weapons yield **Shared XP** distributed across eligible party stacks.
* **Two Handed (Level 75) - `Baptised in Blood`**: Adds $+5$ XP **per troop** to every non-hero infantry stack in the party (effectively $5 \times \text{stack size}$ total XP added to each stack's pool) for each player kill made with a two-handed weapon. Great for active combat players.
* **Leadership (Level 100) - `Famous Commander`**: Newly recruited troops arrive with $+200$ XP **per troop** pre-loaded into their stack.

### Prisoner Logistics: Selling vs. Donating (XP & Value Dynamics)

Capturing enemy combatants presents a choice: selling them to ransom brokers in taverns or donating them to friendly castle/town dungeons. This decision involves trade-offs between wealth generation, direct skill XP, and political capital (influence).

#### 1. XP and Influence Pathways
* **Selling Prisoners**: This is the **only direct source** of Roguery XP. The base XP scales strictly with the prisoner's tier and quantity, completely independent of their gold value:
  $$\text{Base Roguery XP} = 2 \times \sum (\text{Troop Tier} \times \text{Quantity})$$
* **Donating Prisoners**: Awards immediate Kingdom Influence and indirect Charm XP (gained only when the donation triggers a clan relation increase with the fief owner). The influence reward scales sublinearly (diminishing returns) with the prisoner's gold ransom value:
  $$\text{Influence Gain} = 0.2 \times (\text{Ransom Value})^{0.4}$$

#### 2. Regular Troop Ransom Value Formula
A regular troop's ransom value is directly proportional ($25\%$) to their computed recruitment cost ($R$). 
$$\text{Base Ransom Value} = \lfloor R \times 0.25 \rfloor$$
The recruitment cost ($R$) used in ransom calculations is governed by the following formula:
$$R = (\text{Base} \times \text{OccupationMultiplier}) + \text{MountSurcharge}$$

* **Level-Based Base Cost**:
  * **Level 1–5**: $10$ gold (Tier 0)
  * **Level 6–10**: $20$ gold (Tier 1)
  * **Level 11–15**: $50$ gold (Tier 2)
  * **Level 16–20**: $100$ gold (Tier 3)
  * **Level 21–25**: $200$ gold (Tier 4)
  * **Level 26–30**: $400$ gold (Tier 5)
  * **Level 31–35**: $600$ gold (Tier 6)
* **Occupation Multiplier**:
  * **$3.0\times$** for **Mercenaries**, **Gangsters**, and **Caravan Guards**.
  * **$1.0\times$** for all standard faction troops.
* **Mount Surcharge (Horse Surcharge)**:
  * **$+150$ gold** for Tiers 1–4 (Level $< 26$) if the troop is equipped with a mount.
  * **$+500$ gold** for Tiers 5–6 (Level $\ge 26$) if the troop is equipped with a mount.
  * **$+0$ gold** for dismounted troops.

#### 3. Hero Ransom Value Formula
Hero ransom values scale with the hero's level, status, clan wealth, and kingdom holdings:
$$\text{Base Ransom Value} = (\text{RecruitmentCost} + \text{HeroBaseValue} + \text{HeroWealthValue}) \times \text{kingdomMultiplier}$$
* **HeroBaseValue**: Evaluates political status based on their clan tier and role:
  $$\text{HeroBaseValue} = (\text{Clan Tier} + 2) \times 200 \times \text{RoleMultiplier}$$
  * $\text{RoleMultiplier} = 6.0$ for a Kingdom Ruler (e.g., King/Emperor)
  * $\text{RoleMultiplier} = 2.5$ for a Clan Leader
  * $\text{RoleMultiplier} = 1.0$ for standard family/clan members
* **HeroWealthValue**: Scales with the hero's personal purse:
  $$\text{HeroWealthValue} = 6.0 \times \sqrt{\max(0, \text{Hero Gold})}$$
* **Kingdom Multiplier**: Scales with the total fief holdings of their faction:
  * **$0.5\times$** if the hero has no kingdom (e.g., landless clan/minor faction)
  * **$1.0\times$** if the faction is not a kingdom
  * **$\frac{\text{Fief Count} + 1}{9}$** if the faction is a kingdom and has $< 8$ fiefs (ranges from $0.11$ to $0.89$)
  * **$1.0 + 0.1 \times \sqrt{\text{Fief Count} - 8}$** if the kingdom has $\ge 8$ fiefs

#### 4. Ransom Perks and Sea Traversal Quirks
Ransom transactions are augmented by the following Roguery perks, which feature specific penalties when the party is currently at sea (traveling over water):
* **`Manhunter` (Roguery 100)**: $+20\%$ ransom value for regular troops.
  * *Quirk*: **No-op when at sea**. The $+20\%$ bonus is completely disabled while traveling on water.
* **`Ransom Broker` (Roguery 200)**: $+25\%$ ransom value for heroes.
  * *Quirk*: **Halved when at sea**. The $+25\%$ bonus drops to $+12.5\%$ while traveling on water.

#### 5. Troop Ransom Value Comparison (Base vs. Mounted)
Because the mount surcharge (+150 or +500 gold) is so massive relative to a troop's base level cost, **mounted units sell for significantly more than foot units of the same tier—and frequently sell for more than foot units 1 or 2 tiers higher**:

| Troop Tier | Base Cost | Surcharge | Total Cost ($R$) | Base Ransom Value | Manhunter Ransom ($+20\%$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **T1 Foot** | 20 | +0 | 20 | **5 gold** | **6 gold** |
| **T1 Mounted** | 20 | +150 | 170 | **42 gold** | **50 gold** |
| **T2 Foot** | 50 | +0 | 50 | **12 gold** | **14 gold** |
| **T2 Mounted** | 50 | +150 | 200 | **50 gold** | **60 gold** |
| **T3 Foot** | 100 | +0 | 100 | **25 gold** | **30 gold** |
| **T3 Mounted** | 100 | +150 | 250 | **62 gold** | **74 gold** |
| **T4 Foot** | 200 | +0 | 200 | **50 gold** | **60 gold** |
| **T4 Mounted** | 200 | +150 | 350 | **87 gold** | **104 gold** |
| **T5 Foot** | 400 | +0 | 400 | **100 gold** | **120 gold** |
| **T5 Mounted** | 400 | +500 | 900 | **225 gold** | **270 gold** |
| **T6 Foot** | 600 | +0 | 600 | **150 gold** | **180 gold** |
| **T6 Mounted** | 600 | +500 | 1100 | **275 gold** | **330 gold** |

*Note: Mercenary troop counterparts (e.g., caravan guards or mercenary cavalry) multiply their base cost by $3.0\times$ before the surcharge is added. For example, a T5 Mounted Mercenary has a total cost of $(400 \times 3) + 500 = 1700$ gold, yielding a base ransom of **425 gold**.*

#### 6. Strategic Prisoner Optimization
> [!TIP]
> **Prisoner Logistics Strategy**:
> * **Always Sell High-Tier Mounted Prisoners**: T5 and T6 mounted units (selling for 225–275 base gold) represent huge cash opportunities. Converting them into influence is economically inefficient because they convert at a poor Gold-to-Influence ratio ($\approx 128:1$).
> * **Donate Low-to-Mid Tier Foot Prisoners**: T3 and T4 foot units (selling for 25–50 gold) yield excellent influence returns relative to their market value. They convert at a highly favorable Gold-to-Influence ratio ($\approx 35\text{ to }50$ gold per 1.0 Influence), making them the cheapest source of Influence in the game.
> * **Keep Regular Troops for Roguery XP**: Since Roguery XP scales strictly on Troop Tier and is identical for foot and mounted units, you gain the same Roguery progress from a T3 foot unit (25 gold) as you do from a T3 mounted unit (62 gold). Keep your high-value mounts for gold and burn your lower-value foot units for XP/influence.

---


## 3. Troop Combat AI and Skill Scaling

Weapon skills determine a troop's actual combat effectiveness in two distinct ways: by scaling their direct weapon stats (damage/speed) and by feeding the AI decision matrices.

### The Two AI tracks
Bannerlord assigns two distinct AI brains to every agent during live battles:
1. `meleeAI`: Governed by the troop's melee skills.
2. `currentAI`: Governed by the skill of the weapon currently equipped (or Athletics if unarmed).

Under normal/high difficulty configurations, both tracks scale as follows:
$$\text{AI Level} = \text{Clamp}\left(\frac{\text{Effective Skill}}{300} \times 0.96, 0, 1\right)$$

* A $+30$ skill bonus translates to a $+0.096$ boost in AI level.
* A $+80$ skill stack translates to a $+0.256$ boost in AI level.

### Direct Weapon Scaling
Weapon stats scale linearly with effective skill points:

| Skill | Affected Attribute | Mod per Skill Point | $+30$ Skill Bonus | $+80$ Skill Bonus |
| :--- | :--- | :---: | :---: | :---: |
| **One Handed** | Speed, Damage | $+0.07\%$ Speed, $+0.15\%$ Damage | $+2.1\%$ Speed, $+4.5\%$ Damage | $+5.6\%$ Speed, $+12.0\%$ Damage |
| **Two Handed** | Speed, Damage | $+0.06\%$ Speed, $+0.16\%$ Damage | $+1.8\%$ Speed, $+4.8\%$ Damage | $+4.8\%$ Speed, $+12.8\%$ Damage |
| **Polearm** | Speed, Damage | $+0.06\%$ Speed, $+0.07\%$ Damage | $+1.8\%$ Speed, $+2.1\%$ Damage | $+4.8\%$ Speed, $+5.6\%$ Damage |
| **Bow** | Damage, Accuracy | $+0.11\%$ Damage, $+0.09\%$ Accuracy | $+3.3\%$ Damage, $+2.7\%$ Accuracy | $+8.8\%$ Damage, $+7.2\%$ Accuracy |
| **Crossbow** | Reload, Accuracy | $+0.07\%$ Reload, $+0.05\%$ Accuracy | $+2.1\%$ Reload, $+1.5\%$ Accuracy | $+5.6\%$ Reload, $+4.0\%$ Accuracy |
| **Throwing** | Draw, Damage, Accuracy | $+0.07\%$ Draw, $+0.06\%$ Damage, $+0.06\%$ Acc | $+2.1\%$ Draw, $+1.8\%$ Dmg, $+1.8\%$ Acc | $+5.6\%$ Draw, $+4.8\%$ Dmg, $+4.8\%$ Acc |

### Melee AI Behaviors
The AI level is mapped to different combat behaviors through curves (linear, root, and power):

| Driven Property | Formula Shape | Combat Behavior Impact |
| :--- | :--- | :--- |
| `AIBlockOnDecideAbility` | $\text{Lerp}(0.5, 0.99, \sqrt{\text{meleeAI}})$ | Root curve. Massive gains for low-tier units, stabilizing at high tiers. |
| `AIParryOnDecideAbility` | $\text{Lerp}(0.5, 0.95, \text{meleeAI})$ | Linear. Steady increase in parrying probability. |
| `AIParryOnAttackAbility` | $\text{Clamp}(\text{meleeAI}, 0, 1)$ | Linear. Ability to parry during active swings. |
| `AIDecideOnRealizeEnemyBlocking` | $\text{Clamp}(\text{meleeAI}^{2.5} - 0.1, 0, 1)$ | Power curve. Elite troops read blocks instantly; low-tier troops cannot. |
| `AIRealizeBlockingIncorrectSide` | $\text{Clamp}(\text{meleeAI}^{2.5} - 0.01, 0, 1)$ | Power curve. Corrects blocking angle under pressure. |
| `AIRandomizedDefendMistakeChance` | $1 - \text{meleeAI}^3$ | Power curve. Elite troops virtually never make defensive direction mistakes. |
| `AISetNoAttackTimerAfterHit` | $\text{Lerp}(0.33, 1, \text{meleeAI})$ | Linear. Speeds up weapon recovery after being struck. |
| `AISetNoDefendTimerAfterHitting` | $\text{Lerp}(0.1, 0.99, \text{meleeAI}^2)$ | Power curve. Elite troops chain defense into offense smoothly. |

#### Case Study: Recruit vs. Elite Polearm AI Scaling
Because different AI behaviors use different curves, a skill buff has very different effects on a recruit than an elite unit. We model this using a **$+50$ Polearm skill buff**, which is the maximum in-game buff achievable by stacking the Polearm captain perks *Clean Thrust* ($+30$ Polearm) and *Counterweight* ($+20$ Polearm):

* **Imperial Recruit**: Base Polearm 20 (Base AI 0.064)
* **Elite Menavliaton**: Base Polearm 130 (Base AI 0.416)

| Unit State | AI Level | Block-On-Decide (Root Curve) | Realize Enemy Blocking (Power Curve) |
| :--- | :---: | :---: | :---: |
| **Imperial Recruit** | 0.064 | 0.624 | 0.000 |
| **Recruit +50 Polearm Buff** | 0.224 | **0.732** ($+10.8\%$) | 0.000 (No Change) |
| **Elite Menavliaton** | 0.416 | 0.816 | 0.012 |
| **Elite Menavliaton +50 Buff** | 0.576 | **0.872** ($+5.6\%$) | **0.152** ($+14.0\%$ flat / $12.7\times$ relative increase) |

> [!TIP]
> **Recruit vs. Elite Captain Buff Scaling**: The recruit gains a solid defensive blocking boost from the $+50$ skill buff, but gains no offensive block-reading capability. The Elite Menavliaton gains a smaller defensive block percentage increase (due to root-curve diminishing returns), but their ability to read and counter enemy blocks leaps from a negligible $1.2\%$ to $15.2\%$ (a flat $+14.0\%$ increase, which is a massive $12.7\times$ relative improvement).

### Shield and Defensive AI

| Driven Property | Formula Shape | Combat Behavior Impact |
| :--- | :--- | :--- |
| `AIUseShieldMissileProbability` | $0.1 + 0.6 \cdot \text{AI} + 0.2 \cdot (\text{AI} + \text{Defensiveness})$ | Determines how reliably a unit raises their shield against incoming fire. |
| `AIDefendWithShieldDecisionChance` | $\text{Min}(2, 0.5 + \text{AI} + 0.6 \cdot (\text{AI} + \text{Defensiveness}))$ | Affects shield block activation timing in close combat. |

### Ranged AI
Ranged AI governs fire rate and shooting error based on the equipped missile skill:

* **AiShootFreq**: $0.3 + 0.7 \times \text{currentAI}$ (Elites shoot over twice as fast as recruits).
* **AiWaitBeforeShootFactor**: $1 - 0.5 \times \text{currentAI}$ (Elites target immediately).
* **AiRangerLeadError**: Min and Max bounds shrink as $\text{currentAI}$ approaches $1.0$, minimizing missed shots on moving targets.
* **AiRangerVertical/HorizontalError**: Multipliers scale directly with $(1 - \text{currentAI})$, shrinking target spreads.

---

## 4. Combat Physics and Damage Formulas

Melee combat damage in Bannerlord does not use simple linear subtraction. Instead, the game's core collision engine (`DefaultStrikeMagnitudeModel.ComputeRawDamage`) processes incoming kinetic energy (strike magnitude) against local armor using a multi-step formula that accounts for flat armor "soak" and dynamic damage-type scaling.

### The Armor Mitigation Formula
The final raw damage delivered by a strike is calculated as:
$$\text{Final Raw Damage} = \Big[ C_{\text{blunt}} + (1 - B) \cdot C_{\text{nonBlunt}} \Big] \cdot R_{\text{absorb}}$$

Where:
* **Blunt Component ($C_{\text{blunt}}$):** Represents the concussive force transmitted directly through the armor.
  $$C_{\text{blunt}} = B \cdot M \cdot \left(\frac{50}{50 + A}\right)$$
* **Non-Blunt Component ($C_{\text{nonBlunt}}$):** Represents the cutting or piercing force that must overcome the armor's surface resistance before dealing damage.
  $$C_{\text{nonBlunt}} = \max\left(0, M \cdot \left(\frac{50}{50 + A}\right) - k \cdot A\right)$$

#### Equation Constants by Damage Type

| Damage Type | Blunt Damage Factor ($B$) | Armor Soak Factor ($k$) | Key Characteristic |
| :--- | :---: | :---: | :--- |
| **Cut (Slash)** | $0.10$ | $0.50$ | High base damage, heavily mitigated by armor. |
| **Pierce (Thrust)** | $0.25$ | $0.33$ | Moderate armor penetration, scales with velocity. |
| **Blunt (Concussive)** | $0.60$ | $0.20$ | Extreme armor penetration, ignores most soak. |

* **$M$ (Strike Magnitude):** The raw incoming blow magnitude (kinetic energy), scaled by weapon damage, combat skill, and physics speed bonuses.
* **$A$ (Armor Effectiveness):** The target's local armor value at the hit location (e.g., helmet value for headshots).
* **$R_{\text{absorb}}$ (Absorption Ratio):** Damage absorption modifier (typically $1.0$ for human torso hits, modified for mounts or shield strikes).

---

### Damage Type Scaling Grid (Magnitude $M = 100$)
This table models the final damage dealt by a standard $100$-magnitude hit at different armor values ($A$) across all three damage types (assuming $R_{\text{absorb}} = 1.0$):

| Armor Level ($A$) | Cut Damage (Dealt) | Pierce Damage (Dealt) | Blunt Damage (Dealt) |
| :---: | :---: | :---: | :---: |
| **0** (No Armor) | 100.00 | 100.00 | 100.00 |
| **20** (Light Armor) | 62.43 | 66.48 | 69.83 |
| **40** (Medium Armor) | 37.56 | 45.66 | 52.36 |
| **60** (Heavy Armor) | 18.46 | 30.60 | 40.65 |
| **80** (Super Heavy Armor) | 3.85 | 18.67 | 32.06 |

> [!IMPORTANT]
> **Armor Mitigation Divergence**: Against a heavily armored knight ($A = 80$), a **Cut** attack loses its entire non-blunt component to armor soak ($C_{\text{nonBlunt}} = 0$), leaving only the $10\%$ blunt impact component ($3.85$ damage). Conversely, a **Blunt** attack bypasses most of the soak, dealing **$32.06$ damage**—more than **8 times** the damage of Cut under the exact same magnitude!

---

### Case Study: Sturgian Heroic Line Breaker vs. Imperial Elite Menavliaton

Despite the Imperial Elite Menavliaton using a long, high-damage weapon (the **Menavlion**, $120$ Cut swing) and the Sturgian Heroic Line Breaker using a short, lower-damage weapon (the **Northern Reinforced Two-Handed Mace**, $74$ Blunt swing), the Sturgian units consistently win in head-to-head brawls. This counter-intuitive outcome is explained by four distinct mechanics:

1. **Armor Mitigation Mitigation:** Against standard heavy armor ($A = 45–50$), the Menavlion's Cut damage is heavily mitigated by soak ($k=0.5$), reducing a $126$-magnitude hit to **$\sim 35.25$ damage**. The Line Breaker's Mace, utilizing Blunt scaling ($k=0.2$, $B=0.6$), keeps its concussive components intact, dealing **$\sim 34.36$ damage** from an $81.4$-magnitude hit. Despite the Menavlion's $62\%$ base damage advantage, both units require exactly **3 hits** to kill each other.
2. **Attack Frequency:** The Northern Reinforced Two-Handed Mace is a much faster weapon (**89 swing speed** vs. the Menavlion's **75–80**), allowing the Sturgian to hit first and more frequently in a duel.
3. **Combat AI Level Difference:** The Line Breaker has **150 Two-Handed skill** (AI Level **0.480**), while the Menavliaton has **130 Polearm skill** (AI Level **0.416**). This higher AI Level allows the Sturgian to transition from blocking to attacking faster (`AISetNoDefendTimerAfterHitting` uses an $\text{AI}^2$ power curve) and make fewer defensive direction mistakes.
4. **Length and Spacing:** The Menavlion's length (**163 cm**) is a massive liability in a tight infantry blob. When units press chest-to-chest, the Menavlion's blade collides behind or inside the enemy's collision box, triggering a "clash/bounce" animation that deals $0$ damage. The Sturgian Mace's short length (**102 cm**) is optimized for close quarters, swinging cleanly without bouncing.

---

## 5. Village Raiding and Loot Pulses

Village raiding is structured as a damage accumulator loop that yields loot at set intervals.

### Raid Pulse Loop
Raid progress and damage accumulate hourly until a threshold of $0.05$ is reached:
$$\text{Raid Damage Per Hour} = \frac{\sqrt{\text{Attacker Troop Count}} + 5}{900}$$
$$\text{Raid Damage This Update} = \text{Raid Damage Per Hour} \times \Delta\text{Hours}$$

When the total accumulated damage crosses the $0.05$ threshold, the game runs a **Loot Pulse** and resets the accumulator:

$$\text{Lost Hearth} = \text{Pulse Damage} \times 0.5 \times \text{Current Village Hearth}$$
$$\text{Loot Gold} = \lfloor\text{Lost Hearth} \times 4 \times \text{Raid Loot Multiplier}\rfloor$$
$$\text{New Village Hearth} = \text{Current Village Hearth} - \text{Lost Hearth}$$
$$\text{Settlement HP} = \text{Settlement HP} - \text{Pulse Damage}$$

* **Hearth Destruction**: At a standard $0.05$ damage pulse, a village loses $2.5\%$ of its current hearth.
* **Decaying Returns**: Because hearth is subtracted after each pulse, a completed 20-pulse raid reduces a village's total hearth by approximately $39.7\%$ of its starting value:
$$\text{Total Lost Hearth} = \text{Starting Hearth} \times (1 - 0.975^{20})$$

### The Three Item Loot Lanes
Each loot pulse yields items through three separate processing lanes:

#### Lane 1: Stored Village Inventory
Loot is extracted directly from the village's active inventory ledger (varies based on recent village transactions):
$$\text{Stored Items Removed} = \text{Min}(\text{Existing Count}, \text{RoundRandomized}(\text{Existing Count} \times \text{Pulse Damage}))$$
$$\text{Loot Chance} = 0.5 \times \text{Raid Loot Multiplier}$$
* Approximately $5\%$ of stored inventory is removed from the village per pulse.
* Half of those items are added to the player's raid loot ledger.
* **Perk Interaction**: If the item is food and the attacker has `Efficient Campaigner`, each food payout gains one extra unit.

#### Lane 2: Village Production
This lane is deterministic and is dictated entirely by the village type:
$$\text{Production Progress} += \text{Lost Hearth} \times \frac{\text{Production Weight}}{60} \times \text{Raid Loot Multiplier}$$
$$\text{Payout} = \lfloor\text{Production Progress}\rfloor$$

* **Perk Interaction**: If a payout occurs and the item is food, `Efficient Campaigner` adds $+1$ unit. 
* Production food is not doubled as a percentage; it receives a flat $+1$ bonus per payout event. If you are looting rare, low-count foods, this $+1$ can double your yields.

#### Lane 3: Common Loot
Common loot is randomly selected from a global table for every whole point of `Lost Hearth`:
$$\text{Attempts} = \lfloor\text{Lost Hearth}\rfloor$$
$$\text{Success Chance Per Attempt} = 0.25 \times \text{Raid Loot Multiplier}$$

On success, items are selected using value-based weights:
$$\text{Common Weight} = \frac{100}{\text{Item Value} + 1}$$

Because of this weight formula, cheap items dominate the common loot pool:

| Item | Value | Weight | Pick Chance | Expected Count per Attempt |
| :--- | ---: | ---: | ---: | ---: |
| **Grain** (Food) | 10 | 9.091 | 49.85% | 0.1246 |
| **Hardwood** | 25 | 3.846 | 21.09% | 0.0527 |
| **Hides** | 50 | 1.961 | 10.75% | 0.0269 |
| **Sheep** | 80 | 1.235 | 6.77% | 0.0169 |
| **Mule** | 120 | 0.826 | 4.53% | 0.0113 |
| **Pottery** | 210 | 0.474 | 2.60% | 0.0065 |
| **Linen** | 245 | 0.407 | 2.23% | 0.0056 |
| **Tools** | 250 | 0.398 | 2.18% | 0.0055 |

### Roguery, Ransom, And Crime Utility Perks
Roguery is not a single raid-damage lane. Its perks split across bandit handling, ransoms, hostile village actions, crime decay, governor security/economy side effects, and personal combat utilities:
* **Roguery (Level 25) - `Sweet Talker`**: $+20\%$ chance for convincing bandits to leave in peace with barter, or $-20\%$ prisoner escape chance as governor.
* **Roguery (Level 50) - `Deep Pockets`**: Doubles tournament betting allowance, or reduces bandit troop wages by $-20\%$.
* **Roguery (Level 75) - `In Best Light`**: Grants one extra troop from village notables when successfully forced for volunteers, or $+20\%$ faster recovery from raids for your villages as clan leader.
* **Roguery (Level 100) - `Manhunter`**: $+20\%$ better ransom broker deals for regular troops, or $+10$ prisoner limit.
* **Roguery (Level 125) - `White Lies`**: Your criminal rating with factions decays $+20\%$ faster.
* **Roguery (Level 175) - `Salt the Earth`**: $+20\%$ more loot when villagers comply with hostile actions, or $+5\%$ tariff revenue as governor.
* **Roguery (Level 200) - `Carver`**: $+10\%$ damage with daggers or civilian weapons in combat.
* **Roguery (Level 225) - `Dirty Fighting`**: $+50\%$ stun duration for kicking, or smuggles two random food items daily to a besieged governed settlement.
* **Roguery (Level 225) - `Arms Dealer`**: $-20\%$ weapon sell-price penalty, or $+200\%$ militia per day in a besieged governed settlement.
* **Roguery (Level 250) - `Dash and Slash`**: $+50\%$ speed-bonus damage while on foot, or $+2\%$ two handed damage to troops in your formation.
* **Roguery (Level 250) - `Fleet Footed`**: $+10\%$ combat movement speed while carrying no weapons or shields, plus $+30\%$ escape chance when imprisoned by mobile parties.
* **Roguery (Level 275) - `Rogue Extraordinaire`**: $+1\%$ loot amount for every skill point above $200$.

### Production Weights by Village Type
The values below represent the production weights used in Lane 2. The number in parentheses shows the progress generated per clean $0.05$ pulse at $400$ village hearth:

#### Food & Livestock Production Weights
* **wheat_farm**: Grain `50` (`8.33`), Cow `0.2` (`0.03`), Sheep `0.4` (`0.07`), Hog `0.8` (`0.13`)
* **fisherman**: Fish `28` (`4.67`)
* **vineyard**: Grapes `11` (`1.83`)
* **date_farm**: Dates `8` (`1.33`)
* **olive_trees**: Olives `12` (`2.00`)
* **cattle_farm**: Cow `2` (`0.33`), Butter `4` (`0.67`), Cheese `4` (`0.67`)
* **sheep_farm**: Sheep `4` (`0.67`), Wool `10` (`1.67`), Butter `2` (`0.33`), Cheese `2` (`0.33`)
* **swine_farm**: Hog `8` (`1.33`), Butter `2` (`0.33`), Cheese `2` (`0.33`)

#### Raw Resource Production Weights
* **lumberjack**: Hardwood `18` (`3.00`)
* **clay_mine**: Clay `10` (`1.67`)
* **salt_mine**: Salt `15` (`2.50`)
* **iron_mine**: Iron `10` (`1.67`)
* **flax_plant**: Flax `18` (`3.00`)
* **silk_plant**: Cotton `8` (`1.33`)
* **silver_mine**: Silver `3` (`0.50`)
* **trapper**: Fur `1.4` (`0.23`)

#### Mount & Horse Production Weights
* **europe_horse_ranch**: Empire Horse `2.1` (`0.35`), T2 Horse `0.5` (`0.08`), T3 Horse `0.07` (`0.01`), Sumpter `0.5` (`0.08`), Mule `0.5` (`0.08`), Saddle Horse `0.5` (`0.08`), Old Horse `0.5` (`0.08`), Hunter `0.2` (`0.03`), Charger `0.2` (`0.03`)
* **sturgian_horse_ranch**: Sturgia Horse `2.5` (`0.42`), T2 Horse `0.7` (`0.12`), T3 Horse `0.1` (`0.02`), Sumpter/Mule/Saddle/Old Horse `0.5` (`0.08`), Hunter/Charger `0.2` (`0.03`)
* **vlandian_horse_ranch**: Vlandia Horse `2.1` (`0.35`), T2 Horse `0.4` (`0.07`), T3 Horse `0.08` (`0.01`), Sumpter/Mule/Saddle/Old Horse `0.5` (`0.08`), Hunter/Charger `0.2` (`0.03`)
* **battanian_horse_ranch**: Battania Horse `2.3` (`0.38`), T2 Horse `0.7` (`0.12`), T3 Horse `0.09` (`0.02`), Sumpter/Mule/Saddle/Old Horse `0.5` (`0.08`), Hunter/Charger `0.2` (`0.03`)
* **steppe_horse_ranch**: Khuzait Horse `1.8` (`0.30`), T2 Horse `0.4` (`0.07`), T3 Horse `0.05` (`0.01`), Sumpter/Mule `0.5` (`0.08`)
* **desert_horse_ranch**: Aserai Horse `1.7` (`0.28`), T2 Horse `0.3` (`0.05`), T3 Horse `0.05` (`0.01`), Camel/Pack Camel `0.3` (`0.05`), War Camel `0.08` (`0.01`), Sumpter `0.4` (`0.07`), Mule `0.5` (`0.08`)

### Efficient Campaigner Food Payout Bonus
This table models a clean 20-pulse full raid with a starting hearth of $400$ and a default loot multiplier, comparing base production food loot yields with and without `Efficient Campaigner`:

| Source Village | Food Item | Base Production | With `Efficient Campaigner` | Net Yield Increase |
| :--- | :--- | :---: | :---: | ---: |
| **wheat_farm** | Grain | 132 | 152 | $+15.2\%$ |
| **fisherman** | Fish | 74 | 94 | $+27.0\%$ |
| **vineyard** | Grapes | 29 | 49 | $+69.0\%$ |
| **date_farm** | Dates | 21 | 41 | $+95.2\%$ |
| **olive_trees** | Olives | 31 | 51 | $+64.5\%$ |
| **cattle_farm** | Butter | 10 | 20 | $+100.0\%$ |
| **cattle_farm** | Cheese | 10 | 20 | $+100.0\%$ |
| **sheep_farm** | Butter | 5 | 10 | $+100.0\%$ |
| **sheep_farm** | Cheese | 5 | 10 | $+100.0\%$ |
| **swine_farm** | Butter | 5 | 10 | $+100.0\%$ |
| **swine_farm** | Cheese | 5 | 10 | $+100.0\%$ |

### Placed Village Hearth Ranges (Vanilla Map)
Higher hearths act as a direct multiplier for raid gold, production progress, and common loot attempts. Use this distribution chart to select high-value targets:

| Village Type | Total Count | Min Hearth | Median Hearth | Max Hearth |
| :--- | :---: | :---: | :---: | :---: |
| **vlandian_horse_ranch** | 3 | 280 | 680 | 680 |
| **vineyard** | 15 | 125 | 488 | 809 |
| **fisherman** | 22 | 125 | 362 | 655 |
| **date_farm** | 9 | 183 | 454 | 540 |
| **silver_mine** | 7 | 110 | 395 | 705 |
| **lumberjack** | 16 | 132 | 339.5 | 697 |
| **cattle_farm** | 15 | 104 | 339 | 652 |
| **wheat_farm** | 49 | 101 | 267 | 825 |
| **salt_mine** | 12 | 130 | 277 | 722 |

---

## 6. Command, Tactics & Leadership Directory

The following directory outlines the commander, battle management, and lord recruitment perks that shape faction warfare.

### Battle Command & Formations (Tactics)
* **Tactics (Level 25) - `Tight Formations`**: Reduces infantry morale penalty by $-25\%$ when in close formations. (Captain)
* **Tactics (Level 50) - `Decisive Battle`**: $+5\%$ simulation damage in plains, steppes, and deserts; alternate captain side gives $+5\%$ movement speed in those terrains.
* **Tactics (Level 50) - `Extended Skirmish`**: $+10\%$ simulation damage in snow and forest terrain; alternate captain side gives $+2\%$ formation movement speed there.
* **Tactics (Level 75) - `Small Unit Tactics`**: Adds one hideout crew member, or $+5\%$ captain movement speed when the formation has fewer than 15 soldiers.
* **Tactics (Level 100) - `Coaching`**: $+3\%$ simulation damage, or $+1\%$ captain damage to troops in your formation.
* **Tactics (Level 100) - `Law Keeper`**: $+10\%$ simulation damage against bandits, or $+4\%$ captain damage against bandits.
* **Tactics (Level 125) - `Improviser`**: Reduces troop losses by $-25\%$ when breaking into or out of a besieged settlement. (Party Leader)
* **Tactics (Level 125) - `Swift Regroup`**: Reduces troops left behind when escaping from battle by $-50\%$. (Party Leader)
* **Tactics (Level 150) - `On The March`**: $-20\%$ enemy fortification bonus in simulations, or $+20\%$ fortification bonus to the governed settlement.
* **Tactics (Level 175) - `Pick Them Off The Walls`**: $25\%$ chance to deal double damage to defenders during siege bombardment. (Engineer)
* **Tactics (Level 225) - `Besieged`**: $+50\%$ influence gain from winning sieges. (Personal)
* **Tactics (Level 225) - `Pre Battle Maneuvers`**: $+25\%$ influence from winning battles, or $+1\%$ simulation damage per 100 skill difference with the enemy.
* **Tactics (Level 250) - `Counter Offensive`**: $+10\%$ damage in battle simulations when attacking or when outnumbered. (Party Leader)
* **Tactics (Level 275) - `Tactical Mastery`**: $+0.5\%$ damage per skill point above 200 in battle simulations. (Army Leader)

> [!NOTE]
> Tactics is a mixed tree. Several entries in this directory are simulation, siege, escape, or governor-fortification mechanics rather than live formation commands; use them only when that off-bucket role matches the campaign plan.

### Leadership, Morale & Recruitment (Leadership)
* **Leadership (Level 50) - `Fervent Attacker`**: $+4$ starting battle morale when attacking, or $+50\%$ recruitment rate for tier 1-3 prisoners.
* **Leadership (Level 50) - `Stout Defender`**: $+8$ starting battle morale when defending, or $+50\%$ recruitment rate for tier 4+ prisoners.
* **Leadership (Level 100) - `Loyalty and Honor`**: Tier 3+ troops in party do not retreat due to low morale, and $+30\%$ prisoner recruitment speed. (Party Leader)
* **Leadership (Level 125) - `Leader of the Masses`**: $+5$ party size limit for each owned town. (Clan Leader)
* **Leadership (Level 125) - `Presence`**: $+5$ security per day while waiting in a town, or no morale penalty for recruiting prisoners of your faction.
* **Leadership (Level 150) - `Citizen Militia`**: $+20\%$ veteran militia spawn rate as governor, or $+10\%$ morale from victories.
* **Leadership (Level 150) - `Veteran's Respect`**: $+20$ garrison size as governor, or converts bandit troops into regular troops as party leader.
* **Leadership (Level 175) - `Uplifting Spirit`**: $+10$ battle morale in siege battles, or $+10$ party size limit.
* **Leadership (Level 225) - `Great Leader`**: $+5$ battle morale to all troops at the start of a battle. (Army Leader)
* **Leadership (Level 225) - `Make a Difference`**: $+100\%$ battle morale to troops when you kill an enemy. (Personal)
* **Leadership (Level 250) - `Talent Magnet`**: $+10$ party size and $+1$ clan party limit. (Clan Leader)
* **Leadership (Level 250) - `We Pledge our Swords`**: $+1$ companion limit, or up to $+10$ starting battle morale from tier 6 troops in the party.
