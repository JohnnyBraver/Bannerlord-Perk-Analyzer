# Bannerlord XP Award Extraction

Generated: 2026-05-27T16:43:26.6588230+03:00

This report is extracted from local compiled assemblies. It is a map of XP-related model methods, constants, and XP-relevant references, not source comments or decompiled C#.

## Inputs

- Game root: local path omitted; provided by `-GameRoot` or `BANNERLORD_GAME_ROOT`
- Assemblies loaded: `TaleWorlds.Core`, `TaleWorlds.CampaignSystem`
- Methods scanned: 30359
- XP-related methods matched: 123
- Deep caller scan: False
- Include abstract contracts: False

## Reading Notes

- `hero progression` is where hero skill XP is accepted, scaled, and converted into skill levels and character levels.
- `combat xp` covers hit/kill XP and perk bonuses applied to battle XP.
- `troop xp` covers shared party XP, daily training XP, troop roster XP, and upgrade-related XP.
- `activity xp` covers non-combat sources such as charm, persuasion, tournaments, workshops, alleys, and hideouts.
- Numeric constants are raw IL constants. Some are formula values; some are indexes, enum values, or branch helpers, so they need review before becoming prose.
- Run with `-DeepScanCallers` to inspect every method body for calls into XP sinks. That is slower, especially if extra assemblies are included.

## High-Signal Entry Points

- `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.AddSkillXp` (hero progression, IL bytes: 142)
- `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GainRawXp` (hero progression, IL bytes: 92)
- `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.CalculateLearningRate` (hero progression, IL bytes: 216)
- `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetXpFromHit` (combat xp, IL bytes: 297)
- `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetBattleXpBonusFromPerks` (combat xp, IL bytes: 479)
- `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GetEffectiveDailyExperience` (troop xp, IL bytes: 1072)
- `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GenerateSharedXp` (troop xp, IL bytes: 110)
- `Helpers.MobilePartyHelper.CanTroopGainXp` (troop xp, IL bytes: 147)
- `Helpers.MobilePartyHelper.PartyAddSharedXp` (troop xp, IL bytes: 173)
- `TaleWorlds.CampaignSystem.MapEvents.MapEventParty.CommitXpGain` (combat xp, IL bytes: 491)
- `TaleWorlds.CampaignSystem.CampaignBehaviors.CampaignBattleRecoveryBehavior.GiveTroopXp` (troop xp, IL bytes: 22)
- `TaleWorlds.CampaignSystem.Roster.TroopRoster.AddXpToTroop` (troop xp, IL bytes: 17)

## Hero progression

| Method | IL bytes | Constants | XP references |
| --- | ---: | --- | --- |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GetSkillXpProgress` | 48 |  | TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.get_Hero()<br>TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GetSkillXp(TaleWorlds.Core.SkillObject)<br>TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.GetXpRequiredForSkillLevel(System.Int32) |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GetSkillXp` | 55 | 0, 55 | TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper._skillXps |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.AddSkillXp` | 142 | 0 | TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.ChangeSkillLevelFromXpChange(TaleWorlds.Core.SkillObject, System.Int32, System.Boolean)<br>TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GainRawXp(System.Single, System.Boolean)<br>TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.get_Hero()<br>TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GetFocusFactor(TaleWorlds.Core.SkillObject)<br>TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GetSkillXp(TaleWorlds.Core.SkillObject)<br>... |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.set_TotalXp` | 8 |  | TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper._totalXp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.get_TotalXp` | 7 |  | TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper._totalXp |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GainRawXp` | 92 |  | TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper._totalXp<br>TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.CheckLevel(System.Boolean)<br>TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.get_TotalXp()<br>TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.set_TotalXp(System.Int32) |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.SetSkillXp` | 60 | 0, 1E-05 | TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper._skillXps |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultSkillLevelingManager.OnGainingRidingExperience` | 38 | 0.02, 1 | TaleWorlds.CampaignSystem.Hero.AddSkillXp(TaleWorlds.Core.SkillObject, System.Single) |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.TraitLevelingHelper.UpdateTraitXPAccordingToTraitLevels` | 102 |  | TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.GetTraitXpRequiredForTraitLevel(TaleWorlds.CampaignSystem.CharacterDevelopment.TraitObject, System.Int32) |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.InitializeSkillXp` | 43 |  | TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.get_Hero()<br>TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.SetSkillXp(TaleWorlds.Core.PropertyObject, System.Single)<br>TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.GetXpRequiredForSkillLevel(System.Int32) |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.ChangeSkillLevelFromXpChange` | 51 |  | TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.get_Hero() |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.ResetTotalXpForPlayerCharacter` | 8 | 0 | TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.set_TotalXp(System.Int32) |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GetXpRequiredForLevel` | 22 |  |  |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.TraitLevelingHelper.AddPlayerTraitXPAndLogEntry` | 69 | 10 | TaleWorlds.CampaignSystem.CharacterDevelopment.TraitLevelingHelper.AddTraitXp(TaleWorlds.CampaignSystem.CharacterDevelopment.TraitObject, System.Int32) |
| `TaleWorlds.CampaignSystem.CharacterDevelopment.TraitLevelingHelper.AddTraitXp` | 95 |  | TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.GetTraitLevelForTraitXp(TaleWorlds.CampaignSystem.Hero, TaleWorlds.CampaignSystem.CharacterDevelopment.TraitObject, System.Int32, System.Int32&, System.Int32&) |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.InitializeSkillsRequiredForLevel` | 71 | 0, 1, 2, 5, 1000 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.InitializeXpRequiredForSkillLevel` | 117 | 0, 0.3, 1, 10, 30, 1024 | TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel._xpRequiredForSkillLevel |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.SkillsRequiredForLevel` | 35 | 62 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.GetMaxSkillPoint` | 6 | 2147483647 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.GetTraitXpRequiredForTraitLevel` | 41 | -4000, -1000, -1, 0, 1, 1000, 4000 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.CalculateLearningLimit` | 150 | 0, 1, 10, 30 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.CalculateLearningRate` | 216 | -1, 0, 0.1, 0.4, 1, 1.25 | TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.CalculateLearningLimit(TaleWorlds.Core.IReadOnlyPropertyOwner<TaleWorlds.Core.CharacterAttribute>, System.Int32, TaleWorlds.Core.SkillObject, System.Boolean) |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.GetTraitLevelForTraitXp` | 189 | -6000, -4000, -2500, -1000, -2, -1, 0, 1, 2, 1000, 2500, 4000, ... |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.GetXpRequiredForSkillLevel` | 32 | 0, 1, 1024 | TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel._xpRequiredForSkillLevel |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.GetSkillLevelChange` | 78 | 0, 1, 1023, 1024 | TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.GetXpRequiredForSkillLevel(System.Int32) |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterDevelopmentModel.GetXpAmountForSkillLevelChange` | 46 | 1 | TaleWorlds.CampaignSystem.ComponentInterfaces.CharacterDevelopmentModel.GetXpRequiredForSkillLevel(System.Int32) |
| `TaleWorlds.CampaignSystem.CampaignCheats.AddSkillXpToHero` | 2176 | 0, 1, 2, 3, 4, 100, 300 | TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.AddSkillXp(TaleWorlds.Core.SkillObject, System.Single, System.Boolean, System.Boolean)<br>TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.GetFocusFactor(TaleWorlds.Core.SkillObject)<br>TaleWorlds.CampaignSystem.Hero.get_HeroDeveloper() |
| `TaleWorlds.CampaignSystem.Hero.AddSkillXp` | 21 | 1 | TaleWorlds.CampaignSystem.CharacterDevelopment.HeroDeveloper.AddSkillXp(TaleWorlds.Core.SkillObject, System.Single, System.Boolean, System.Boolean) |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultSiegeAftermathModel.GetSiegeAftermathTraitXpChangeForPlayer` | 53 | -50, -30, 0, 2, 10, 20 |  |

## Combat xp

| Method | IL bytes | Constants | XP references |
| --- | ---: | --- | --- |
| `TaleWorlds.CampaignSystem.MapEvents.MapEventSide.CommitXpGains` | 52 |  | TaleWorlds.CampaignSystem.MapEvents.MapEventParty.CommitXpGain() |
| `TaleWorlds.CampaignSystem.MapEvents.MapEvent.CommitXpGains` | 30 | 0, 1 | TaleWorlds.CampaignSystem.MapEvents.MapEventSide.CommitXpGains() |
| `TaleWorlds.CampaignSystem.MapEvents.MapEventParty.CommitXpGain` | 491 | 0 | Helpers.MobilePartyHelper.CanTroopGainXp(TaleWorlds.CampaignSystem.Party.PartyBase, TaleWorlds.CampaignSystem.CharacterObject, System.Int32&)<br>Helpers.MobilePartyHelper.PartyAddSharedXp(TaleWorlds.CampaignSystem.Party.MobileParty, System.Single)<br>System.Collections.Generic.IEnumerator<TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement>.get_Current()<br>TaleWorlds.CampaignSystem.CharacterDevelopment.SkillLevelingManager.OnBattleEnded(TaleWorlds.CampaignSystem.Party.PartyBase, TaleWorlds.CampaignSystem.CharacterObject, System.Int32)<br>TaleWorlds.CampaignSystem.ComponentInterfaces.PartyTrainingModel.CalculateXpGainFromBattles(TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement, TaleWorlds.CampaignSystem.Party.PartyBase)<br>... |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetSkillForWeapon` | 29 |  |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetBattleXpBonusFromPerks` | 479 | 0, 1 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.get_CaptainRadius` | 6 | 10 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetXpFromHit` | 297 | 0, 0.4, 0.5, 1 | TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetBattleXpBonusFromPerks(TaleWorlds.CampaignSystem.Party.PartyBase, TaleWorlds.CampaignSystem.ExplainedNumber&, TaleWorlds.CampaignSystem.CharacterObject)<br>TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetXpfMultiplierForMissionType(TaleWorlds.CampaignSystem.ComponentInterfaces.CombatXpModel+MissionTypeEnum) |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetXpfMultiplierForMissionType` | 67 | 0, 0.0625, 0.33, 0.9, 1, 2, 3, 4 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultCombatXpModel.GetXpMultiplierFromShotDifficulty` | 49 | 0, 1E-05, 1, 2, 13.4, 14.4 |  |

## Troop xp

| Method | IL bytes | Constants | XP references |
| --- | ---: | --- | --- |
| `TaleWorlds.CampaignSystem.Roster.TroopRoster.AddXpToTroop` | 17 |  | TaleWorlds.CampaignSystem.Roster.TroopRoster.AddXpToTroopAtIndex(System.Int32, System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.FindIndexOfTroop(TaleWorlds.CampaignSystem.CharacterObject) |
| `TaleWorlds.CampaignSystem.Roster.TroopRoster.AddXpToTroopAtIndex` | 49 | 0 | TaleWorlds.CampaignSystem.Roster.TroopRoster._count<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.data<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.GetElementXp(TaleWorlds.CampaignSystem.CharacterObject)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.SetElementXp(System.Int32, System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement<br>... |
| `TaleWorlds.CampaignSystem.Roster.FlattenedTroopRoster.OnTroopGainXp` | 70 |  | System.Collections.Generic.Dictionary<TaleWorlds.Core.UniqueTroopDescriptor, TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement>.get_Item(TaleWorlds.Core.UniqueTroopDescriptor)<br>System.Collections.Generic.Dictionary<TaleWorlds.Core.UniqueTroopDescriptor, TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement>.set_Item(TaleWorlds.Core.UniqueTroopDescriptor, TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement)<br>TaleWorlds.CampaignSystem.Roster.FlattenedTroopRoster._elementDictionary<br>TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement..ctor(TaleWorlds.CampaignSystem.CharacterObject, TaleWorlds.CampaignSystem.Roster.RosterTroopState, System.Int32, TaleWorlds.Core.UniqueTroopDescriptor, System.Int32)<br>TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement.get_Descriptor()<br>... |
| `TaleWorlds.CampaignSystem.Roster.TroopRoster.GetElementXp` | 14 |  | TaleWorlds.CampaignSystem.Roster.TroopRoster.FindIndexOfTroop(TaleWorlds.CampaignSystem.CharacterObject)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.GetElementXp(System.Int32) |
| `TaleWorlds.CampaignSystem.Roster.TroopRoster.SetElementXp` | 71 | 0 | TaleWorlds.CampaignSystem.Party.PartyBase.OnXpChanged(TaleWorlds.CampaignSystem.Roster.TroopRoster, TaleWorlds.CampaignSystem.Roster.TroopRosterElement&)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster._count<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.data<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.get_OwnerParty()<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement<br>... |
| `TaleWorlds.CampaignSystem.Roster.TroopRoster.GetElementXp` | 33 | 0 | TaleWorlds.CampaignSystem.Roster.TroopRoster._count<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.data<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement.get_Xp() |
| `TaleWorlds.CampaignSystem.Roster.FlattenedTroopRoster.ResetTroopXP` | 127 | 0 | System.Collections.Generic.Dictionary<TaleWorlds.Core.UniqueTroopDescriptor, TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement>.get_Item(TaleWorlds.Core.UniqueTroopDescriptor)<br>System.Collections.Generic.Dictionary<TaleWorlds.Core.UniqueTroopDescriptor, TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement>.get_Keys()<br>System.Collections.Generic.Dictionary<TaleWorlds.Core.UniqueTroopDescriptor, TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement>.set_Item(TaleWorlds.Core.UniqueTroopDescriptor, TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement)<br>TaleWorlds.CampaignSystem.Roster.FlattenedTroopRoster._elementDictionary<br>TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement..ctor(TaleWorlds.CampaignSystem.CharacterObject, TaleWorlds.CampaignSystem.Roster.RosterTroopState, System.Int32, TaleWorlds.Core.UniqueTroopDescriptor, System.Int32)<br>... |
| `TaleWorlds.CampaignSystem.Party.PartyBase.OnXpChanged` | 159 | 0, 1 | TaleWorlds.CampaignSystem.CharacterObject.GetUpgradeXpCost(TaleWorlds.CampaignSystem.Party.PartyBase, System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement.Character<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement.get_Number()<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement.get_Xp()<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement.set_Xp(System.Int32) |
| `TaleWorlds.CampaignSystem.Roster.TroopRosterElement.set_Xp` | 42 | 0, 77 | TaleWorlds.CampaignSystem.Roster.TroopRosterElement._xp |
| `TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement.get_Xp` | 7 |  | TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement._xp |
| `TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement.get_XpGained` | 7 |  | TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement._xpGain |
| `TaleWorlds.CampaignSystem.Roster.TroopRosterElement.get_Xp` | 7 |  | TaleWorlds.CampaignSystem.Roster.TroopRosterElement._xp |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.CampaignBattleRecoveryBehavior.GiveTroopXp` | 22 |  | TaleWorlds.CampaignSystem.Roster.TroopRoster.AddXpToTroop(TaleWorlds.CampaignSystem.CharacterObject, System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement.Character |
| `TaleWorlds.CampaignSystem.CampaignBehaviors.GarrisonRecruitmentCampaignBehavior.HandleGarrisonXpChange` | 146 | 0 | System.Collections.Generic.List<TaleWorlds.CampaignSystem.Roster.TroopRosterElement><br>System.Collections.Generic.List<TaleWorlds.CampaignSystem.Roster.TroopRosterElement>.get_Current()<br>System.Collections.Generic.List<TaleWorlds.CampaignSystem.Roster.TroopRosterElement>.GetEnumerator()<br>System.Collections.Generic.List<TaleWorlds.CampaignSystem.Roster.TroopRosterElement>.MoveNext()<br>TaleWorlds.CampaignSystem.ComponentInterfaces.DailyTroopXpBonusModel.CalculateDailyTroopXpBonus(TaleWorlds.CampaignSystem.Settlements.Town)<br>... |
| `TaleWorlds.CampaignSystem.CampaignCheats.AddPrisonersXp` | 221 | 0, 1, 2, 3, 4 | TaleWorlds.CampaignSystem.Roster.TroopRoster.get_Count()<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.GetElementCopyAtIndex(System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.GetElementXp(System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.SetElementXp(System.Int32, System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement.Character |
| `TaleWorlds.CampaignSystem.CampaignCheats.AddTroopsXp` | 236 | 0, 1, 2, 3, 4 | TaleWorlds.CampaignSystem.Roster.TroopRoster.get_Count()<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.GetElementCopyAtIndex(System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.GetElementXp(System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.SetElementXp(System.Int32, System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement.Character |
| `TaleWorlds.CampaignSystem.CharacterObject.GetUpgradeXpCost` | 50 | 0 | TaleWorlds.CampaignSystem.ComponentInterfaces.PartyTroopUpgradeModel.GetXpCostForUpgrade(TaleWorlds.CampaignSystem.Party.PartyBase, TaleWorlds.CampaignSystem.CharacterObject, TaleWorlds.CampaignSystem.CharacterObject) |
| `Helpers.MobilePartyHelper.GetMaximumXpAmountPartyCanGet` | 62 | 0, 1 | Helpers.MobilePartyHelper.CanTroopGainXp(TaleWorlds.CampaignSystem.Party.PartyBase, TaleWorlds.CampaignSystem.CharacterObject, System.Int32&)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.get_Count()<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.GetElementCopyAtIndex(System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement.Character |
| `Helpers.MobilePartyHelper.PartyAddSharedXp` | 173 | 0, 1 | Helpers.MobilePartyHelper.CanTroopGainXp(TaleWorlds.CampaignSystem.Party.PartyBase, TaleWorlds.CampaignSystem.CharacterObject, System.Int32&)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.AddXpToTroopAtIndex(System.Int32, System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.get_Count()<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.GetElementCopyAtIndex(System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement.Character |
| `Helpers.MobilePartyHelper.CanTroopGainXp` | 147 | 0, 1, 3843 | TaleWorlds.CampaignSystem.CharacterObject.GetUpgradeXpCost(TaleWorlds.CampaignSystem.Party.PartyBase, System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.FindIndexOfTroop(TaleWorlds.CampaignSystem.CharacterObject)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.GetElementNumber(System.Int32)<br>TaleWorlds.CampaignSystem.Roster.TroopRoster.GetElementXp(System.Int32) |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.get_XpGainFromDonations` | 7 |  |  |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.set_XpGainFromDonations` | 57 | 0 | TaleWorlds.CampaignSystem.Inventory.InventoryLogic.get_DonationXpChange() |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.InitializeXpGainFromDonations` | 66 | 0, 2 | TaleWorlds.CampaignSystem.ComponentInterfaces.ItemDiscardModel.GetXpBonusForDiscardingItems(TaleWorlds.CampaignSystem.Roster.ItemRoster)<br>TaleWorlds.CampaignSystem.Inventory.InventoryLogic.set_XpGainFromDonations(System.Single) |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.set_CanGainXpFromDiscarding` | 8 |  | TaleWorlds.CampaignSystem.Inventory.InventoryLogic.<CanGainXpFromDiscarding>k__BackingField |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.get_DonationXpChange` | 7 |  | TaleWorlds.CampaignSystem.Inventory.InventoryLogic.<DonationXpChange>k__BackingField |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.set_DonationXpChange` | 8 |  | TaleWorlds.CampaignSystem.Inventory.InventoryLogic.<DonationXpChange>k__BackingField |
| `TaleWorlds.CampaignSystem.Inventory.InventoryLogic.get_CanGainXpFromDiscarding` | 7 |  | TaleWorlds.CampaignSystem.Inventory.InventoryLogic.<CanGainXpFromDiscarding>k__BackingField |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.CalculateXpGainFromBattles` | 86 | 0 | TaleWorlds.CampaignSystem.Roster.FlattenedTroopRosterElement.get_XpGained() |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTroopUpgradeModel.GetXpCostForUpgrade` | 178 | 0, 1, 1.333, 2, 3, 4, 5, 6, 7, 100, 300, 550, ... |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTroopUpgradeModel.GetSkillXpFromUpgradingTroops` | 12 | 10 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GenerateSharedXp` | 110 | 0 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GetXpReward` | 13 | 3, 6 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GetEffectiveDailyExperience` | 1072 | 0, 1, 2, 3, 4, 10, 15, 75 | TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GetPerkExperiencesForTroops(TaleWorlds.CampaignSystem.CharacterDevelopment.PerkObject)<br>TaleWorlds.CampaignSystem.Roster.TroopRosterElement.Character |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyTrainingModel.GetPerkExperiencesForTroops` | 114 | 0 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultDailyTroopXpBonusModel.CalculateDailyTroopXpBonus` | 8 |  | TaleWorlds.CampaignSystem.GameComponents.DefaultDailyTroopXpBonusModel.CalculateTroopXpBonusInternal(TaleWorlds.CampaignSystem.Settlements.Town) |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultDailyTroopXpBonusModel.CalculateTroopXpBonusInternal` | 59 | 0, 11 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultDailyTroopXpBonusModel.CalculateGarrisonXpBonusMultiplier` | 6 | 1 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultItemDiscardModel.GetXpBonusForDiscardingItem` | 86 | 0, 35, 75, 150, 250, 300 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultItemDiscardModel.GetXpBonusForDiscardingItems` | 56 | 0, 1 | TaleWorlds.CampaignSystem.ComponentInterfaces.ItemDiscardModel.GetXpBonusForDiscardingItem(TaleWorlds.Core.ItemObject, System.Int32) |

## Healing xp

| Method | IL bytes | Constants | XP references |
| --- | ---: | --- | --- |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPartyHealingModel.GetSkillXpFromHealingTroop` | 2 | 5 |  |

## Crafting xp

| Method | IL bytes | Constants | XP references |
| --- | ---: | --- | --- |
| `TaleWorlds.CampaignSystem.CraftingSystem.CraftingOrder.GetOrderExperience` | 131 | 0, 0.25, 0.5, 1, 3 |  |
| `TaleWorlds.CampaignSystem.Issues.VillageNeedsCraftingMaterialsIssueBehavior+VillageNeedsCraftingMaterialsIssue.get_CompanionSkillRewardXP` | 20 | 500, 700 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForSmithingInCraftingOrderMode` | 19 | 0.1 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForSmithingInFreeBuildMode` | 19 | 0.02 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForRefining` | 39 | 0.3 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultSmithingModel.GetSkillXpForSmelting` | 19 | 0.02 |  |

## Activity xp

| Method | IL bytes | Constants | XP references |
| --- | ---: | --- | --- |
| `TaleWorlds.CampaignSystem.Issues.IssueBase.get_CompanionSkillRewardXP` | 7 |  | TaleWorlds.CampaignSystem.Issues.IssueBase.<CompanionSkillRewardXP>k__BackingField |
| `TaleWorlds.CampaignSystem.Issues.LandLordTheArtOfTheTradeIssueBehavior+LandLordTheArtOfTheTradeIssue.get_CompanionSkillRewardXP` | 20 | 800, 900 |  |
| `TaleWorlds.CampaignSystem.Issues.LandlordTrainingForRetainersIssueBehavior+LandlordTrainingForRetainersIssue.get_CompanionSkillRewardXP` | 20 | 500, 700 |  |
| `TaleWorlds.CampaignSystem.Issues.LesserNobleRevoltIssueBehavior+LesserNobleRevoltIssue.get_CompanionSkillRewardXP` | 20 | 800, 1000 |  |
| `TaleWorlds.CampaignSystem.Issues.LandLordNeedsManualLaborersIssueBehavior+LandLordNeedsManualLaborersIssue.get_CompanionSkillRewardXP` | 20 | 500, 700 |  |
| `TaleWorlds.CampaignSystem.Issues.HeadmanNeedsToDeliverAHerdIssueBehavior+HeadmanNeedsToDeliverAHerdIssue.get_CompanionSkillRewardXP` | 20 | 500, 700 |  |
| `TaleWorlds.CampaignSystem.Issues.HeadmanVillageNeedsDraughtAnimalsIssueBehavior+HeadmanVillageNeedsDraughtAnimalsIssue.get_CompanionSkillRewardXP` | 20 | 500, 700 |  |
| `TaleWorlds.CampaignSystem.Issues.LandlordNeedsAccessToVillageCommonsIssueBehavior+LandlordNeedsAccessToVillageCommonsIssue.get_CompanionSkillRewardXP` | 20 | 700, 900 |  |
| `TaleWorlds.CampaignSystem.Issues.LordNeedsGarrisonTroopsIssueQuestBehavior+LordNeedsGarrisonTroopsIssue.get_CompanionSkillRewardXP` | 20 | 800, 900 |  |
| `TaleWorlds.CampaignSystem.Issues.SmugglersIssueBehavior+SmugglersIssue.get_CompanionSkillRewardXP` | 20 | 500, 1000 |  |
| `TaleWorlds.CampaignSystem.Issues.VillageNeedsToolsIssueBehavior+VillageNeedsToolsIssue.get_CompanionSkillRewardXP` | 20 | 500, 700 |  |
| `TaleWorlds.CampaignSystem.Issues.NearbyBanditBaseIssueBehavior+NearbyBanditBaseIssue.get_CompanionSkillRewardXP` | 20 | 1000, 1250 |  |
| `TaleWorlds.CampaignSystem.Issues.LordNeedsHorsesIssueBehavior+LordNeedsHorsesIssue.get_CompanionSkillRewardXP` | 20 | 500, 700 |  |
| `TaleWorlds.CampaignSystem.Issues.MerchantArmyOfPoachersIssueBehavior+MerchantArmyOfPoachersIssue.get_CompanionSkillRewardXP` | 20 | 800, 1000 |  |
| `TaleWorlds.CampaignSystem.Issues.MerchantNeedsHelpWithOutlawsIssueQuestBehavior+MerchantNeedsHelpWithOutlawsIssue.get_CompanionSkillRewardXP` | 20 | 600, 800 |  |
| `TaleWorlds.CampaignSystem.Incidents.IncidentEffect+<>c__DisplayClass50_0.<PartyExperienceChance>b__1` | 99 | 1, 100 |  |
| `TaleWorlds.CampaignSystem.Issues.ArtisanCantSellProductsAtAFairPriceIssueBehavior+ArtisanCantSellProductsAtAFairPriceIssue.get_CompanionSkillRewardXP` | 20 | 400, 1700 |  |
| `TaleWorlds.CampaignSystem.Issues.ArtisanOverpricedGoodsIssueBehavior+ArtisanOverpricedGoodsIssue.get_CompanionSkillRewardXP` | 20 | 400, 1700 |  |
| `TaleWorlds.CampaignSystem.Incidents.IncidentEffect+<>c__DisplayClass50_0.<PartyExperienceChance>b__0` | 60 |  | Helpers.MobilePartyHelper.PartyAddSharedXp(TaleWorlds.CampaignSystem.Party.MobileParty, System.Single) |
| `TaleWorlds.CampaignSystem.Issues.CapturedByBountyHuntersIssueBehavior+CapturedByBountyHuntersIssue.get_CompanionSkillRewardXP` | 20 | 750, 1000 |  |
| `TaleWorlds.CampaignSystem.Issues.GangLeaderNeedsToOffloadStolenGoodsIssueBehavior+GangLeaderNeedsToOffloadStolenGoodsIssue.get_CompanionSkillRewardXP` | 20 | 1000, 1250 |  |
| `TaleWorlds.CampaignSystem.Issues.GangLeaderNeedsWeaponsIssueQuestBehavior+GangLeaderNeedsWeaponsIssue.get_CompanionSkillRewardXP` | 20 | 800, 900 |  |
| `TaleWorlds.CampaignSystem.Issues.HeadmanNeedsGrainIssueBehavior+HeadmanNeedsGrainIssue.get_CompanionSkillRewardXP` | 20 | 500, 700 |  |
| `TaleWorlds.CampaignSystem.Issues.GangLeaderNeedsRecruitsIssueBehavior+GangLeaderNeedsRecruitsIssue.get_CompanionSkillRewardXP` | 20 | 500, 700 |  |
| `TaleWorlds.CampaignSystem.Issues.CaravanAmbushIssueBehavior+CaravanAmbushIssue.get_CompanionSkillRewardXP` | 20 | 600, 800 |  |
| `TaleWorlds.CampaignSystem.Issues.EscortMerchantCaravanIssueBehavior+EscortMerchantCaravanIssue.get_CompanionSkillRewardXP` | 20 | 800, 1000 |  |
| `TaleWorlds.CampaignSystem.Issues.ExtortionByDesertersIssueBehavior+ExtortionByDesertersIssue.get_CompanionSkillRewardXP` | 20 | 800, 1000 |  |
| `TaleWorlds.CampaignSystem.Incidents.IncidentEffect.PartyExperienceChance` | 44 |  | TaleWorlds.CampaignSystem.Incidents.IncidentEffect+<>c__DisplayClass50_0.<PartyExperienceChance>b__0()<br>TaleWorlds.CampaignSystem.Incidents.IncidentEffect+<>c__DisplayClass50_0.<PartyExperienceChance>b__1(TaleWorlds.CampaignSystem.Incidents.IncidentEffect) |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultAlleyModel.GetXpGainAfterSuccessfulAlleyDefenseForMainHero` | 6 | 6000 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultAlleyModel.GetDailyXpGainForAssignedClanMember` | 6 | 200 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultAlleyModel.GetDailyXpGainForMainHero` | 6 | 40 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultAlleyModel.GetInitialXpGainForMainHero` | 6 | 1500 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultPersuasionModel.GetSkillXpFromPersuasion` | 10 | 0, 1, 5 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultTournamentModel.GetSkillXpGainFromTournament` | 84 | 0.2, 0.4, 0.6, 0.8, 500 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultWorkshopModel.GetTradeXpPerWarehouseProduction` | 15 | 0.1 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultHideoutModel.GetRogueryXpGainOnHideoutMissionEnd` | 37 | 225, 400, 700, 1000 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultDiplomacyModel.GetCharmExperienceFromRelationGain` | 184 | 1, 10, 20, 30 |  |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultHideoutModel.GetRogueryXpGainAsGhost` | 16 | 1000, 1400 |  |

## Xp multiplier

| Method | IL bytes | Constants | XP references |
| --- | ---: | --- | --- |
| `TaleWorlds.CampaignSystem.GameComponents.DefaultGenericXpModel.GetXpMultiplier` | 37 | 1, 1.2 |  |

## Outputs

- JSON index: `Data\generated\xp-award-methods.json`
- IL dump: `Data\generated\reports\xp-award-il.md`
