# Village Raiding Loot

This note covers the loot produced by actual village raids. It focuses on the raid pulse loop, village production loot, common loot, stored village inventory, and the perks that do or do not affect those lanes.

## Main Takeaways

- A raid loot pulse has three item lanes: stored village inventory, village production, and common raid loot.
- Production loot is deterministic accumulator math, not a direct random drop chance. Low-weight items pay out less often, which makes `Efficient Campaigner` much stronger when they do pay out.
- Common loot is random and value-weighted. Cheap grain dominates the common pool.
- `No Rest for the Wicked` increases raid speed. It mostly gives more raid progress per day, not more loot from a fully completed raid.
- In the default raid model, `GetRaidLootMultiplier` returns `1`. Several Roguery perks talk about loot, villagers, or hostile actions, but they are not all part of the actual village raid pulse loop.

## Raid Pulse Model

Raid damage accumulates until `_nextSettlementDamage > 0.05`. When that threshold is crossed, the game runs one loot pulse and then resets `_nextSettlementDamage` to `0`.

```text
raidDamagePerHour = (sqrt(attackerTroopCount) + 5) / 900
raidDamageThisUpdate = raidDamagePerHour * deltaHours
```

`No Rest for the Wicked` adds its secondary bonus as a factor to this damage number. In a one-party raid that is `+5%` raid speed. The model loops attacker parties, so multiple attacking party leaders with the perk can add multiple factors.

On a village loot pulse:

```text
pulseDamage = _nextSettlementDamage
lostHearth = pulseDamage * 0.5 * currentVillageHearth
gold = floor(lostHearth * 4 * raidLootMultiplier)
currentVillageHearth -= lostHearth
settlementHitPoints -= pulseDamage
```

The default `raidLootMultiplier` is `1`. At a clean `0.05` pulse, the village loses `2.5%` of its current hearth.

| Current hearth | Lost hearth at 0.05 pulse | Gold at default multiplier |
| ---: | ---: | ---: |
| 200 | 5.0 | 20 |
| 400 | 10.0 | 40 |
| 600 | 15.0 | 60 |
| 800 | 20.0 | 80 |

If every pulse were exactly `0.05`, a full 20-pulse raid would remove about `39.7%` of starting hearth because hearth is reduced after every pulse:

```text
totalLostHearth = startingHearth * (1 - 0.975^20)
```

Actual pulses can be slightly larger than `0.05` if the update overshoots the threshold.

## Item Lanes

### Stored Village Inventory

The raid first looks at the settlement item roster. This lane depends on the live save, so it cannot be predicted from village type alone.

```text
storedItemsRemoved = min(existingItemCount, RoundRandomized(existingItemCount * pulseDamage))
```

Each removed item is selected from the village item roster weighted by stack count. For each removed item:

```text
lootChance = 0.5 * raidLootMultiplier
```

At the default multiplier and a `0.05` pulse, this means roughly:

- About `5%` of stored inventory is removed from the village.
- About half of those removed items are added to the attacker loot roster.
- Expected player-facing gain is roughly `2.5%` of stored inventory per pulse.
- If the selected item is food and the party leader has `Efficient Campaigner`, the looted count becomes `2` instead of `1`.

Stored village food is the cleanest "doubled food" case for `Efficient Campaigner`.

### Village Production

Village production loot is the village-type-specific lane. It uses `lostHearth`, not stored inventory.

```text
productionProgress[item] += lostHearth * productionWeight / 60 * raidLootMultiplier
payout = floor(productionProgress[item])
productionProgress[item] -= payout
```

Then the payout is passed through `LootItemInRaid`. If the item is food and the party leader has `Efficient Campaigner`, the payout becomes:

```text
finalFoodPayout = payout + 1
```

That is the important detail: production food is not doubled as a percentage. It gets `+1` for every payout event. If payouts are often `1`, the perk effectively doubles them. If payouts are large, the relative gain is smaller.

Every village type has a default grain entry, but the raid loop skips that grain unless the village's primary production is grain. In practice, non-wheat villages do not also pay production-lane grain during raids.

For a clean `0.05` pulse:

```text
productionProgress = currentHearth * productionWeight / 2400
```

At `400` current hearth, the per-pulse progress is `productionWeight / 6`.

### Common Loot

Common loot is shared by all villages. The game runs one common-loot attempt for each whole point of `lostHearth`:

```text
attempts = floor(lostHearth)
successChancePerAttempt = 0.25 * raidLootMultiplier
```

On success, the item is selected from the common pool with weight:

```text
commonWeight = 100 / (itemValue + 1)
```

Default common loot pool:

| Item | Value | Weight | Chance on successful common pick | Expected count per attempt |
| --- | ---: | ---: | ---: | ---: |
| grain | 10 | 9.091 | 49.85% | 0.1246 |
| hardwood | 25 | 3.846 | 21.09% | 0.0527 |
| hides | 50 | 1.961 | 10.75% | 0.0269 |
| sheep | 80 | 1.235 | 6.77% | 0.0169 |
| mule | 120 | 0.826 | 4.53% | 0.0113 |
| pottery | 210 | 0.474 | 2.60% | 0.0065 |
| linen | 245 | 0.407 | 2.23% | 0.0056 |
| tools | 250 | 0.398 | 2.18% | 0.0055 |

Only grain is food in the common pool. `Efficient Campaigner` therefore doubles successful common-grain pickups from `1` to `2`.

## Production Weights By Village Type

The values below are production weights. The number in parentheses is progress per clean `0.05` pulse at `400` current hearth.

### Food And Livestock Villages

| Village type | Raid production outputs |
| --- | --- |
| `wheat_farm` | grain `50` (`8.33`), cow `0.2` (`0.03`), sheep `0.4` (`0.07`), hog `0.8` (`0.13`) |
| `fisherman` | fish `28` (`4.67`) |
| `vineyard` | grapes `11` (`1.83`) |
| `date_farm` | date fruit `8` (`1.33`) |
| `olive_trees` | olives `12` (`2.00`) |
| `cattle_farm` | cow `2` (`0.33`), butter `4` (`0.67`), cheese `4` (`0.67`) |
| `sheep_farm` | sheep `4` (`0.67`), wool `10` (`1.67`), butter `2` (`0.33`), cheese `2` (`0.33`) |
| `swine_farm` | hog `8` (`1.33`), butter `2` (`0.33`), cheese `2` (`0.33`) |

### Resource Villages

| Village type | Raid production outputs |
| --- | --- |
| `lumberjack` | hardwood `18` (`3.00`) |
| `clay_mine` | clay `10` (`1.67`) |
| `salt_mine` | salt `15` (`2.50`) |
| `iron_mine` | iron `10` (`1.67`) |
| `flax_plant` | flax `18` (`3.00`) |
| `silk_plant` | cotton `8` (`1.33`) |
| `silver_mine` | silver `3` (`0.50`) |
| `trapper` | fur `1.4` (`0.23`) |

### Horse Villages

| Village type | Raid production outputs |
| --- | --- |
| `europe_horse_ranch` | empire horse `2.1` (`0.35`), tier 2 empire horse `0.5` (`0.08`), tier 3 empire horse `0.07` (`0.01`), sumpter horse `0.5` (`0.08`), mule `0.5` (`0.08`), saddle horse `0.5` (`0.08`), old horse `0.5` (`0.08`), hunter `0.2` (`0.03`), charger `0.2` (`0.03`) |
| `sturgian_horse_ranch` | sturgia horse `2.5` (`0.42`), tier 2 sturgia horse `0.7` (`0.12`), tier 3 sturgia horse `0.1` (`0.02`), sumpter horse `0.5` (`0.08`), mule `0.5` (`0.08`), saddle horse `0.5` (`0.08`), old horse `0.5` (`0.08`), hunter `0.2` (`0.03`), charger `0.2` (`0.03`) |
| `vlandian_horse_ranch` | vlandia horse `2.1` (`0.35`), tier 2 vlandia horse `0.4` (`0.07`), tier 3 vlandia horse `0.08` (`0.01`), sumpter horse `0.5` (`0.08`), mule `0.5` (`0.08`), saddle horse `0.5` (`0.08`), old horse `0.5` (`0.08`), hunter `0.2` (`0.03`), charger `0.2` (`0.03`) |
| `battanian_horse_ranch` | battania horse `2.3` (`0.38`), tier 2 battania horse `0.7` (`0.12`), tier 3 battania horse `0.09` (`0.02`), sumpter horse `0.5` (`0.08`), mule `0.5` (`0.08`), saddle horse `0.5` (`0.08`), old horse `0.5` (`0.08`), hunter `0.2` (`0.03`), charger `0.2` (`0.03`) |
| `steppe_horse_ranch` | khuzait horse `1.8` (`0.30`), tier 2 khuzait horse `0.4` (`0.07`), tier 3 khuzait horse `0.05` (`0.01`), sumpter horse `0.5` (`0.08`), mule `0.5` (`0.08`) |
| `desert_horse_ranch` | aserai horse `1.7` (`0.28`), tier 2 aserai horse `0.3` (`0.05`), tier 3 aserai horse `0.05` (`0.01`), camel `0.3` (`0.05`), war camel `0.08` (`0.01`), pack camel `0.3` (`0.05`), sumpter horse `0.4` (`0.07`), mule `0.5` (`0.08`) |

## Efficient Campaigner Examples

This table uses a clean 20-pulse full-raid model with starting hearth `400`, default loot multiplier, and production loot only. Common grain and stored inventory are separate.

| Source | Food item | Base production loot | With `Efficient Campaigner` | Relative gain |
| --- | --- | ---: | ---: | ---: |
| `wheat_farm` | grain | 132 | 152 | +15.2% |
| `fisherman` | fish | 74 | 94 | +27.0% |
| `vineyard` | grapes | 29 | 49 | +69.0% |
| `date_farm` | date fruit | 21 | 41 | +95.2% |
| `olive_trees` | olives | 31 | 51 | +64.5% |
| `cattle_farm` | butter | 10 | 20 | +100.0% |
| `cattle_farm` | cheese | 10 | 20 | +100.0% |
| `sheep_farm` | butter | 5 | 10 | +100.0% |
| `sheep_farm` | cheese | 5 | 10 | +100.0% |
| `swine_farm` | butter | 5 | 10 | +100.0% |
| `swine_farm` | cheese | 5 | 10 | +100.0% |

For common grain over the same clean 20-pulse model:

| Starting hearth | Expected common grain | With `Efficient Campaigner` |
| ---: | ---: | ---: |
| 200 | 8.7 | 17.4 |
| 400 | 18.7 | 37.4 |
| 600 | 28.5 | 57.1 |
| 800 | 38.6 | 77.3 |

Practical read:

- Wheat farms are best for raw food volume.
- Fishers are strong raw food villages too.
- Dates, olives, grapes, and dairy are where `Efficient Campaigner` feels most dramatic because the base payout events are smaller.
- Dairy villages get excellent percentage gains, but the raw food count is much lower than wheat or fish.

## Placed Village Hearth Ranges

These are the vanilla placed village types from `settlements.xml`.

| Village type | Count | Min hearth | Median hearth | Max hearth |
| --- | ---: | ---: | ---: | ---: |
| `battanian_horse_ranch` | 2 | 374 | 381.5 | 389 |
| `cattle_farm` | 15 | 104 | 339 | 652 |
| `clay_mine` | 16 | 131 | 349.5 | 640 |
| `date_farm` | 9 | 183 | 454 | 540 |
| `desert_horse_ranch` | 9 | 150 | 243 | 375 |
| `europe_horse_ranch` | 9 | 145 | 192 | 427 |
| `fisherman` | 22 | 125 | 362 | 655 |
| `flax_plant` | 13 | 132 | 347 | 640 |
| `iron_mine` | 11 | 104 | 370 | 489 |
| `lumberjack` | 16 | 132 | 339.5 | 697 |
| `olive_trees` | 12 | 120 | 373.5 | 667 |
| `salt_mine` | 12 | 130 | 277 | 722 |
| `sheep_farm` | 17 | 130 | 240 | 670 |
| `silk_plant` | 8 | 170 | 331 | 621 |
| `silver_mine` | 7 | 110 | 395 | 705 |
| `steppe_horse_ranch` | 7 | 106 | 230 | 321 |
| `sturgian_horse_ranch` | 3 | 100 | 293 | 293 |
| `swine_farm` | 9 | 112 | 283 | 347 |
| `trapper` | 9 | 250 | 339 | 683 |
| `vineyard` | 15 | 125 | 488 | 809 |
| `vlandian_horse_ranch` | 3 | 280 | 680 | 680 |
| `wheat_farm` | 49 | 101 | 267 | 825 |

Higher hearth is a direct loot multiplier for gold, production progress, and common-loot attempts.

## Looting-Related Perks

| Skill | Level | Perk | Applies to village raid pulse loot? | Notes |
| --- | ---: | --- | --- | --- |
| Roguery | 25 | `No Rest for the Wicked` | Speed only | Adds `+5%` raid speed. More loot per campaign day, not more loot from the same completed raid. |
| Steward | 100 | `Efficient Campaigner` | Yes, food only | Adds `+1` to each food item payout through `LootItemInRaid`. Affects stored food, production food, and common grain. |
| Roguery | 75 | `Know-How` | No direct raid-pulse hook found | Text is `+5%` loot from defeated villagers and caravans. Treat as villager/caravan party loot, not village burning loot. |
| Roguery | 125 | `Scarface` | No | Surrender chance for bandits, villagers, and caravans. Useful for hostile encounters, not the raid loot pulse. |
| Roguery | 175 | `Salt the Earth` | No direct raid-pulse hook found | Text is `+20%` more loot when villagers comply to hostile actions. This belongs to compliance/hostile-action results, not the actual raid burn loop. |
| Roguery | 275 | `Rogue Extraordinaire` | No default raid-pulse effect found | Generic `+1%` loot amount per Roguery point above 200. The default raid model's `GetRaidLootMultiplier` returns `1`, so this is not part of the default village raid item formula. |
| Engineering | 225 | `Metallurgy` | Quality cleanup, not count | `30%` chance to remove negative modifiers on looted items. It does not increase raid item counts. |

The implementation has two food hooks. Stored-inventory loot checks `Efficient Campaigner` inline and turns a looted food item from `1` into `2`. Production loot and common loot call `LootItemInRaid`; if the item is food and the looting party's mobile party has `Efficient Campaigner`, that method increments the payout count by `1` before adding it to both the pulse loot roster and the party inventory.

## Planning Targets

- For food volume, raid high-hearth wheat farms and fishing villages.
- For `Efficient Campaigner` leverage, dates, olives, grapes, butter, and cheese gain the most relative value.
- For trade goods, use the village production table: salt, hardwood, flax, fish, grain, and high-hearth vineyards/olive/date villages are more predictable than the common pool.
- Stored inventory can swing outcomes hard. A village that has accumulated food in its settlement item roster can be much better than the village type alone suggests.
