# Medicine and Party Survival Manual

This manual covers the complete mechanics of troop survivability in Bannerlord: how casualties are processed into wound or death rolls, how to maximize troop hit points, and how to stack captain armor and damage resistance perks in combat formations.

---

## 1. The Surgery Equation (Death vs. Wound Roll)

A casualty in Bannerlord is not immediately fatal. When a unit falls, the party surgeon's Medicine skill and active perks determine if the unit is killed or merely wounded.

### The Surgery Formula
For regular non-hero troops who take a lethal blow:
$$\text{Base Denominator} = 1 + (\text{Surgeon Medicine} \times 0.01 \times \text{Event Multiplier}) + (\text{Troop Level} \times 0.02) + \sum\text{Additive Survival Bonuses}$$
$$\text{Final Denominator} = \text{Base Denominator} \times (1 + \sum\text{Factor Survival Bonuses})$$
$$\text{Wound Chance} = 1 - \frac{1}{\text{Final Denominator}}$$
$$\text{Death Chance} = \frac{1}{\text{Final Denominator}}$$

* **Event Multipliers**: The Medicine skill term is scaled based on the campaign map context:
  - **Player Map Events**: $1.0\times$ (full Medicine effectiveness).
  - **AI Map Events**: $0.25\times$ (halved effectiveness for non-player armies).
* **Troop Level Impact**: The formula checks `character.Level` (which ranges from 1 to 31+), not their visible tier. High-level troops have a higher base denominator, making them naturally more resilient to death.
* **Blunt Damage**: Victims of blunt damage are automatically processed as wounded ($100\%$ wound chance) and skip the surgery check.

#### Case Study: Level 20 Troop Survival Scaling (Player Party)
The following table models the survival rates of a level 20 troop in the player's party across different Surgeon Medicine levels (assuming no additional perk bonuses):

| Surgeon Medicine Skill | Base Denominator | Wound Chance | Death Chance |
| :---: | :---: | :---: | ---: |
| **0** | 1.40 | 28.6% | 71.4% |
| **80** | 2.20 | 54.5% | 45.5% |
| **150** | 2.90 | 65.5% | 34.5% |
| **200** | 3.40 | 70.6% | 29.4% |
| **300** | 4.40 | 77.3% | 22.7% |
| **330 (Cap)** | 4.70 | **78.7%** | **21.3%** |

> [!TIP]
> Surgeon Medicine is a denominator bonus. Going from 0 to 330 Medicine cuts your troop death rate from $71.4\%$ to $21.3\%$ (over a $70\%$ relative reduction in fatalities).

---

## 2. Medicine and Surgery Perks

The Medicine skill tree contains several passive and active perks that govern troop survival, healing rates, and character longevity:

### Surgery & Troop Survival Perks
* **Medicine (Level 75) - `Doctor's Oath`**: Applies your Medicine survival bonus to enemy casualties, increasing the number of wounded enemies available for recruitment or ransom. Operates at $1.0\times$ in player battles and $0.1\times$ in simulated battles.
* **Medicine (Level 125) - `Siege Medic`**: Grants a flat $50\%$ chance for troops to be wounded instead of killed during siege bombardment events.
* **Medicine (Level 125) - `Veterinarian`**: Reduces troop mount loss by $-50\%$ when a mounted troop is killed in battle (mount is recovered and recycled).
* **Medicine (Level 200) - `Physician of People`**: Multiplies the survival denominator by $1.3$ (acting as a $+30\%$ factor bonus) for Tier 1 and Tier 2 troops in your party.

### Healing Rate & Utility Perks
* **Medicine (Level 25) - `Self Medication`**: $+10\%$ personal healing rate and $+5$ max HP to the surgeon.
* **Medicine (Level 50) - `Triage Tent`**: $+15\%$ healing rate to the party while stationary on the campaign map.
* **Medicine (Level 100) - `Best Medicine`**: $+15\%$ healing rate to the party while moving on the campaign map, and increases hero healing by $+10\%$.
* **Medicine (Level 100) - `Good Lodging`**: $+15\%$ healing rate to the party when resting inside a settlement.
* **Medicine (Level 150) - `Bush Doctor`**: $+20\%$ healing rate in forest terrain, and reduces campaign map speed penalties from wounded troops by $-10\%$.
* **Medicine (Level 175) - `Health Advice`**: $+10\%$ healing rate to heroes in the party.
* **Medicine (Level 175) - `Perfect Health`**: $+10\%$ healing rate to regular troops in the party.
* **Medicine (Level 200) - `Clean Infrastructure`**: $+15\%$ party healing rate when inside territory owned by your own faction.
* **Medicine (Level 225) - `Cheat Death`**: Grants a one-time cheat death buffer, preventing the player character's death from combat execution or old age.
* **Medicine (Level 225) - `Fortitude Tonic`**: Adds $+5$ flat hit points to all heroes in your party.

---

## 3. Troop Hit Points Scaling

Pre-roll survivability prevents troops from taking lethal damage in the first place, avoiding the surgery check entirely.

### Theoretical Maximum Troop Hit Points Stacks

| Troop Class | Max HP Bonus | Stacking Requirements |
| :--- | :---: | :--- |
| **Any Regular Troop** | $+90$ HP | `Minister of Health` (at 330 Medicine), `Hardy Frontline`, `Thick Hides`. |
| **Foot Infantry** | $+108$ HP | Any regular troop stack + `Well Built`, `Unwavering Defense`, `Hard Knock`. |
| **Foot Ranged Troop** | $+100$ HP | Any regular troop stack + `Well Built`, `Picked Shots`. |
| **Mounted Ranged Troop** | $+95$ HP | Any regular troop stack + `Picked Shots` (using broad ranged flags). |
| **Troop Mounts** | $+15$ HP & $+10\%$ HP | `Sledges` ($+15$ flat HP), `Veterinary` ($+10\%$ HP). |

### Hit Point Buffing Perks

| Skill | Level | Perk | Role | Effect | Scope |
| :--- | ---: | :--- | :--- | :--- | :--- |
| **Medicine** | 75 | `Sledges` | Party Leader | $+15$ HP to mounts | Mounts in player party. |
| **Medicine** | 275 | `Minister of Health` | Personal | $+1$ HP per skill point $>250$ | $+80$ HP at 330 Medicine cap. |
| **Athletics** | 25 | `Well Built` | Party Leader | $+5$ HP to foot troops | Foot troops in party. |
| **Crossbow** | 250 | `Picked Shots` | Party Leader | $+5$ HP to ranged troops | Ranged troops in party. |
| **One Handed**| 225 | `Unwavering Defense` | Party Leader | $+10$ HP to infantry | Infantry in party. |
| **Polearm** | 100 | `Hard Knock` | Party Leader | $+3$ HP to infantry | Infantry in party. |
| **Polearm** | 200 | `Hardy Frontline` | Party Leader | $+5$ HP to all troops | All troops in party. |
| **Riding** | 50 | `Veterinary` | Party Leader | $+10\%$ HP to mounts | Mounts of troops in party. |
| **Two Handed**| 200 | `Thick Hides` | Party Leader | $+5$ HP to all troops | All troops in party. |

---

## 4. Formation Armor Scaling

Armor reduces incoming damage before it is processed, making it the most critical pre-roll survival layer when paired with high Medicine.

### Theoretical Maximum Captain Armor Stacks

| Formation Class | Max Armor Bonus | Stacking Requirements |
| :--- | :---: | :--- |
| **Any Formation Unit** | $+5$ Armor per slot | `Metallurgy` (Engineering 225). |
| **Foot Formation Unit** | $+10$ Armor per slot | `Metallurgy` + `Ignore Pain` (Athletics 250). |
| **Mounted Formation Unit**| $+10$ Armor per slot | `Metallurgy` + `Dauntless Steed` (Riding 250). |
| **Troop Mounts** | $+10$ Mount Armor | `Tough Steed` (Riding 250). |

* **Armor Perk Application**: These perks add flat armor points directly to every equipped armor slot (head, chest, shoulders, hands, feet), multiplying their effectiveness.

---

## 5. Damage Resistance & Shield Coverage

Damage resistance acts as a third pre-roll defense layer, applying percentage cuts to final damage values.

### Theoretical Maximum Overlapping Resistance Stacks

* **Broad Formation Damage Mitigation**: $-5\%$ damage taken (`Elite Reserves` captain).
* **Melee Infantry vs. Projectiles (Body Hits)**: $-8\%$ damage taken (`Skirmisher` + `Elite Reserves`).
* **Melee Infantry vs. Projectiles + Tier 3 Banner**: $-23\%$ damage taken (`Skirmisher` + `Elite Reserves` + Tier 3 ranged resistance banner).
* **Bow Ranged Troops vs. Projectiles**: $-18\%$ damage taken (`Skirmish Phase Master` + `Skirmisher` + `Elite Reserves`).
* **Crossbow Troops vs. Projectiles (Crossbow Equipped)**: $-21\%$ damage taken (`Skirmish Phase Master` + `Counter Fire` + `Skirmisher` + `Elite Reserves`).
* **Bow Troops vs. Projectiles + Tier 3 Banner**: $-33\%$ damage taken (Best Fian Champion defense stack).
* **Crossbow Troops vs. Projectiles + Tier 3 Banner**: $-36\%$ damage taken (Best Imperial Sharpshooter defense stack).
* **Cavalry Charge Damage Mitigation**: $-60\%$ charge damage taken (`Braced` + `Sure Footed` captains).

### Damage Resistance & Shield Perks

| Skill | Level | Perk | Role | Scope / Conditions | Effect |
| :--- | ---: | :--- | :--- | :--- | :--- |
| **Bow** | 175 | `Skirmish Phase Master` | Captain | Ranged troops in formation | $-10\%$ damage from projectiles. |
| **Crossbow** | 175 | `Counter Fire` | Captain | Crossbow must be equipped | $-3\%$ damage from projectiles. |
| **Throwing** | 125 | `Skirmisher` | Captain | All formation troops | $-3\%$ damage from ranged attacks. |
| **One Handed**| 25 | `Basher` | Captain | Infantry in Shield Wall | $-4\%$ damage from melee attacks. |
| **Tactics** | 200 | `Elite Reserves` | Captain | All formation troops | $-5\%$ general damage taken. |
| **Athletics** | 125 | `Braced` | Captain | Anti-cavalry charges | $-30\%$ charge damage taken. |
| **Polearm** | 225 | `Sure Footed` | Captain | Anti-cavalry charges | $-30\%$ charge damage taken. |
| **One Handed**| 125 | `Arrow Catcher` | Captain | All formation troops | Increases shield projectile block area. |
| **One Handed**| 125 | `Shieldwall` | Captain | Infantry in Shield Wall | Increases shield block area in Shield Wall. |
| **One Handed**| 200 | `Steel Core Shields` | Captain | Infantry in formation | $-10\%$ damage taken by shields. |

---

## 6. Practical Durability Strategies

* **The Elite Army Payoff**: Stacking `Minister of Health` ($+80$ HP at 330 Medicine) with high-tier units (such as Imperial Legionaries or Battanian Fian Champions) creates an almost unkillable core. Their naturally high base armor reduces incoming damage, their expanded health pools prevent one-shot kills, and your surgeon's Medicine level ensures that the rare casualties that do occur are wounded rather than killed.
* **Cultivate a Surgeon Companion**: If your main hero does not invest in Intelligence, recruit and assign a high-Intelligence companion with the surgeon role immediately. The daily party survival rates depend entirely on the active surgeon's Medicine skill.
* **Shield Wall Defense**: Standard shield walls do not receive baseline ranged body-hit damage reductions; their survival depends on shield block coverage. Combine `Arrow Catcher` and `Shieldwall` to maximize the protection area of your front-line infantry.
* **Simulated vs. Live Battle Split**: Ensure you do not waste perk slots on simulation-only perks (such as Tactics `Loose Formations` or `Elite Reserves` party leader versions) if you personally command your field battles. Those perks do not apply to live combat.
