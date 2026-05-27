# Bannerlord XP Insights

Generated: 2026-05-27T21:17:10.303640+03:00

This is the approachable companion to `Data/generated/reports/xp-formulas.md`. The formula report keeps the evidence trail; this guide turns the same findings into gameplay and analysis notes.

## Fast Takeaways

- XP usually has three parts: how much raw XP an action creates, which multiplier stack touches it, and which skill or troop stack receives it.
- Combat XP cares about target value and effective damage, not just the damage number shown on screen.
- A lethal hit is special: damage is capped at target max HP, then a kill adds another target max HP chunk. Overkill beyond max HP does not keep scaling.
- Ranged difficulty is a real XP lever. Distance helps, lateral movement helps, and headshots multiply difficulty by `1.2`.
- Riding XP from mounted actions is separate from weapon XP, so mounted ranged play can look like it pays unusually well even when the weapon XP formula is unchanged.
- Learning rate can dominate everything. A high-value action at zero learning rate is still effectively wasted for that skill.
- Troop XP is capacity-based. Stacks that still need XP toward an upgrade can absorb shared XP; stacks that are already capped for upgrades stop being useful sinks.

## Combat Tips

Combat hit XP starts from this shape:

```text
baseXp = 0.4 * attackerPower * targetPower * effectiveDamage * missionTypeMultiplier
effectiveDamage = min(damage, targetHp) + targetHp if the hit is fatal
```

- Full-health one-shot kills are valuable because they can count as roughly two target-HP chunks: one from capped damage and one from the fatal branch.
- Massive overkill is less special than it feels. Once damage reaches target max HP, extra damage past that point does not increase the damage chunk.
- Stronger targets matter because target troop power is in the base formula. Farming very weak enemies should fall off even if they die quickly.
- Mission type matters: battle is `1.0x`, simulation battle is `0.9x`, tournament is about `0.33x`, and practice fight is `0.0625x`.
- Training in practice fights is therefore a very poor direct combat-XP farm compared with real battles.

## Ranged Difficulty

Shot difficulty is built from distance and relative lateral movement, then clamped before the headshot bonus:

```text
rawDifficulty = 0.3 * ((distance + 4) / 4) * ((4 + lateralMotion * relativeSpeed) / 4)
shotDifficulty = clamp(rawDifficulty, 1, 12)
headshotDifficulty = shotDifficulty * 1.2
```

- Long shots help directly.
- Targets moving across your aim line are better than targets moving straight toward or away from you.
- Headshots do not add a separate XP award; they raise shot difficulty, which then raises the ranged XP multiplier.
- Non-Bow ranged skills can reach about `3.0x` final ranged XP from capped shot difficulty. Bow uses a smaller skill factor and tops out around `2.0x`.
- The theoretical dream shot is long range, high lateral movement, and a headshot on a valuable target that dies from the hit.

## Mounted Play

Mounted actions can produce Riding XP on top of the main action XP:

```text
ridingXp = baseXpAmount * (1 + horseDifficulty * 0.02)
```

- A harder horse increases Riding XP by about `2%` per horse difficulty point.
- Mounted ranged play can stack weapon XP, shot-difficulty XP, and Riding XP. That explains why horseback long shots can feel so rewarding.
- Travel on horse also awards Riding XP from `roundRandomized(0.3 * speed)`, routed through the same horse-difficulty bonus.

## Learning Rate And Build Planning

Skill XP is scaled by learning rate when the award is focus-affected:

```text
skillXpDelta = rawXp * genericXpMultiplier * learningRate
peakLearningRange = 10 * (attribute - 1) + 30 * focus
skillLimit = 4 + 14 * (attribute - 1) + 40 * focus
```

- Focus is narrow but powerful: it helps one skill and pushes both peak learning range and skill limit up.
- Attribute points help every skill under that attribute. Raising Control helps Bow, Crossbow, and Throwing at the same time.
- Past peak learning range, the over-limit penalty starts cutting learning rate. At the skill limit, learning reaches zero.
- The best time to do expensive or rare XP actions is while the target skill is still inside a good learning range.
- Endurance attribute perks remain build-warping because their permanent attribute points can stretch later skill limits across the whole attribute group.

## Troop XP

The direct troop battle XP reward grows roughly quadratically with troop level:

| Killed troop level | XP reward |
| ---: | ---: |
| 1 | 16 |
| 6 | 48 |
| 11 | 96 |
| 16 | 161 |
| 21 | 243 |
| 26 | 341 |

- Higher-level kills are much better troop-XP fuel than low-level kills.
- Shared XP distribution is proportional to each stack's remaining upgrade capacity.
- If a stack is already sitting on enough XP to upgrade, it stops being a good shared-XP target. Upgrading or diversifying stacks can keep XP from bunching up awkwardly.
- Daily training from towns, buildings, and perks is useful background pressure, but the battle reward formula is the larger lever for fast troop growth.

## Smithing And Value-Based XP

Smithing formulas are strongly value-based:

```text
refiningXp = round(0.3 * outputMaterialValue * outputCount)
smeltingXp = round(0.02 * itemValue)
smithingCraftingOrderXp = round(0.1 * itemValue)
smithingFreeBuildXp = round(0.02 * itemValue)
```

- Item value is the main signal. More valuable inputs and outputs should matter more than the count of actions alone.
- Crafting-order smithing XP uses `0.1 * itemValue`, which is five times the free-build `0.02 * itemValue` rate before other order logic.
- Refining XP is based on produced material value and output count, so valuable refinement outputs can be more interesting than they look.
- Crafting order experience has extra tier and requirement checks; keep that one as a candidate for deeper hand-reading before turning it into final player advice.

## Activity XP

- Tournament model XP is `500` to one random skill from five equal bands: One Handed, Two Handed, Polearm, Riding, or Athletics.
- Hideout Roguery XP is sizable: ghost clearing rolls `1000-1400`, mission success rolls `700-1000`, and failure rolls `225-400`.
- Alley XP has big spikes: initial main hero XP is `1500`, successful defense is `6000`, daily main hero XP is `40`, and daily assigned clan member XP is `200`.
- Persuasion XP scales with difficulty and argument coefficient: `difficultyEnumValue * 5 * argumentDifficultyBonusCoefficient`.
- Warehouse production Trade XP is `0.1 * productionBaseValue`.
- Charm relation XP uses relation change times a branch multiplier. The multiplier branches need friendlier naming, but the constants suggest leaders and notables can matter a lot.

## Things Worth Checking Next

- Decode the exact branch names in `GetCharmExperienceFromRelationGain` so the charm multipliers become player-readable.
- Hand-read crafting-order bonus and penalty checks; the IL shows a base, tier factor, and halving path, but the condition names matter.
- Check whether discard/donation XP candidates need a dedicated insight section once the scan query is widened or hand-read.
- Connect perk effects to these formulas, especially troop training perks, battle XP perks, smithing learning perks, and ranged shot-difficulty helpers.

## Source

- Formula evidence: `Data\generated\reports\xp-formulas.md`
