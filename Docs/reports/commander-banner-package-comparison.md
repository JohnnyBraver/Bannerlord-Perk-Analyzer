# Commander Banner Package Comparison

Generated: 2026-06-05T15:19:54.709962+03:00

This report scores full commander-relevant perk alternative sets around each major banner option. It is a package model over extracted perk rows, not a battle simulator.

Banner mechanics are confirmed in the generated [banner effects reference](banner-effects.md); use that as the source of truth for what each banner modifies before interpreting these package totals.

## Inputs

- Commander JSON: `Data\intermediate\commander_perks_extracted.json`
- perk_export: `Data\export\perk-effects.json`
- banner_items: `Data\raw\banner-items.json`

## Package Totals

| Package | Banner | Infantry movement | Melee damage | Ranged damage taken | Weapon inaccuracy | Accuracy penalty | HP | Shield damage | Differing picks vs speed |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Shock Speed | Increased Troop Movement Speed T3 (30%) - Banner of Dust Devils, Strider's Flag | 63% | 122% | 13% |  | 5% | 10 | 58% | 0 |
| Anti-Arrow Durability | Decreased Taken Ranged Attack Damage T3 (-15%) - Locked Shields Banner, Testudo Standard | 25% | 95% | 37% |  | 5% | 28 | 68% | 8 |
| Archer Accuracy | Decreased Ranged Accuracy Penalty T3 (-8%) - Banner of Sultan's Eagle, Tug of Whistling Arrow | 13% | 72% | 12% | 8% | 100% | 33 |  | 26 |
| Melee Damage | Increased Melee Damage T3 (15%) - Standard of Wrath | 30% | 139% | 13% |  | 5% | 10 | 58% | 1 |

## Delta vs Shock Speed

| Package | Infantry movement | Melee damage | Ranged damage taken | Weapon inaccuracy | Accuracy penalty | HP | Shield damage | Read |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Anti-Arrow Durability | -38% | -27% | +24% |  |  | +18 | +10% | Trades speed and some damage for a much larger ranged-damage, HP, and shield package. |
| Archer Accuracy | -50% | -50% | -1% | +8% | +95% | +23 | -58% | Real but specialized: adds base inaccuracy reduction and ranged accuracy perks, while giving up most shock-infantry priorities. |
| Melee Damage | -33% | +17% |  |  |  |  |  | Mostly the same perk package as shock speed, but swaps about 33% infantry movement for 17% melee damage. |

## Accuracy Banner Mechanics

- Effect: `DecreasedRangedAccuracyPenalty`
- Applied in: `SandBox.GameComponents.SandboxAgentStatCalculateModel.SetPerkAndBannerEffectsOnAgent`
- Applied to: `AgentDrivenProperties.WeaponInaccuracy`
- Mechanical read: The banner bonus is added to the WeaponInaccuracy ExplainedNumber and then written back with set_WeaponInaccuracy. Tier 3 is -8%, so it should multiply the base inaccuracy/spread component by about 0.92.
- Practical read: Helpful when raw spread is the limiting factor for many ranged troops firing often, but weaker than it looks if misses are mostly movement, rotation, target motion, range, projectile travel, line of sight, or AI timing.
- Not applied to: `WeaponMaxMovementAccuracyPenalty`, `WeaponMaxUnsteadyAccuracyPenalty`, `WeaponRotationalAccuracyPenaltyInRadians`, `direct hit chance`

That makes the tier 3 accuracy banner real, but narrow: it reduces base weapon inaccuracy/spread by 8%. It does not directly grant 8% hit chance, and it does not reduce the movement, unsteady, or rotational penalty properties that several personal/captain perks touch.

## Pick Differences vs Shock Speed

Only choices that differ from the shock-speed package are shown here. The full selected side for every commander-relevant alternative pair is in the JSON output.

### Anti-Arrow Durability

Infantry that expects to trade under ranged fire before contact.

| Package pick | Shock-speed pick | Why the package flips it |
| --- | --- | --- |
| One Handed 25 - Basher | One Handed 25 - Wrapped Handles | -30 melee skill; +4% ranged damage reduction |
| Polearm 100 - Hard Knock | Polearm 100 - Footwork | -2% infantry movement; +3 HP |
| Throwing 100 - Running Throw | Throwing 100 - Knock Off | -5% melee damage; +30 melee skill |
| One Handed 200 - Steel Core Shields | One Handed 200 - Fleet of Foot | -4% infantry movement; +10% shield damage reduction |
| Tactics 200 - Elite Reserves | Tactics 200 - Encirclement | -5% melee damage; +5% ranged damage reduction |
| Two Handed 200 - Thick Hides | Two Handed 200 - Reckless Charge | -2% infantry movement; -2% melee damage; +5 HP |
| Engineering 225 - Metallurgy | Engineering 225 - Improved Tools | -5% melee damage; +5 armor |
| One Handed 225 - Unwavering Defense | One Handed 225 - Deadly Purpose | -10% melee damage; +10 HP |

### Archer Accuracy

Ranged-heavy formation where hit rate is the bottleneck.

| Package pick | Shock-speed pick | Why the package flips it |
| --- | --- | --- |
| Athletics 25 - Well Built | Athletics 25 - Morning Exercise | -5% infantry movement; +5 HP |
| One Handed 25 - Basher | One Handed 25 - Wrapped Handles | -30 melee skill; +4% ranged damage reduction |
| Polearm 25 - Cavalry | Polearm 25 - Pikeman | -2% melee damage |
| Riding 25 - Full Speed | Riding 25 - Nimble Steed | -30 melee skill |
| Throwing 25 - Quick Draw | Throwing 25 - Shield Breaker | -8% shield damage reduction |
| Crossbow 75 - Sheriff | Crossbow 75 - Donkey's Swiftness | +10% ranged damage; -30 ranged skill |
| One Handed 75 - Cavalry | One Handed 75 - Shield Bearer | -3% infantry movement |
| Tactics 75 - Horde Leader | Tactics 75 - Small Unit Tactics | -5% infantry movement; +9 party size |
| Athletics 100 - Powerful | Athletics 100 - Sprint | -3% infantry movement; +2% melee damage |
| Bow 100 - Mounted Archery | Bow 100 - Merry Men | +30% accuracy penalty reduction; -5 party size |
| Polearm 100 - Hard Knock | Polearm 100 - Footwork | -2% infantry movement; +3 HP |
| Riding 100 - Sagittarius | Riding 100 - Sweeping Wind | +15% accuracy penalty reduction |
| Tactics 100 - Coaching | Tactics 100 - Law Keeper | -3% melee damage |
| Crossbow 125 - Puncture | Crossbow 125 - Fletcher | +5% ranged armor penetration |
| Crossbow 150 - Loose and Move | Crossbow 150 - Deft Hands | +5% ranged movement |
| Bow 175 - Eagle Eye | Bow 175 - Skirmish Phase Master | -10% ranged damage reduction |
| Crossbow 200 - Steady | Crossbow 200 - Long Shots | +50% accuracy penalty reduction |
| Tactics 200 - Elite Reserves | Tactics 200 - Encirclement | -5% melee damage; +5% ranged damage reduction |
| Throwing 200 - Resourceful | Throwing 200 - Splinters | -50% shield damage reduction |
| Two Handed 200 - Thick Hides | Two Handed 200 - Reckless Charge | -2% infantry movement; -2% melee damage; +5 HP |
| Bow 225 - Horse Master | Bow 225 - Deep Quivers | +30 ranged skill |
| One Handed 225 - Unwavering Defense | One Handed 225 - Deadly Purpose | -10% melee damage; +10 HP |
| Two Handed 225 - Blade Master | Two Handed 225 - Vandal | -20% melee damage |
| Polearm 250 - Counterweight | Polearm 250 - Sharpen the Tip | -5% melee damage; +20 melee skill |
| Riding 250 - Dauntless Steed | Riding 250 - Tough Steed | -5 armor |
| Scouting 250 - Rearguard | Scouting 250 - Vanguard | -5% melee damage |

### Melee Damage

Shock infantry damage breakpoints and fast cleanup.

| Package pick | Shock-speed pick | Why the package flips it |
| --- | --- | --- |
| Athletics 100 - Powerful | Athletics 100 - Sprint | -3% infantry movement; +2% melee damage |

## Assumptions

- This is a deterministic scoring model over extracted commander-relevant perk alternatives, not a battle simulator.
- The full chosen perk set is stored in JSON. The markdown focuses on package totals and choices that differ from the shock-speed package.
- Banner bonuses are added as package metrics: infantry speed, ranged damage reduction, weapon inaccuracy reduction, or melee damage.
- The archer accuracy banner applies to WeaponInaccuracy, so the model treats it as base inaccuracy reduction rather than direct hit chance.
- Non-alternative perks common to every package are not re-listed in the markdown comparison.

