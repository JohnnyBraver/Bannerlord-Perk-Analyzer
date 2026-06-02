# Settlement Supply Chain

This note covers the settlement market loop: village production, villager delivery, hidden town artisans, workshops, town demand, consumption, and price pressure. Read it with `settlement-economy.md` for taxes and governor perks, `settlement-workshops.md` for workshop ownership, and `trade-economy.md` for shop spread and Trade skill.

## Main Takeaways

- Towns do have native production outside the three visible player workshops. Every town gets a hidden `artisans` workshop slot that produces everyday goods and equipment into the town market.
- Villages are not just map labels. They accumulate goods in their own item roster, then villager parties physically carry goods to the bound town and sell them into the town roster.
- Demand is mostly prosperity-driven. Larger towns have higher category demand, and towns above `3000` prosperity add luxury demand on top.
- Yes, the same item can be more expensive to buy from and more profitable to sell to a large town, because both buy and sell use the same market factor before the trade penalty spread is applied.
- The caveat is stock. Market price also depends on category supply and stored value, so a large town with heavy inventory can be cheaper than a smaller town with a real shortage.
- War, raids, dead villagers, disrupted caravans, and bad workshop input supply all matter because the economy is inventory-based, not only abstract price math.

## Supply Sources

Town market stock comes from several different paths:

| Source | How it enters the market | Practical read |
| --- | --- | --- |
| Hidden artisans | The hidden `artisans` workshop consumes town inputs and produces outputs into the town item roster. | Native town production exists even when the player sees only three workshops. |
| Visible workshops | Normal workshops consume inputs from town market or warehouse and produce outputs to town market or player warehouse. | Workshop profit depends on both input availability and output demand. |
| Villages | Village goods accumulate locally, then villager parties load them and sell them into the trade-bound town. | Protecting villager parties protects town supply. |
| Caravans and parties | Trade parties buy and sell goods through town markets. | Long routes can smooth shortages; war and bandits can create them. |
| Player trades | Player buying and selling changes the same item roster used by the market model. | Bulk trades can move prices, especially for trade goods. |

## Native Town Production

The installed `spworkshops.xml` defines a hidden workshop type:

```text
id = artisans
isHidden = true
frequency = 0
description = every town has craftsmen making everyday stuff
```

This is the missing "native production" layer. Existing workshop extraction also shows towns have `4` internal workshop slots, with slot `0` initialized as `artisans`; the normal visible slots are the three player-facing workshops.

The artisan recipes are broad. They include:

| Artisan lane | Inputs | Outputs |
| --- | --- | --- |
| Butchery | cow, sheep, hog | meat, hides |
| Simple processing | grape, olives, iron | wine, oil, tools |
| Basic equipment | none or simple inputs | garments, light armor, arrows, low-tier weapons, shields, horse equipment |
| Better equipment | iron, hardwood, leather | higher-tier melee weapons, ranged weapons, shields, armor, horse equipment |

That means a town can generate ordinary equipment and processed goods even without a visible brewery, smithy, tannery, or similar workshop. It is not free from the market, though: many artisan recipes still need inputs from the town roster.

## Village Production

Village production is hearth-tiered:

| Village hearths | Hearth level | Goods multiplier | Food production units |
| ---: | ---: | ---: | ---: |
| `< 200` | `0` | `0.5x` | `1` |
| `200-599` | `1` | `1.0x` | `2` |
| `600+` | `2` | `1.5x` | `3` |

For a normal, non-deserted village, each listed village production item uses:

```text
dailyGoods = productionWeight * 0.5 * (hearthLevel + 1)
```

The result is rounded randomly, then added to the village item roster. Perks, culture feats, and buildings can modify the result. Relevant confirmed modifiers include `Granary Accountant`, `Tradeyard Foreman`, `Steady`, `Perfect Health`, `Breeder`, Khuzait animal production, Sturgian grain production, and Vlandian castle-village production.

Food production is separate:

```text
dailyFood = hearthLevel + 1
```

Food output is randomized among consumable raw foods with a weight of roughly `1 / itemValue`, so cheaper staple foods are naturally more common.

Villages have a production brake:

```text
warehouseCapacity = ceil(max(1, dailyFood + sum(dailyGoods)) * 5)
production pauses when storedGoods >= 1.5 * warehouseCapacity
```

This means a village can stockpile goods, but only up to a practical limit. If villagers cannot safely carry stock to town, production eventually slows or stops.

## Villager Delivery

The villager delivery loop is physical:

1. Village production adds goods to the village roster.
2. The villager behavior has a random send gate and checks whether stored goods have reached at least warehouse capacity.
3. The village creates or refills a villager party when hearths and party-size rules allow it.
4. `MoveItemsToVillagerParty` transfers goods from village roster to villager party inventory.
5. On town entry, `SellGoodsForTradeAction.ApplyByVillagerTrade` sells those goods into the town item roster.
6. The villager party's trade gold later becomes village tax when it returns home.

The loading step runs several passes. Each pass tries to move about `20%` of each village stack, limited by party capacity, and the code repeats this four times. In expectation, that can move a little over half of stored goods if the party has enough carrying room.

The sell step is explicit: the town item roster gains the sold equipment elements, the villager party loses them, town gold pays for them, and the party stores the trade gold. Villagers keep a reserve of cheap pack animals for carrying capacity rather than selling every pack animal.

Practical read: killing or blocking villagers does not merely hurt flavor traffic. It prevents village stock from becoming town stock, which can raise prices and starve workshops.

## Demand And Consumption

Daily category demand is based on town prosperity and each item category's base/luxury demand:

```text
basePopulation = max(0, prosperity + extraDemand)
luxuryPopulation = max(0, prosperity - 3000)

dailyDemand =
    categoryBaseDemand * basePopulation
  + categoryLuxuryDemand * luxuryPopulation
```

The market update uses `extraDemand = 1000`, so there is a baseline demand buffer beyond current prosperity. Luxury demand only starts once prosperity is above `3000`.

The market does not replace supply/demand instantly. It smooths them:

```text
supply = max(0.1, oldSupply * 0.85 + currentInStoreValue * 0.15)
demand = oldDemand * 0.85 + estimatedDemand * 0.15
```

So shortages and surpluses decay over time rather than disappearing after one delivery or one purchase.

Consumption removes items from the town roster. The behavior builds category budgets, adjusts a category's daily budget by:

```text
dailyBudgetForCategory = budget * priceIndex^0.3
```

Then it consumes up to:

```text
amountToConsume = min(stackAmount, dailyBudgetForCategory / localPrice)
```

The consumed goods are removed from the town roster and the town receives the matching gold transfer. This is why high-prosperity demand creates ongoing inventory pressure instead of only changing a hidden price number.

Some item categories can substitute for each other. The extracted category data includes examples like grain and fish substituting heavily with each other, meat partially substituting with fish, and oil partially substituting with butter. The demand-shift step can move demand toward substitute categories when relative supply/demand makes that sensible.

## Demand Constants

These are category demand constants from `DefaultItemCategories.InitializeAll`. They are not item counts; they feed the prosperity-based demand formula above.

| Category | Base demand | Luxury demand | Read |
| --- | ---: | ---: | --- |
| Grain | 140 | 0 | Huge basic staple demand. |
| Horse | 140 | 0 | Huge animal demand. |
| War horse | 120 | 20 | High base demand plus rich-town pressure. |
| Noble horse | 120 | 50 | Very rich towns should pull hard when supply is low. |
| Beer | 46 | 20 | Strong everyday processed-good demand. |
| Felt | 34 | 23 | High processed-material demand. |
| Meat | 30 | 50 | Big luxury-town food pressure. |
| Tools | 30 | 30 | Strong general demand and workshop relevance. |
| Arrows | 30 | 30 | Equipment demand, but non-trade-good price swings are clamped tighter. |
| Linen | 28 | 30 | Strong textile demand. |
| Oil | 26 | 30 | Strong processed-food demand. |
| Salt | 25 | 25 | Strong broad demand. |
| Planks | 25 | 15 | Good construction/material pressure. |
| Pottery | 22 | 20 | Solid processed-good demand. |
| Pack animal | 20 | 3 | Useful demand, but much less luxury pull than horses. |
| Hides | 17 | 10 | Animal-derived material demand. |
| Velvet | 15 | 32 | Rich-town luxury good. |
| Jewelry | 15 | 32 | Rich-town luxury good. |
| Wine | 15 | 30 | Rich-town processed luxury food/drink. |
| Fish | 15 | 15 | Staple substitute category. |
| Fur | 10 | 38 | Very luxury-sensitive. |
| Date fruit | 7 | 32 | More luxury-sensitive than its base demand suggests. |
| Grape / olives | 5 | 20 | Low base, meaningful rich-town demand. |

Equipment categories usually have smaller base demand and higher luxury demand as tier rises. That helps rich towns want better gear, but non-trade goods are price-factor clamped to a much narrower band than trade goods, so equipment does not arbitrage like grain, salt, tools, or velvet.

## Price Pressure

The market factor comes from category demand, category supply, and stored value:

```text
if selling:
    storeValue += transferValue

rawFactor = demand / (0.1 * supply + 0.04 * storeValue + 2)

marketFactor = rawFactor ^ 0.6       # normal categories
marketFactor = rawFactor ^ 0.3       # animals
```

Trade goods clamp to `0.1x` through `10.0x`. Non-trade goods clamp to `0.8x` through `1.3x`.

`trade-economy.md` covers the next layer, but the simple version is:

```text
buyPrice = itemValue * marketFactor * (1 + tradePenalty)
sellPrice = itemValue * marketFactor / (1 + tradePenalty)
```

So the same high market factor makes both buying expensive and selling profitable. That is the part behind the "larger town pays more" intuition.

The caveats:

- Selling into a market adds transfer value before pricing, so dumping a large stack worsens the factor during the sale.
- Existing town stock and stored value push the factor down.
- Large towns usually have more demand, but they can also have more supply from villages, artisans, workshops, caravans, and previous trades.
- Non-trade goods have narrow market-factor clamps, so gear prices are dominated more by trade penalty than by local demand.

## Practical Trading Read

Large prosperous towns are best buyers when the item category has high demand and low stock. Look for rich towns with disrupted villages, missing inputs, active consumption, or no recent caravan deliveries.

Good sell candidates for large towns:

| Lane | Why |
| --- | --- |
| Grain and staple food | Grain has extreme base demand, and food is constantly consumed. |
| Meat, wine, oil, date fruit, fur, jewelry, velvet | Luxury demand matters above `3000` prosperity. |
| Tools, salt, felt, linen, planks, pottery | Strong base/luxury demand and trade-good movement. |
| War horses and noble horses | High demand, animal exponent, and useful rich-town pull when supply is scarce. |

Good buy candidates are the opposite: towns or villages with abundant local production, recent deliveries, saturated workshop output, or low demand. A large town can still be a good place to buy something if its supply network is flooding that category.

For workshops, the clean heuristic is:

```text
profit wants cheap/reliable inputs + output demand that is not already saturated
```

For kingdom economy, the clean heuristic is:

```text
protect villages -> villagers deliver goods -> towns consume/sell/process goods -> prosperity turns into demand, taxes, and workshop activity
```

## Answer To The Large-Town Price Hunch

Mostly yes.

A larger, richer town has higher category demand because prosperity feeds demand directly, and high prosperity adds luxury demand. Since buy and sell both use the same market factor, a scarce item in a large town can be both expensive to buy there and a good item to sell there.

But it is not a universal "larger town always pays more" rule. The denominator includes category supply and stored value, and selling a stack increases store value for the transaction. A smaller town with a shortage can beat a larger town with full warehouses.

## Evidence

Primary local evidence:

- Local game XML `Modules/SandBox/ModuleData/spworkshops.xml`: hidden `artisans` workshop and recipes.
- `DefaultSettlementEconomyModel.GetDailyDemandForCategory`: prosperity and luxury demand formula.
- `DefaultSettlementEconomyModel.GetSupplyDemandForCategory`: `85%` old, `15%` new smoothing.
- `ItemConsumptionBehavior.MakeConsumption`: town consumption removes goods from the town roster.
- `DefaultTradeItemPriceFactorModel.GetBasePriceFactor`: demand/supply/store-value price factor.
- `DefaultItemCategories.InitializeAll`: base and luxury demand constants.
- `DefaultVillageProductionCalculatorModel.CalculateDailyProductionAmount`: hearth-tiered village output and production perk hooks.
- `VillageGoodProductionCampaignBehavior.TickProductions`: village production pause at `1.5 * warehouseCapacity`.
- `VillagerCampaignBehavior.MoveItemsToVillagerParty`: village stock physically loads into villager parties.
- `SellGoodsForTradeAction.ApplyInternal`: villager sales add goods to the town item roster.
