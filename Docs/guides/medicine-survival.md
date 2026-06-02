# Troop Survival And Medicine

This note focuses only on troop-facing survivability: death vs wound rolls, hit points, armor, damage resistance, shield protection, and mount durability. It intentionally excludes Medicine healing-rate perks, personal-only hero survival, social effects, governor economy, and settlement management.

Sources used for this pass:

- `Data/generated/postprocessed-perk-effects.json`
- `DefaultPartyHealingModel.GetSurvivalChance`
- `DefaultPartyHealingModel.AddSurgeonSurvivalBonus`
- `DefaultPartyHealingModel.AddDoctorsOathSkillBonusForParty`
- `DefaultPartyHealingModel.GetSiegeBombardmentHitSurgeryChance`
- `SiegeEventCampaignBehavior.KillRandomTroopsOfEnemy`
- `DefaultSkillLevelingManager.OnSurgeryApplied`
- `Docs/notes/troop-category-counting.md`

## Death Vs Wound Roll

The Medicine tooltip is easy to misread. The surgeon survival bonus is not a flat final survival percentage. It is added into a denominator, then the game converts that denominator into a death chance.

For regular non-hero troops after a casualty has become lethal:

```text
baseDenominator =
  1
  + surgeon Medicine * 0.01 * eventMultiplier
  + troop level * 0.02
  + additive survival bonuses

finalDenominator =
  baseDenominator * (1 + factor survival bonuses)

wound chance = 1 - (1 / finalDenominator)
death chance = 1 / finalDenominator
```

Important details:

- The troop term uses `character.Level`, not troop tier.
- The Medicine skill cap is `330`, so the surgeon skill term can reach `+3.3` in player map events.
- In player map events, the surgeon Medicine multiplier is `1.0`.
- In non-player map events, the surgeon Medicine multiplier is `0.25`, so Medicine 330 contributes `+0.825`.
- `add_factor` survival perks multiply the denominator. A 30% `add_factor` is `* 1.3`, not `+30` final survival percentage points.
- Blunt damage normally gives `100%` wound chance unless that damage is explicitly allowed to kill even if blunt.

Example with a level 20 troop and no survival factor perks:

| Surgeon Medicine | Denominator | Wound chance | Death chance |
| ---: | ---: | ---: | ---: |
| 0 | 1.40 | 28.6% | 71.4% |
| 80 | 2.20 | 54.5% | 45.5% |
| 150 | 2.90 | 65.5% | 34.5% |
| 200 | 3.40 | 70.6% | 29.4% |
| 300 | 4.40 | 77.3% | 22.7% |
| 330 | 4.70 | 78.7% | 21.3% |

This is why visible values like `+0.8` or `+3.3` feel much larger than normal percentage bonuses. They are denominator bonuses, so they reduce `1 / denominator` death chance.

## Direct Death And Wound Perks

These perks affect death vs wound outcomes directly, or apply Medicine to casualty conversion.

| Level | Perk | Role | Effect | Survivability note |
| ---: | --- | --- | --- | --- |
| 75 | Doctor's Oath | Surgeon | Your medicine skill partially applies to enemy casualties, increasing potential prisoners. | Applies your Medicine survival bonus to enemy casualties, making more enemies wounded instead of dead. Full effect in player map events, `0.1` multiplier in non-player map events. |
| 125 | Siege Medic | Surgeon | 50% chance of troops getting wounded instead of getting killed during siege bombardment. | Used by the siege bombardment casualty split. |
| 125 | Siege Medic | Surgeon | 30% chance to recover from lethal wounds during siege bombardment. | Present in perk data. This pass found the primary 50% path directly; keep this secondary effect marked for a deeper siege-path audit. |
| 200 | Physician of People | Surgeon | 30% chance to recover from lethal wounds for tier 1 and 2 troops. | In normal map-event survival, this is an `add_factor`, so it multiplies the survival denominator by `1.3` for tier 1-2 regular troops. |

## Hit Points

Hit points are pre-roll survivability. They make a lethal casualty less likely before Medicine has to decide whether that casualty becomes a wound or a death.

Troop type wording in this section follows `Docs/notes/troop-category-counting.md`: foot troops are broader than infantry, mounted troops include horse archers unless the consuming code also requires melee/cavalry, and `TroopUsageFlags.Ranged` can include mounted ranged troops.

Theoretical maximum party-leader/personal stacks:

| Troop or mount type | Max stack | Ingredients | Notes |
| --- | ---: | --- | --- |
| Any regular troop | +90 HP | `Minister of Health` at Medicine 330, `Hardy Frontline`, `Thick Hides` | Baseline for every troop if the party leader has the relevant perks. |
| Foot infantry | +108 HP | Any regular troop stack, `Well Built`, `Unwavering Defense`, `Hard Knock` | Largest flat troop HP stack found in the data. |
| Foot ranged troop | +100 HP | Any regular troop stack, `Well Built`, `Picked Shots` | Foot and ranged are separate concepts; a foot archer can satisfy both. |
| Mounted non-ranged troop | +90 HP | Any regular troop stack | Rider HP only; mount HP is separate. |
| Mounted ranged troop | +95 HP | Any regular troop stack, `Picked Shots` | Applies only in contexts that use the broad `TroopUsageFlags.Ranged` meaning, not live-agent `IsRanged`. |
| Troop mounts | +15 HP and +10% mount HP | `Sledges`, `Veterinary` | Flat mount HP and percentage mount HP are different effect types, so do not combine them as one flat number. |

Hit point perks:

| Skill | Level | Perk | Role | Effect |
| --- | ---: | --- | --- | --- |
| Medicine | 75 | Sledges | Party leader | 15 hit points to mounts in your party. |
| Medicine | 275 | Minister of Health | Personal | 1 hit point to troops for every skill point above 250. At the 330 cap, this is +80 HP. |
| Athletics | 25 | Well Built | Party leader | 5 hit points to foot troops in your party. |
| Crossbow | 250 | Picked Shots | Party leader | 5 hit points to ranged troops in your party. |
| One Handed | 225 | Unwavering Defense | Party leader | 10 hit points to infantry in your party. |
| Polearm | 100 | Hard Knock | Party leader | 3 hit points to infantry in your party. |
| Polearm | 200 | Hardy Frontline | Party leader | 5 hit points to troops in your party. |
| Riding | 50 | Veterinary | Party leader | 10% hit points to mounts of troops in your party. |
| Two Handed | 200 | Thick Hides | Party leader | 5 hit points to troops in your party. |

## Armor

Armor is also pre-roll survivability. It reduces damage before the casualty roll, and therefore pairs extremely well with high Medicine.

Theoretical maximum captain armor stacks:

| Formation type | Max armor stack | Ingredients | Notes |
| --- | ---: | --- | --- |
| Any troop in formation | +5 armor per equipped armor piece | `Metallurgy` | Broad Engineering captain layer. |
| Foot troop in formation | +10 armor per equipped armor piece | `Metallurgy`, `Ignore Pain` | Best foot-troop armor stack. |
| Mounted troop rider in formation | +10 armor per equipped armor piece | `Metallurgy`, `Dauntless Steed` | Best cavalry rider armor stack. |
| Troop mounts in formation | +10 mount armor | `Tough Steed` | Mount armor, not rider armor. |

Armor perks:

| Skill | Level | Perk | Role | Effect |
| --- | ---: | --- | --- | --- |
| Athletics | 250 | Ignore Pain | Captain | 5 armor to all equipped armor pieces of foot troops in your formation. |
| Engineering | 225 | Metallurgy | Captain | 5 armor to all equipped armor pieces of troops in your formation. |
| Riding | 250 | Dauntless Steed | Captain | 5 armor to all equipped armor pieces of mounted troops in your formation. |
| Riding | 250 | Tough Steed | Captain | 10 armor to mounts of troops in your formation. |

## Damage Resistance

Damage resistance is the third pre-roll layer. The percentage damage-taken and shield-damage rows here are generated as `add_factor` effects. Exact stacking is handled by the consuming combat model, so the totals below should be treated as buildable overlapping factors rather than a guaranteed final UI line.

Theoretical maximum overlapping resistance stacks:

| Situation | Max listed stack | Ingredients | Notes |
| --- | ---: | --- | --- |
| Broad live-battle formation damage | -5% | `Elite Reserves` captain | Applies to troops in the captain's formation. |
| Melee infantry vs projectile body hits | -8% | `Skirmisher`, `Elite Reserves` captain | `Skirmish Phase Master` is ranged-troop only; `Counter Fire` is crossbow-current-weapon only; `Basher` is in the melee-hit branch. |
| Melee infantry vs projectile body hits with best ranged-resistance banner | -23% | `Skirmisher`, `Elite Reserves` captain, tier 3 `DecreasedRangedAttackDamage` banner | Best live-battle body-hit mitigation for normal melee infantry found so far. Shields add a separate coverage/blocking layer. |
| Bow ranged troops vs projectiles/ranged attacks | -18% | `Skirmish Phase Master`, `Skirmisher`, `Elite Reserves` captain | `Counter Fire` does not apply to bow troops in the damage code. |
| Crossbow troops vs projectiles/ranged attacks while holding a crossbow | -21% | `Skirmish Phase Master`, `Counter Fire`, `Skirmisher`, `Elite Reserves` captain | `Counter Fire` is code-gated to the victim's current main-hand weapon class being `Crossbow`. |
| Bow ranged troops vs projectiles with best ranged-resistance banner | -33% | `Skirmish Phase Master`, `Skirmisher`, `Elite Reserves` captain, tier 3 `DecreasedRangedAttackDamage` banner | Best Fian-style live-battle ranged mitigation stack found so far. |
| Crossbow troops vs projectiles with best ranged-resistance banner while holding a crossbow | -36% | `Skirmish Phase Master`, `Counter Fire`, `Skirmisher`, `Elite Reserves` captain, tier 3 `DecreasedRangedAttackDamage` banner | Best Sharpshooter-style live-battle ranged mitigation stack found so far. |
| Infantry in shield wall vs general damage | -9% | `Basher`, `Elite Reserves` captain | Shield wall condition required for `Basher`. |
| Infantry in shield wall vs ranged attacks | -8% to -23% plus shield coverage | `Skirmisher`, `Elite Reserves` captain, optional ranged-resistance banner, shield coverage perks | Shield wall does not add a body-damage resistance factor against arrows/bolts through `Basher`; `Arrow Catcher` and `Shieldwall` add coverage rather than a simple damage-taken percentage. |
| Charge damage to formation | -60% charge-specific | `Braced`, `Sure Footed` | Very large anti-cavalry impact layer. |
| Charge damage with broad mitigation | -65% listed factors | `Braced`, `Sure Footed`, `Elite Reserves` captain | If broad damage mitigation applies to the same hit. |
| Charge damage to infantry in shield wall | -69% listed factors | `Braced`, `Sure Footed`, `Elite Reserves` captain, `Basher` | If all formation and damage-type conditions apply. |
| Simulation infantry vs ranged troops | -10% | `Loose Formations` | Autoresolve only. |
| Simulation tier 3+ units | -20% | `Elite Reserves` party leader | Autoresolve only. |
| Simulation tier 3+ infantry vs ranged troops | -30% listed factors | `Loose Formations`, `Elite Reserves` party leader | Autoresolve only, if both conditions apply. |
| Shield protection | +0.01 to +0.02 coverage, -10% shield damage | `Arrow Catcher`, `Shieldwall`, `Steel Core Shields` | Coverage and shield durability are separate from troop damage resistance. |

Damage resistance and shield perks:

| Skill | Level | Perk | Role | Scope or condition | Effect |
| --- | ---: | --- | --- | --- | --- |
| Bow | 175 | Skirmish Phase Master | Captain | Ranged troops in formation | -10% damage taken from projectiles by ranged troops in your formation. |
| Crossbow | 175 | Counter Fire | Captain | Victim's current main-hand weapon must be a crossbow | -3% damage taken from projectiles by your troops. The text is broader than the code path; bow archers and melee infantry do not benefit. |
| Throwing | 125 | Skirmisher | Captain | Troops in formation | -3% damage taken by ranged attacks to troops in your formation. |
| One Handed | 25 | Basher | Captain | Infantry in shield wall, melee-hit branch | -4% damage taken by infantry while in shield wall formation. Does not reduce arrow/bolt body-hit damage in the ranged branch. |
| Tactics | 200 | Elite Reserves | Captain | Troops in formation | -5% damage taken by troops in your formation. |
| Tactics | 25 | Loose Formations | Party leader | Simulation; infantry vs ranged | -10% damage to your infantry from ranged troops when troops are sent to confront the enemy. |
| Tactics | 200 | Elite Reserves | Party leader | Simulation; tier 3+ units | -20% less damage to tier 3+ units when troops are sent to confront the enemy. |
| Athletics | 125 | Braced | Captain | Charge damage to formation | -30% charge damage taken by troops in your formation. |
| Polearm | 225 | Sure Footed | Captain | Charge damage to formation | -30% charge damage taken by troops in your formation. |
| One Handed | 125 | Arrow Catcher | Captain | Troops in formation | Larger shield protection area against projectiles for troops in your formation. |
| One Handed | 125 | Shieldwall | Captain | Troops in shield wall | Larger shield protection area against projectiles to troops in your formation while in shield wall formation. |
| One Handed | 200 | Steel Core Shields | Captain | Infantry shields in formation | -10% damage to shields of infantry troops in your formation. |

## Practical Takeaways

- Medicine skill itself is the core death-prevention engine. It reduces death chance through `1 / denominator`, so the practical effect is much larger than the tooltip looks.
- `Physician of People` is the direct low-tier troop survival perk. Because it multiplies the denominator by `1.3`, it stacks well with high Medicine.
- `Minister of Health` is the major elite-army payoff. At Medicine 330, `+80` troop hit points can prevent many lethal casualties before the death-vs-wound roll is reached.
- Hit points, armor, and resistance are separate pre-roll layers. Stacking them with high Medicine is the real durability curve: fewer troops become lethal casualties, and a larger share of lethal casualties become wounded instead of dead.
- Captain armor, shield, projectile, charge, and damage-reduction perks are powerful, but only for the relevant formation or condition.
- Simulation-only wording such as "troops are sent to confront the enemy" should stay separate from live battle troop combat effects.
