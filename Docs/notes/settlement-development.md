# Settlement Development

This note covers the growth and stability layer for settlements: loyalty, prosperity, hearth recovery, construction power, project effects, and food pressure. It overlaps with both settlement economy and defense on purpose. In Bannerlord, development is the bridge between "the town makes money" and "the town survives long enough to keep making money."

## Main Takeaways

- Loyalty is a central development stat because it affects stability, tax, militia behavior, and construction effectiveness.
- Loyalty has strong drift toward `50`. The extracted model adds `-0.1 * (loyalty - 50)` per day, so low loyalty self-recovers somewhat and high loyalty naturally decays without support.
- Construction starts from prosperity, but governor perks, boost projects, prisoners, buildings, loyalty, and policies can all matter.
- Food is a development cap. More prosperity and larger garrisons consume more food, so a rich town can starve itself if villages and reserves cannot keep up.
- Culture and governor assignment matter: owner-culture mismatch and governor-culture mismatch are steady loyalty pressures.

## Loyalty Drift

The extracted loyalty drift formula is:

```text
dailyLoyaltyDrift = -0.1 * (currentLoyalty - 50)
```

Examples:

| Current loyalty | Daily drift |
| ---: | ---: |
| 25 | +2.5 |
| 40 | +1.0 |
| 50 | 0.0 |
| 60 | -1.0 |
| 75 | -2.5 |

This means raw loyalty bonuses have different value depending on where the town already sits. A town at `20` loyalty gets help from drift, but it is also near rebellion danger. A town at `75` loyalty is comfortable, but the model is actively pulling it back down.

Important extracted loyalty pressures and thresholds:

| Source | Value | Read |
| --- | ---: | --- |
| Owner different culture | `-3` loyalty/day | The big conquered-town problem. |
| Governor same culture | `+1` loyalty/day | A same-culture governor softens conquest. |
| Governor different culture | `-1` loyalty/day | A mismatched governor can make things worse. |
| High security effect | `+1` loyalty/day | Security is a development stat. |
| Low security effect | `-2` loyalty/day | Security collapse can pull loyalty down too. |
| Rebellious state threshold | `25` loyalty | Danger zone. |
| Rebellion start threshold | `15` loyalty | Critical zone. |

Notables also matter. The loyalty model includes support from notable relations: notables supporting the owner clan are positive, while notables supporting an enemy faction are negative.

## Construction Power

The extracted `DefaultBuildingConstructionModel.CalculateDailyConstructionPowerInternal` starts from prosperity:

```text
baseConstructionPower ~= prosperity * 0.01
```

Then the model layers in settlement projects, boost funding, governor effects, prisoners, building effects, loyalty, policies, and perk-specific project bonuses.

Practical consequences:

- Prosperity helps development twice: it pays taxes and builds faster.
- Low loyalty is a construction problem, not just a rebellion problem.
- Construction perks are best on a governor who will stay in the town long enough for project queues to finish.
- Prisoner-based construction from `Forced Labor` exists in the construction path, but it should be treated as a governor/town project effect, not a generic party-management perk.

## Food Pressure

The extracted food model constants:

| Constant | Value | Read |
| --- | ---: | --- |
| Town food stock upper limit | `300` | Base reserve cap. |
| Castle food stock bonus | `+150` | Castles can hold more. |
| Garrison food use | `1 food per 20 garrison troops` | Big garrisons need supply. |
| Prosperity food use | `1 food per 40 prosperity` | Rich towns eat a lot. |

Food turns development into a balancing problem. Prosperity is excellent until the settlement cannot feed itself; then starvation can eat prosperity and weaken the garrison. Food-reserve and food-consumption perks are therefore development perks even when they look defensive.

## Development Governor Perks

### Loyalty And Stability

| Skill | Level | Perk | Effect | Read |
| --- | ---: | --- | --- | --- |
| Athletics | 175 | `Durable` | +1 daily loyalty. | Strong simple governor stabilizer. |
| Bow | 150 | `Discipline` | +1 daily loyalty. | Useful if a bow governor is already planned. |
| Charm | 225 | `Parade` | +5 loyalty while waiting in the settlement. | Personal, not a normal remote-governor solution. |
| Leadership | 75 | `Heroic Leader` | +1 daily loyalty. | Excellent early governor stability. |
| Medicine | 200 | `Physician of People` | +1 daily loyalty. | Nice because Medicine also has prosperity and village recovery support. |
| Riding | 50 | `Well Strapped` | +0.5 daily loyalty. | Small but cheap if the governor has Riding. |

### Construction And Project Effects

| Skill | Level | Perk | Effect | Read |
| --- | ---: | --- | --- | --- |
| Engineering | 75 | `Carpenters` | +12% town project construction speed. | Early Engineering governor value. |
| Engineering | 125 | `Foreman` | +100 prosperity when a project is finished. | Makes completed projects feed growth. |
| Engineering | 150 | `Stonecutters` | +30% fortification, aqueduct, and barrack project build speed. | Both development and defense. |
| Engineering | 200 | `Apprenticeship` | +1% prosperity gain for each unique project. | Better in well-developed towns. |
| Engineering | 250 | `Clockwork` | +20% boosting project effectiveness. | High-end project accelerator. |
| Steward | 150 | `Relocation` | +20% boosting project effectiveness. | Good if using boost projects often. |
| Steward | 200 | `Contractors` | +10% town project effects. | Broad project improvement. |
| Steward | 200 | `Forced Labor` | Prisoners increase construction speed. | Needs prisoners in the settlement context. |
| Steward | 250 | `Master of Planning` | +20% continuous project effectiveness. | Strong for long-running town management. |
| Trade | 225 | `Self-made Man` | +30% build speed for marketplace, kiln, and aqueduct. | Narrow but meaningful project set. |
| Trade | 250 | `Spring of Gold` | +20% boosting project effectiveness. | High Trade development support. |

### Hearth, Prosperity, Food, And Recovery

| Skill | Level | Perk | Effect | Read |
| --- | ---: | --- | --- | --- |
| Athletics | 175 | `Energetic` | +20% hearth growth in bound villages. | Village-growth layer. |
| Medicine | 150 | `Bush Doctor` | +20% hearth growth in bound villages. | Village-growth layer. |
| Medicine | 150 | `Pristine Streets` | +1 prosperity/day. | Simple town growth. |
| Medicine | 200 | `Clean Infrastructure` | +1 prosperity from civilian projects and faster raid recovery. | Good conquered-town recovery tool. |
| Medicine | 250 | `Helping Hands` | -50% prosperity loss from starvation. | Emergency insurance for food-stressed towns. |
| Steward | 150 | `Aid Corps` | +20% hearth growth in bound villages. | Strong long-term village support. |
| Steward | 250 | `Master of Warcraft` | -5% town population food consumption. | Food-pressure reduction. |
| Trade | 275 | `Trickle Down` | +2 daily prosperity while building a project. | High-investment growth perk. |

## Development Priorities

For a new or conquered town:

1. Stabilize loyalty first, especially if owner culture does not match the settlement.
2. Keep security above bad thresholds because it supports loyalty, tax, and rebellion safety.
3. Protect villages so hearths, production, and food supply can recover.
4. Build food and stability projects before chasing maximum prosperity.
5. Move into tax, tariff, and workshop optimization once the town can feed itself.

For castles:

- Food reserve and garrison pressure matter more than tariffs.
- Construction speed on fortifications and military projects is more valuable.
- Militia and garrison perks from `settlement-defense.md` are part of the development plan because castles exist to survive sieges.

## Evidence

Primary local evidence:

- `Data/generated/settlement-methods.json`: extracted `DefaultSettlementLoyaltyModel`, `DefaultBuildingConstructionModel`, `DefaultSettlementFoodModel`, and related settlement methods.
- `Data/export/perk-effects.json`: postprocessed governor perk effects and custom classifications.
- `Docs/notes/settlement-economy.md`: tax, production, tariff, and prosperity income notes.
- `Docs/notes/settlement-defense.md`: security, militia, garrison, and siege notes.
