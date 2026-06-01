# Settlement Economy

This note covers the money and production side of settlements: taxes, tariffs, village production, hearth growth, prosperity income, and economy-facing governor perks. It deliberately points workshop-specific details to `settlement-workshops.md` so towns do not become one giant unreadable bucket.

Read this together with `settlement-development.md`: loyalty, security, food, and construction are not pure economy effects, but they control how much prosperity can actually turn into money.

## Main Takeaways

- Settlement economy is not just "town tax". It is town tax, tariffs, village taxes, bound-village production, workshop production, caravan/villager visits, and construction projects.
- Prosperity is the core tax base. The extracted daily town tax starts from roughly `prosperity * 0.35` before the rest of the tax model adds policies, buildings, loyalty, security, issues, and other modifiers.
- High prosperity is not free. It increases food consumption and also creates a security drag, so growth needs food and security support.
- Security and loyalty are economy stats. Low security can reduce settlement commission, while tax/security/loyalty thresholds feed into corruption or boost paths.
- Governor perks are the main perk layer for owned settlements. Many great economy perks do nothing unless the perk holder is actually governing that settlement.

## Tax And Tariff Layers

The extracted `DefaultSettlementTaxModel` shows the town tax calculation feeding an `ExplainedNumber`:

```text
rawTownTax ~= prosperity * 0.35
```

That raw value then flows through policy cuts, building effects, loyalty effects, security effects, and issue effects. In other words, prosperity is the base, but stability determines how much of that base survives.

Security also affects settlement commission. The model has a security threshold at `75`, with a maximum security-based commission decrease of `10%` when security is too low. This makes high-security towns better economically even before considering raids, sieges, and village safety.

The practical read:

- A rich but unstable town can underperform.
- Security and loyalty perks should be treated as income support, not just governance flavor.
- Village protection matters twice: villages feed production and taxes, and raided villages create settlement penalties.

## Prosperity, Food, And Security

Prosperity increases income and construction, but it creates pressure elsewhere:

| System | Extracted relationship | Practical read |
| --- | ---: | --- |
| Tax base | `prosperity * 0.35` before modifiers | Prosperity is the main town-tax engine. |
| Construction base | `prosperity * 0.01` before modifiers | Prosperity also helps build faster. |
| Food consumption | `1 food per 40 prosperity` | Very rich towns need food support. |
| Security drag | `max(-5, -0.0005 * prosperity)` | Prosperity slowly pulls security down, capped at `-5`. |

This is why "develop the town" and "defend the town" are hard to separate. Prosperity pays, but it asks for food and order.

## Economy Governor Perks

### Tax, Tariff, And Visit Income

| Skill | Level | Perk | Effect | Read |
| --- | ---: | --- | --- | --- |
| Bow | 250 | `Quick Draw` | +5% tax gain. | Late, simple tax multiplier. |
| Crossbow | 200 | `Steady` | +5% tariff gain. | Tariff-focused governor lane. |
| Roguery | 175 | `Salt the Earth` | +5% tariff revenue. | Economy payoff inside a crime skill. |
| Scouting | 75 | `Desert Born` | +2.5% tax income. | Small but early. |
| Scouting | 75 | `Forest Kin` | +10% tax income from bound villages. | Stronger if the town's villages are valuable and intact. |
| Steward | 125 | `Giving Hands` | +10% tariff income. | Good governor economy perk, separate from donation XP role. |
| Steward | 125 | `Logistician` | +10% tax income. | Clean tax pick for a governor. |
| Steward | 275 | `Price of Loyalty` | +0.5% tax income per Steward point above 200. | Big only on a very high Steward governor. |
| Trade | 100 | `Toll Gates` | +30 gold per visiting caravan. | Better in busy trade towns. |
| Trade | 100 | `Traveling Rumors` | +20 gold per visiting villager party. | Better when villages are safe and frequently visiting. |
| Trade | 150 | `Content Trades` | +10% tariff income. | Straight tariff support. |

### Village Production And Hearths

| Skill | Level | Perk | Effect | Read |
| --- | ---: | --- | --- | --- |
| Athletics | 175 | `Energetic` | +20% hearth growth in bound villages. | Long-term village growth. |
| Athletics | 200 | `Steady` | +10% production in bound farms, mines, lumber camps, and clay pits. | Broad village-output perk. |
| Medicine | 150 | `Bush Doctor` | +20% hearth growth in bound villages. | Stacks conceptually with other hearth-growth choices. |
| Medicine | 175 | `Perfect Health` | +10% animal production rate in bound villages. | Good for livestock-bound villages. |
| Medicine | 200 | `Clean Infrastructure` | +30% recovery rate from raids in bound villages. | Economic resilience, not just prosperity flavor. |
| Riding | 175 | `Breeder` | +5% production rate to bound villages. | Small general village production. |
| Riding | 175 | `Shepherd` | 15% chance of producing tier 2 horses in bound villages. | Niche but useful for horse villages. |
| Scouting | 200 | `Village Network` | +10% villager party size from bound villages. | More goods reach town if parties survive. |
| Steward | 150 | `Aid Corps` | +20% hearth growth in bound villages. | Strong long-term governor support. |
| Trade | 200 | `Granary Accountant` | +20% production to grain, olives, fish, and dates in bound villages. | Food economy and village income lane. |
| Trade | 200 | `Tradeyard Foreman` | +20% production to clay, iron, silk, and silver in bound villages. | Raw-material and luxury-material lane. |

### Prosperity, Food, And Project Income

| Skill | Level | Perk | Effect | Read |
| --- | ---: | --- | --- | --- |
| Engineering | 125 | `Foreman` | +100 prosperity when a project is finished. | Development payoff from building. |
| Engineering | 175 | `Battlements` | +100 max food reserve. | Lets prosperity and garrisons survive longer. |
| Engineering | 200 | `Apprenticeship` | +1% prosperity gain for each unique project. | Rewards a developed town. |
| Engineering | 250 | `Architectural Commissions` | +20 gold/day for continuous projects. | Small passive income while running continuous projects. |
| Medicine | 150 | `Pristine Streets` | +1 prosperity/day. | Simple and steady prosperity. |
| Medicine | 200 | `Clean Infrastructure` | +1 prosperity from civilian projects. | Project-linked growth. |
| Medicine | 250 | `Helping Hands` | -50% prosperity loss from starvation. | Insurance for stressed towns. |
| Steward | 250 | `Master of Warcraft` | -5% town population food consumption. | Economy support by reducing food pressure. |
| Trade | 275 | `Trickle Down` | +2 daily prosperity while building a project. | High Trade governor development payoff. |

## Practical Governor Read

For money, the strongest practical governor identities are:

| Governor lane | Why it works |
| --- | --- |
| Steward governor | Tax, tariff, hearth growth, food pressure, and project effects all live here. |
| Trade governor | Tariffs, visit income, material production, workshop production, prosperity during projects. |
| Engineering governor | Construction and project completion convert into prosperity, reserves, and later income. |
| Medicine governor | Hearth recovery, prosperity, starvation protection, and loyalty support. |

For early settlement ownership, stability is usually worth more than one more income line. A governor that keeps loyalty and security above bad thresholds can outperform a governor with better visible income perks but poor control stats.

## Evidence

Primary local evidence:

- `Data/generated/settlement-methods.json`: extracted settlement tax, security, loyalty, food, construction, workshop, and alley methods.
- `Data/export/perk-effects.json`: postprocessed governor perk effects and custom classifications.
- `Docs/notes/settlement-development.md`: loyalty, construction, food, and growth mechanics.
- `Docs/notes/settlement-defense.md`: security, garrison, militia, and siege resilience mechanics.
