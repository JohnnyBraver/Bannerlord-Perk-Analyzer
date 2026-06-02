# XP Awards

This note summarizes the local assembly extraction report in `Data/generated/reports/xp-awards.md`.

## Hero Skill XP

- `Hero.AddSkillXp(skill, xpAmount)` is a wrapper around `HeroDeveloper.AddSkillXp(skill, rawXp, true, true)`.
- `HeroDeveloper.AddSkillXp` ignores non-positive XP.
- When `isAffectedByFocusFactor` is true, the same raw XP is also added to total character XP through `GainRawXp` before the generic XP multiplier or learning/focus multiplier is applied.
- Skill XP is multiplied by `DefaultGenericXpModel.GetXpMultiplier(hero)`, then by the hero focus factor when `isAffectedByFocusFactor` is true.
- `DefaultGenericXpModel.GetXpMultiplier` returns `1.2` for player companions if the main hero has the Charm `Natural Leader` perk; otherwise it returns `1`.
- After adding skill XP, `DefaultCharacterDevelopmentModel.GetSkillLevelChange` decides whether the stored skill XP crosses one or more skill thresholds.

The important split is that a normal skill XP event feeds two ledgers:

```text
character total XP += round(rawXp)
skill stored XP += rawXp * genericXpMultiplier * learningRate
```

That means attributes, focus points, and learning rate make the skill grow faster, but they do not multiply the main character-level XP from the same event. Conversely, an over-limit or low-learning-rate skill can still feed character total XP if the award goes through the normal focus-affected path.

Some calls can pass `isAffectedByFocusFactor = false`. Those skip `GainRawXp`, do not apply the focus/learning multiplier, and add only `rawXp * genericXpMultiplier` to the skill's stored XP.

## Character Level XP

`HeroDeveloper.GainRawXp` rounds incoming raw XP, adds it to `TotalXp`, caps it at `CharacterDevelopmentModel.GetMaxSkillPoint()`, and then calls `CheckLevel`.

`HeroDeveloper.GetXpRequiredForLevel(level)` delegates to `DefaultCharacterDevelopmentModel.SkillsRequiredForLevel(level)`. The method name is a little misleading: this is the cumulative raw-XP threshold for the hero's main level, not a count of literal skill points gained.

The extracted threshold table is initialized like this:

```text
level 1 threshold = 1
level 2 threshold = 1001
for each next level:
  nextDelta = currentDelta + 1000 + floor(currentDelta / 5)
  nextThreshold = previousThreshold + nextDelta
```

Sample thresholds:

| Character level | Total raw XP required | XP from previous level |
| --- | ---: | ---: |
| 2 | 1,001 | 1,000 |
| 5 | 12,209 | 5,368 |
| 10 | 79,784 | 20,795 |
| 15 | 285,123 | 59,183 |
| 20 | 833,261 | 154,704 |
| 25 | 2,234,392 | 392,390 |
| 30 | 5,758,047 | 983,831 |
| 40 | 36,510,511 | 6,117,572 |
| 50 | 227,181,147 | 37,904,341 |
| 62 | 2,027,685,990 | 337,998,478 |

Practical read:

- Main level is not based on the number of skill levels gained.
- A high learning rate gives more skill progress per action, but not more main-level XP per raw XP event.
- Big raw-XP actions, such as hard combat hits, expensive smithing actions, or high-value activity rewards, are what push main level.
- Focus and attributes still matter indirectly because they let useful skills keep converting those actions into actual skill levels and perks instead of only feeding the raw character XP pool.

## Combat XP

- `DefaultCombatXpModel.GetXpFromHit` is the central hit/kill combat XP formula.
- The direct hit formula is:
  `0.4 * (attacker troop power + 0.5) * (target troop power + 0.5) * effective damage * mission multiplier`.
- `effective damage = min(damage, target max hit points) + target max hit points` when the hit is fatal.
- Fatal hits therefore add a full target max-HP chunk after damage is capped at max HP.
- Mission type multipliers are:
  - Battle: `1`
  - PracticeFight: `0.0625`
  - Tournament: `0.33`
  - SimulationBattle: `0.9`
  - NoXp: `0`
- `GetBattleXpBonusFromPerks` applies perk factors after the base hit XP is built.
- A targeted module scan found `Mission.GetShootDifficulty(affectedAgent, affectorAgent, isHeadShot)`.
- Mission-side shot difficulty is:
  `clamp(0.3 * ((distance + 4) / 4) * ((4 + lateralMotion * relativeSpeed) / 4), 1, 12)`.
- `distance` is the distance between attacker and target. `relativeSpeed` is target movement minus attacker movement. `lateralMotion` is the perpendicular share of that relative movement against the shot line.
- Headshots multiply the clamped shot difficulty by `1.2`, raising the possible max from `12` to `14.4`.
- `GetXpMultiplierFromShotDifficulty(shotDifficulty)` maps difficulty `1..14.4` to a raw factor from `0..2`: `lerp(0, 2, (min(shotDifficulty, 14.4) - 1) / 13.4)`.
- `DefaultSkillLevelingManager.OnCombatHit` applies that as an XP factor: `finalXp = baseXp * (1 + skillFactor * shotDifficultyFactor)`, where `skillFactor` is `0.5` for Bow and `1.0` for other ranged skills.
- `OnGainingRidingExperience(hero, baseXpAmount, horse)` awards separate Riding XP while mounted: `baseXpAmount * (1 + horse.Difficulty * 0.02)`. This is separate from `GetXpFromHit`, so horseback can increase total XP without being a direct combat-hit multiplier.

## Battle Troop XP

- `MapEvent.CommitXpGains` calls `MapEventSide.CommitXpGains`, which calls `MapEventParty.CommitXpGain` for each party.
- `MapEventParty.CommitXpGain` reads each `FlattenedTroopRosterElement.XpGained`, passes it through `DefaultPartyTrainingModel.CalculateXpGainFromBattles`, caps gainable XP with `MobilePartyHelper.CanTroopGainXp`, and writes regular troop XP through `TroopRoster.AddXpToTroop`.
- Any shared battle XP generated by `DefaultPartyTrainingModel.GenerateSharedXp` flows into `MobilePartyHelper.PartyAddSharedXp`.
- `DefaultPartyTrainingModel.GetXpReward(character)` returns `(level + 6)^2 / 3`.

## Troop XP Storage And Caps

- `TroopRoster.AddXpToTroop` delegates to `AddXpToTroopAtIndex`, then `SetElementXp`.
- `PartyBase.OnXpChanged` clamps prisoner XP against conformity needed for recruitment.
- For regular troops, XP is clamped against the largest upgrade XP cost available to that troop.
- `MobilePartyHelper.CanTroopGainXp` is the main helper for checking whether a troop can accept more XP.

## Other Sources

- Daily party and garrison training is under `DefaultPartyTrainingModel` and `DefaultDailyTroopXpBonusModel`.
- Discarded item donation XP is under `InventoryLogic` and `DefaultItemDiscardModel`.
- Healing skill XP is `DefaultPartyHealingModel.GetSkillXpFromHealingTroop`, currently a flat `5`.
- Smithing XP uses item value multipliers:
  - smelting: `0.02 * item value`
  - free-build smithing: `0.02 * item value`
  - crafting order smithing: `0.1 * item value`
  - refining: driven by the refining formula, with visible multiplier `0.3`
- Smithing part research and craft/smelt optimization notes are expanded in `Docs/notes/smithing.md`.
- Activity XP sources include alley XP, hideout roguery XP, tournament skill XP, workshop trade XP, persuasion XP, charm XP from relation gain, and companion quest reward XP.
