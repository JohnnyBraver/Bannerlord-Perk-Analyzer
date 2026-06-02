# Smithing and Crafting Manual

This manual covers the complete mechanics of the smithing and crafting systems in Bannerlord. It detail the mathematical formulas governing skill experience, weapon valuation, part research unlocks, design difficulty weights, and stamina consumption.

---

## 1. Smithing Skill XP Formulas

Smithing experience is calculated using the final market value of the crafted, smelted, or refined item, rather than the raw design difficulty displayed in the crafting UI.

### Extracted Skill XP Formulas
Experience points ($XP$) for the three primary activities are determined as follows:

* **Refining**:
$$\text{Refining XP} = \text{Round}(0.3 \times \text{Produced Material Value} \times \text{Output Count})$$
* **Smelting**:
$$\text{Smelting XP} = \text{Round}(0.02 \times \text{Smelted Item Value})$$
* **Smithing (Free Build Mode)**:
$$\text{Smithing Free Build XP} = \text{Round}(0.02 \times \text{Crafted Item Value})$$
* **Smithing (Crafting Order Mode)**:
$$\text{Smithing Crafting Order XP} = \text{Round}(0.10 \times \text{Crafted Item Value})$$

> [!NOTE]
> Crafting orders yield five times more experience than Free Build mode for a weapon of the same market value. However, orders are subject to target constraints; failing to meet the order requirements applies a multiplier penalty that degrades the final XP yield.

### The Charcoal Refining Strategy
Early skill leveling is heavily accelerated by the Smithing level 25 perk `Efficient Charcoal Maker`:
* **Base charcoal recipe**: 2 Hardwood $\rightarrow$ 2 Charcoal.
* **Perk charcoal recipe**: 2 Hardwood $\rightarrow$ 3 Charcoal.
* **Refining XP yield with perk**:
$$\text{Charcoal Refining XP} = \text{Round}(0.3 \times \text{Charcoal Value} \times 3)$$

Because the refining XP formula only checks the gross output count and value, and does not subtract the input hardwood value, `Efficient Charcoal Maker` increases refining XP by $+50\%$. This makes charcoal refining the cheapest and most repeatable method to grind Smithing skill before you have unlocked high-tier weapon parts.

---

## 2. Part Research Mechanics

Weapon parts are unlocked through a research point pool that is separate from skill experience. Research progress is weapon-template specific (e.g. unlocking two-handed sword parts requires crafting or smelting two-handed swords).

### Extracted Research Formulas
Research points generated per item are calculated as follows:

* **Smelting Research**:
$$\text{Smelting Research Base} = 1 + \text{Round}(0.02 \times \text{Item Value})$$
$$\text{Smelting Research Final} = \lfloor\text{Smelting Research Base} \times \text{Smelting Perk Multiplier}\rfloor$$
* **Smithing Research (Free Build)**:
$$\text{Smithing Research Final} = 1 + \lfloor0.1 \times \text{Item Value} \times \text{Smithing Multiplier}\rfloor$$

* **Curious Smelter Perk**: Increases the Smelting Perk Multiplier by $+100\%$ ($2.0\times$ total multiplier) when smelting.
* **Curious Smith Perk**: Increases the Smithing Multiplier by $+100\%$ ($2.0\times$ total multiplier) when crafting.
* **Free Build Mode Multiplier**: Adds a baseline $+10\%$ bonus ($1.1\times$) to crafting research.

#### Target Research Requirements
The research points required to unlock the next random part in a weapon template scales based on the number of parts already unlocked:
$$\text{Research Required} = \sqrt{\frac{100}{\text{Total Parts in Template}}} \times (9 \times \text{Opened Parts} + 10)$$

* **Random unlocks**: New parts are selected randomly from the lowest locked tier available in that weapon template.
* **Unlocking loops**: Smelting a crafted weapon returns half of its value as research points. Stacking `Curious Smelter` makes the craft-and-smelt loop the most efficient path for unlocking high-tier parts.

---

## 3. Design Difficulty & Stamina Cost

A weapon design's difficulty is calculated as a weighted average of its selected parts:

| Part Piece Type | Piece Weight |
| :---: | ---: |
| **Blade/Head (Piece 0)** | 100 |
| **Guard (Piece 1)** | 20 |
| **Grip (Piece 2)** | 60 |
| **Pommel (Piece 3)** | 20 |

$$\text{Design Difficulty} = \text{Round}\left(\frac{100 \cdot D_0 + 20 \cdot D_1 + 60 \cdot D_2 + 20 \cdot D_3}{200}\right)$$

* **Stamina Cost**: Crafting weapons drains character stamina:
$$\text{Stamina Cost} = 10 + 5 \times \text{Item Tier}$$
* **Practical Smith Perk**: Reduces all stamina consumption by $50\%$.

---

## 4. Crafted Weapon Value Model

Because both skill experience and part research scale directly with final item value, maximizing item value is the key to grinding smithing.

### Weapon Value Formula
Weapon valuation is exponential relative to its calculated item tier:
$$\text{Equipment Value} = 2.75^{\text{Clamp}(\text{Item Tier}, -1, 7.5)}$$
$$\text{Weapon Value} = \lfloor100 \times \text{Equipment Value} \times (1 + 0.2 \times (\text{Appearance} - 1)) + 100 \times \text{Max}(0, \text{Appearance} - 1)\rfloor$$

* **Calculated Item Tier**: A combination of combat stats and material tier:
$$\text{Item Tier} = 0.6 \times \text{Melee Stat Tier} + 0.4 \times \text{Design Material Tier}$$
* **Design Material Tier**: Determined by the average tier of the selected parts and the quality of iron/steel used.

### Melee Stat Tier Calculation
For each attack mode (thrust/swing), the weapon's stat tier is calculated using its attack score:
$$\text{Thrust Score} = \text{Thrust Damage} \times \text{Damage Type Factor} \times \left(\frac{\text{Thrust Speed}}{100}\right)^{1.5}$$
$$\text{Swing Score} = \text{Swing Damage} \times \text{Damage Type Factor} \times \left(\frac{\text{Swing Speed}}{100}\right)^{1.5}$$
$$\text{Attack Score} = \text{Max}(\text{Thrust Score}, 1.1 \times \text{Swing Score})$$
$$\text{Mode Tier} = 0.06 \times \text{Attack Score} \times \left(1 + \frac{\text{Weapon Length}}{100}\right) - 3.5$$

#### Damage Type Factors
The value model rates different damage types unequally:

| Damage Type | Valuation Factor |
| :--- | ---: |
| **Cut** | 1.00 |
| **Pierce** | 1.15 |
| **Blunt** | 1.45 |

#### Valuation Adjustments
* **Two-Handed Penalty**: Weapons that can only be used with two hands apply a $0.8$ multiplier to their attack score in the value formula.
* **Throwing Weapons**: Throwing axes and throwing knives receive a $1.2$ multiplier; javelins are penalized with a $0.6$ multiplier.
* **Multi-Mode Weapons**: Weapons that support both thrusting and swinging receive a small value bonus from their secondary attack mode.

> [!IMPORTANT]
> Weapon handling is entirely absent from the value calculation. While handling is vital for combat ergonomics, it does not affect sale prices, free-build experience, or part research. When grinding, you should sacrifice handling to maximize damage, speed, and reach.

---

## 5. Optimized Crafting Strategy

* **High Damage + Speed Priority**: Damage is the primary driver of item value, but it is heavily scaled by attack speed. A slightly slower weapon with high damage is often less valuable than a faster weapon with moderate damage.
* **Reach Multiplier**: Weapon length acts as a multiplier to the final mode tier. Ensure you maximize the size slider of your blades and poles when crafting for profit, provided it does not catastrophically degrade swing/thrust speed.
* **Blunt/Pierce Domination**: Pierce and blunt weapons are valued significantly higher than cut weapons. Focus on unlocking and crafting weapons that deal blunt/pierce damage (such as maces and spears) to accelerate value scaling.
* **Curious Smelter Loop**: Craft the highest-value weapon design you can afford, and immediately smelt it down. With `Curious Smelter`, the smelting returns $50\%$ of the item value as part research, recycling materials and unlocking new parts rapidly.
* **Step-Down for Quality**: Attempting to craft a design that exceeds your current Smithing skill can trigger penalty rolls that reduce the weapon's final stats and value. If your skill is too low, step down to an easier design to ensure a high-value output.
