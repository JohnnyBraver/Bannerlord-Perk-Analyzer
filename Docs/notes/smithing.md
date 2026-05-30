# Smithing Mechanics

This note collects the smithing-specific findings from local assembly extraction.
It is meant as the readable companion to the generated XP reports.

## Main Takeaways

- Smithing skill XP is value-based. The formulas use the actual item value or output material value, not the displayed weapon design difficulty directly.
- Part unlock research is also value-based, but it is a separate track from skill XP.
- Curious Smelter helps only the smelting part-research gain. Curious Smith helps only the smithing part-research gain.
- These curiosity perks do not double smithing skill XP; they affect new-part learning.
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

## Skill Gap Interpretation

No separate "under-skilled craft gives less XP" branch was found in the extracted XP or part research methods. The important input is the final item value.

Crafted item generation flows through `Crafting.GenerateItem`, `CraftedItemGenerationHelper.GenerateCraftedItem`, and then item value determination. That means the value after generation is the number to watch in-game.

That means an over-difficulty craft is inefficient only through its consequences:

- The generated item can be lower quality or lower value.
- The same stamina/materials might produce a better actual value in an easier design.
- Crafting orders can punish mismatches separately from free-build value grinding.

So the useful rule is: craft the highest actual-value item you can reliably produce, not simply the highest difficulty item shown in the crafting screen.

## Current Optimization Notes

For a player with Curious Smelter:

- If the goal is part unlocks, craft valuable weapons in the template whose parts you want, then smelt them.
- If materials are cheap and stamina is the bottleneck, compare actual item value per stamina spent.
- If money is abundant and skill/materials are the bottleneck, buy expensive weapons in the target template and smelt them.
- If a too-hard design rolls poor output value, step down to the easier design that produces the better actual value.

Open question for a later extraction pass: trace the exact item modifier/quality selection path for crafted weapons, especially where hero skill versus design difficulty is translated into final item value.
