# Commander Perks and Build Optimization Guide

This guide provides a comprehensive cost-benefit analysis of the primary commanding general build:
$$\text{VIG 3(5) | CTR 3(5) | END 3(5) | CNG 7 | SOC 2 | INT 7}$$

It goes skill-by-skill to calculate the exact focus point cost required to reach target perks under this attribute profile, outlines why maxing every skill is a trap, and designs a zero-waste, optimized focus point budget.

---

## 1. Skill-by-Skill Focus Point Cost Analysis

To avoid wasting scarce focus points, you must align your allocations with your planned final attribute levels. The learning limit formula dictates how many focus points ($F$) are required to reach a target perk level:
$$\text{Skill Limit} = 4 + 14 \times (\text{Attribute} - 1) + 40 \times F$$

### A. Intelligence Skills (Base 7, Pushing to 10 in Late Game)

#### Medicine (Target: 275 or 330)
* **Strategic Value**: Extremely High for party-wide troop durability in this commander build. Medicine 200 `Physician of People` improves low-tier lethal-wound recovery, while Medicine 275 `Minister of Health` turns skill above 250 into flat troop hit points. Pushing to 330 is the late-game stretch goal for maximizing that HP layer.
* **Focus Cost**:
  * *At 7 Intelligence*: **5 Focus** is required to reach 275 (limit 288).
  * *At 9-10 Intelligence*: **4 Focus** is enough to reach 275 (limit 276 / 290).
  * *At 10 Intelligence*: **5 Focus** is required to reach the 330 stretch goal (limit 330).

#### Scouting (Target: 250 or 275)
* **Strategic Value**: High. Campaign map speed and spotting are critical. Target level is 250 (`Vanguard`/`Rearguard`) or 275 (`Uncanny Insight`).
* **Focus Cost**:
  * *At 7 Cunning*: **5 Focus** is required to reach 250/275 (limit 288). 4 focus only caps at 248, falling just short of the 250 milestone.

#### Steward (Target: 250 or 275)
* **Strategic Value**: High. Steward covers siege-camp logistics, wages, food consumption, and quartermaster scaling. Target level is 250 (`Master of Warcraft` / `Master of Planning`) or 275 (`Price of Loyalty` scaling).
* **Focus Cost**:
  * *At 7 Intelligence*: **5 Focus** is required to reach 250/275 (limit 288).
  * *At 10 Intelligence*: **4 Focus** is enough to reach 250/275 (limit 290).

#### Engineering (Target: 0 or 3 - Dump or Delegate to Companion)
* **Strategic Value**: Low to Moderate. Reaching level 150 unlocks **`Stonecutters`** or **`Siege Engineer`** (allowing the builder to construct Fire Catapults and Fire Ballistas). However, in the context of the Combat Commander build, investing 3 focus points just to get fire catapults on the player character is highly inefficient. 
* **Delegation Strategy**: It is far better to hire a dedicated **Engineer Companion** to run the Engineer role in your clan, allowing them to construct fire catapults and manage siege engines. This allows the player character to completely dump Engineering to **0 Focus Points** (learning cap 88 at 7 INT), saving 3 focus points for combat or leadership skills.
* **Focus Cost**:
  * *Player-Builder Option (If you insist on being the active Engineer)*: **3 Focus** is required to reach 150 (limit 208).
  * *Optimal Dump Option (Delegate to Companion)*: **0 Focus** (limit 88).

> [!WARNING]
> **The Engineering 225 Metallurgy Trap**:
> Reaching level 225 unlocks **`Metallurgy`** (which grants $+5$ armor to your formation troops). While $+5$ armor is valuable, digging through the entire Engineering tree just for this perk is a massive focus point trap for the modern **7 Cunning / 7 Intelligence** build.
> * Under the **7 INT** profile, reaching 225 requires **4 Focus Points** (limit 248).
> * Under the older pure INT build (**3/5 3/5 3/5 2 2 10**), Metallurgy was much more viable because 10 INT naturally lowered the required investment to **3 Focus Points** (limit 250), and the build did not suffer from Cunning-split focus point starvation (having 2 Cunning instead of 7 Cunning meant Scouting, Tactics, and Roguery did not eat up focus).
> * In the current **7 INT / 7 CNG** setup, focus points are extremely scarce due to Scouting (5), Medicine (5), and Steward (5). Keeping Engineering capped at **3 Focus Points** (for the level 150 project speed boost) is the most efficient choice, saving 1-2 focus points for combat or social scaling.

> [!TIP]
> **Fire Catapults for Siege Domination & XP**:
> While fire catapults are extremely lethal (deal massive area-of-effect damage and rack up defender kills far better than standard variants), **unlocking level 150 on the player character is generally not worth the 3 focus point cost**. You can construct fire catapults just as effectively by assigning a companion with 150+ Engineering to the **Engineer** role in your party. If you do choose to build them yourself, manually aiming and getting kills with a fire catapult during a siege assault is the fastest way to farm Engineering XP.

#### Tactics (Target: 25 or 75)
* **Strategic Value**: Low. Tactics primarily scales simulated battle (autoresolve) strength. If you personally command your field battles, autoresolve strength is wasted. Pushing beyond 75 is unnecessary.
* **Focus Cost**:
  * *At 7 Cunning*: **0 Focus** is required! With 0 focus and 7 Cunning, your limit is exactly **88** ($4 + 14 \times 6$). This is more than enough to unlock the level 25 close-formation morale perk and the level 75 `Horde Leader` ($+10$ party size) perk without spending a single focus point.

#### Roguery (Target: 50 or 75)
* **Strategic Value**: Low for this combat-commander plan. Pushing past 75 mostly adds niche loot, security, or crime-side options rather than core party durability or speed.
* **Focus Cost**:
  * *At 7 Cunning*: **0 Focus** is required! With 0 focus, your learning cap is **88**, enabling you to grab the level 50 and 75 perks for free.

---

### B. Social Skills (Base 2)

#### Leadership (Target: 75 or 175)
* **Strategic Value**: High. Targets are level 75 (`Authority` $+5$ party size) or level 175 (`Uplifting Spirit` $+10$ party size).
* **Focus Cost**:
  * *At 2 Social*: **2 Focus** is required to reach 75 (limit 98). **5 Focus** is required to reach 175 (limit 218). *(Note: With 2 Social, you cannot reach the level 250 perk, as 5 focus caps at 218).*

#### Charm (Target: 50)
* **Strategic Value**: Moderate. Target is level 50 (`Oratory` $+1$ renown and $+1$ influence per issue resolved).
* **Focus Cost**:
  * *At 2 Social*: **1 Focus** is required to reach 50 (limit 58).

#### Trade (Target: 50)
* **Strategic Value**: Moderate. Target is level 50 (`Caravan Master` for price marking or Quartermaster carrying capacity, depending on the build role).
* **Focus Cost**:
  * *At 2 Social*: **1 Focus** is required to reach 50 (limit 58).

---

### C. Combat & Physical Skills (Pushed to 5 via Respec Trick)

#### Athletics & Smithing (Target: 175 / 225 during leveling phase)
* **Focus Cost**: **5 Focus** each during the training phase. Pushing these to 5 focus points raises your learning limit to 232 with 3 Endurance, which is required to unlock `Durable` (Athletics 175) and `Enduring Smith` (Smithing 225) to push Endurance to 5. Once maxed and rotated via the Arena respec, they retain their cap.

#### Riding (Target: 100)
* **Focus Cost**: **1 Focus**. Once Endurance is pushed to 5, 1 focus point is enough to reach exactly 100 ($4 + 14 \times 4 + 40 \times 1 = 100$) to unlock `Sweeping Wind` ($+2\%$ party speed).

#### Weapon Skills (One-Handed, Two-Handed, Bow, Crossbow, Throwing)
* **Target**: Level 100 for cheap utility perks like Two-Handed `Beast Slayer` / `Shield breaker`, One-Handed `Shield Bearer`, or Bow `Merry Men` $+5$ party size. `Projectile Deflection` is a stronger defensive tool, but it is a level 150 perk and requires a separate investment plan.
* **Focus Cost**: **1 Focus** each. Once Vigor and Control are pushed to 5 via the respec trick, exactly 1 focus point guarantees a learning limit of **100** ($4 + 14 \times 4 + 40 \times 1 = 100$). Putting 2 focus points into these early on is a waste.

---

## 2. Optimized Focus Point Budget (Level 28 Milestone)

At character level 28, you have **40-41 Focus Points** available. By utilizing your attribute learning rate multipliers and selective dumping, you can build a highly optimized commander with zero wasted points:

| Skill | Focus Invested | Attribute Level | Learning Limit | Target Perk Unlocked |
| :--- | :---: | :---: | :---: | :--- |
| **Athletics** | **5** | 3 (5) | 232 (growth) | level 175 `Durable` ($+1$ Endurance) |
| **Smithing** | **5** | 3 (5) | 232 (growth) | level 225 `Enduring Smith` ($+1$ Endurance) |
| **Riding** | **1** | 5 (rotated) | 100 | level 100 `Sweeping Wind` ($+2\%$ Party Speed) |
| **Medicine** | **5** | 7 (to 10) | 288 (to 330) | level 275 `Minister of Health` (troop HP scaling; level 200 `Physician of People` is also covered) |
| **Scouting** | **5** | 7 | 288 | level 275 `Uncanny Insight` (passive map speed) |
| **Steward** | **5** | 7 (to 10) | 288 (to 330) | level 250 `Master of Warcraft` / `Master of Planning` (siege-camp wages or food logistics) |
| **Engineering** | **0 (or 3)**| 7 (to 10) | 88 (to 250) | level 80 (Dumped) / level 150 `Stonecutters` (If player builds) |
| **Tactics** | **0** | 7 | **88** | level 75 `Horde Leader` ($+10$ Party Size) |
| **Roguery** | **0** | 7 | **88** | level 75 `Know-How` (villager/caravan loot or governor security) |
| **Leadership** | **2** | 2 | 98 | level 75 `Authority` ($+5$ Party Size) |
| **Charm** | **1** | 2 | 58 | level 50 `Oratory` ($+1$ Renown / $+1$ Influence per issue) |
| **Trade** | **1** | 2 | 58 | level 50 `Caravan Master` (price marking or +30% carrying capacity) |
| **One-Handed** | **1** | 5 (rotated) | 100 | level 25 `Wrapped Handles` ($+30$ skill to infantry) |
| **Two-Handed** | **1** | 5 (rotated) | 100 | level 100 `Beast Slayer` / `Shield breaker` (mount or shield damage) |
| **Bow** | **1** | 5 (rotated) | 100 | level 100 `Merry Men` ($+5$ Party Size) |
| **TOTAL SPENT** | **33-36 Focus**| -- | -- | **4-8 Focus Points Leftover (Flexible Buffer)** |

### Progression Path for Leftover Points:
* **Weapon Splashes**: Spend 1 focus point on **Polearm** (limit 100 for infantry speed buffs) or **Throwing** (limit 100 for infantry stat boosts).
* **Diplomacy Pushes**: Spend 3 additional focus points in **Leadership** (bringing it to 5 focus) to reach the level 175 perk `Uplifting Spirit` ($+10$ party size).

---

## 3. Directory of Key Commander & Party Leader Perks

Prioritize these perks to scale party size, campaign speed, and infantry/archer combat performance:

### A. Party Size Perks
* **Athletics (75) - `Imposing Stature`** (Party Leader): $+5$ Party Size.
* **Bow (100) - `Merry Men`** (Party Leader): $+5$ Party Size.
* **Tactics (75) - `Horde Leader`** (Party Leader): $+10$ Party Size. (Unlocked with 0 focus).
* **Scouting (150) - `Mounted Scouts`** (Party Leader): $+5$ Party Size.
* **Leadership (75) - `Authority`** (Party Leader): $+5$ Party Size.
* **Leadership (175) - `Uplifting Spirit`** (Party Leader): $+10$ Party Size.
* **Steward (250+) - `Price of Loyalty`** (Quartermaster): $+0.25$ Party Size per skill point above 250.

### B. Campaign Map Speed & Logistics Perks
* **Riding (100) - `Sweeping Wind`** (Party Leader): $+2\%$ campaign travel speed.
* **Medicine (75) - `Sledges`** (Surgeon): $-50\%$ party speed penalty from carrying wounded troops.
* **Athletics (200) - `Strong`** (Party Leader): $+5\%$ campaign map speed contribution from foot troops.
* **Scouting (75) - `Forest Kin`** (Scout): $-50\%$ speed penalty from forest terrain if party is $\ge 75\%$ infantry.
* **Scouting (100) - `Forced March`** (Scout): $+2.5\%$ travel speed when party morale is $>75$.

---

## 4. Troop Combat Commander Perks (Captain Role)

### A. Infantry & Shock Troop Formations (Vigor/Endurance)
* **One-Handed (25) - `Wrapped Handles`**: $+30$ One-Handed skill to infantry in your formation.
* **Two-Handed (25) - `Strong Grip`**: $+30$ Two-Handed skill to infantry in your formation.
* **One-Handed (75) - `Shield Bearer`**: $+3\%$ combat movement speed to infantry in your formation.
* **One-Handed (125) - `Arrow Catcher` / `Shieldwall`**: Increases shield coverage area for troops in your formation.
* **Polearm (75) - `Clean Thrust`**: $+30$ Polearm skill to infantry in your formation.
* **Polearm (100) - `Footwork`**: $+2\%$ combat movement speed to infantry in your formation.
* **Athletics (250) - `Ignore Pain`**: $+5$ flat armor to all equipped armor pieces of foot troops in your formation.

### B. Archer & Ranged Formations (Control)
* **Bow (25) - `Dead Aim`**: $+20$ Bow skill to troops in your formation.
* **Bow (25) - `Bow Control`**: $+5\%$ damage with bows to troops in your formation.
* **Bow (50) - `Bodkin`**: $+5\%$ armor penetration with bows to troops in your formation.
* **Bow (50) - `Nocking Point`**: $+3\%$ combat movement speed to archers in your formation.
* **Bow (75) - `Quick Adjustments`**: $-5\%$ accuracy penalty to archers in your formation.
* **Bow (125) - `Strong Bows`**: $+5\%$ damage with bows by Tier 3+ troops in your formation.
* **Bow (175) - `Skirmish Phase Master`**: $-10\%$ damage taken from projectiles by ranged troops in your formation.
