# Fiefs and Settlement Governance Manual

This manual covers the complete mechanics of fief stabilization, economic taxation, garrison defense, trade-bound supply chains, workshops, and alley systems. It details the mathematical models governing loyalty drift, price pressure, village production tiers, and governor perk synergies.

---

## 1. Fief Development and Stability

Fief development is the foundation of faction dominance in Bannerlord. A town's stability directly dictates its daily tax yields, construction speeds, and defense capacities.

### Loyalty Drift Formula
Loyalty is the central metric of stability. It possesses a natural drift toward the baseline of $50$:
$$\text{Daily Loyalty Drift} = -0.1 \times (\text{Current Loyalty} - 50)$$

> [!IMPORTANT]
> **Loyalty Decay and Cultural Drag**:
> * **Decaying Drift**: Raw loyalty bonuses have varying impacts depending on where the town currently sits. A town at $25$ loyalty gains $+2.5$ daily loyalty from drift (helping it recover), whereas a highly stable town at $75$ loyalty loses $-2.5$ daily loyalty from drift.
> * **Cultural Penalties**: Conquering a town of a different culture applies a massive $-3$ daily loyalty penalty.
> * **Governor Mitigation**: Assigning a governor of the same culture as the settlement offsets this with a $+1$ daily loyalty bonus, whereas mismatching cultures adds a $-1$ penalty.

| Current Loyalty | Daily Drift | Drift Tendency |
| :---: | :---: | :--- |
| **15** | +3.5 | Rapid recovery pressure (Rebellion imminent) |
| **25** | +2.5 | Strong recovery pressure (Rebellious state) |
| **40** | +1.0 | Moderate recovery pressure |
| **50** | 0.0 | Neutral equilibrium |
| **60** | -1.0 | Mild decay pressure |
| **75** | -2.5 | Strong decay pressure |

### Construction Power
The base construction speed is derived directly from a settlement's prosperity:
$$\text{Base Construction Power} \approx \text{Prosperity} \times 0.01$$

* **Loyalty Penalties**: Low loyalty significantly degrades construction power. At $0$ loyalty, projects cease entirely.
* **Boost Projects**: Spending gold to boost projects increases construction speed, scaled by the governor's Steward, Engineering, or Trade perks.

### Food Pressure and Reserves
Food acts as the ultimate hard cap on settlement growth. Prosperity and garrison sizes consume food daily:
* **Garrison Consumption**: $1$ unit of food per $20$ garrisoned troops.
* **Prosperity Consumption**: $1$ unit of food per $40$ prosperity points.
* **Storage Limits**: Towns have a base storage limit of $300$ food units; Castles receive a $+150$ bonus (totaling $450$ units).

> [!WARNING]
> High prosperity can starve a town. If prosperity growth outpaces village food production and caravan imports, food reserves will empty, triggering starvation. Starvation causes daily prosperity loss and garrison desertion.

### Development Governor Perks

| Skill | Level | Perk | Effect | Tactical Read |
| :--- | ---: | :--- | :--- | :--- |
| **Athletics** | 175 | `Durable` | $+1$ daily loyalty | Reliable passive loyalty anchor. |
| **Leadership** | 75 | `Heroic Leader` | $+1$ daily loyalty | Early, highly efficient loyalty driver. |
| **Medicine** | 200 | `Physician of People` | $+1$ daily loyalty | Excellent dual-utility perk (loyalty and healing). |
| **Riding** | 50 | `Well Strapped` | $+0.5$ daily loyalty | Cheap early stabilizer if governor has Riding skill. |
| **Bow** | 150 | `Discipline` | $+1$ daily loyalty | Strong loyalty anchor for ranged governors. |
| **Engineering** | 75 | `Carpenters` | $+12\%$ town project speed | Speeds up building projects in towns. |
| **Engineering** | 75 | `Military Planner` | $+25\%$ castle project speed | Saves time on projects in castles. |
| **Engineering** | 150 | `Stonecutters` | $+30\%$ military project speed | Fast-tracks walls, barracks, and fortifications. |
| **Engineering** | 175 | `Battlements` | $+100$ maximum food storage | Expands town food reserve limits to prevent starvation. |
| **Engineering** | 250 | `Architectural Commissions` | $+20$ gold/day bonus | Daily gold bonus for continuous projects. |
| **Steward** | 150 | `Relocation` | $+20\%$ project boost effect | Speeds up projects when boosted by money. |
| **Steward** | 200 | `Contractors` | $+10\%$ project effects | Increases the output efficiency of completed buildings. |
| **Steward** | 200 | `Forced Labor` | $+1\%$ speed per 3 prisoners | Utilizes captive labor for faster construction. |
| **Athletics** | 175 | `Energetic` | $+20\%$ village hearth growth | Accelerates bound village production and tax yields. |
| **Medicine** | 150 | `Pristine Streets` | $+1$ daily prosperity | Simple, steady town-value scaling. |
| **Medicine** | 250 | `Helping Hands` | $-50\%$ starvation prosperity loss | Crucial safety net for high-prosperity settlements. |

---

## 2. Fief Economy and Revenue Layers

A fief's financial yield consists of town taxes, market tariffs, village taxes, and workshop revenues.

### Tax and Tariff Formulas
Daily town taxes scale directly with prosperity:
$$\text{Raw Town Tax} \approx \text{Prosperity} \times 0.35$$

* **Tariffs**: Every trade transaction by caravans, villagers, or players adds a commission tariff to the town treasury, scaled by Steward and Trade perks.
* **Security commission**: Security directly controls market efficiency. If security drops below $75$, a commission penalty is applied, scaling up to a maximum $-10\%$ tax revenue cut.

### The Prosperity Balancing Act
While prosperity scales tax base and construction power, it introduces security drag and food consumption:

| Metric | Calculation | Economic Impact |
| :--- | :---: | :--- |
| **Tax Base** | $\approx \text{Prosperity} \times 0.35$ | Primary source of clan passive income. |
| **Construction Base** | $\approx \text{Prosperity} \times 0.01$ | Speeds up building progression. |
| **Food Consumption** | $1 \text{ food} \text{ per } 40 \text{ prosperity}$ | Reduces food reserves, limiting maximum garrison size. |
| **Security Drag** | $\text{Max}(-5, -0.0005 \times \text{Prosperity})$ | Prosperity decreases security, requiring stronger garrisons. |

### Economy Governor Perks

* **Steward (Level 125) - `Logistician`**: $+10\%$ tax income.
* **Steward (Level 125) - `Giving Hands`**: $+10\%$ tariff income.
* **Steward (Level 275) - `Price of Loyalty`**: $+0.5\%$ tax income per Steward point above $200$.
* **Trade (Level 100) - `Toll Gates`**: $+30$ gold per visiting caravan.
* **Trade (Level 100) - `Traveling Rumors`**: $+20$ gold per visiting villager party.
* **Trade (Level 150) - `Content Trades`**: $+10\%$ tariff income.
* **Trade (Level 200) - `Granary Accountant`**: $+20\%$ production to food villages (grain, olives, fish, dates).
* **Trade (Level 200) - `Tradeyard Foreman`**: $+20\%$ production to raw material villages (clay, iron, silk, silver).
* **Engineering (Level 50) - `Siegeworks`**: $+10\%$ tariff revenue.
* **Engineering (Level 225) - `Improved Tools`**: $+10\%$ production speed to bound villages.
* **Athletics (Level 200) - `Steady`**: $+10\%$ production to mines, lumber camps, and clay pits.

---

## 3. Settlement Defense and Garrison Logistics

Defending a fief involves managing security, maintaining garrisons, training veteran militias, and surviving siege bombardments.

### Security Drift
Security acts as the law-and-order tracker. It drifts back to $50$ daily:
$$\text{Daily Security Drift} = \frac{-(\text{Security} - 50)}{15}$$

> [!NOTE]
> **Security Drift and Drag**:
> * **Garrison Strength**: Garrisoned troops supply positive security pressure based on their total combat power. Unwounded elite troops yield far higher security pressure than recruits.
> * **Prosperity Drag**: High prosperity lowers security (up to a max drag of $-5$), necessitating larger, higher-tier garrisons to maintain the law-and-order bonus.

### Defense, Garrison, And Siege Perks

| Skill | Level | Perk | Effect | Tactical Read |
| :--- | ---: | :--- | :--- | :--- |
| **One Handed** | 50 | `To Be Blunt` | $+0.5$ daily security | Cheap flat security anchor. |
| **One Handed** | 175 | `Stand United` | $+30\%$ security from garrison | Scales positive pressure of existing garrison. |
| **Bow** | 100 | `Mounted Archery` | $+20\%$ security from archers | Multiplies security output of ranged garrisons. |
| **Tactics** | 250 | `Gens d'armes` | $+1$ daily security | Late Tactics governor stabilizer. |
| **Bow** | 100 | `Merry Men` | $+1$ daily militia recruitment | Fast-tracks militia headcount expansion. |
| **Steward** | 50 | `Seven Veterans` | $+10\%$ veteran militia rate | Improves the spawn quality of defense forces. |
| **Polearm** | 200 | `Drills` | $+100\%$ veteran militia rate | Crucial quality multiplier for garrisoned defenders. |
| **Leadership** | 25 | `Raise The Meek` | $+3$ daily XP to garrison | Passively trains defenders. |
| **Athletics** | 225 | `Strong Legs` | $-20\%$ food use under siege | Significantly extends survival time when blockaded. |
| **Bow** | 150 | `Hunter Clan` | $+30\%$ garrison size limit | Increases maximum garrison capacity. |
| **Engineering** | 25 | `Torsion Engines` | $+10\%$ ranged siege engine build speed | Accelerates ranged engine construction. |
| **Engineering** | 100 | `Dreadful Besieger` | $+10\%$ accuracy to siege engines during bombardment | Improves governed-settlement bombardment reliability. |
| **Engineering** | 100 | `Wall Breaker` | $+25\%$ wall damage during siege bombardment | Increases wall-breaking output. |
| **Engineering** | 125 | `Salvager` | $+20\%$ salvage yield | Enhances scrap recovery during sieges. |
| **Engineering** | 150 | `Siege Engineer` | $+30\%$ defensive siege engine hit points / fire engine construction | Strengthens defensive engines or unlocks fire versions through the Engineer role. |
| **Engineering** | 175 | `Camp Building` | $-20\%$ casualty chance from siege bombardments | Reduces bombardment losses through the Engineer role. |
| **Engineering** | 200 | `Engineering Guilds` | $+25\%$ wall hit points | Directly improves siege defense resilience. |
| **Engineering** | 250 | `Clockwork` | $+25\%$ ballista reload speed / $+20\%$ boost-project effect | Improves siege-engine tempo or governed-settlement project boosting. |
| **Tactics** | 175 | `Make Them Pay` | $+25\%$ damage to siege engines | Boosts bombardment defense. |

---

## 4. The Settlement Supply Chain

Bannerlord's economy is inventory-based. Real goods must flow from villages to markets, and workshops must consume physical inputs to generate outputs.

### Hidden Artisans
Every town contains a hidden `artisans` workshop in slot $0$ (the first of its four internal workshop slots):
* **Artisan Production**: Craftsmen make everyday processed goods (garments, light armor, tools, basic weapons) and sell them directly into the town market.
* **Input Dependency**: Artisans draw raw materials (hides, wood, iron, grapes) from the town market, driving baseline demand for these resources.

### Bound Village Production Tiers
Villages produce goods based on their current hearth levels:

| Village Hearths | Hearth Level | Production Goods Multiplier | Daily Food Units Produced |
| :---: | :---: | :---: | :---: |
| **$< 200$** | Level 0 | $0.5\times$ | 1 |
| **$200\text{--}599$** | Level 1 | $1.0\times$ | 2 |
| **$600+$** | Level 2 | $1.5\times$ | 3 |

The formula for daily non-food goods produced by a village is:
$$\text{Daily Goods} = \text{Production Weight} \times 0.5 \times (\text{Hearth Level} + 1)$$

* **Food Production**: Randomly selected from raw foods based on a weight of $\approx 1/\text{Item Value}$, making grain and fish more common.
* **Warehouse Limits**: Villages stop producing when stockpiled goods exceed their storage limit:
$$\text{Warehouse Capacity} = \text{Ceil}(\text{Max}(1, \text{Daily Food} + \text{Daily Non-Food})) \times 5$$
$$\text{Production Halt Threshold} = 1.5 \times \text{Warehouse Capacity}$$

> [!IMPORTANT]
> If villager parties cannot reach their bound town due to bandit activity or enemy blockades, the village stockpile will cap out. Once stockpile reach the $1.5\times$ halt threshold, village production ceases entirely, starving the bound town of food and raw materials.

### Town Demand and Consumption
Daily consumer demand is modeled using a town's prosperity:
$$\text{Base Population} = \text{Max}(0, \text{Prosperity} + 1000)$$
$$\text{Luxury Population} = \text{Max}(0, \text{Prosperity} - 3000)$$
$$\text{Daily Category Demand} = \text{Base Demand} \times \text{Base Population} + \text{Luxury Demand} \times \text{Luxury Population}$$

* **Luxury goods**: Category demand for luxury items (velvet, wine, dates, jewelry, fur) scales dramatically once prosperity exceeds $3,000$.
* **Market Smoothing**: Shortages and gluts are smoothed daily to prevent instant price spikes:
$$\text{Supply} = \text{Max}(0.1, \text{Old Supply} \times 0.85 + \text{Current Store Value} \times 0.15)$$
$$\text{Demand} = \text{Old Demand} \times 0.85 + \text{Estimated Demand} \times 0.15$$

### Price Pressure and Arbitrage
The market price factor is calculated from the supply-to-demand ratio and current stored inventory:
$$\text{Raw Factor} = \frac{\text{Demand}}{0.1 \times \text{Supply} + 0.04 \times \text{Store Value} + 2}$$
$$\text{Market Factor} = \text{Raw Factor}^{0.6} \quad (\text{Normal Goods})$$
$$\text{Market Factor} = \text{Raw Factor}^{0.3} \quad (\text{Animals})$$

* **Clamping Limits**: Trade goods clamp to a wide $[0.1\times, 10.0\times]$ range. Non-trade goods (weapons, armor) are clamped tightly to a narrow $[0.8\times, 1.3\times]$ range.
* **Transaction Pricing**:
$$\text{Buy Price} = \text{Item Value} \times \text{Market Factor} \times (1 + \text{Trade Penalty})$$
$$\text{Sell Price} = \frac{\text{Item Value} \times \text{Market Factor}}{1 + \text{Trade Penalty}}$$

---

## 5. Workshops Appendix

Player-owned workshops process raw trade goods into processed materials or equipment.

### Workshop Operations
* **Capacity**: A player can own up to $\text{Clan Tier} + 1$ workshops.
* **Bankruptcy**: If a workshop fails to make a profit and exhausts its capital, the owner has a $3$-day save window to inject capital before the workshop is permanently lost.
* **Warehouse XP**: Withdrawing finished goods from the workshop warehouse directly into your inventory yields Trade experience:
$$\text{Warehouse Trade XP} = 0.1 \times \text{Production Base Value}$$

### Workshop-Specific Perks
* **Steward (Level 75) - `Sweatshops`**: $+20\%$ production speed to owned workshops (Personal perk).
* **Smithing (Level 100) - `Experienced Smith`**: $+10\%$ production speed to owned workshops (Personal perk).
* **Trade (Level 50) - `Market Dealer`**: Reduces workshop input material costs by $-10\%$ (Clan Leader perk).
* **Trade (Level 150) - `Mercenary Connections`**: $+25\%$ workshop production speed (Governor perk).
* **Trade (Level 125) - `Artisan Community`**: $+1$ daily renown for every profiting workshop (Clan Leader perk).
* **Trade (Level 175) - `Rapid Development`**: $5,000$ gold payout if a workshop's town is captured by an enemy.

---

## 6. Alleys Appendix

Alleys represent criminal holdings that tie into the Roguery and crime systems.

### Alley Operations
* **Troop Requirement**: Operating an alley requires a garrison between $5$ and $10$ troops.
* **Economic Returns**: Yields a flat $+50$ gold daily.
* **Crime Cost**: Generates $+0.5$ daily crime rating with the owning faction.
* **Leader Death**: If the assigned alley leader companion dies, the player has $4$ days to assign a replacement before the alley is destroyed.

### Alley Experience Yields
Alleys serve as a highly effective tool for leveling up companions in Roguery and combat:

| Action | Experience Awarded | Target |
| :--- | ---: | :--- |
| **Initial Alley Takeover** | 1,500 XP | Main Hero |
| **Daily Operation Drip** | 40 XP | Main Hero |
| **Daily Assigned Leader Drip** | 200 XP | Assigned Companion |
| **Defending an Alley Attack** | 6,000 XP | Main Hero |

### Roguery Perks Relevant To Crime And Loot
The current perk export does not show direct alley profit or alley-garrison modifiers. Avoid treating Roguery perks as alley-income multipliers unless a separate code-path review confirms that behavior.

* **Roguery (Level 50) - `Two Faced`**: $+50\%$ chance for sneaking into towns, or no morale loss from converting bandit prisoners.
* **Roguery (Level 75) - `Know-How`**: $+5\%$ more loot from defeated villagers and caravans, or $+1$ security per day as governor.
* **Roguery (Level 125) - `Scarface`**: $+30\%$ chance for bandits, villagers, and caravans to surrender, or a governed-settlement relation tick.
* **Roguery (Level 150) - `Partners in Crime`**: Surrendering bandit parties can be recruited, or bandit troops in your formation deal $+2\%$ damage.
* **Roguery (Level 175) - `One of the Family`**: Bandit units in your party gain $+10$ Vigor and Control skills, or governor recruitment from gang leaders gains one slot.
