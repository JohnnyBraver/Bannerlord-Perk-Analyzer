# Smithing Mechanics

This note collects the smithing-specific findings from local assembly extraction.
It is meant as the readable companion to the generated XP reports.

## Main Takeaways

- Smithing skill XP is value-based. The formulas use the actual item value or output material value, not the displayed weapon design difficulty directly.
- Part unlock research is also value-based, but it is a separate track from skill XP.
- Curious Smelter helps only the smelting part-research gain. Curious Smith helps only the smithing part-research gain.
- These curiosity perks do not double smithing skill XP; they affect new-part learning.
- Efficient Charcoal Maker is a very strong early Smithing skill XP perk because refining XP is paid from gross output value and output count.
- For part unlocks, crafting a high-value weapon and then smelting it is usually better than only buying expensive weapons to smelt, if the player can afford the materials and stamina.
- Buying expensive weapons to smelt is still valid as a cash-for-unlocks shortcut, especially when the player cannot yet craft valuable items in the desired weapon template.
- Part research is attached to the crafted or smelted weapon template, so target the weapon class whose parts you actually want.
- Crafting above current smithing skill is not directly bad for XP. It is bad only if the resulting item comes out lower quality/lower value, if it wastes scarce materials/stamina, or if it fails a crafting order target.

## Skill XP

Sources:

- `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForRefining`
- `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForSmelting`
- `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForSmithingInFreeBuildMode`
- `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForSmithingInCraftingOrderMode`
- `TaleWorlds.CampaignSystem.CraftingSystem.CraftingOrder.GetOrderExperience`

Extracted formulas:

```text
refiningXp = round(0.3 * outputMaterialValue * outputCount)
smeltingXp = round(0.02 * itemValue)
smithingFreeBuildXp = round(0.02 * itemValue)
smithingCraftingOrderXp = round(0.1 * itemValue)
craftingOrderBaseExperience = 0.25 * theoreticalMaxItemMarketValue(requestedDesignItem)
```

Crafting orders can also halve the order base experience and apply a clamped tier-difference factor. Treat orders as their own optimization problem: a valuable free-build craft is not the same thing as a good order submission.

Refining was found as a smithing skill XP source, but no refining part-research path was found in this trace.

### Efficient Charcoal Maker

Efficient Charcoal Maker changes charcoal production to produce three units of charcoal from two units of hardwood. Since the refining XP formula uses output material value and output count, the perk directly improves the XP yield of the charcoal recipe:

```text
charcoalRefiningXpWithPerk = round(0.3 * charcoalValue * 3)
```

The input hardwood value is not subtracted from the XP formula. This makes charcoal refining unusually good early Smithing skill XP: it is cheap, repeatable, and helps push the character toward higher Smithing levels before serious weapon crafting starts.

Important distinction: this is Smithing skill XP, not part research. Refining charcoal can help the hero get enough skill and perks to craft better weapons, but it does not appear to unlock weapon parts by itself.

## Part Research

Sources:

- `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetPartResearchGainForSmeltingItem`
- `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetPartResearchGainForSmithingItem`
- `TaleWorlds.CampaignSystem.CampaignBehaviors.CraftingCampaignBehavior.AddResearchPoints`
- `TaleWorlds.CampaignSystem.CampaignBehaviors.CraftingCampaignBehavior.OpenNewPart`
- `TaleWorlds.CampaignSystem.CampaignBehaviors.CraftingCampaignBehavior.ResearchPointsNeedForNewPart`

Extracted formulas:

```text
smeltingPartResearchBase = 1 + round(0.02 * itemValue)
smeltingPartResearch = int(smeltingPartResearchBase * smeltingPerkMultiplier)

smithingPartResearch = 1 + floor(0.1 * itemValue * smithingMultiplier)
researchNeededForNextPart = sqrt(100 / totalPartsInTemplate) * (9 * openedPartsInTemplate + 10)
```

Observed perk and mode effects:

- Curious Smelter adds +100% part learning rate from smelting, so the smelting research gain is effectively doubled.
- Curious Smith adds +100% part learning rate from smithing, so the smithing research gain is effectively doubled.
- Free-build smithing adds a smaller extra smithing-research factor; from the extraction notes this was +10%, so without Curious Smith free-build research is roughly `1 + floor(0.11 * itemValue)`.
- `AddResearchPoints` applies research to the weapon template pool and can open more than one part if the gain crosses multiple thresholds.
- `OpenNewPart` chooses a random unopened, non-hidden part from the lowest available locked tier in that weapon template.
- Default-given parts count as opened parts for the next-part research threshold.

Practical example with an `itemValue` of `10000`:

```text
smelt with Curious Smelter: 2 * (1 + round(0.02 * 10000)) = 402 research
free-build craft without Curious Smith: about 1 + floor(0.11 * 10000) = 1101 research
craft then smelt with Curious Smelter: about 1503 total research
```

The exact craft-side number can vary with the mode/perk multiplier, but the pattern is clear: high-value crafting is the main research engine, and Curious Smelter makes the smelt-after-craft loop much better.

Important perk note: Curious Smelter doubles the smelting research chunk, not the skill XP from smelting. Curious Smith does the same for smithing research, not free-build skill XP.

## Design Difficulty And Stamina

Sources:

- `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.CalculateWeaponDesignDifficulty`
- `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetEnergyCostForSmithing`

Design difficulty is a weighted average of the selected part difficulties. The extracted weights are:

| Piece type | Weight |
| --- | ---: |
| 0 | 100 |
| 1 | 20 |
| 2 | 60 |
| 3 | 20 |

The method returns the rounded weighted average. This difficulty is not itself an XP multiplier in the skill XP or part research formulas above. Keep the numeric piece types until the enum is documented in the repo; the extraction was from IL, not friendly source names.

Smithing energy cost is:

```text
smithingEnergyCost = 10 + 5 * itemTier
```

The Practical Smith perk can apply a factor to that energy cost.

## Crafted Weapon Value

Sources:

- `TaleWorlds.Core.ItemObject.DetermineValue`
- `TaleWorlds.Core.DefaultItemValueModel.CalculateValue`
- `TaleWorlds.Core.DefaultItemValueModel.GetEquipmentValueFromTier`
- `TaleWorlds.Core.DefaultItemValueModel.CalculateWeaponTier`
- `TaleWorlds.Core.DefaultItemValueModel.CalculateTierMeleeWeapon`
- `TaleWorlds.Core.DefaultItemValueModel.CalculateTierCraftedWeapon`
- `TaleWorlds.Core.DefaultItemValueModel.GetFactor`

The value path is exponential in the computed item tier:

```text
equipmentValueFromTier = 2.75 ^ clamp(itemTierf, -1, 7.5)
weaponValue = int(100 * equipmentValueFromTier * (1 + 0.2 * (appearance - 1)) + 100 * max(0, appearance - 1))
```

For crafted melee weapons, the weapon tier combines final combat stats and the design/material tier:

```text
craftedWeaponTier = 0.6 * meleeStatTier + 0.4 * designMaterialTier
```

The design/material tier is built from average piece tier and material quality. In simplified terms, higher-tier pieces and better materials matter even before the final weapon stats are considered.

For each melee weapon mode, the stat tier is driven by attack power and reach:

```text
thrustScore = thrustDamage * damageTypeFactor * (thrustSpeed / 100)^1.5
swingScore = swingDamage * damageTypeFactor * (swingSpeed / 100)^1.5
attackScore = max(thrustScore, 1.1 * swingScore)
modeTier = 0.06 * attackScore * (1 + weaponLength / 100) - 3.5
```

Damage type factors:

| Damage type | Factor |
| --- | ---: |
| Cut | 1.00 |
| Pierce | 1.15 |
| Blunt | 1.45 |

Other observed melee valuation adjustments:

- Weapons not usable with one hand apply a `0.8` attack-score factor for that mode.
- Throwing axes and throwing knives apply a `1.2` factor.
- Javelins apply a `0.6` factor.
- Weapons with multiple melee modes get a small bonus from the second-best mode.
- The tier calculation is clamped, so extremely optimized weapons can eventually stop gaining full value from more stats.

Important absence: handling was not found in the crafted weapon value formula. Handling matters for how good the weapon feels in combat, but it does not appear to raise sale value, free-build Smithing XP, or part research directly.

## Skill Gap Interpretation

No separate "under-skilled craft gives less XP" branch was found in the extracted XP or part research methods. The important input is the final item value.

Crafted item generation flows through `Crafting.GenerateItem`, `CraftedItemGenerationHelper.GenerateCraftedItem`, and then item value determination. That means the value after generation is the number to watch in-game.

That means an over-difficulty craft is inefficient only through its consequences:

- The generated item can be lower quality or lower value.
- The same stamina/materials might produce a better actual value in an easier design.
- Crafting orders can punish mismatches separately from free-build value grinding.

So the useful rule is: craft the highest actual-value item you can reliably produce, not simply the highest difficulty item shown in the crafting screen.

## Crafting Tips

For Smithing XP, part research, and sale value, optimize for the displayed crafted item value.

- Damage is a major value driver, but it is multiplied by speed. A slower weapon with slightly higher damage can be worse than a faster weapon with a bit less damage.
- Reach is valuable because it multiplies the attack score, but only after damage and speed are already set. Long reach is good when it does not badly crater speed or damage.
- Swing damage is favored slightly by the formula because swing score gets a `1.1` multiplier before being compared with thrust score.
- Pierce and blunt damage are valued above cut damage. This does not automatically mean they are always better in real combat, only that the item value model rates them higher.
- Handling does not seem to help item value. For grinding, do not sacrifice damage, speed, reach, or material tier just to improve handling.
- For a weapon the player will actually use, handling still matters. The value formula is not the same as practical combat feel.
- High-tier parts and better materials matter because 40% of crafted weapon tier comes from design/material tier.
- Multi-mode weapons can get a small value bump from the second-best attack mode, but the best mode still dominates.
- If two recipes are close, craft one of each and compare displayed item value. That final value already includes stat output, material/design tier, and generated quality/appearance effects.

## Current Optimization Notes

For a player with Curious Smelter:

- Efficient Charcoal Maker is an excellent early pick if the immediate goal is raising Smithing skill. It turns hardwood into repeatable, high-efficiency refining XP and helps reach the skill/perk range where crafted weapon value starts improving.
- If the goal is part unlocks, craft valuable weapons in the template whose parts you want, then smelt them.
- If materials are cheap and stamina is the bottleneck, compare actual item value per stamina spent.
- If money is abundant and skill/materials are the bottleneck, buy expensive weapons in the target template and smelt them.
- If a too-hard design rolls poor output value, step down to the easier design that produces the better actual value.

Open question for a later extraction pass: trace the exact item modifier/appearance selection path for crafted weapons, especially where hero skill versus design difficulty is translated into final item quality before value is calculated.
