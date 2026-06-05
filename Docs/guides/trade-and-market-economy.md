# Trade and Market Economy Manual

This manual covers the complete mechanics of trade pricing, market arbitrage, trade penalties, and experience progression. It explains the mathematical relationship between market factors, trade penalty spreads, and the formulas governing trade profits and skill progression.

---

## 1. Shop Price Formulation & Trade Penalty

A shop's pricing structure is divided into two primary layers: the local **Market Factor** (supply and demand) and the **Trade Penalty** (transaction spread). 

### Pricing Formulas
The final purchase and sale prices of any item are calculated as follows:
$$\text{Buy Price} = \lceil\text{Item Value} \times \text{Market Factor} \times (1 + \text{Trade Penalty})\rceil$$
$$\text{Sell Price} = \left\lfloor\frac{\text{Item Value} \times \text{Market Factor}}{1 + \text{Trade Penalty}}\right\rfloor$$

* **Spread impact**: A trade penalty of $0.50$ means:
  - You buy the item at $150\%$ ($1.50\times$) of its market-adjusted value.
  - You sell the item at $66.7\%$ ($\approx 1/1.50$) of its market-adjusted value.
* **Price spreads**: This transactional penalty is the primary reason why flipping items is highly inefficient unless a large supply-and-demand mismatch exists.

### Market Factor Modeling
The baseline market factor is calculated using category demand, supply, and stored value:
$$\text{Raw Factor} = \frac{\text{Demand}}{0.1 \times \text{Supply} + 0.04 \times \text{Store Value} + 2}$$
$$\text{Market Factor} = \text{Raw Factor}^{\text{Exponent}}$$

* **Exponents**: The exponent is $0.3$ for animals and $0.6$ for other item categories.
* **Clamps**: Trade goods have wide pricing ranges, clamping between $[0.1\times, 10.0\times]$. Non-trade goods (weapons, armor) are clamped tightly to a narrow $[0.8\times, 1.3\times]$ range.
* **Transaction decay**: Selling items into a market increases the `Store Value` term in the denominator, progressively lowering the sell price of each subsequent item sold during that transaction.

---

## 2. Trade Penalty Reduction (Skill-Based)

The party leader's Trade skill reduces the active trade penalty through a decaying multiplier:
$$\text{Trade Penalty Multiplier} = \frac{1}{1 + 0.002 \times \text{Party Leader Trade}}$$

Here is how the remaining trade penalty scales with Trade skill level:

| Party Leader Trade Skill | Remaining Penalty % |
| :---: | ---: |
| **0** | 100.0% |
| **50** | 90.9% |
| **100** | 83.3% |
| **150** | 76.9% |
| **200** | 71.4% |
| **250** | 66.7% |
| **300** | 62.5% |
| **330** | 60.2% |

> [!IMPORTANT]
> Even at the maximum Trade skill of 330, a character still retains $60.2\%$ of the baseline trade penalty. You cannot rely on skill points alone to eliminate market transaction spreads; you must utilize dedicated trade perks.

---

## 3. Trade Penalty Sources & Perk Adjustments

Trade penalties scale based on the transaction context and item type:
* **Baseline Shop Spread**: Adds $+0.06$ to the penalty.
* **War Mismatch**: Trading with a faction currently at war with your kingdom adds a massive $+0.50$ penalty.
* **Loot Sales**: Selling equipment to non-caravans applies a severe penalty:
$$\text{Equipment Sale Penalty} = +1.5 + 0.25 \times \text{Max}(0, \text{Item Tier} - 1)$$
This formula dictates why battle loot sells for a fraction of its purchase value, with higher-tier gear penalized exponentially.
* **Mount Sales**: Selling horses or pack animals to non-caravans adds a $+0.8$ penalty.
* **Caravan Discount**: Trading with mobile caravans halves the total trade penalty.

### Perk Impact Example
Assume a Tier 5 sword with a base value of $1,000$ gold and a flat $1.0$ local Market Factor:

| Scenario | Active Penalty | Buy Price | Sell Price | Net Spread |
| :--- | :---: | :---: | :---: | ---: |
| **Recruit (0 Trade, no perks)** | 2.56 | N/A | 280 gold | $-72.0\%$ |
| **Vassal (100 Trade, no perks)** | 2.13 | N/A | 319 gold | $-68.1\%$ |
| **Merchant (100 Trade + `Appraiser` perk)** | 1.81 | N/A | 355 gold | $-64.5\%$ |

> [!NOTE]
> The `Appraiser` perk ($-15\%$ equipment sale penalty) reduces the penalty term itself, rather than applying a flat percentage multiplier to the final price.

---

## 4. Trade Penalty Perks

| Skill | Level | Perk | Role | Affected Lane |
| :--- | ---: | :--- | :--- | :--- |
| **Trade** | 25 | `Appraiser` | Party Leader | $-15\%$ price penalty when selling equipment. |
| **Trade** | 25 | `Whole Seller` | Party Leader | $-15\%$ price penalty when selling trade goods. |
| **Trade** | 50 | `Market Dealer` / `Caravan Master` | Personal | Marks item prices relative to average (no penalty reduction). |
| **Trade** | 75 | `Distributed Goods` | Quartermaster | $-15\%$ price penalty when buying from villages. |
| **Trade** | 75 | `Local Connection` | Quartermaster | $-15\%$ price penalty when selling animals. |
| **Trade** | 175 | `Insurance Plans` | Quartermaster | $-25\%$ price penalty when buying food items. |
| **Trade** | 175 | `Rapid Development` | Quartermaster | $-25\%$ price penalty when buying clay, iron, silk, and silver. |
| **Trade** | 200 | `Granary Accountant` | Personal | $-20\%$ price penalty when selling food items. |
| **Trade** | 200 | `Tradeyard Foreman` | Personal | $-20\%$ price penalty when selling pottery, tools, silk, and jewelry. |
| **Smithing**| 175 | `Artisan Smith` | Party Leader | $-50\%$ trade penalty when selling player-crafted weapons. |
| **Riding** | 75 | `Deeper Sacks` | Party Leader | $-10\%$ trade penalty when trading mounts. |
| **Steward** | 225 | `Arenicos' Horses` | Personal | $-20\%$ trade penalty when trading mounts. |
| **Steward** | 225 | `Arenicos' Mules` | Quartermaster | $-20\%$ trade penalty when trading pack animals. |
| **Roguery** | 150 | `Smuggler Connections`| Party Leader | $-50\%$ penalty when trading in cities where you have crime. |
| **Scouting** | 200 | `Rumor Network` | Party Leader | $-5\%$ trade penalty in cities of your own kingdom. |

---

## 5. Non-Trade Price Modifiers

Certain economic perks target specific transaction types outside the standard shop price penalty model:

| Perk Family | Example Perks | Function | System Checked |
| :--- | :--- | :--- | :--- |
| **Barter Penalty** | `Self-made Man`, `Slick Negotiator` | Reduces costs during lord-to-lord barters. | Diplomacy Barter Model |
| **Ransom Values** | `Ransom Broker`, `Man of Means` | Increases gold received from selling prisoners. | Ransom Broker Model |
| **Wages** | `Mercenary Connections`, `Picked Shots` | Reduces recurring party/garrison wages. | Party Finance Model |
| **Recruitment Cost**| `Great Investor`, `Head Hunter` | Lowers hiring and upgrading expenses. | Troop Recruitment Model |
| **Settlement Revenue**| `Toll Gates`, `Traveling Rumors` | Adds gold from visiting caravans/parties. | Fief Finance Model |

### Key Non-Trade Economic Perks
* **Steward (Level 25) - `Frugal`**: Reduces party wages by $-5\%$ (Quartermaster).
* **Steward (Level 75) - `Stiff Upper Lip`**: Reduces party food consumption by $-10\%$ while in an army (Quartermaster) / reduces garrison wages in castles by $-20\%$ (Governor).
* **Trade (Level 225) - `Sword For Barter`**: Reduces mercenary hiring costs by $-20\%$ (Personal) / reduces caravan guard wages by $-15\%$ (Quartermaster).
* **Trade (Level 250) - `Silver Tongue`**: Reduces gold required to defect lords by $-15\%$ (Personal) / $15\%$ better trade deals from caravans and villagers (Quartermaster).
* **Trade (Level 250) - `Spring of Gold`**: Generates a $+0.1\%$ daily interest on your current gold reserves (up to $+1,000$ gold per day, Clan Leader) / $+20\%$ project boosting effect in governed settlements (Governor).
* **Trade (Level 275) - `Trickle Down`**: $+1$ relationship with merchants when spending $10,000+$ denars (Party Leader) / $+2$ daily prosperity while building a project in governed settlements (Governor).

---

## 6. Trade Experience (XP) Progression

Trade skill experience is generated through two distinct methods:

### Method 1: Profitable Trading
Experience is awarded when you sell trade goods to a city market at a net profit:
$$\text{Trade XP} = 0.5 \times \text{Net Trade Profit}$$

> [!WARNING]
> **Average Cost Reset Trap**: The game engine tracks the average purchase cost of items in your inventory to determine profit. Moving items between your party and companions, or storing them in fief warehouses, completely resets this average cost tracker, wiping out your accumulated trade profit record and preventing you from gaining Trade XP when you sell them.
* **Flipping limits**: Selling items at a loss yields zero experience.

### Method 2: Warehouse Production
Withdrawing finished products from your owned workshop warehouses yields passive experience:
$$\text{Warehouse Trade XP} = 0.1 \times \text{Production Base Value}$$

This allows you to level up your Trade skill passively without running manual trade routes across the campaign map.

---

## 7. Practical Trading Advice

* **Splash Utility**: Spending points to reach Trade level 50 is highly recommended for all characters. Both `Appraiser`/`Whole Seller` (level 25) and `Caravan Master` (level 50) mark profit colors and highlight average prices directly in the trade screen, providing invaluable information.
> [!TIP]
> **The 300 Trade Target**: Pushing Trade to level 300 unlocks `Everything Has a Price`, which allows you to trade fiefs and settlements in lord barters. This is a game-changing political tool. If you do not plan to reach level 300, stopping at Trade level 50 or 75 is the most point-efficient setup.
* **Caravan Arbitrage**: Caravans are subject to halved trade penalties. Always prioritize buying from or selling to caravans rather than town markets when their inventories allow it.
* **Crafted Weapon Sales**: If you are funding your clan by selling crafted weapons, the Smithing perk `Artisan Smith` ($-50\%$ penalty) is far more effective than generic Trade skill penalty reductions.
