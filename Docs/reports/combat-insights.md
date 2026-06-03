# Combat Damage and Armor Mitigation Insights

This report aggregates combat damage formulas, coefficients, and damage-type interactions extracted directly from decompiled local game assemblies.
- **Source Reference Report:** [Docs\reports\combat-formulas.md](combat-formulas.md)

---

## Core Damage and Armor Formula

Decompiled from `DefaultStrikeMagnitudeModel.ComputeRawDamage` and `GetBluntDamageFactorByDamageType`, the core combat damage is processed as follows:

$$\text{Final Raw Damage} = \Big[ C_{\text{blunt}} + (1 - B) \cdot C_{\text{nonBlunt}} \Big] \cdot R_{\text{absorb}}$$

Where:
* **Blunt Component ($C_{\text{blunt}}$):** Concussive force transmitted directly through the armor.
  $$C_{\text{blunt}} = B \cdot M \cdot \left(\frac{50}{50 + A}\right)$$
* **Non-Blunt Component ($C_{\text{nonBlunt}}$):** Cutting/piercing surface force that must overcome armor soak.
  $$C_{\text{nonBlunt}} = \max\left(0, M \cdot \left(\frac{50}{50 + A}\right) - k \cdot A\right)$$

### Formula Constants by Damage Type

| Damage Type | Blunt Damage Factor ($B$) | Armor Soak Factor ($k$) | Key Characteristic |
| :--- | :---: | :---: | :--- |
| **Cut (Slash)** | $0.10$ | $0.50$ | High base damage, heavily mitigated by armor. |
| **Pierce (Thrust)** | $0.25$ | $0.33$ | Moderate armor penetration, scales with velocity. |
| **Blunt (Concussive)** | $0.60$ | $0.20$ | Extreme armor penetration, ignores most soak. |

* **$M$ (Strike Magnitude):** Incoming kinetic energy (blow magnitude), scaled by weapon damage and speed bonuses.
* **$A$ (Armor Effectiveness):** Target's local armor rating at the hit location.
* **$R_{\text{absorb}}$ (Absorption Ratio):** Damage modifier (defaults to $1.0$ for human torso hits).

---

## Simulated Armor Scaling (Magnitude $M = 100$)

Final damage dealt by a standard $100$-magnitude hit at different armor values ($A$):

| Armor Level ($A$) | Cut Damage (Dealt) | Pierce Damage (Dealt) | Blunt Damage (Dealt) |
| :---: | :---: | :---: | :---: |
| **0** (No Armor) | 100.00 | 100.00 | 100.00 |
| **20** (Light Armor) | 62.43 | 66.48 | 69.83 |
| **40** (Medium Armor) | 37.56 | 45.66 | 52.36 |
| **60** (Heavy Armor) | 18.46 | 30.60 | 40.65 |
| **80** (Super Heavy Armor) | 3.85 | 18.67 | 32.06 |

---

## Case Study: Sturgian Heroic Line Breaker vs. Elite Menavliaton

The Sturgian Heroic Line Breaker ( Northern Reinforced Two-Handed Mace, $74$ Blunt swing) consistently defeats the Imperial Elite Menavliaton (Menavlion, $120$ Cut swing) in brawls because of these mechanics:

1. **Blunt Damage Efficiency:** Against heavy armor ($A=45-50$), the Menavlion's Cut damage is heavily mitigated by soak ($k=0.5$), reducing a $126$-magnitude hit to **$\sim 35.25$ damage**. The Line Breaker's Mace, utilizing Blunt scaling ($k=0.2$, $B=0.6$), keeps its concussive components intact, dealing **$\sim 34.36$ damage** from a smaller $81.4$-magnitude hit. Despite the Menavlion's $62\%$ base damage advantage, both units require exactly **3 hits** to kill each other.
2. **Attack Frequency:** The Northern Reinforced Two-Handed Mace is much faster (**89 swing speed** vs. the Menavlion's **75–80**).
3. **Higher AI Level:** The Line Breaker's 150 skill provides a **0.480 AI Level** vs the Menavliaton's 130 skill (**0.416 AI Level**), leading to faster attack chaining and fewer parrying mistakes.
4. **Weapon Spacing:** The shorter mace (**102 cm**) does not clash or bounce chest-to-chest, whereas the long Menavlion (**163 cm**) frequently bounces dealing $0$ damage.
