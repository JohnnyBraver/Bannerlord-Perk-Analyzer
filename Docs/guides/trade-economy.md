# Trade And Economy Guide

This note covers shop prices, trade penalty, Trade XP, and economy-facing perks. It focuses on what the extracted campaign models appear to do, because the in-game phrase "trade penalty" is easy to read as a direct price discount when it is really a spread modifier.

## Main Takeaways

- Trade penalty is not a direct percent change to final price. It is a penalty term that makes buying more expensive and selling less profitable.
- The Trade skill does not change an item's market supply/demand factor. It reduces the trade penalty after the market factor has already been calculated.
- Trade goods have much wider supply/demand movement than normal equipment. Non-trade goods are clamped into a narrow market-factor range, then selling penalties do most of the damage.
- "Price penalty while selling X" perks reduce the penalty for that lane. They do not mean the final sell price rises by that full percent.
- Positive trade profit gives Trade XP. Warehouse production also gives Trade XP to the main hero.
- Barter penalty, ransom broker deals, mercenary hiring costs, wages, and settlement income are separate economy systems. They should not be lumped into normal shop trade penalty.

## Price Layers

The shop price has two big layers:

```text
marketFactor = supply/demand price factor
tradePenalty = shop spread, skill reduction, and applicable perk factors

buyPrice = ceil(itemValue * marketFactor * (1 + tradePenalty))
sellPrice = floor(itemValue * marketFactor / (1 + tradePenalty))
```

So a `0.50` trade penalty means:

- Buying: `1.50x` the market-adjusted value.
- Selling: `1 / 1.50`, or about `66.7%` of the market-adjusted value.

That spread is why the same item can be painful to flip even when the market factor looks close to fair.

### Market Factor

The extracted `DefaultTradeItemPriceFactorModel.GetBasePriceFactor` starts from demand, supply, and store value:

```text
if selling:
    storeValue += item.Value

rawFactor = demand / (0.1 * supply + 0.04 * storeValue + 2)
marketFactor = rawFactor ^ exponent
```

The exponent is `0.3` for animals and `0.6` for other categories. Trade goods are clamped from `0.1` to `10.0`, while non-trade goods are clamped from `0.8` to `1.3`.

Practical read:

- Trade goods can have huge real arbitrage because their market factor can move from very low to very high.
- Equipment and most non-trade goods cannot swing as hard from supply/demand alone.
- Selling an item into a market slightly worsens the store-value side of the calculation for that transaction.

## Trade Penalty

The base trade penalty starts at `0.06`, then the game adds context penalties and applies Trade skill and perk factors.

The party leader's Trade skill applies through the `TradePenaltyReduction` skill effect:

```text
tradeSkillPenaltyFactor = 1 / (1 + 0.002 * partyLeaderTrade)
```

| Party leader Trade | Penalty remaining |
| ---: | ---: |
| 0 | 100.0% |
| 50 | 90.9% |
| 100 | 83.3% |
| 150 | 76.9% |
| 200 | 71.4% |
| 250 | 66.7% |
| 300 | 62.5% |
| 330 | 60.2% |

This is useful, but it is not magic. Even a very high Trade skill still leaves a large chunk of the penalty in place, especially when the item category has a big penalty before skill reduction.

### Penalty Sources

The extracted `GetTradePenalty` method includes these major sources:

| Source | Effect on penalty | Practical read |
| --- | ---: | --- |
| Baseline shop spread | `+0.06` | Present even on clean trades. |
| War with merchant faction | `+0.50` | Trading with enemies is deliberately bad. |
| Selling equipment to a non-caravan | `+1.5 + 0.25 * max(0, tier - 1)` | This is why loot sells for so little. Higher-tier gear is punished harder. |
| Selling player-crafted smithing weapons | Uses the equipment penalty, then `Artisan Smith` can reduce it | `Artisan Smith` is a serious crafted-weapon selling perk. |
| Selling mounts or pack animals to a non-caravan | `+0.8` for the matching horse component | Mount trade penalty perks matter only if this is a real lane for the run. |
| Village trades | Extra village-side penalty terms | Villages are not just small towns; the model treats them differently. |
| Caravan as the trading party | Penalty is halved | Caravans get better trade treatment than a normal party. |
| No client party | Penalty is multiplied by `0.2` | Mostly an internal/non-player case. |

The village branch is especially worth treating with caution. The IL shows village-specific additions and a special pack-animal buying path, so village animal trades can be much worse than the perk text alone suggests.

### What A Penalty Perk Really Does

Because penalty affects the spread, a `-20% trade penalty` perk reduces the penalty number, not the final price.

Assume `itemValue = 1000` and `marketFactor = 1.0`:

| Situation | Penalty | Buy price | Sell price |
| --- | ---: | ---: | ---: |
| Clean baseline | 0.06 | 1060 | 943 |
| Clean baseline, Trade 100 | 0.05 | 1050 | 952 |
| Heavy penalty | 0.50 | 1500 | 666 |
| Heavy penalty with `-20% trade penalty` | 0.40 | 1400 | 714 |
| Tier 5 equipment sale, no perk | 2.56 | n/a | 280 |
| Tier 5 equipment sale with `Appraiser` | 2.176 | n/a | 314 |

The last two rows are the important mental model: a penalty perk can be worth taking, but the final sell price improvement is much smaller than the displayed percentage when the penalty is already large.

## Trade Penalty Perks

Role matters. The Trade skill penalty effect is party-leader based, but many category perks use quartermaster, personal, or party-leader roles.

| Skill | Level | Perk | Role | Lane |
| --- | ---: | --- | --- | --- |
| Trade | 25 | `Appraiser` | party leader | `-15%` price penalty while selling equipment. |
| Trade | 25 | `Whole Seller` | party leader | `-15%` price penalty while selling trade goods. |
| Trade | 75 | `Distributed Goods` | quartermaster | `-15%` price penalty while buying from villages. |
| Trade | 75 | `Local Connection` | quartermaster | `-15%` price penalty while selling animals. |
| Trade | 175 | `Insurance Plans` | quartermaster | `-25%` price penalty while buying food items. |
| Trade | 175 | `Rapid Development` | quartermaster | `-25%` price penalty while buying clay, iron, silk, and silver. |
| Trade | 200 | `Granary Accountant` | personal | `-20%` price penalty while selling food items. |
| Trade | 200 | `Tradeyard Foreman` | personal | `-20%` price penalty while selling pottery, tools, silk, and jewelry. |
| Trade | 250 | `Silver Tongue` | quartermaster | `15%` better trade deals from caravans and villagers. |
| Smithing | 175 | `Artisan Smith` | party leader | `-50%` trade penalty when selling player-crafted smithing weapons. |
| Riding | 75 | `Deeper Sacks` | party leader | `-10%` trade penalty for mounts. |
| Steward | 225 | `Arenicos' Horses` | personal | `-20%` trade penalty for trading mounts. |
| Steward | 225 | `Arenicos' Mules` | quartermaster | `-20%` trade penalty for trading pack animals. |
| Roguery | 150 | `Smuggler Connections` | party leader | `-50%` penalty when trading with a faction where the main hero has crime rating. |
| Roguery | 225 | `Arms Dealer` | party leader | `-20%` sell price penalty for weapons. |
| Scouting | 200 | `Rumor Network` | party leader | `-5%` trade penalty within cities of your own kingdom. |
| Scouting | 200 | `Village Network` | party leader | `-10%` trade penalty with villages of your own culture. |

The Aserai trader cultural feat also appears in the trade penalty method as a `-10%` factor.

## Not Normal Trade Penalty

Some economy perks are currently close enough in wording that they can be misclassified if read by pattern matching alone.

| Effect family | Examples | Why it is separate |
| --- | --- | --- |
| Barter penalty | `Self-made Man`, `Effort For The People`, `Slick Negotiator` | Uses the barter model, not the shop price model. |
| Ransom value or ransom cost | `Manhunter`, `Ransom Broker`, `Man of Means` | Ransom broker deals and prisoner freedom costs are not item shop spread. |
| Wages | `Mercenary Connections`, `Content Trades`, `Sword For Barter`, `Picked Shots` | These reduce recurring costs, not trade prices. |
| Recruitment and upgrade cost | `Great Investor`, `Head Hunter`, `Renowned Archer` | These change hiring/upgrading costs, not shop prices. |
| Settlement income | `Toll Gates`, `Traveling Rumors`, `Content Trades`, governor tax/tariff perks | These are settlement or clan income streams. |

This distinction matters for build planning. A perk can be an economy perk without improving buy/sell prices.

## Trade XP

Profitable trade gives Trade XP only when profit is positive:

```text
tradeXp = 0.5 * tradeProfit
```

The party version exercises Trade as a party skill with party-leader role. The hero version exercises the hero's personal Trade skill.

Warehouse production gives Trade XP to the main hero:

```text
warehouseProductionTradeXp = 0.1 * productionBaseValue
```

This makes actual profitable routes and warehouse output the direct Trade XP sources we have confirmed. Merely moving expensive items around is not enough if the game does not count the transaction as profit.

## Trade Perk Read

### Low Investment

Trade 25 and Trade 50 remain excellent quality-of-life splashes.

| Level | Pick | Read |
| ---: | --- | --- |
| 25 | `Appraiser` | Better if the character sells lots of loot and equipment. |
| 25 | `Whole Seller` | Better if the character actively flips trade goods. |
| 50 | `Caravan Master` | Usually the stronger practical pick because of carrying capacity. |
| 50 | `Market Dealer` | More niche, unless safe-passage barter is part of the campaign. |

Both level 25 perks mark profits, and both level 50 perks mark item prices relative to average price. That information layer is often worth more than the early penalty number.

### Medium Investment

Trade 75 to 200 is where the skill becomes lane-specific:

- Food/material buying perks are good if you repeatedly buy those goods in bulk.
- Animal and mount penalty perks are good only if you actually trade animals or maintain a horse-heavy economy.
- `Content Trades` and `Mercenary Connections` are campaign-cost perks, not shop-price perks.
- `Granary Accountant` and `Tradeyard Foreman` are stronger when the character is already running focused trade routes.

### High Investment

Trade 225+ is campaign-shaping rather than normal shopping:

| Level | Perk | Read |
| ---: | --- | --- |
| 225 | `Self-made Man` | Strong for item-heavy lord barters; separate from shop trade. |
| 225 | `Sword For Barter` | Mercenary hiring and caravan guard wage economy. |
| 250 | `Silver Tongue` | Political economy: lord defection cost and caravan/villager deals. |
| 250 | `Spring of Gold` | Passive interest, capped by the perk text at 1000 denars per day. |
| 275 | `Man of Means` | Minor-faction recruitment cost and personal ransom safety. |
| 300 | `Everything Has a Price` | The unique settlement-barter unlock. Build around it if taking it. |

`Everything Has a Price` is the reason to push Trade to 300. The normal penalty reductions alone are not enough to justify that investment for most builds.

## Practical Advice

- Use Trade 25/50 for information even on non-merchant characters.
- Treat trade penalty perks as lane unlocks. They are strongest when you repeat the exact item category they mention.
- Do not expect equipment flipping to behave like trade-good arbitrage. Equipment has a narrow market factor and a huge selling penalty.
- If selling crafted weapons is the plan, `Artisan Smith` is a bigger lever than generic Trade skill alone.
- For Trade XP, chase positive profit and warehouse output. The XP formula cares about profit, not just transaction size.
- Keep barter perks mentally separate from shop perks. They matter for diplomacy, settlement trades, and lord deals, not for buying grain in town.

## Evidence

Primary local evidence:

- `Data/generated/trade-economy-methods.json`: extracted methods for `DefaultTradeItemPriceFactorModel`, `DefaultPartyTradeModel`, `DefaultBarterModel`, and related economy models.
- `Data/generated/reports/xp-formulas.md`: confirmed warehouse Trade XP formula.
- `Data/generated/skill-xp-source-methods.json`: profitable trade XP and warehouse production XP call sites.
- `Data/export/perk-effects.json`: postprocessed perk effects and custom classifications.
