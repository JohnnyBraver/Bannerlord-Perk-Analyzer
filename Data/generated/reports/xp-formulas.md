# Bannerlord XP Formula Extraction

Generated: 2026-05-27T21:17:10.303640+03:00

This report is produced by `src/bannerlord_perk_analyzer/extract_xp_formulas.py`, which uses the local .NET extractor's `find-methods` command to search campaign, mission, and module assemblies for XP formula candidates.

## Confirmed Formula Leads

### Combat Hit And Kill XP

Source: `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetXpFromHit`

```text
effectiveDamage = min(damage, targetHp) + (targetHp if isFatal else 0)
baseXp = 0.4 * (attackerPower + 0.5) * (targetPower + 0.5) * effectiveDamage * missionTypeMultiplier
```

Constants found: `0, 0.4, 0.5, 1`

### Shot Difficulty XP

Mission-side source: `TaleWorlds.MountAndBlade.Mission.GetShootDifficulty`
Campaign-side source: `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetXpMultiplierFromShotDifficulty` and `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnCombatHit`

```text
rawDifficulty = 0.3 * ((distance + 4) / 4) * ((4 + lateralMotion * relativeSpeed) / 4)
shotDifficulty = clamp(rawDifficulty, 1, 12)
if isHeadShot: shotDifficulty *= 1.2
shotDifficultyFactor = lerp(0, 2, (min(shotDifficulty, 14.4) - 1) / 13.4)
finalXp = baseXp * (1 + skillFactor * shotDifficultyFactor)
skillFactor = 0.5 for Bow, 1.0 for other ranged skills
```

Mission constants found: `-1, 0, 0.3, 1, 1.2, 4, 12`
Campaign constants found: `0, 0.00001, 1, 2, 13.4, 14.4`

### Riding XP From Mounted Combat

Source: `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnGainingRidingExperience`

```text
ridingXp = baseXpAmount * (1 + horse.Difficulty * 0.02)
```

Constants found: `0.02, 1`

### Troop Battle XP Reward

Source: `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GetXpReward`

```text
troopBattleXpReward = (troopLevel + 6)^2 / 3
```

Constants found: `3, 6`

### Healing XP

Source: `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyHealingModel.GetSkillXpFromHealingTroop`

Constants found: `5`

The healing method is tiny in IL and should be decompiled or hand-read before turning the constant into prose.

### Hero Skill XP, Learning Rate, And Limits

Sources: `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.AddSkillXp`, `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.CalculateLearningLimit`, `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.CalculateLearningRate`

```text
genericXp = rawXp * GenericXpModel.GetXpMultiplier(hero)
skillXpDelta = genericXp * learningRate if isAffectedByFocusFactor else genericXp
peakLearningRange = max(0, 10 * (averageAttribute - 1)) + 30 * focus
skillLimit = peakLearningRange + 4 * averageAttribute + 10 * focus
learningRate starts at 1.25
learningRate factors include +0.4 * averageAttribute and +1.0 * focus
if currentSkill > peakLearningRange: over-limit factor is -1.0 - 0.1 * (currentSkill - peakLearningRange)
learningRate is clamped to at least 0
```

Learning constants found: `-1, 0, 0.1, 0.4, 1, 1.25`

### Troop XP Distribution And Upgrade Costs

Sources: `Helpers.MobilePartyHelper.CanTroopGainXp`, `Helpers.MobilePartyHelper.PartyAddSharedXp`, `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTroopUpgradeModel.GetXpCostForUpgrade`, `TaleWorlds.CampaignSystem.GameComponents.DefaultDailyTroopXpBonusModel.CalculateTroopXpBonusInternal`

```text
troopBattleXpReward = (troopLevel + 6)^2 / 3
upgradeCost sums each tier step from current tier + 1 through target tier
upgrade tier costs: <=1:100, 2:300, 3:550, 4:900, 5:1300, 6:1700, 7:2100
upgrade fallback per higher tier: int(1.333 * (targetLevel + 4)^2)
sharedXpCapacity is the remaining XP needed by stacks that can still upgrade
sharedXpAddedToStack = floor(max(1, remainingSharedXp * stackCapacity / remainingCapacity))
daily town troop XP starts from buildings plus RaiseTheMeek and ProjectileDeflection perk bonuses
```

Upgrade constants found: `0, 1, 1.333, 2, 3, 4, 5, 6, 7, 100, 300, 550, 900, 1300, 1700, 2100, ...`

### Travel And Simulation XP

Sources: `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnTravelOnFoot`, `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnTravelOnHorse`, `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnSimulationCombatKill`

```text
travelOnFootAthleticsXp = roundRandomized(0.2 * speed) + 1
travelOnHorseRidingXp = OnGainingRidingExperience(roundRandomized(0.3 * speed), horse)
simulationKillWeaponXp = GetXpReward(killedCharacter)
simulationKillMovementXp = roundRandomized(0.3 * simulationKillWeaponXp) to Riding if mounted, otherwise Athletics
simulationCommanderTacticsXp = ceil(0.02 * simulationKillWeaponXp) when a different valid commander party is present
```

Simulation constants found: `0, 0.02, 0.3`

### Smithing And Crafting Order XP

Sources: `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForRefining`, `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForSmelting`, `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForSmithingInCraftingOrderMode`, `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForSmithingInFreeBuildMode`, `TaleWorlds.CampaignSystem.CraftingSystem.CraftingOrder.GetOrderExperience`

```text
refiningXp = round(0.3 * outputMaterialValue * outputCount)
smeltingXp = round(0.02 * itemValue)
smithingCraftingOrderXp = round(0.1 * itemValue)
smithingFreeBuildXp = round(0.02 * itemValue)
craftingOrderBaseExperience = 0.25 * theoreticalMaxItemMarketValue(requestedDesignItem)
crafting order checks can halve the base and apply a clamped tier-difference factor
```

Smithing constants found: `0.3 | 0.02 | 0.1 | 0.02`
Crafting order constants found: `0, 0.25, 0.5, 1, 3`

### Activity XP Constants And Small Formulas

Sources: `TaleWorlds.CampaignSystem.GameComponents.DefaultTournamentModel.GetSkillXpGainFromTournament`, `TaleWorlds.CampaignSystem.GameComponents.DefaultHideoutModel.GetRogueryXpGainAsGhost`, `TaleWorlds.CampaignSystem.GameComponents.DefaultHideoutModel.GetRogueryXpGainOnHideoutMissionEnd`, `TaleWorlds.CampaignSystem.GameComponents.DefaultPersuasionModel.GetSkillXpFromPersuasion`, `TaleWorlds.CampaignSystem.GameComponents.DefaultWorkshopModel.GetTradeXpPerWarehouseProduction`, `TaleWorlds.CampaignSystem.GameComponents.DefaultDiplomacyModel.GetCharmExperienceFromRelationGain`

```text
tournamentXp = one random combat/movement skill from 5 equal 20% bands, amount 500
hideoutGhostRogueryXp = randomFloat(1000, 1400)
hideoutMissionRogueryXp = randomInt(700, 1000) on success, randomInt(225, 400) on failure
alleyInitialMainHeroXp = 1500; alleyDailyMainHeroXp = 40; alleyDailyAssignedClanMemberXp = 200
alleySuccessfulDefenseMainHeroXp = 6000
persuasionXp = difficultyEnumValue * 5 * argumentDifficultyBonusCoefficient
warehouseProductionTradeXp = 0.1 * productionBaseValue
charmRelationXp = round(relationChange * branchMultiplier), with branch multipliers built from 20, 10, 20, and 30
```

Alley constants found: `1500 | 40 | 200 | 6000`
Activity constants found: `0.2, 0.4, 0.6, 0.8, 500 | 1000, 1400 | 225, 400, 700, 1000 | 0, 1, 5 | 0.1 | 1, 10, 20, 30`

## Scan Groups

### Combat Hit, Kill, Shot, And Riding XP

- Includes the direct hit/kill XP model, mission-side shot difficulty, campaign shot-difficulty XP factor, and mounted Riding XP hook.
- Queries: `getxpfromhit, getbattlexpbonusfromperks, getxpfmultiplierformissiontype, getxpmultiplierfromshotdifficulty, getshootdifficulty, oncombathit, ongainingridingexperience`
- Methods scanned: 51215
- Methods matched in scan: 21

| Method | Constants | IL bytes | Matched queries |
| --- | --- | ---: | --- |
| `SandBox.Missions.MissionLogics.Arena.ArenaPracticeFightMissionController.EnemyHitReward` | 0, 1, 3 | 118 | oncombathit |
| `SandBox.Missions.MissionLogics.BattleAgentLogic.EnemyHitReward` | 0, 1, 3 | 518 | oncombathit |
| `SandBox.Tournaments.MissionLogics.TournamentFightMissionController.EnemyHitReward` | 0, 1, 2, 3 | 124 | oncombathit |
| `StoryMode.GameComponents.StoryModeCombatXpModel.GetXpFromHit` | 0 | 55 | getxpfromhit |
| `StoryMode.GameComponents.StoryModeCombatXpModel.GetXpMultiplierFromShotDifficulty` |  | 13 | getxpmultiplierfromshotdifficulty |
| `TaleWorlds.CampaignSystem.AgentOrigins.SimpleAgentOrigin.TaleWorlds.Core.IAgentOriginBase.OnScoreHit` | 0 | 112 | getxpfromhit |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnCombatHit` | 0, 0.02, 0.15, 0.5, 1, 1.5, 78 | 535 | getxpfromhit, getxpmultiplierfromshotdifficulty, oncombathit, ongainingridingexperience |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnGainingRidingExperience` | 0.02, 1 | 38 | ongainingridingexperience |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnSimulationCombatKill` | 0, 0.02, 0.3 | 255 | ongainingridingexperience |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnTravelOnHorse` | 0.3 | 46 | ongainingridingexperience |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.ISkillLevelingManager.OnCombatHit` |  | 0 | oncombathit |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.SkillLevelingManager.OnCombatHit` |  | 41 | oncombathit |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.CombatXpModel.GetXpFromHit` |  | 0 | getxpfromhit |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.CombatXpModel.GetXpMultiplierFromShotDifficulty` |  | 0 | getxpmultiplierfromshotdifficulty |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetBattleXpBonusFromPerks` | 0, 1 | 479 | getbattlexpbonusfromperks |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetXpFromHit` | 0, 0.4, 0.5, 1 | 297 | getxpfromhit, getbattlexpbonusfromperks, getxpfmultiplierformissiontype |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetXpMultiplierFromShotDifficulty` | 0, 0.00001, 1, 2, 13.4, 14.4 | 49 | getxpmultiplierfromshotdifficulty |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetXpfMultiplierForMissionType` | 0, 0.0625, 0.33, 0.9, 1, 2, 3, 4 | 67 | getxpfmultiplierformissiontype |
| `TaleWorlds.CampaignSystem.MapEvents.MapEventParty.OnTroopScoreHit` | 0, 3 | 158 | getxpfromhit |
| `TaleWorlds.MountAndBlade.Mission.GetShootDifficulty` | -1, 0, 0.3, 1, 1.2, 4, 12 | 170 | getshootdifficulty |
| `TaleWorlds.MountAndBlade.Mission.OnAgentHit` | -1, 0 | 345 | getshootdifficulty |

### Hero Skill XP, Learning, And Level Progression

- Captures the path from raw skill XP through learning-rate/focus scaling and skill/character level thresholds.
- Queries: `addskillxp, gainrawxp, getfocusfactor, calculatelearninglimit, calculatelearningrate, initializexprequiredforskilllevel, getxprequiredforskilllevel, getskilllevelchange, getxpamountforskilllevelchange, getxprequiredforlevel, skillsrequiredforlevel`
- Methods scanned: 27184
- Methods matched in scan: 61

| Method | Constants | IL bytes | Matched queries |
| --- | --- | ---: | --- |
| `TaleWorlds.CampaignSystem.AgentOrigins.SimpleAgentOrigin.TaleWorlds.Core.IAgentOriginBase.OnScoreHit` | 0 | 112 | getxpfromhit |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.CraftingCampaignBehavior.CreateCraftedWeaponInCraftingOrderMode` | 0 | 62 | addskillxp |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.CraftingCampaignBehavior.CreateCraftedWeaponInFreeBuildMode` | 1 | 55 | addskillxp |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.CraftingCampaignBehavior.DoRefinement` | 0 | 304 | addskillxp |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.CraftingCampaignBehavior.DoSmelting` | -1, 0, 1, 8 | 229 | addskillxp |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.MobilePartyTrainingBehavior.OnDailyTickParty` | 0, 2147483647 | 307 | addskillxp |
| `TaleWorlds.CampaignSystem.CampaignCheats.AddSkillXpToHero` | 0, 1, 2, 3, 4, 100, 300 | 2176 | addskillxp, getfocusfactor |
| `TaleWorlds.CampaignSystem.CharacterData.InitializeHeroFromCharacterData` | 0, 1, 2, 3, 4, 5, 6, 7, 12 | 1304 | getxprequiredforskilllevel |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnAIPartiesTravel` | 2, 3, 4, 5 | 54 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnAIPartyLootCasualties` | -1, 0, 0.15, 0.75, 1 | 84 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnAlleyCleared` |  | 36 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnBattleEnded` | 0.025, 0.05, 15 | 63 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnBoardGameWonAgainstLord` | 20, 50, 100 | 104 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnCombatHit` | 0, 0.02, 0.15, 0.5, 1, 1.5, 78 | 535 | getxpfromhit, getxpmultiplierfromshotdifficulty, oncombathit, ongainingridingexperience |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnDailyAlleyTick` |  | 79 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnGainingRidingExperience` | 0.02, 1 | 38 | ongainingridingexperience |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnHideoutClearedAsGhost` | 0, 1 | 169 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnHideoutMissionEnd` |  | 39 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnPartySkillExercised` |  | 20 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnPersonalSkillExercised` | 1 | 19 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnPersuasionSucceeded` | 0 | 42 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnPrisonBreakEnd` | 0 | 48 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnSettlementSkillExercised` |  | 68 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnSimulationCombatKill` | 0, 0.02, 0.3 | 255 | ongainingridingexperience |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnTravelOnFoot` | 0.2, 1 | 27 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnUpgradeTroops` | 0.025, 0.05, 15 | 94 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnWarehouseProduction` |  | 37 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.AddSkillXp` | 0 | 142 | addskillxp, gainrawxp, getfocusfactor, getskilllevelchange |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.AfterLoad` | 0 | 281 | skillsrequiredforlevel |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.ChangeSkillLevel` | 0, 1 | 144 | addskillxp, getxprequiredforskilllevel |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.CheckLevel` | 0, 1 | 92 | getxprequiredforlevel |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GainRawXp` |  | 92 | gainrawxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GetFocusFactor` | 0 | 61 | getfocusfactor, calculatelearningrate |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GetSkillXpProgress` |  | 48 | getxprequiredforskilllevel |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GetXpRequiredForLevel` |  | 22 | getxprequiredforlevel, skillsrequiredforlevel |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.InitializeSkillXp` |  | 43 | getxprequiredforskilllevel |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.SetInitialLevel` | 1 | 18 | getxprequiredforlevel |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.SetInitialSkillLevel` |  | 52 | getxprequiredforskilllevel |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.CalculateLearningLimit` |  | 0 | calculatelearninglimit |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.CalculateLearningRate` |  | 0 | calculatelearningrate |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.GetSkillLevelChange` |  | 0 | getskilllevelchange |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.GetXpAmountForSkillLevelChange` |  | 0 | getxpamountforskilllevelchange |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.GetXpRequiredForSkillLevel` |  | 0 | getxprequiredforskilllevel |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.SkillsRequiredForLevel` |  | 0 | skillsrequiredforlevel |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel..ctor` | 63, 1024 | 48 | initializexprequiredforskilllevel, skillsrequiredforlevel |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.CalculateLearningLimit` | 0, 1, 10, 30 | 150 | calculatelearninglimit |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.CalculateLearningRate` | -1, 0, 0.1, 0.4, 1, 1.25 | 216 | calculatelearninglimit, calculatelearningrate |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.GetNextAttributeToUpgrade` | -340282346638528859811704183484516925440, 0, 1, 75, 340282346638528859811704183484516925440 | 430 | calculatelearninglimit |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.GetNextSkillToAddFocus` | -340282346638528859811704183484516925440, 0 | 144 | calculatelearninglimit |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.GetSkillLevelChange` | 0, 1, 1023, 1024 | 78 | getxprequiredforskilllevel, getskilllevelchange |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.GetXpAmountForSkillLevelChange` | 1 | 46 | getxprequiredforskilllevel, getxpamountforskilllevelchange |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.GetXpRequiredForSkillLevel` | 0, 1, 1024 | 32 | getxprequiredforskilllevel |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.InitializeSkillsRequiredForLevel` | 0, 1, 2, 5, 1000 | 71 | skillsrequiredforlevel |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.InitializeXpRequiredForSkillLevel` | 0, 0.3, 1, 10, 30, 1024 | 117 | initializexprequiredforskilllevel |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.SkillsRequiredForLevel` | 62 | 35 | skillsrequiredforlevel |
| `TaleWorlds.CampaignSystem.Hero.AddSkillXp` | 1 | 21 | addskillxp |
| `TaleWorlds.CampaignSystem.Incidents.IncidentEffect+<>c__DisplayClass17_0.<SkillChange>b__1` | 0, 1 | 208 | addskillxp, calculatelearningrate |
| `TaleWorlds.CampaignSystem.Incidents.IncidentEffect+<>c__DisplayClass17_0.<SkillChange>b__2` | 0, 1, 100 | 233 | calculatelearningrate |
| `TaleWorlds.CampaignSystem.Issues.CaravanAmbushIssueBehavior+CaravanAmbushIssue.AlternativeSolutionEndWithSuccessConsequence` | 0.33, 0.66, 1, 3, 5, 600, 800 | 144 | addskillxp |
| `TaleWorlds.CampaignSystem.Issues.IssueBase.AlternativeSolutionEndWithSuccess` | 0, 0.1, 0.5, 0.9, 1, 1.2, 2, 3, 4, 12, 17592186044416 | 913 | addskillxp |
| `TaleWorlds.CampaignSystem.TournamentGames.TournamentManager.SimulateTournament` | -1, 0.25, 0.75, 1 | 171 | addskillxp |

### Troop XP, Shared XP, Upgrade Costs, And Daily Training

- Covers battle troop XP conversion, shared party XP distribution, upgrade XP caps/costs, and garrison/daily training bonuses.
- Queries: `getxpreward, generatesharedxp, calculatexpgainfrombattles, geteffectivedailyexperience, getperkexperiencesfortroops, cantroopgainxp, partyaddsharedxp, getmaximumxpamountpartycanget, addxptotroop, getxpcostforupgrade, getskillxpfromupgradingtroops, calculatedailytroopxpbonus, calculatetroopxpbonusinternal, calculategarrisonxpbonusmultiplier`
- Methods scanned: 27184
- Methods matched in scan: 43

| Method | Constants | IL bytes | Matched queries |
| --- | --- | ---: | --- |
| `Helpers.MobilePartyHelper.CanTroopGainXp` | 0, 1, 3843 | 147 | cantroopgainxp |
| `Helpers.MobilePartyHelper.GetMaximumXpAmountPartyCanGet` | 0, 1 | 62 | cantroopgainxp, getmaximumxpamountpartycanget |
| `Helpers.MobilePartyHelper.PartyAddSharedXp` | 0, 1 | 173 | cantroopgainxp, partyaddsharedxp, addxptotroop |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.BattleCampaignBehavior.OnHeroCombatHit` | 0, 1 | 146 | addxptotroop |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.CampaignBattleRecoveryBehavior.GiveTroopXp` |  | 22 | addxptotroop |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.DiscardItemsCampaignBehavior.OnItemsDiscardedByPlayer` | 0 | 44 | partyaddsharedxp |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.GarrisonRecruitmentCampaignBehavior.HandleGarrisonXpChange` | 0 | 146 | addxptotroop, calculatedailytroopxpbonus, calculategarrisonxpbonusmultiplier |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.MobilePartyTrainingBehavior.OnDailyTickParty` | 0, 2147483647 | 307 | addskillxp |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.RecruitPrisonersCampaignBehavior.GenerateConformityForTroop` | 1 | 53 | addxptotroop |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.RecruitmentCampaignBehavior.OnTroopRecruited` | 15 | 109 | addxptotroop |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.RecruitmentCampaignBehavior.OnUnitRecruited` | 15 | 86 | addxptotroop |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.SiegeEventCampaignBehavior.OnSiegeEngineBuilt` | 0, 1 | 129 | addxptotroop |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnSimulationCombatKill` | 0, 0.02, 0.3 | 255 | ongainingridingexperience |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnUpgradeTroops` | 0.025, 0.05, 15 | 94 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterObject.GetUpgradeXpCost` | 0 | 50 | getxpcostforupgrade |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.DailyTroopXpBonusModel.CalculateDailyTroopXpBonus` |  | 0 | calculatedailytroopxpbonus |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.DailyTroopXpBonusModel.CalculateGarrisonXpBonusMultiplier` |  | 0 | calculategarrisonxpbonusmultiplier |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.PartyTrainingModel.CalculateXpGainFromBattles` |  | 0 | calculatexpgainfrombattles |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.PartyTrainingModel.GenerateSharedXp` |  | 0 | generatesharedxp |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.PartyTrainingModel.GetEffectiveDailyExperience` |  | 0 | geteffectivedailyexperience |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.PartyTrainingModel.GetXpReward` |  | 0 | getxpreward |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.PartyTroopUpgradeModel.GetSkillXpFromUpgradingTroops` |  | 0 | getskillxpfromupgradingtroops |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.PartyTroopUpgradeModel.GetXpCostForUpgrade` |  | 0 | getxpcostforupgrade |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultDailyTroopXpBonusModel.CalculateDailyTroopXpBonus` |  | 8 | calculatedailytroopxpbonus, calculatetroopxpbonusinternal |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultDailyTroopXpBonusModel.CalculateGarrisonXpBonusMultiplier` | 1 | 6 | calculategarrisonxpbonusmultiplier |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultDailyTroopXpBonusModel.CalculateTroopXpBonusInternal` | 0, 11 | 59 | calculatetroopxpbonusinternal |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.CalculateXpGainFromBattles` | 0 | 86 | calculatexpgainfrombattles |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GenerateSharedXp` | 0 | 110 | generatesharedxp |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GetEffectiveDailyExperience` | 0, 1, 2, 3, 4, 10, 15, 75 | 1072 | geteffectivedailyexperience, getperkexperiencesfortroops |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GetPerkExperiencesForTroops` | 0 | 114 | getperkexperiencesfortroops |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GetXpReward` | 3, 6 | 13 | getxpreward |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTroopUpgradeModel.GetSkillXpFromUpgradingTroops` | 10 | 12 | getskillxpfromupgradingtroops |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTroopUpgradeModel.GetXpCostForUpgrade` | 0, 1, 1.333, 2, 3, 4, 5, 6, 7, 100, 300, 550, ... | 178 | getxpcostforupgrade |
| `TaleWorlds.CampaignSystem.Incidents.IncidentEffect+<>c__DisplayClass50_0.<PartyExperienceChance>b__0` |  | 60 | partyaddsharedxp |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.DonateItem` | -1, 0, 1, 12, 100, 17592186044416 | 296 | addxptotroop |
| `TaleWorlds.CampaignSystem.MapEvents.MapEventParty.CommitXpGain` | 0 | 491 | generatesharedxp, calculatexpgainfrombattles, cantroopgainxp, partyaddsharedxp, addxptotroop |
| `TaleWorlds.CampaignSystem.Party.PartyScreenLogic+<>c__DisplayClass161_0.<TransferTroop>b__0` |  | 33 | getxpcostforupgrade |
| `TaleWorlds.CampaignSystem.Party.PartyScreenLogic.RecruitPrisoner` | -1, 0, 1 | 246 | addxptotroop |
| `TaleWorlds.CampaignSystem.Party.PartyScreenLogic.TransferTroopToLeaderSlot` | 0, 1 | 274 | addxptotroop |
| `TaleWorlds.CampaignSystem.Party.PartyScreenLogic.TransferTroop` | -1, 0, 1, 2, 6 | 1396 | addxptotroop |
| `TaleWorlds.CampaignSystem.Roster.TroopRoster.AddXpToTroopAtIndex` | 0 | 49 | addxptotroop |
| `TaleWorlds.CampaignSystem.Roster.TroopRoster.AddXpToTroop` |  | 17 | addxptotroop |
| `TaleWorlds.CampaignSystem.TroopUpgradeTracker.CalculateReadyToUpgradeSafe` | 0, 1 | 264 | cantroopgainxp |

### Smithing, Crafting Orders, And Item Discard XP

- Covers smithing/free-build/refine/smelt/order constants and donation/discard XP conversions.
- Queries: `getskillxpforsmithing, getskillxpforrefining, getskillxpforsmelting, getorderexperience, getxpbonusfordiscardingitem, getxpbonusfordiscardingitems, xpgainfromdonations, donationxpchange`
- Methods scanned: 27184
- Methods matched in scan: 26

| Method | Constants | IL bytes | Matched queries |
| --- | --- | ---: | --- |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.CraftingCampaignBehavior.CreateCraftedWeaponInCraftingOrderMode` | 0 | 62 | addskillxp |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.CraftingCampaignBehavior.CreateCraftedWeaponInFreeBuildMode` | 1 | 55 | addskillxp |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.CraftingCampaignBehavior.DoRefinement` | 0 | 304 | addskillxp |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.CraftingCampaignBehavior.DoSmelting` | -1, 0, 1, 8 | 229 | addskillxp |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.DiscardItemsCampaignBehavior.OnItemsDiscardedByPlayer` | 0 | 44 | partyaddsharedxp |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.ItemDiscardModel.GetXpBonusForDiscardingItems` |  | 0 | getxpbonusfordiscardingitem, getxpbonusfordiscardingitems |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.ItemDiscardModel.GetXpBonusForDiscardingItem` |  | 0 | getxpbonusfordiscardingitem |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.SmithingModel.GetSkillXpForRefining` |  | 0 | getskillxpforrefining |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.SmithingModel.GetSkillXpForSmelting` |  | 0 | getskillxpforsmelting |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.SmithingModel.GetSkillXpForSmithingInCraftingOrderMode` |  | 0 | getskillxpforsmithing |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.SmithingModel.GetSkillXpForSmithingInFreeBuildMode` |  | 0 | getskillxpforsmithing |
| `TaleWorlds.CampaignSystem.CraftingSystem.CraftingOrder.GetOrderExperience` | 0, 0.25, 0.5, 1, 3 | 131 | getorderexperience |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultItemDiscardModel.GetXpBonusForDiscardingItems` | 0, 1 | 56 | getxpbonusfordiscardingitem, getxpbonusfordiscardingitems |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultItemDiscardModel.GetXpBonusForDiscardingItem` | 0, 35, 75, 150, 250, 300 | 86 | getxpbonusfordiscardingitem |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForRefining` | 0.3 | 39 | getskillxpforrefining |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForSmelting` | 0.02 | 19 | getskillxpforsmelting |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForSmithingInCraftingOrderMode` | 0.1 | 19 | getskillxpforsmithing |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForSmithingInFreeBuildMode` | 0.02 | 19 | getskillxpforsmithing |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.HandleDonationOnTransferItem` | -1, 1 | 81 | getxpbonusfordiscardingitem, xpgainfromdonations |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.InitializeXpGainFromDonations` | 0, 2 | 66 | getxpbonusfordiscardingitem, getxpbonusfordiscardingitems, xpgainfromdonations |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.Initialize` | 0, 1, 2, 4 | 230 | xpgainfromdonations |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.ResetLogic` | 0, 1, 2, 12, 17592186044416 | 156 | xpgainfromdonations |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.get_DonationXpChange` |  | 7 | donationxpchange |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.get_XpGainFromDonations` |  | 7 | xpgainfromdonations |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.set_DonationXpChange` |  | 8 | donationxpchange |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.set_XpGainFromDonations` | 0 | 57 | xpgainfromdonations, donationxpchange |

### Activity, Quest, Tournament, Persuasion, Hideout, Alley, And Healing XP

- Collects non-combat and quest/activity XP methods. Many issue rewards are simple constants multiplied by issue difficulty.
- Queries: `getskillxpfromhealingtroop, getskillxpgainfromtournament, getskillxpfrompersuasion, getrogueryxpgain, getcharmexperience, gettradexp, getdailyxpgain, getinitialxpgain, getxpgainaftersuccessfulalleydefenseformainhero, partyexperiencechance, companionskillrewardxp`
- Methods scanned: 34244
- Methods matched in scan: 71

| Method | Constants | IL bytes | Matched queries |
| --- | --- | ---: | --- |
| `SandBox.CampaignBehaviors.AlleyCampaignBehavior+PlayerAlleyData.AlleyFightWon` | -1, 0, 0.2, 1 | 157 | getxpgainaftersuccessfulalleydefenseformainhero |
| `SandBox.Issues.FamilyFeudIssueBehavior+FamilyFeudIssue.get_CompanionSkillRewardXP` | 500, 700 | 20 | companionskillrewardxp |
| `SandBox.Issues.NotableWantsDaughterFoundIssueBehavior+NotableWantsDaughterFoundIssue.get_CompanionSkillRewardXP` | 500, 1000 | 20 | companionskillrewardxp |
| `SandBox.Issues.ProdigalSonIssueBehavior+ProdigalSonIssue.get_CompanionSkillRewardXP` | 700, 900 | 20 | companionskillrewardxp |
| `SandBox.Issues.RivalGangMovingInIssueBehavior+RivalGangMovingInIssue.get_CompanionSkillRewardXP` | 750, 1000 | 20 | companionskillrewardxp |
| `SandBox.Issues.RuralNotableInnAndOutIssueBehavior+RuralNotableInnAndOutIssue.get_CompanionSkillRewardXP` | 500, 1000 | 20 | companionskillrewardxp |
| `SandBox.Issues.SnareTheWealthyIssueBehavior+SnareTheWealthyIssue.get_CompanionSkillRewardXP` | 800, 1000 | 20 | companionskillrewardxp |
| `SandBox.Issues.TheSpyPartyIssueQuestBehavior+TheSpyPartyIssue.get_CompanionSkillRewardXP` | 600, 800 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.IncidentsCampaignBehaviour.InitializeIncidents` | -300, -200, -150, -100, -50, -20, -15, -10, -5, -3, -2, -1, ... | 35642 | partyexperiencechance |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnAlleyCleared` |  | 36 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnDailyAlleyTick` |  | 79 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnGainRelation` | 0, 1, 5 | 90 | getcharmexperience |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnHeroHealedWhileWaiting` | 0.1, 0.2, 1, 7 | 160 | getskillxpfromhealingtroop |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnHideoutClearedAsGhost` | 0, 1 | 169 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnHideoutMissionEnd` |  | 39 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnPersuasionSucceeded` | 0 | 42 | addskillxp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnRegularTroopHealedWhileWaiting` | 1, 2, 7 | 84 | getskillxpfromhealingtroop |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnWarehouseProduction` |  | 37 | addskillxp |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.AlleyModel.GetDailyXpGainForAssignedClanMember` |  | 0 | getdailyxpgain |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.AlleyModel.GetDailyXpGainForMainHero` |  | 0 | getdailyxpgain |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.AlleyModel.GetInitialXpGainForMainHero` |  | 0 | getinitialxpgain |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.AlleyModel.GetXpGainAfterSuccessfulAlleyDefenseForMainHero` |  | 0 | getxpgainaftersuccessfulalleydefenseformainhero |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.DiplomacyModel.GetCharmExperienceFromRelationGain` |  | 0 | getcharmexperience |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.HideoutModel.GetRogueryXpGainAsGhost` |  | 0 | getrogueryxpgain |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.HideoutModel.GetRogueryXpGainOnHideoutMissionEnd` |  | 0 | getrogueryxpgain |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.PartyHealingModel.GetSkillXpFromHealingTroop` |  | 0 | getskillxpfromhealingtroop |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.PersuasionModel.GetSkillXpFromPersuasion` |  | 0 | getskillxpfrompersuasion |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.TournamentModel.GetSkillXpGainFromTournament` |  | 0 | getskillxpgainfromtournament |
| `TaleWorlds.CampaignSystem.ComponentInterfaces.WorkshopModel.GetTradeXpPerWarehouseProduction` |  | 0 | gettradexp |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultAlleyModel.GetDailyXpGainForAssignedClanMember` | 200 | 6 | getdailyxpgain |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultAlleyModel.GetDailyXpGainForMainHero` | 40 | 6 | getdailyxpgain |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultAlleyModel.GetInitialXpGainForMainHero` | 1500 | 6 | getinitialxpgain |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultAlleyModel.GetXpGainAfterSuccessfulAlleyDefenseForMainHero` | 6000 | 6 | getxpgainaftersuccessfulalleydefenseformainhero |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultDiplomacyModel.GetCharmExperienceFromRelationGain` | 1, 10, 20, 30 | 184 | getcharmexperience |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultHideoutModel.GetRogueryXpGainAsGhost` | 1000, 1400 | 16 | getrogueryxpgain |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultHideoutModel.GetRogueryXpGainOnHideoutMissionEnd` | 225, 400, 700, 1000 | 37 | getrogueryxpgain |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyHealingModel.GetSkillXpFromHealingTroop` | 5 | 2 | getskillxpfromhealingtroop |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPersuasionModel.GetSkillXpFromPersuasion` | 0, 1, 5 | 10 | getskillxpfrompersuasion |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultTournamentModel.GetSkillXpGainFromTournament` | 0.2, 0.4, 0.6, 0.8, 500 | 84 | getskillxpgainfromtournament |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultWorkshopModel.GetTradeXpPerWarehouseProduction` | 0.1 | 15 | gettradexp |
| `TaleWorlds.CampaignSystem.Incidents.IncidentEffect+<>c__DisplayClass50_0.<PartyExperienceChance>b__0` |  | 60 | partyaddsharedxp |
| `TaleWorlds.CampaignSystem.Incidents.IncidentEffect+<>c__DisplayClass50_0.<PartyExperienceChance>b__1` | 1, 100 | 99 | partyexperiencechance |
| `TaleWorlds.CampaignSystem.Incidents.IncidentEffect.PartyExperienceChance` |  | 44 | partyexperiencechance |
| `TaleWorlds.CampaignSystem.Issues.ArtisanCantSellProductsAtAFairPriceIssueBehavior+ArtisanCantSellProductsAtAFairPriceIssue.get_CompanionSkillRewardXP` | 400, 1700 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.ArtisanOverpricedGoodsIssueBehavior+ArtisanOverpricedGoodsIssue.get_CompanionSkillRewardXP` | 400, 1700 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.CapturedByBountyHuntersIssueBehavior+CapturedByBountyHuntersIssue.get_CompanionSkillRewardXP` | 750, 1000 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.CaravanAmbushIssueBehavior+CaravanAmbushIssue.get_CompanionSkillRewardXP` | 600, 800 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.EscortMerchantCaravanIssueBehavior+EscortMerchantCaravanIssue.get_CompanionSkillRewardXP` | 800, 1000 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.ExtortionByDesertersIssueBehavior+ExtortionByDesertersIssue.get_CompanionSkillRewardXP` | 800, 1000 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.GangLeaderNeedsRecruitsIssueBehavior+GangLeaderNeedsRecruitsIssue.get_CompanionSkillRewardXP` | 500, 700 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.GangLeaderNeedsToOffloadStolenGoodsIssueBehavior+GangLeaderNeedsToOffloadStolenGoodsIssue.get_CompanionSkillRewardXP` | 1000, 1250 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.GangLeaderNeedsWeaponsIssueQuestBehavior+GangLeaderNeedsWeaponsIssue.get_CompanionSkillRewardXP` | 800, 900 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.HeadmanNeedsGrainIssueBehavior+HeadmanNeedsGrainIssue.get_CompanionSkillRewardXP` | 500, 700 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.HeadmanNeedsToDeliverAHerdIssueBehavior+HeadmanNeedsToDeliverAHerdIssue.get_CompanionSkillRewardXP` | 500, 700 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.HeadmanVillageNeedsDraughtAnimalsIssueBehavior+HeadmanVillageNeedsDraughtAnimalsIssue.get_CompanionSkillRewardXP` | 500, 700 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.IssueBase.AlternativeSolutionEndWithSuccess` | 0, 0.1, 0.5, 0.9, 1, 1.2, 2, 3, 4, 12, 17592186044416 | 913 | addskillxp |
| `TaleWorlds.CampaignSystem.Issues.IssueBase.get_CompanionSkillRewardXP` |  | 7 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.LandLordNeedsManualLaborersIssueBehavior+LandLordNeedsManualLaborersIssue.get_CompanionSkillRewardXP` | 500, 700 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.LandLordTheArtOfTheTradeIssueBehavior+LandLordTheArtOfTheTradeIssue.get_CompanionSkillRewardXP` | 800, 900 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.LandlordNeedsAccessToVillageCommonsIssueBehavior+LandlordNeedsAccessToVillageCommonsIssue.get_CompanionSkillRewardXP` | 700, 900 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.LandlordTrainingForRetainersIssueBehavior+LandlordTrainingForRetainersIssue.get_CompanionSkillRewardXP` | 500, 700 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.LesserNobleRevoltIssueBehavior+LesserNobleRevoltIssue.get_CompanionSkillRewardXP` | 800, 1000 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.LordNeedsGarrisonTroopsIssueQuestBehavior+LordNeedsGarrisonTroopsIssue.get_CompanionSkillRewardXP` | 800, 900 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.LordNeedsHorsesIssueBehavior+LordNeedsHorsesIssue.get_CompanionSkillRewardXP` | 500, 700 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.MerchantArmyOfPoachersIssueBehavior+MerchantArmyOfPoachersIssue.get_CompanionSkillRewardXP` | 800, 1000 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.MerchantNeedsHelpWithOutlawsIssueQuestBehavior+MerchantNeedsHelpWithOutlawsIssue.get_CompanionSkillRewardXP` | 600, 800 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.NearbyBanditBaseIssueBehavior+NearbyBanditBaseIssue.get_CompanionSkillRewardXP` | 1000, 1250 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.SmugglersIssueBehavior+SmugglersIssue.get_CompanionSkillRewardXP` | 500, 1000 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.VillageNeedsCraftingMaterialsIssueBehavior+VillageNeedsCraftingMaterialsIssue.get_CompanionSkillRewardXP` | 500, 700 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.Issues.VillageNeedsToolsIssueBehavior+VillageNeedsToolsIssue.get_CompanionSkillRewardXP` | 500, 700 | 20 | companionskillrewardxp |
| `TaleWorlds.CampaignSystem.TournamentGames.TournamentManager.SimulateTournament` | -1, 0.25, 0.75, 1 | 171 | addskillxp |

## Outputs

- JSON: `Data\generated\xp-formula-methods.json`
- Report: `Data\generated\reports\xp-formulas.md`
