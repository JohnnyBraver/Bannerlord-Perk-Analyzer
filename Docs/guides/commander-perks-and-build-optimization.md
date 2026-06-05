# Commander Perks and Build Optimization Guide

This guide provides a comprehensive cost-benefit analysis of the primary commanding general build:
$$\text{VIG 3(5) | CTR 2(4) | END 3(5) | CNG 7 | SOC 2 | INT 7}$$

It goes skill-by-skill to calculate the exact focus point cost required to reach target perks under this attribute profile, outlines why maxing every skill is a trap, and ranks investments by commander doctrine instead of by cheap unlock count.

The commander doctrine assumed here is an elite one-party army: maximize live combat power per troop first, keep enough campaign mobility to choose fights second, and grow party size after the force can still catch worthwhile targets. For shock infantry, combat movement speed belongs in the combat-power bucket, not the convenience bucket, because faster troops spend less time under arrows and force melee contact more reliably.

Control is deliberately lower than the older `CTR 3(5)` draft. The default shock-infantry plan can stay at purchased Control 2, then use `Controlled Smith` plus `Steady` to operate at effective Control 4 while the relevant Control skills are trained. That reaches Bow 100 and Throwing 125 with two focus each; buying the extra Control point mostly saves one focus on Bow 100 and is better reserved for archer, crossbow, or throwing-specialist variants.

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

#### Scouting (Target: 275)
* **Strategic Value**: Extremely High for engagement control. The tree has useful path pickups, but the real target is level 275 `Uncanny Insight`: at unlock it gives $+7.5\%$ party speed immediately ($0.1\% \times (275 - 200)$), then continues scaling. Scouting 250 is weak for live-command doctrine because its rows are army/siege/simulation leaning.
* **Focus Cost**:
  * *At 7 Cunning*: **5 Focus** is required to reach 275 (limit 288). 4 focus only caps at 248, missing the real speed perk.

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

### C. Combat & Physical Skills (Endurance-Assisted Physical Planning)

#### Athletics & Smithing (Target: 175 / 225 during leveling phase)
* **Focus Cost**: **5 Focus** each during the training phase. Pushing these to 5 focus points raises your learning limit to 232 with 3 Endurance, which is required to unlock `Durable` (Athletics 175) and the Smithing 225 attribute/focus choice. `Enduring Smith` pushes Endurance, while `Fencer Smith` gives +1 focus to both One Handed and Two Handed. `Fencer Smith` stacks with the +2 Vigor package from `Vigorous Smith` and `Strong`, but it replaces the +1 Endurance option while active.
* **Vigor hyper-stretch note**: Because focus caps at 5, `Fencer Smith` should be read as saving one manual focus allocation in One Handed and one in Two Handed, not as pushing either skill past 5 focus. It can be used as a training/refund tool: let the granted focus help reach the target weapon perks, then later respec once the skill levels are already trained. This does not help Polearm.

#### Riding (Target: 100)
* **Focus Cost**: **1 Focus**. Once Endurance is pushed to 5, 1 focus point is enough to reach exactly 100 ($4 + 14 \times 4 + 40 \times 1 = 100$) to unlock `Sweeping Wind` ($+2\%$ party speed).

#### Weapon Skills (One-Handed, Two-Handed, Bow, Crossbow, Throwing)
* **Target**: Level 100 for cheap utility perks like Two-Handed `Beast Slayer` / `Shield breaker`, One-Handed `Shield Bearer`, or Bow `Merry Men` $+5$ party size. `Projectile Deflection` is a stronger defensive tool, but it is a level 150 perk and requires a separate investment plan.
* **Vigor Focus Cost**: Vigor can still justify a 5-attribute package when One Handed and Polearm are both pushed. At Vigor 5, 1 focus reaches level 100, 3 focus reaches Two Handed 175, and 5 focus reaches the 225/250 Vigor stretch.
* **Control Focus Cost**: Control should normally be planned from assisted Control 4, not bought to 3(5). At Control 4, 2 focus reaches level 126, enough for both Bow 100 `Merry Men` and Throwing 125 `Skirmisher`. Crossbow is usually 0 for shock infantry. Control 5 is a ranged-specialist or luxury focus-saver, not a default attribute purchase.

---

## 2. Commander Investment Priority Table

The build should not be optimized around a fixed level-28 focus total or around grabbing every cheap-looking perk. The real target is an elite one-party army that wins badly outnumbered live battles, can choose those battles, and only then grows the stack. Read this as a modular priority table: buy the core package first, then add stretches only when they support the troop composition.

| Doctrine Role | Skill / Package | Efficient Target | Stretch Target | Investment Read |
| :--- | :--- | :--- | :--- | :--- |
| **Engagement control** | **Scouting** | 275 | N/A | This is a core build target, not a luxury stretch. `Uncanny Insight` gives $+7.5\%$ party speed the moment it unlocks and keeps scaling, which directly controls which fights the elite party can take. The 175/225 rows are path utility; 250 is weak for live command. |
| **Core troop lethality** | **One Handed infantry package** | 225 | 250 if Vigor 5 is already justified | Best Vigor sink for shield infantry. `Wrapped Handles`, shield coverage, `Fleet of Foot` / `Steel Core Shields`, and `Deadly Purpose` / `Unwavering Defense` are all real commander value. `Prestige` at 250 adds +15 party size, but it is a stretch, not the reason to buy Vigor alone. |
| **Core troop lethality** | **Polearm infantry package** | 175 | 250 as part of the Vigor 5 package | `Clean Thrust`, `Footwork`, and `Phalanx` are efficient shock-infantry power. Push 250 only when the +20 Polearm skill from `Counterweight` supports the actual troop mix and shares the Vigor 5 cost with One Handed. |
| **Cheap troop support** | **Two Handed infantry package** | 100 or 175 | 200 / 225 only with spare focus or personal two-hander use | The early rows are useful, especially skill, shield, and mount damage. The 175 tier is the clean stop if +5 party size matters. At Vigor 5, 200 costs another focus for only +2% infantry speed/damage or +5 HP; 225 costs two extra focus over 175 for +2% infantry attack speed. |
| **Combat staying power** | **Medicine** | 275 | 330 | One of the best late-game point homes. `Minister of Health` converts extra Medicine into broad troop HP, which makes small HP alternatives less urgent elsewhere. |
| **Combat staying power / enabler** | **Athletics + Smithing engine** | Athletics 200, Smithing 150 / 225 | Athletics 250 if foot armor is central | These are not just perks; they are the physical attribute engine. Use Athletics/Smithing to unlock Vigor, Control, or Endurance plans, then judge the live troop perks separately. `Ignore Pain` at Athletics 250 is a real foot-troop armor stretch. |
| **Engagement control** | **Riding** | 100 | Niche logistics only | `Sweeping Wind` is the infantry-party payoff. Past 100, Riding is ally-battle morale, herding, prisoners, mounted-only captain value, mounted armor, or personal mount scaling. |
| **Party scaling** | **Leadership** | 75 / 175 | 250+ only for Social builds | Party size is good, but it comes after per-troop power and fight selection. With low Social, 75 is cheap and 175 is the practical high stop; 250+ needs a deliberate Social plan. |
| **Party scaling / logistics** | **Steward** | 250 if the player is quartermaster | 275+ for dedicated quartermasters | Steward scales the elite party and keeps it affordable, but it is a support package. Delegate it if another hero can cover quartermaster better than the player. |
| **Composition-specific support** | **Bow / Throwing / Crossbow** | Control 2(4): Bow 100, Throwing 125, Crossbow usually 0 | Higher only for ranged or throwing-heavy armies | `Merry Men`, `Flexible Fighter`, and `Skirmisher` are the broad pickups, and assisted Control 4 reaches them with two focus each. Do not buy Control 3 just to save one Bow focus. Bow 175+ is for archer-heavy parties. Crossbow `Counter Fire` is crossbow-user mitigation, not universal infantry resistance. |
| **Free or QoL pickups** | **Tactics, Roguery, Charm, Trade** | 0-1 focus where the attribute already supports it | Campaign-plan dependent | Take free Cunning milestones and one-focus QoL such as Trade price marking. Do not let autoresolve, loot, or diplomacy perks crowd out the commander core unless that is the campaign plan. |
| **Delegate / avoid by default** | **Engineering** | 0 on the player | 150 / 225 only if the player is the active engineer | Fire engines and `Metallurgy` are useful, but they are expensive for this doctrine. A companion engineer is usually the cleaner solution. |

### Reinvestment Bar
The generated [commander perk investment bars](../reports/commander-perk-investment-bars.md) are the current stopping-point reference. The main point-budget read is:

The neutral cost model starts every skill at 2 attribute, but the practical physical model is better than that once the Endurance perks are online. Athletics and Smithing can provide two free points into a chosen physical attribute, so Vigor, Control, or Endurance can often be planned from a 4-attribute baseline. That means level 225 physical perks can become focus-only, and level 250 physical perks can become a one-purchased-attribute stretch. For Control, this changes the default profile to `CTR 2(4)`: the old bought Control point is dropped unless the build is truly ranged-focused. The enabler perks still have to be reached first, and the free points cannot sit in every physical attribute at the same time.

The extreme Vigor plan has one more wrinkle: `Fencer Smith` at Smithing 225 stacks with the +2 Vigor path and gives +1 focus to One Handed and +1 focus to Two Handed. In practice, that can win back two manual focus points while those skills are being trained. The tradeoff is losing `Enduring Smith` while Fencer is selected, so it is strongest as a temporary weapon-training enabler or as a final choice only if the build does not need the extra Endurance point.

| Skill Area | Practical Stop | Why |
| --- | ---: | --- |
| Scouting | 275 | `Uncanny Insight` is the point of the tree: $+7.5\%$ party speed immediately at unlock, then more above 275. |
| Control baseline | 2(4) | Drop the bought Control point for shock infantry. Assisted Control 4 reaches Bow 100 and Throwing 125 with 2 focus each; Control 5 is mostly a ranged-specialist focus saver. |
| Bow | 100 | `Merry Men` is the universal prize; later perks are archer-specialist or personal. |
| Crossbow | 0 | Skip for shock infantry. `Counter Fire` is crossbow-user mitigation, not universal infantry ranged resistance. |
| Throwing | 125 | `Flexible Fighter` and `Skirmisher` are the clean commander rows; later tiers are morale/QoL or throwing-specialist. |
| Riding | 100 | `Sweeping Wind` is the infantry-party map-speed prize; later rows are niche logistics, mounted-specific, or personal mount value. |
| Two Handed | 175 / 200 / 225 | The efficient commander stop is 175. At Vigor 5, 200 costs one extra focus for only +2% infantry movement/damage or +5 HP; 225 costs two extra focus over 175 for +2% infantry attack speed. |
| Polearm | 175 / 250 | Strong skill/speed package through `Phalanx`; if Vigor 5 is already planned, 250 `Counterweight` is a worthwhile +20 Polearm skill extension. |
| One Handed | 225 / 250 | `Deadly Purpose` / `Unwavering Defense` justify 225; if Vigor 5 is already planned, 250 `Prestige` adds +15 party size. |
| Athletics | 200 / 250 | 225 is weak, but 250 `Ignore Pain` is a real +5 armor stretch if Athletics is already central. |

The points freed by stopping physical skills earlier usually belong in **Scouting**, **Medicine**, **Steward**, or **Leadership**. Attribute points get better when shared by several skills under the same attribute, so a single late physical perk should not be evaluated as if it owns the whole Vigor/Control/Endurance purchase. In the current Vigor read, the fifth attribute point is defensible only as a package: One Handed 250 plus Polearm 250, while Two Handed usually stops at 175 unless the build has spare focus or the player personally fights with two-handers.

---

## 3. Directory of Key Commander & Party Leader Perks

Prioritize these perks by doctrine: live troop lethality and responsiveness first, campaign engagement control second, party size and logistics third. The generated commander report in `Data/intermediate/commander_perks_report.txt` applies that ranking across the full perk export and separates campaign party speed, troop combat movement, weapon handling speed, projectile speed, and siege speed. For speed, defense, and banner tradeoffs, use the generated [banner package comparison](../reports/commander-banner-package-comparison.md) together with the [banner effects reference](../reports/banner-effects.md), where the confirmed mechanics and package assumptions are visible instead of compressed into a simplified exposure shortcut.

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
* **Scouting (275) - `Uncanny Insight`** (Scout): $+7.5\%$ party speed at unlock, then $+0.1\%$ per Scouting point above 275.

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

> [!NOTE]
> When movement speed competes with small HP gains, the speed side can be better for elite shock infantry than it first looks. Medicine, armor, and resistance perks can stack a lot of survivability, while movement speed directly reduces exposure before contact and improves how quickly infantry respond to orders.

### B. Archer & Ranged Formations (Control)
* **Bow (25) - `Dead Aim`**: $+20$ Bow skill to troops in your formation.
* **Bow (25) - `Bow Control`**: $+5\%$ damage with bows to troops in your formation.
* **Bow (50) - `Bodkin`**: $+5\%$ armor penetration with bows to troops in your formation.
* **Bow (50) - `Nocking Point`**: $+3\%$ combat movement speed to archers in your formation.
* **Bow (75) - `Quick Adjustments`**: $-5\%$ accuracy penalty to archers in your formation.
* **Bow (125) - `Strong Bows`**: $+5\%$ damage with bows by Tier 3+ troops in your formation.
* **Bow (175) - `Skirmish Phase Master`**: $-10\%$ damage taken from projectiles by ranged troops in your formation.

### C. Battle Banner Shortlist
The generated [banner effects report](../reports/banner-effects.md) now extracts the actual banner tier values from `DefaultBannerEffects.InitializeAll` and joins them to banner item XML. The generated [banner package comparison](../reports/commander-banner-package-comparison.md) scores full commander-relevant perk alternative sets around the main banner options.

For the shock-infantry commander doctrine, the main competitors are:
* **Banner of Dust Devils / Strider's Flag**: $+30\%$ infantry movement speed at tier 3.
* **Locked Shields Banner / Testudo Standard**: $-15\%$ ranged attack damage taken at tier 3. The raw game description string is misleading, but the effect id and combat formulas point to ranged damage reduction.
* **Banner of Sultan's Eagle / Tug of Whistling Arrow**: $-8\%$ ranged accuracy penalty for ranged troops at tier 3, mostly for archer-heavy commanders. The effect applies to `WeaponInaccuracy`, so read it as base spread/inaccuracy reduction rather than a direct $+8\%$ hit chance or movement-penalty fix.
* **Standard of Wrath**: $+15\%$ melee damage at tier 3, strong on paper but less certain when elite shock troops already overkill many targets.
