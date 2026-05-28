# Bannerlord Skill XP Sources

Generated: 2026-05-27T22:22:54.0058870+03:00

This report groups extracted skill-XP source candidates by Bannerlord skill. It is generated from local compiled assemblies by scanning for skill XP sinks such as `AddSkillXp`, party/personal/settlement skill exercise hooks, and skill XP model methods.

## Reading Notes

- `high` means the method directly sends a named skill into an XP sink.
- `medium` means the method returns or calculates a skill XP amount but another caller applies it.
- `inferred` means the skill is selected dynamically, usually from the weapon used in combat.
- `Smithing` appears as `Crafting` in the compiled `DefaultSkills` API; this report displays the player-facing skill name.
- This is a coverage map, not a final prose guide. Some event branches still need hand-reading before we turn them into optimized player advice.

## Scouting Detail

The scan found these concrete Scouting XP paths:

- `OnTraverseTerrain`: Scouting party-skill exercise while a mobile party traverses terrain. The formula uses party speed, party size, and a terrain multiplier. Desert, snow, forest, and dune terrain use the higher `0.25` multiplier; other terrain uses `0.15`; caravans get half. XP is only applied when the calculated amount reaches at least `5`.
- `OnTrackDetected`: Scouting party-skill exercise for the main party when a track is detected. The amount comes from `MapTrackModel.GetSkillFromTrackDetected(track)`, and the party role is `Scout`.
- `OnHideoutSpotted`: Scouting party-skill exercise worth `100`, also for the `Scout` role.
- `OnAIPartiesTravel`: direct Scouting XP for AI party travel. Forest terrain gives `roundRandomized(5)`, other terrain gives `roundRandomized(3)`, and caravan parties receive half.
- `CaravanAmbushIssue.AlternativeSolutionEndWithSuccessConsequence`: the assigned hero gets `600 + 800 * IssueDifficultyMultiplier` Scouting XP, plus the same amount to a random melee skill.

## Skill Coverage Summary

| Skill | Source count |
| --- | ---: |
| One Handed | 7 |
| Two Handed | 7 |
| Polearm | 7 |
| Bow | 4 |
| Crossbow | 3 |
| Throwing | 3 |
| Riding | 3 |
| Athletics | 4 |
| Smithing | 4 |
| Scouting | 5 |
| Tactics | 1 |
| Roguery | 20 |
| Charm | 2 |
| Leadership | 4 |
| Trade | 3 |
| Steward | 5 |
| Medicine | 3 |
| Engineering | 4 |

## Sources By Skill

### One Handed

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `CaravanAmbushIssue.AlternativeSolutionEndWithSuccessConsequence` | Alternative solution reward: the assigned hero receives Scouting XP plus a random melee skill reward. | 0.33, 0.66, 1, 3, 5, 600, 800 | high |
| `DefaultSkillLevelingManager.OnCombatHit` | Combat hit/kill XP; the skill comes from the weapon used, so it can feed any combat weapon skill. | 0, 0.02, 0.15, 0.5, 1, 1.5, 78 | inferred |
| `DefaultSkillLevelingManager.OnSimulationCombatKill` | Simulation kill XP; weapon XP is based on the killed troop reward, with extra Riding or Athletics movement XP. | 0, 0.02, 0.3 | inferred |
| `DefaultTournamentModel.GetSkillXpGainFromTournament` | Tournament reward model: 500 XP to one random skill from five equal bands. | 0.2, 0.4, 0.6, 0.8, 500 | medium |
| `FamilyFeudIssue.AlternativeSolutionEndWithSuccessConsequence` | Issue alternative-solution skill XP reward. | 0.33, 0.66, 500, 700 | high |
| `NotableWantsDaughterFoundIssue.AlternativeSolutionEndWithSuccessConsequence` | Issue alternative-solution skill XP reward. | 0.33, 0.66, 500, 1000 | high |
| `SimpleAgentOrigin.TaleWorlds.Core.IAgentOriginBase.OnScoreHit` | Mission score-hit hook that applies weapon-skill XP to hero attackers. | 0 | inferred |

### Two Handed

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `CaravanAmbushIssue.AlternativeSolutionEndWithSuccessConsequence` | Alternative solution reward: the assigned hero receives Scouting XP plus a random melee skill reward. | 0.33, 0.66, 1, 3, 5, 600, 800 | high |
| `DefaultSkillLevelingManager.OnCombatHit` | Combat hit/kill XP; the skill comes from the weapon used, so it can feed any combat weapon skill. | 0, 0.02, 0.15, 0.5, 1, 1.5, 78 | inferred |
| `DefaultSkillLevelingManager.OnSimulationCombatKill` | Simulation kill XP; weapon XP is based on the killed troop reward, with extra Riding or Athletics movement XP. | 0, 0.02, 0.3 | inferred |
| `DefaultTournamentModel.GetSkillXpGainFromTournament` | Tournament reward model: 500 XP to one random skill from five equal bands. | 0.2, 0.4, 0.6, 0.8, 500 | medium |
| `FamilyFeudIssue.AlternativeSolutionEndWithSuccessConsequence` | Issue alternative-solution skill XP reward. | 0.33, 0.66, 500, 700 | high |
| `NotableWantsDaughterFoundIssue.AlternativeSolutionEndWithSuccessConsequence` | Issue alternative-solution skill XP reward. | 0.33, 0.66, 500, 1000 | high |
| `SimpleAgentOrigin.TaleWorlds.Core.IAgentOriginBase.OnScoreHit` | Mission score-hit hook that applies weapon-skill XP to hero attackers. | 0 | inferred |

### Polearm

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `CaravanAmbushIssue.AlternativeSolutionEndWithSuccessConsequence` | Alternative solution reward: the assigned hero receives Scouting XP plus a random melee skill reward. | 0.33, 0.66, 1, 3, 5, 600, 800 | high |
| `DefaultSkillLevelingManager.OnCombatHit` | Combat hit/kill XP; the skill comes from the weapon used, so it can feed any combat weapon skill. | 0, 0.02, 0.15, 0.5, 1, 1.5, 78 | inferred |
| `DefaultSkillLevelingManager.OnSimulationCombatKill` | Simulation kill XP; weapon XP is based on the killed troop reward, with extra Riding or Athletics movement XP. | 0, 0.02, 0.3 | inferred |
| `DefaultTournamentModel.GetSkillXpGainFromTournament` | Tournament reward model: 500 XP to one random skill from five equal bands. | 0.2, 0.4, 0.6, 0.8, 500 | medium |
| `FamilyFeudIssue.AlternativeSolutionEndWithSuccessConsequence` | Issue alternative-solution skill XP reward. | 0.33, 0.66, 500, 700 | high |
| `NotableWantsDaughterFoundIssue.AlternativeSolutionEndWithSuccessConsequence` | Issue alternative-solution skill XP reward. | 0.33, 0.66, 500, 1000 | high |
| `SimpleAgentOrigin.TaleWorlds.Core.IAgentOriginBase.OnScoreHit` | Mission score-hit hook that applies weapon-skill XP to hero attackers. | 0 | inferred |

### Bow

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnCombatHit` | Combat hit/kill XP; the skill comes from the weapon used, so it can feed any combat weapon skill. | 0, 0.02, 0.15, 0.5, 1, 1.5, 78 | inferred |
| `DefaultSkillLevelingManager.OnSimulationCombatKill` | Simulation kill XP; weapon XP is based on the killed troop reward, with extra Riding or Athletics movement XP. | 0, 0.02, 0.3 | inferred |
| `SimpleAgentOrigin.TaleWorlds.Core.IAgentOriginBase.OnScoreHit` | Mission score-hit hook that applies weapon-skill XP to hero attackers. | 0 | inferred |
| `MobilePartyTrainingBehavior.OnDailyTickParty` | Bow Trainer perk hook: daily Bow XP goes to the hero party member with the lowest Bow skill. | 0, 2147483647 | high |

### Crossbow

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnCombatHit` | Combat hit/kill XP; the skill comes from the weapon used, so it can feed any combat weapon skill. | 0, 0.02, 0.15, 0.5, 1, 1.5, 78 | inferred |
| `DefaultSkillLevelingManager.OnSimulationCombatKill` | Simulation kill XP; weapon XP is based on the killed troop reward, with extra Riding or Athletics movement XP. | 0, 0.02, 0.3 | inferred |
| `SimpleAgentOrigin.TaleWorlds.Core.IAgentOriginBase.OnScoreHit` | Mission score-hit hook that applies weapon-skill XP to hero attackers. | 0 | inferred |

### Throwing

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnCombatHit` | Combat hit/kill XP; the skill comes from the weapon used, so it can feed any combat weapon skill. | 0, 0.02, 0.15, 0.5, 1, 1.5, 78 | inferred |
| `DefaultSkillLevelingManager.OnSimulationCombatKill` | Simulation kill XP; weapon XP is based on the killed troop reward, with extra Riding or Athletics movement XP. | 0, 0.02, 0.3 | inferred |
| `SimpleAgentOrigin.TaleWorlds.Core.IAgentOriginBase.OnScoreHit` | Mission score-hit hook that applies weapon-skill XP to hero attackers. | 0 | inferred |

### Riding

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnCombatHit` | Combat hit/kill XP; the skill comes from the weapon used, so it can feed any combat weapon skill. | 0, 0.02, 0.15, 0.5, 1, 1.5, 78 | inferred |
| `DefaultTournamentModel.GetSkillXpGainFromTournament` | Tournament reward model: 500 XP to one random skill from five equal bands. | 0.2, 0.4, 0.6, 0.8, 500 | medium |
| `DefaultSkillLevelingManager.OnGainingRidingExperience` | Riding XP from mounted actions, scaled by horse difficulty. | 0.02, 1 | high |

### Athletics

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnCombatHit` | Combat hit/kill XP; the skill comes from the weapon used, so it can feed any combat weapon skill. | 0, 0.02, 0.15, 0.5, 1, 1.5, 78 | inferred |
| `DefaultSkillLevelingManager.OnSimulationCombatKill` | Simulation kill XP; weapon XP is based on the killed troop reward, with extra Riding or Athletics movement XP. | 0, 0.02, 0.3 | inferred |
| `DefaultTournamentModel.GetSkillXpGainFromTournament` | Tournament reward model: 500 XP to one random skill from five equal bands. | 0.2, 0.4, 0.6, 0.8, 500 | medium |
| `DefaultSkillLevelingManager.OnTravelOnFoot` | Athletics XP while traveling on foot: roundRandomized(0.2 * speed) + 1. | 0.2, 1 | high |

### Smithing

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `CraftingCampaignBehavior.CreateCraftedWeaponInCraftingOrderMode` | Skill XP source candidate. | 0 | high |
| `CraftingCampaignBehavior.CreateCraftedWeaponInFreeBuildMode` | Skill XP source candidate. | 1 | high |
| `CraftingCampaignBehavior.DoRefinement` | Skill XP source candidate. | 0 | high |
| `CraftingCampaignBehavior.DoSmelting` | Skill XP source candidate. | -1, 0, 1, 8 | high |

### Scouting

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `CaravanAmbushIssue.AlternativeSolutionEndWithSuccessConsequence` | Alternative solution reward: the assigned hero receives Scouting XP plus a random melee skill reward. | 0.33, 0.66, 1, 3, 5, 600, 800 | high |
| `DefaultSkillLevelingManager.OnAIPartiesTravel` | Scouting XP for AI party travel: forest terrain uses roundRandomized(5), other terrain uses roundRandomized(3), and caravan parties receive half. | 2, 3, 4, 5 | high |
| `DefaultSkillLevelingManager.OnHideoutSpotted` | Scouting party-skill exercise when a hideout is spotted; amount is 100 for the Scout party role. | 9, 100 | high |
| `DefaultSkillLevelingManager.OnTrackDetected` | Scouting party-skill exercise when a track is detected; amount comes from MapTrackModel.GetSkillFromTrackDetected(track) for the Scout party role. | 9 | high |
| `DefaultSkillLevelingManager.OnTraverseTerrain` | Scouting party-skill exercise while traversing terrain; requires speed above 1 and calculated XP of at least 5. | 0, 0.15, 0.25, 0.5, 0.66, 1, 2, 3, 4, 5, ... | high |

### Tactics

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnTacticsUsed` | Tactics XP from simulated/commander tactics use. | 0, 5 | high |

### Roguery

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnCombatHit` | Combat hit/kill XP; the skill comes from the weapon used, so it can feed any combat weapon skill. | 0, 0.02, 0.15, 0.5, 1, 1.5, 78 | inferred |
| `DefaultSkillLevelingManager.OnAIPartyLootCasualties` | Skill XP hook for aiparty loot casualties. | -1, 0, 0.15, 0.75, 1 | high |
| `DefaultSkillLevelingManager.OnAlleyCleared` | Skill XP hook for alley cleared. |  | high |
| `DefaultSkillLevelingManager.OnBanditsRecruited` | Skill XP hook for bandits recruited. | 0, 1, 2 | high |
| `DefaultSkillLevelingManager.OnBattleEnded` | Post-battle skill XP hook; constants suggest tiered battle/participation rewards. | 0.025, 0.05, 15 | high |
| `DefaultSkillLevelingManager.OnBribeGiven` | Skill XP hook for bribe given. | 0, 0.1, 5 | high |
| `DefaultSkillLevelingManager.OnDailyAlleyTick` | Skill XP hook for daily alley tick. |  | high |
| `DefaultSkillLevelingManager.OnForceSupplies` | Skill XP hook for force supplies. | 0.5, 0.75, 1, 50, 200 | high |
| `DefaultSkillLevelingManager.OnForceVolunteers` | Skill XP hook for force volunteers. | 1, 10 | high |
| `DefaultSkillLevelingManager.OnHideoutClearedAsGhost` | Skill XP hook for hideout cleared as ghost. | 0, 1 | high |
| `DefaultSkillLevelingManager.OnHideoutMissionEnd` | Skill XP hook for hideout mission end. |  | high |
| `DefaultSkillLevelingManager.OnLoot` | Skill XP hook for loot. | 0, 0.1, 0.15, 0.5, 0.75, 1, 50, 200 | high |
| `DefaultSkillLevelingManager.OnMainHeroDisguised` | Skill XP hook for main hero disguised. | 1, 5, 10, 25 | high |
| `DefaultSkillLevelingManager.OnMainHeroReleasedFromCaptivity` | Skill XP hook for main hero released from captivity. | 0.5, 1 | high |
| `DefaultSkillLevelingManager.OnMainHeroTortured` | Skill XP hook for main hero tortured. | 1, 50, 100 | high |
| `DefaultSkillLevelingManager.OnPrisonBreakEnd` | Skill XP hook for prison break end. | 0 | high |
| `DefaultSkillLevelingManager.OnPrisonerSell` | Skill XP hook for prisoner sell. | 0, 1, 2, 5 | high |
| `DefaultSkillLevelingManager.OnRaid` | Skill XP hook for raid. | 0.5, 1, 25, 100 | high |
| `DefaultSkillLevelingManager.OnUpgradeTroops` | Skill XP from upgrading troops; the upgrade model returns 10 as the base skill XP. | 0.025, 0.05, 15 | high |
| `PlayerAlleyData.AlleyFightWon` | Skill XP source candidate. | -1, 0, 0.2, 1 | high |

### Charm

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnGainRelation` | Charm XP from relation gain. | 0, 1, 5 | high |
| `ProdigalSonIssue.AlternativeSolutionEndWithSuccessConsequence` | Issue alternative-solution skill XP reward. | 0, 3, 5, 700, 900 | high |

### Leadership

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnBattleEnded` | Post-battle skill XP hook; constants suggest tiered battle/participation rewards. | 0.025, 0.05, 15 | high |
| `DefaultSkillLevelingManager.OnUpgradeTroops` | Skill XP from upgrading troops; the upgrade model returns 10 as the base skill XP. | 0.025, 0.05, 15 | high |
| `DefaultSkillLevelingManager.OnLeadingArmy` | Leadership XP from leading an army. | 0.0004, 5 | high |
| `DefaultSkillLevelingManager.OnTroopRecruited` | Skill XP hook for troop recruited. | 0, 1, 2 | high |

### Trade

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnTradeProfitMade` | Trade XP from profitable trade. | 0, 0.5, 5 | high |
| `DefaultSkillLevelingManager.OnTradeProfitMade` | Trade XP from profitable trade. | 0, 0.5 | high |
| `DefaultSkillLevelingManager.OnWarehouseProduction` | Trade XP from warehouse production value. |  | high |

### Steward

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnBoardGameWonAgainstLord` | Steward XP from winning board games against lords; constants show 20, 50, and 100 branches. | 20, 50, 100 | high |
| `DefaultSkillLevelingManager.OnFoodConsumed` | Skill XP hook for food consumed. | 2, 3, 10, 100 | high |
| `DefaultSkillLevelingManager.OnInfluenceSpent` | Steward XP from spending influence through a party-leader skill exercise hook. | 5, 10 | high |
| `DefaultSkillLevelingManager.OnSettlementGoverned` | Skill XP hook for settlement governed. | 0, 1, 30 | high |
| `DefaultSkillLevelingManager.OnSettlementProjectFinished` | Skill XP hook for settlement project finished. | 1000 | high |

### Medicine

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnHeroHealedWhileWaiting` | Medicine XP when a hero heals while waiting. | 0.1, 0.2, 1, 7 | high |
| `DefaultSkillLevelingManager.OnRegularTroopHealedWhileWaiting` | Medicine XP when regular troops heal while waiting. | 1, 2, 7 | high |
| `DefaultSkillLevelingManager.OnSurgeryApplied` | Medicine XP from surgery/casualty treatment. | 5, 7, 10 | high |

### Engineering

| Source | Summary | Constants | Confidence |
| --- | --- | --- | --- |
| `DefaultSkillLevelingManager.OnSiegeEngineBuilt` | Engineering XP when siege engines are built. | 2, 8, 30 | high |
| `DefaultSkillLevelingManager.OnSiegeEngineDestroyed` | Engineering XP when siege engines are destroyed. | 8, 20 | high |
| `DefaultSkillLevelingManager.OnSieging` | Engineering XP while conducting a siege. | 0.25, 8 | high |
| `DefaultSkillLevelingManager.OnWallBreached` | Engineering XP when a wall is breached. | 8, 250 | high |

## Outputs

- JSON: `Data\generated\skill-xp-source-methods.json`
- Report: `Data\generated\reports\skill-xp-sources.md`
