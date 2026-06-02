# Troop AI Fighting Behavior

This note focuses on live-battle combat AI and the direct weapon stat effects that share the same skill inputs. It does not cover campaign-map AI, autoresolve, or survival/death rolls.

The short version: weapon skills matter twice. They give direct weapon stat bonuses, and they feed the AI decision values that control blocking, parrying, shooting, aiming error, shield use, and combat timing.

## Two AI Skill Tracks

`SetAiRelatedProperties` builds two AI levels for an agent:

- `meleeAI`, based on `GetMeleeSkill`.
- `currentAI`, based on the currently equipped weapon's relevant skill, or Athletics if no weapon is equipped.

In the normal/high difficulty band, with the default AI multiplier, both are calculated like this:

```text
AI level = clamp(effective skill / 300 * 0.96, 0, 1)
```

Other difficulty bands use `0.32` or `0.1` instead of `0.96`. The first step is linear, so a +30 skill bonus is about +0.096 AI level and a +80 skill stack is about +0.256 AI level before caps.

## Which Unit Skills Feed AI

These are the skills usually listed on troop XML entries and how they feed the AI behavior pass.

| Unit skill | AI use found | Practical note |
| --- | --- | --- |
| One Handed | Melee AI for one-handed weapons. Also the melee-AI fallback when the equipped weapon is not One Handed, Two Handed, or Polearm. | This means archers and crossbowmen still care about One Handed for melee reactions while holding a ranged weapon, and usually for sidearms too. |
| Two Handed | Melee AI for two-handed weapons when there is no secondary item. | Gives the full melee AI package for two-handed users. If a secondary item is present, the method falls back to One Handed. |
| Polearm | Melee AI for polearm weapons. | Especially important because Polearm has several stackable troop skill perks. |
| Bow | Current/ranged AI while a bow is equipped. | Affects shooting frequency, aim error, wait-before-shoot behavior, and ranged horseback missile range. It does not drive melee blocking. |
| Crossbow | Current/ranged AI while a crossbow is equipped. | Same ranged AI track as Bow, plus crossbow-specific direct reload effects elsewhere. |
| Throwing | Current/ranged AI while a throwing weapon is equipped. | Affects throwing AI while throwing. Melee behavior while holding a throwing weapon falls back to One Handed in `GetMeleeSkill`. |
| Athletics | Fallback skill when no weapon is equipped. Also used by movement/stat code elsewhere. | Not the normal combat brain for an armed troop, but still important for foot movement and fallback cases. |
| Riding | Not used by `SetAiRelatedProperties` as a melee or ranged AI skill. Used by mounted stat and mount-handling code elsewhere. | `Nimble Steed` improves Riding for mounted troops, but that is not the same as improving their block/shoot AI level. |

## Direct Weapon Effects

The direct skill effects are linear:

```text
effect value = base value + bonus per skill point * effective skill
```

The relevant combat effects use `AddFactor`, so `0.0007` means `+0.07%` per skill point. The normal combat-skill effects do not hit a practical cap in normal troop ranges.

| Skill | Direct effects checked | Per skill point | +30 skill | +80 skill |
| --- | --- | --- | --- | --- |
| One Handed | Weapon speed, weapon damage | +0.07% speed, +0.15% damage | +2.1% speed, +4.5% damage | +5.6% speed, +12.0% damage |
| Two Handed | Weapon speed, weapon damage | +0.06% speed, +0.16% damage | +1.8% speed, +4.8% damage | +4.8% speed, +12.8% damage |
| Polearm | Weapon speed, weapon damage | +0.06% speed, +0.07% damage | +1.8% speed, +2.1% damage | +4.8% speed, +5.6% damage |
| Bow | Damage, accuracy | +0.11% damage, +0.09% accuracy effect | +3.3% damage, +2.7% accuracy effect | +8.8% damage, +7.2% accuracy effect |
| Crossbow | Reload speed, accuracy | +0.07% reload, +0.05% accuracy effect | +2.1% reload, +1.5% accuracy effect | +5.6% reload, +4.0% accuracy effect |
| Throwing | Ready speed, damage, accuracy | +0.07% ready speed, +0.06% damage, +0.06% accuracy effect | +2.1% speed, +1.8% damage, +1.8% accuracy effect | +5.6% speed, +4.8% damage, +4.8% accuracy effect |

The accuracy effects are stored as negative factors in the code because they reduce inaccuracy or penalty. The UI presents them as positive accuracy.

For one-handed, two-handed, and polearm weapons, the skill speed effect is applied to both swing speed and thrust or ready speed. Crossbow skill affects crossbow reload speed. Throwing skill affects throwing ready speed.

## Ranged AI

Ranged behavior uses `currentAI`, so the relevant skill is Bow, Crossbow, or Throwing while that weapon is equipped.

| Driven property | Formula shape | Meaning |
| --- | --- | --- |
| `AiShootFreq` | `0.3 + 0.7 * currentAI` | Higher skill shoots more frequently. |
| `AiWaitBeforeShootFactor` | `1 - 0.5 * currentAI`, unless reset by a modifier | Higher skill waits less before shooting. |
| `AiRangedHorsebackMissileRange` | `0.3 + 0.4 * currentAI` | Higher skill improves mounted ranged missile range behavior. |
| `AiRangerLeadErrorMin` | `-(1 - currentAI) * 0.35` | Aim lead error shrinks as skill rises. |
| `AiRangerLeadErrorMax` | `(1 - currentAI) * 0.2` | Aim lead error shrinks as skill rises. |
| `AiRangerVerticalErrorMultiplier` | `(1 - currentAI) * 0.1` | Vertical aim error shrinks as skill rises. |
| `AiRangerHorizontalErrorMultiplier` | `(1 - currentAI) * 0.034906585` | Horizontal aim error shrinks as skill rises. |

Ranged skill therefore improves both volume and quality of fire. The direct stat table above covers the separate damage, accuracy, reload, and ready-speed effects.

## Melee AI

Melee behavior uses `meleeAI`, which is usually the current melee weapon skill, with the fallback rules listed above.

| Driven property | Formula shape | Practical meaning |
| --- | --- | --- |
| `AIBlockOnDecideAbility` | `lerp(0.5, 0.99, sqrt(meleeAI))` | Big early gain, then diminishing returns. Weak troops become less helpless quickly. |
| `AIParryOnDecideAbility` | `lerp(0.5, 0.95, meleeAI)` | Linear parry-decision improvement. |
| `AIParryOnAttackAbility` | `clamp(meleeAI, 0, 1)` | Linear ability to parry during attack situations. |
| `AIParryOnAttackingContinueAbility` | `lerp(0.5, 0.95, meleeAI)` | Linear improvement while continuing an attack. |
| `AIDecideOnRealizeEnemyBlockingAttackAbility` | `clamp(meleeAI^2.5 - 0.1, 0, 1)` | High-skill weighted. Low troops get almost nothing; elites gain a lot. |
| `AIRealizeBlockingFromIncorrectSideAbility` | `clamp(meleeAI^2.5 - 0.01, 0, 1)` | High-skill weighted block-side correction. |
| `AiRandomizedDefendDirectionChance` | `1 - meleeAI^3` | High skill sharply reduces random defense-direction mistakes. |
| `AISetNoAttackTimerAfterBeingHitAbility` | `lerp(0.33, 1, meleeAI)` | Linear recovery/timing improvement after being hit. |
| `AISetNoAttackTimerAfterBeingParriedAbility` | `lerp(0.2, 1, meleeAI^2)` | High-skill weighted recovery after being parried. |
| `AISetNoDefendTimerAfterHittingAbility` | `lerp(0.1, 0.99, meleeAI^2)` | High-skill weighted follow-up behavior after hitting. |
| `AISetNoDefendTimerAfterParryingAbility` | `lerp(0.15, 1, meleeAI^2)` | High-skill weighted follow-up behavior after parrying. |
| `AIHoldingReadyMaxDuration` | `lerp(0.25, 0, min(1, meleeAI * 2))` | Reaches the low end by about `0.5` AI level. |
| `AiKick` | `-0.1 + min(meleeAI, 0.4)` | Improves early and then caps. |
| `AiTryChamberAttackOnDecide` | `(meleeAI - 0.15) * 0.1` | Skill-gated tendency; exact native handling of low negative values is not confirmed. |

The important pattern is not one simple curve. Some behavior is linear, some has diminishing returns, and some is heavily weighted toward elite troops.

## Example: +80 Skill

So the answer to "does +80 skill do the same thing to a peasant and an elite troop?" is mixed:

- Direct weapon stats: yes. +80 Polearm is +4.8% polearm speed and +5.6% polearm damage whether the troop started at 20 or 130.
- Base AI level: yes, until capped. +80 skill is the same AI-level increase before the follow-up curves.
- Specific AI behaviors: no. Some behaviors reward low troops more, while others only really wake up at high skill.

For a concrete Polearm example, an Imperial Recruit has Polearm 20, a Menavliaton has Polearm 100, and an Elite Menavliaton has Polearm 130 in the checked local data.

| Example | AI level | Block-on-decide | Realize blocking attack |
| --- | --- | --- | --- |
| Recruit, Polearm 20 | 0.064 | 0.624 | 0.000 |
| Recruit with +80 Polearm, 100 | 0.320 | 0.777 | 0.000 |
| Elite Menavliaton, Polearm 130 | 0.416 | 0.816 | 0.012 |
| Elite Menavliaton with +80 Polearm, 210 | 0.672 | 0.902 | 0.270 |

That is the wrinkle: the recruit gets a larger improvement in the square-root blocking example, but the elite troop gets a much larger improvement in the high-skill "realize blocking attack" behavior.

## Shield And Defensive AI

Shield behavior also uses `meleeAI`, plus the agent's `Defensiveness` value.

| Driven property | Formula shape | Practical meaning |
| --- | --- | --- |
| `AiUseShieldAgainstEnemyMissileProbability` | `0.1 + 0.6 * meleeAI + 0.2 * (meleeAI + defensiveness)` | Higher melee skill and defensiveness make shield use against missiles more likely. |
| `AiDefendWithShieldDecisionChanceValue` | `min(2, 0.5 + meleeAI + 0.6 * (meleeAI + defensiveness))` | Higher melee skill and defensiveness improve shield defense decisions. |
| `AiRaiseShieldDelayTimeBase` | `-0.75 + 0.5 * meleeAI` | Skill changes shield timing. The exact native interpretation of this timing value needs engine-side confirmation. |
| `AiParryDecisionChangeValue` | `0.05 + 0.7 * meleeAI` | Higher skill changes parry decision behavior more strongly. |

This is one reason melee skill buffs can be defensive perks in practice, even when the tooltip only says "+skill."

## Skill Bonus Perks That Feed AI

Because these perks add to effective skill, they feed the AI formulas above when they affect the skill the troop is actually using.

| Skill affected | Perk | Role | Bonus | Scope |
| --- | --- | --- | ---: | --- |
| One Handed | `Wrapped Handles` | Captain | +30 | One-handed infantry troops in formation. |
| Two Handed | `Strong Grip` | Captain | +30 | Foot two-handed troops in formation. |
| Polearm | `Clean Thrust` | Captain | +30 | Foot polearm users in formation. |
| Polearm | `Counterweight` | Captain | +20 | Polearm users in formation. |
| Melee weapon skills | `Phalanx` | Party leader | +30 | Troops in the party while in shield wall formation. Applies through the effective-skill path for One Handed, Two Handed, and Polearm. |
| Bow | `Dead Aim` | Captain | +20 | Bow users in formation. |
| Bow | `Horse Master` | Captain | +30 | Mounted bow users in formation. |
| Crossbow | `Donkey's Swiftness` | Captain | +30 | Crossbow users in formation. |
| Throwing | `Strong Arms` | Captain | +20 | Throwing-weapon users in formation. |
| Throwing | `Running Throw` | Captain | +30 | Throwing-weapon users in formation. |
| Control or Vigor skills | `Flexible Fighter` | Captain | +15 | Control skills of infantry and Vigor skills of archers in formation. This is a category-sensitive perk, not a simple global weapon-skill buff. |
| Vigor and Control skills | `One of the Family` | Party leader | +10 | Bandit units in the party, when the party leader has the perk and the party is not at sea. |
| Riding | `Nimble Steed` | Captain | +30 | Mounted troops in formation. Useful for mounted stat handling, but not a direct `SetAiRelatedProperties` combat-AI boost. |

Normal/high difficulty AI-level gains from these bonuses:

| Skill bonus | AI-level gain |
| ---: | ---: |
| +10 | +0.032 |
| +15 | +0.048 |
| +20 | +0.064 |
| +30 | +0.096 |
| +50 | +0.160 |
| +60 | +0.192 |
| +65 | +0.208 |
| +80 | +0.256 |

## Polearm Level 75

The level 75 Polearm captain choice is more interesting than the perk text makes it look.

| Perk | Captain effect | Who gets it | Notes |
| --- | --- | --- | --- |
| `Clean Thrust` | +30 Polearm skill | Foot polearm users in the formation | Gives about +1.8% polearm speed, +2.1% polearm damage, and a small AI-level increase. |
| `Swift Swing` | +2% swing speed | Foot melee troops in the formation | Broader, but only affects swing speed and does not improve Polearm damage or AI. |

For a polearm-heavy infantry formation, `Clean Thrust` is likely the stronger captain effect. It is not just "less than 2% swing speed"; it is also damage, thrust/ready speed, and AI level. For mixed melee infantry, `Swift Swing` can still win on coverage because it applies to all foot melee troops, not only polearm users.

## High-Value AI Stacks

These are the obvious build directions for a future "maximize troop AI" list.

| Troop plan | Skill stack | Why it matters |
| --- | ---: | --- |
| Foot polearm shield wall | +80 Polearm from `Clean Thrust`, `Counterweight`, and `Phalanx` | The strongest clean melee-AI stack found so far. Also adds direct polearm speed and damage. |
| Foot one-handed shield wall | +60 One Handed from `Wrapped Handles` and `Phalanx` | Strong for shield infantry because it feeds melee reactions and shield AI. |
| Foot two-handed shield wall | +60 Two Handed from `Strong Grip` and `Phalanx` | Strong offensive melee AI stack, but without shield-specific defensive payoff. |
| Horse archers | +50 Bow from `Dead Aim` and `Horse Master` | Improves fire frequency, wait time, ranged errors, and bow direct damage/accuracy. |
| Throwing infantry | +65 Throwing from `Flexible Fighter`, `Strong Arms`, and `Running Throw` | Very strong for javelin-heavy infantry because it improves the ranged AI track and throwing direct stats. |
| Bandit weapon troops | Add `One of the Family` to any Vigor or Control weapon stack | +10 looks small, but it feeds every relevant weapon AI curve for qualifying bandit units. |

`Phalanx` is the sleeper here. It is not just a polearm damage perk pair; the party-leader side adds +30 melee weapon skills in shield wall, which can stack with captain skill bonuses and improve the melee AI values for an entire shield-wall formation.

## Practical Takeaways

- Skill bonuses are combat-brain bonuses when they affect the skill currently driving `meleeAI` or `currentAI`.
- Direct stat gains are linear, but AI behavior gains are mixed. Low troops can gain a lot from the square-root block curve, while elite troops gain more from high-skill curves such as `AI^2.5`.
- One Handed is quietly important for ranged troops because non-melee equipped weapons fall back to One Handed for melee AI.
- Polearm infantry in shield wall can stack a very large AI boost, which makes `Clean Thrust`, `Counterweight`, and `Phalanx` look much stronger together than each tooltip does alone.
- Riding matters for mounted fighting stats, but the checked combat-AI behavior method does not use Riding as the block/shoot decision skill.

## Sources Checked

- `AgentStatCalculateModel.SetAiRelatedProperties`
- `AgentStatCalculateModel.CalculateAILevel`
- `AgentStatCalculateModel.GetMeleeSkill`
- `AgentStatCalculateModel.GetEffectiveSkillForWeapon`
- `SandboxAgentStatCalculateModel.GetEffectiveSkill`
- `SkillEffect.GetSkillEffectValue`
- `SkillHelper.AddSkillBonusForSkillLevel`
- `SandboxAgentStatCalculateModel.SetWeaponSkillEffectsOnAgent`
- `SandboxAgentStatCalculateModel.GetWeaponDamageMultiplier`
- `spnpccharacters.xml` and `sandboxcore_skill_sets.xml` for example troop values
- `Data/generated/postprocessed-perk-effects.json`
