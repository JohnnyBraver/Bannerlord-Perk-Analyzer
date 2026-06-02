# Workshop Appendix

This appendix covers workshop-specific settlement economy. It is separate from `settlement-economy.md` because workshops have their own ownership limits, production model, warehouse XP, bankruptcy handling, and perk hooks. For the broader market loop around hidden artisans, villages, demand, and consumption, see `settlement-supply-chain.md`.

## Main Takeaways

- Workshops are settlement economy, but they are not normal town tax or tariff income.
- Towns have `4` internal workshop slots, but only `3` are normal visible/purchasable workshops.
- Slot `0` is initialized as the hidden `artisans` workshop type, so the in-game player-facing limit you usually see is `3` town workshops.
- Player workshop capacity scales with clan tier. The extracted model returns `clanTier + 1` for max workshops at a given clan tier.
- Warehouse production gives Trade XP to the main hero: `0.1 * productionBaseValue`.
- A workshop can be saved from bankruptcy for `3` days according to the extracted model.
- Workshop value depends on production output, input availability, town market conditions, and the owner-income path. It should not be evaluated only by the raw purchase price.

## Extracted Workshop Constants

| Model value | Extracted value | Practical read |
| --- | ---: | --- |
| Internal workshop slots per town | `4` | The town array has four workshop objects. |
| Visible normal workshops per town | `3` | Slot `0` is the hidden `artisans` workshop; slots `1-3` become normal workshops. |
| Max player workshops by clan tier | `clanTier + 1` | Clan tier is the main ownership cap. |
| Bankruptcy save window | `3` days | Short window to intervene. |
| Warehouse Trade XP | `0.1 * productionBaseValue` | Warehouse output is a confirmed Trade XP source. |

The `DefaultWorkshopModel` exposes `DefaultWorkshopCountInSettlement = 4`, and `Town.InitializeWorkshops(4)` really does create four workshop objects. At game start, though, `BuildArtisanWorkshop` fills slot `0` with workshop type `artisans`; the XML marks that type as `isHidden="true"` and `frequency="0"`. The notable-owner buy dialogue filters to non-hidden workshop types, which leaves the three ordinary production workshops that players normally interact with.

The `DefaultWorkshopModel` also exposes capital, daily expense, warehouse capacity, conversion cost, notable cost, player cost, and effective production speed methods. Those are good candidates for a future generated workshop calculator.

## Workshop Perks

| Skill | Level | Perk | Role | Effect | Read |
| --- | ---: | --- | --- | --- | --- |
| Steward | 75 | `Sweatshops` | personal | +20% production rate to owned workshops. | Direct owner-side workshop production. |
| Trade | 150 | `Mercenary Connections` | governor | +25% workshop production rate. | Applies through the governed settlement, so it is a governor pick. |
| Trade | 100 | `Toll Gates` | personal | Workshops gather trade rumors. | Useful information layer for workshop owners. |
| Trade | 100 | `Toll Gates` | governor | +30 gold per caravan visiting the governed settlement. | Settlement-income support, not workshop production. |
| Trade | 125 | `Artisan Community` | clan leader | +1 daily renown from every profiting workshop. | Turns profit into clan progression. |
| Trade | 175 | `Rapid Development` | clan leader | 5000 denar return for each workshop when its town is captured by an enemy. | Ownership protection, not production. |

`Sweatshops` and `Mercenary Connections` are the big production-facing perks. They are different lanes: one belongs to the workshop owner, the other to the governor of the settlement where the workshop operates.

## Practical Workshop Read

Good workshop planning is mostly about repeatable inputs and town demand:

- Prefer towns whose bound villages or nearby trade routes can supply the workshop's inputs.
- Watch whether the town market can actually support the output. High-value output is not enough if inputs are scarce or output is saturated.
- A production perk is better when the underlying workshop already has a stable input/output loop.
- Warehouse Trade XP means workshops can support a Trade build even when the player is not constantly running manual routes.
- Workshop income should be read separately from town taxes and tariffs. A governor can improve both, but they are different systems.

## Open Follow-Ups

- Extract workshop type inputs, outputs, and conversion speeds into a generated table.
- Build a town-by-town workshop recommender from bound-village production and local market stocks.
- Decode the owner-income path deeply enough to estimate profit, not just production speed.

## Evidence

Primary local evidence:

- `Data/generated/settlement-methods.json`: extracted `DefaultWorkshopModel`, workshop campaign behavior, and clan-finance references.
- Local game XML `Modules/SandBox/ModuleData/spworkshops.xml`: confirms the `artisans` workshop type is hidden.
- `Docs/notes/trade-economy.md`: warehouse Trade XP and trade penalty context.
- `Data/export/perk-effects.json`: postprocessed workshop-related perk effects.
