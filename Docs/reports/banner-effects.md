# Banner Effects

Generated: 2026-06-05T12:56:53.1104801+03:00

This report joins singleplayer banner item XML to `DefaultBannerEffects.InitializeAll`, then cross-checks effect IDs against formula usage from the local game assemblies.

## Inputs

- JSON: `Data\raw\banner-items.json`
- Banner XML: `Modules\SandBoxCore\ModuleData\items\banners.xml`
- Usage scan: `Data\raw\banner-effect-usages.json`

> [!WARNING]
> `DecreasedRangedAttackDamage` has a misleading raw description string in `DefaultBannerEffects.InitializeAll`: it reuses morale-penalty wording. The formulas reference the `DecreasedRangedAttackDamage` effect for ranged damage reduction, so this report treats it mechanically as ranged damage taken reduction.

## How Banner Effects Apply

- Battle banners are formation-scoped. Combat/stat models ask `BattleBannerBearersModel.GetActiveBanner(formation)` and add the matching active banner effect to an explained/factored number.
- Damage-dealt banners use the attacker's active banner formation; damage-taken and shield-damage banners use the victim/defending formation path.
- Movement banners are live-battle agent stats, not campaign party speed.
- Accuracy banner mechanics are narrow: the ranged accuracy banner modifies `WeaponInaccuracy`, not every accuracy penalty property and not direct hit chance.
- Usage confirmation: 13 banner effects were found in formula usage scan.

## Commander Shortlist

| Effect | Tiers | Tier 3 items | Mechanical read | Note |
| --- | --- | --- | --- | --- |
| Increased Troop Movement Speed | T1 15%, T2 25%, T3 30% | Banner of Dust Devils, Strider's Flag | +30% infantry movement speed in the formation. | Core shock-infantry banner: tier 3 is the huge +30% foot movement breakpoint. |
| Increased Mount Movement Speed | T1 5%, T2 8%, T3 10% | Tug of the Endless Steppe | +10% mount movement speed in the formation. | Mounted version of the speed idea, but much smaller: tier 3 is +10% mount movement. |
| Decreased Taken Ranged Attack Damage | T1 -5%, T2 -10%, T3 -15% | Locked Shields Banner, Testudo Standard | -15% ranged attack damage taken by troops in the formation. | Core anti-arrow banner. The raw game description string is misleading, but combat formulas use this as ranged damage taken reduction. |
| Decreased Ranged Accuracy Penalty | T1 -4%, T2 -6%, T3 -8% | Banner of Sultan's Eagle, Tug of Whistling Arrow | -8% ranged accuracy penalty for ranged troops in the formation. | Specialist archer-commander banner for dense ranged formations. |
| Increased Melee Damage | T1 5%, T2 10%, T3 15% | Standard of Wrath | +15% melee damage dealt by troops in the formation. | Looks strong on paper, but may be less valuable when elite shock troops already overkill common targets. |

## Mechanics Reference

| Effect ID | Tier values | Top tier items | Applies mechanically to | Formula usage | Confirmed methods | Practical read | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DecreasedChargeDamage | T1 -10%, T2 -20%, T3 -30% | No singleplayer banner item | Incoming charge damage on the charge-damage branch. | Added as a negative factor in the charge branch of ApplyDamageAmplifications. | SandBox: SandboxAgentApplyDamageModel.ApplyDamageAmplifications<br>TaleWorlds.MountAndBlade: CustomAgentApplyDamageModel.ApplyDamageAmplifications | Anti-charge durability for the relevant formation. | Not general melee or ranged resistance. |
| DecreasedMeleeAttackDamage | T1 -5%, T2 -10%, T3 -15% | Steel Banner | Incoming melee attack damage to troops in the active banner formation. | Added in the melee branch of ApplyDamageReductions. | SandBox: SandboxAgentApplyDamageModel.ApplyDamageReductions<br>TaleWorlds.MountAndBlade: CustomAgentApplyDamageModel.ApplyDamageReductions | General anti-melee durability. | Does not reduce ranged or shield-only damage. |
| DecreasedMoraleShock | T1 -10%, T2 -20%, T3 -30% | Standard of Discipline | Morale penalty from casualties and panic. | Added in CalculateMaxMoraleChangeDueToAgentIncapacitated and CalculateMaxMoraleChangeDueToAgentPanicked. | SandBox: SandboxBattleMoraleModel.CalculateMaxMoraleChangeDueToAgentIncapacitated<br>SandBox: SandboxBattleMoraleModel.CalculateMaxMoraleChangeDueToAgentPanicked<br>TaleWorlds.MountAndBlade: CustomBattleMoraleModel.CalculateMaxMoraleChangeDueToAgentIncapacitated<br>TaleWorlds.MountAndBlade: CustomBattleMoraleModel.CalculateMaxMoraleChangeDueToAgentPanicked | Keeps the formation morale steadier when troops die or panic. | Not HP, damage resistance, or troop survival chance. |
| DecreasedRangedAccuracyPenalty | T1 -4%, T2 -6%, T3 -8% | Banner of Sultan's Eagle, Tug of Whistling Arrow | AgentDrivenProperties.WeaponInaccuracy for ranged weapons. | Added in SetPerkAndBannerEffectsOnAgent/SetBannerEffectsOnAgent, then written to WeaponInaccuracy. | SandBox: SandboxAgentStatCalculateModel.SetPerkAndBannerEffectsOnAgent<br>TaleWorlds.MountAndBlade: CustomBattleAgentStatCalculateModel.SetBannerEffectsOnAgent | Reduces base weapon spread/inaccuracy. Tier 3 -8% means roughly 0.92x the affected inaccuracy component. | Not direct hit chance; does not touch movement, unsteady, or rotational accuracy penalties. |
| DecreasedRangedAttackDamage | T1 -5%, T2 -10%, T3 -15% | Locked Shields Banner, Testudo Standard | Incoming ranged attack damage to troops in the active banner formation. | Added in the ranged branch of ApplyDamageReductions. | SandBox: SandboxAgentApplyDamageModel.ApplyDamageReductions<br>TaleWorlds.MountAndBlade: CustomAgentApplyDamageModel.ApplyDamageReductions | The anti-arrow banner: tier 3 -15% is a real ranged damage taken reduction. | The raw description string is wrong and reuses morale text. |
| DecreasedShieldDamage | T1 -15%, T2 -25%, T3 -30% | Banner of Steel Shields | Damage dealt to shields of troops in the victim formation. | Added in CalculateShieldDamage. | SandBox: SandboxAgentApplyDamageModel.CalculateShieldDamage<br>TaleWorlds.MountAndBlade: CustomAgentApplyDamageModel.CalculateShieldDamage | Protects shields, which indirectly preserves shield wall uptime. | Does not directly reduce HP damage when an attack bypasses or breaks through the shield. |
| IncreasedChargeDamage | T1 10%, T2 20%, T3 30% | Banner of the Knight | Outgoing horse charge damage. | Added in the horse-charge branch of ApplyDamageAmplifications. | SandBox: SandboxAgentApplyDamageModel.ApplyDamageAmplifications<br>TaleWorlds.MountAndBlade: CustomAgentApplyDamageModel.ApplyDamageAmplifications | Cavalry charge specialist effect. | Does not affect normal melee swings. |
| IncreasedMeleeDamage | T1 5%, T2 10%, T3 15% | Standard of Wrath | Outgoing melee attack damage by troops in the active banner formation. | Added in the melee branch of ApplyDamageAmplifications. | SandBox: SandboxAgentApplyDamageModel.ApplyDamageAmplifications<br>TaleWorlds.MountAndBlade: CustomAgentApplyDamageModel.ApplyDamageAmplifications | Best when it changes hits-to-kill; less valuable when elite melee troops already overkill. | Not ranged damage, charge damage, or a party-wide passive. |
| IncreasedMeleeDamageAgainstMountedTroops | T1 10%, T2 20%, T3 30% | Horse Bane Flag, Pike Wall Banner | Outgoing melee attack damage when the victim has a mount agent. | Added in ApplyDamageAmplifications after the victim-mounted check. | SandBox: SandboxAgentApplyDamageModel.ApplyDamageAmplifications<br>TaleWorlds.MountAndBlade: CustomAgentApplyDamageModel.ApplyDamageAmplifications | Specialist anti-cavalry damage banner for formations fighting mounted targets. | Does nothing against foot troops. |
| IncreasedMoraleShockByMeleeTroops | T1 10%, T2 20%, T3 30% | No singleplayer banner item | Morale shock inflicted by melee troops when agents are incapacitated. | Added in CalculateMaxMoraleChangeDueToAgentIncapacitated. | SandBox: SandboxBattleMoraleModel.CalculateMaxMoraleChangeDueToAgentIncapacitated<br>TaleWorlds.MountAndBlade: CustomBattleMoraleModel.CalculateMaxMoraleChangeDueToAgentIncapacitated | Offensive morale-pressure banner for melee-heavy formations. | Not raw damage; value depends on morale shock mattering in the fight. |
| IncreasedMountMovementSpeed | T1 5%, T2 8%, T3 10% | Tug of the Endless Steppe | Mount speed in UpdateHorseStats. | Added to the horse-speed explained/factored number before MountSpeed is written. | SandBox: SandboxAgentStatCalculateModel.UpdateHorseStats<br>TaleWorlds.MountAndBlade: CustomBattleAgentStatCalculateModel.UpdateHorseStats | Mounted formation speed banner; tier 3 is +10% mount speed. | Not campaign map speed and not primarily a mount maneuver bonus. |
| IncreasedRangedDamage | T1 4%, T2 6%, T3 8% | Marksman's Flag | Outgoing ranged/projectile damage by troops in the active banner formation. | Added in the ranged/consumable weapon branch of ApplyDamageAmplifications. | SandBox: SandboxAgentApplyDamageModel.ApplyDamageAmplifications<br>TaleWorlds.MountAndBlade: CustomAgentApplyDamageModel.ApplyDamageAmplifications | Direct ranged lethality; better when ranged damage breakpoints matter. | Does not improve accuracy, projectile speed, or reload behavior. |
| IncreasedTroopMovementSpeed | T1 15%, T2 25%, T3 30% | Banner of Dust Devils, Strider's Flag | AgentDrivenProperties.MaxSpeedMultiplier for troops in the active banner formation. | Added in SetPerkAndBannerEffectsOnAgent/SetBannerEffectsOnAgent, then written to MaxSpeedMultiplier. | SandBox: SandboxAgentStatCalculateModel.SetPerkAndBannerEffectsOnAgent<br>TaleWorlds.MountAndBlade: CustomBattleAgentStatCalculateModel.SetBannerEffectsOnAgent | The shock-infantry speed banner. Tier 3 +30% is a major close-to-contact and formation responsiveness effect. | Not campaign map speed, projectile speed, reload speed, or CombatMaxSpeedMultiplier. |

## All Banner Effects

| Effect ID | Name | Tiers | Mechanical tier 3 read | Items |
| --- | --- | --- | --- | ---: |
| DecreasedChargeDamage | Decreased Charge Damage | T1 -10%, T2 -20%, T3 -30% | -30% charge damage taken by mounted troops in the formation. | 0 |
| DecreasedMeleeAttackDamage | Decreased Taken Melee Attack Damage | T1 -5%, T2 -10%, T3 -15% | -15% melee attack damage taken by troops in the formation. | 3 |
| DecreasedMoraleShock | Decreased Morale Shock | T1 -10%, T2 -20%, T3 -30% | -30% morale penalty from casualties to troops in the formation. | 3 |
| DecreasedRangedAccuracyPenalty | Decreased Ranged Accuracy Penalty | T1 -4%, T2 -6%, T3 -8% | -8% ranged accuracy penalty for ranged troops in the formation. | 6 |
| DecreasedRangedAttackDamage | Decreased Taken Ranged Attack Damage | T1 -5%, T2 -10%, T3 -15% | -15% ranged attack damage taken by troops in the formation. | 6 |
| DecreasedShieldDamage | Decreased Taken Shield Damage | T1 -15%, T2 -25%, T3 -30% | -30% damage taken by shields of troops in the formation. | 3 |
| IncreasedChargeDamage | Increased Charge Damage | T1 10%, T2 20%, T3 30% | +30% charge damage dealt by mounted troops in the formation. | 3 |
| IncreasedMeleeDamage | Increased Melee Damage | T1 5%, T2 10%, T3 15% | +15% melee damage dealt by troops in the formation. | 3 |
| IncreasedMeleeDamageAgainstMountedTroops | Increased Melee Damage Against Mounted Troops | T1 10%, T2 20%, T3 30% | +30% melee damage dealt by troops in the formation against cavalry or mounted targets. | 6 |
| IncreasedMoraleShockByMeleeTroops | Increased Morale Shock | T1 10%, T2 20%, T3 30% | +30% morale shock from melee troops in the formation. | 0 |
| IncreasedMountMovementSpeed | Increased Mount Movement Speed | T1 5%, T2 8%, T3 10% | +10% mount movement speed in the formation. | 3 |
| IncreasedRangedDamage | Increased Ranged Damage | T1 4%, T2 6%, T3 8% | +8% ranged damage dealt by troops in the formation. | 3 |
| IncreasedTroopMovementSpeed | Increased Troop Movement Speed | T1 15%, T2 25%, T3 30% | +30% infantry movement speed in the formation. | 6 |

## Banner Items

| Effect | Tier | Item | Culture | Bonus | Mechanical read | Raw description |
| --- | ---: | --- | --- | ---: | --- | --- |
| DecreasedMeleeAttackDamage | 1 | Stone Banner | neutral_culture | -5% | -5% melee attack damage taken by troops in the formation. | -5% damage by melee attacks to troops in your formation. |
| DecreasedMeleeAttackDamage | 2 | Iron Banner | neutral_culture | -10% | -10% melee attack damage taken by troops in the formation. | -10% damage by melee attacks to troops in your formation. |
| DecreasedMeleeAttackDamage | 3 | Steel Banner | neutral_culture | -15% | -15% melee attack damage taken by troops in the formation. | -15% damage by melee attacks to troops in your formation. |
| DecreasedMoraleShock | 1 | Standard of Duty | empire | -10% | -10% morale penalty from casualties to troops in the formation. | -10% morale penalty from casualties to troops in your formation. |
| DecreasedMoraleShock | 2 | Standard of Courage | empire | -20% | -20% morale penalty from casualties to troops in the formation. | -20% morale penalty from casualties to troops in your formation. |
| DecreasedMoraleShock | 3 | Standard of Discipline | empire | -30% | -30% morale penalty from casualties to troops in the formation. | -30% morale penalty from casualties to troops in your formation. |
| DecreasedRangedAccuracyPenalty | 1 | Banner of Faris' Falcon | aserai | -4% | -4% ranged accuracy penalty for ranged troops in the formation. | -4% accuracy penalty for ranged troops in your formation. |
| DecreasedRangedAccuracyPenalty | 1 | Tug of Wooden Arrow | khuzait | -4% | -4% ranged accuracy penalty for ranged troops in the formation. | -4% accuracy penalty for ranged troops in your formation. |
| DecreasedRangedAccuracyPenalty | 2 | Banner of Emir's Hawk | aserai | -6% | -6% ranged accuracy penalty for ranged troops in the formation. | -6% accuracy penalty for ranged troops in your formation. |
| DecreasedRangedAccuracyPenalty | 2 | Tug of Bone Arrow | khuzait | -6% | -6% ranged accuracy penalty for ranged troops in the formation. | -6% accuracy penalty for ranged troops in your formation. |
| DecreasedRangedAccuracyPenalty | 3 | Banner of Sultan's Eagle | aserai | -8% | -8% ranged accuracy penalty for ranged troops in the formation. | -8% accuracy penalty for ranged troops in your formation. |
| DecreasedRangedAccuracyPenalty | 3 | Tug of Whistling Arrow | khuzait | -8% | -8% ranged accuracy penalty for ranged troops in the formation. | -8% accuracy penalty for ranged troops in your formation. |
| DecreasedRangedAttackDamage | 1 | Close Shields Banner | sturgia | -5% | -5% ranged attack damage taken by troops in the formation. | -5% morale penalty from casualties to troops in your formation. |
| DecreasedRangedAttackDamage | 1 | Phalanx Standard | empire | -5% | -5% ranged attack damage taken by troops in the formation. | -5% morale penalty from casualties to troops in your formation. |
| DecreasedRangedAttackDamage | 2 | Fulcum Standard | empire | -10% | -10% ranged attack damage taken by troops in the formation. | -10% morale penalty from casualties to troops in your formation. |
| DecreasedRangedAttackDamage | 2 | Shield Wall Banner | sturgia | -10% | -10% ranged attack damage taken by troops in the formation. | -10% morale penalty from casualties to troops in your formation. |
| DecreasedRangedAttackDamage | 3 | Locked Shields Banner | sturgia | -15% | -15% ranged attack damage taken by troops in the formation. | -15% morale penalty from casualties to troops in your formation. |
| DecreasedRangedAttackDamage | 3 | Testudo Standard | empire | -15% | -15% ranged attack damage taken by troops in the formation. | -15% morale penalty from casualties to troops in your formation. |
| DecreasedShieldDamage | 1 | Banner of Oaken Shields | sturgia | -15% | -15% damage taken by shields of troops in the formation. | -15% damage to shields of troops in your formation. |
| DecreasedShieldDamage | 2 | Banner of Iron Shields | sturgia | -25% | -25% damage taken by shields of troops in the formation. | -25% damage to shields of troops in your formation. |
| DecreasedShieldDamage | 3 | Banner of Steel Shields | sturgia | -30% | -30% damage taken by shields of troops in the formation. | -30% damage to shields of troops in your formation. |
| IncreasedChargeDamage | 1 | Banner of the Horseman | vlandia | 10% | +10% charge damage dealt by mounted troops in the formation. | 10% charge damage to mounted troops in your formation. |
| IncreasedChargeDamage | 2 | Banner of the Squire | vlandia | 20% | +20% charge damage dealt by mounted troops in the formation. | 20% charge damage to mounted troops in your formation. |
| IncreasedChargeDamage | 3 | Banner of the Knight | vlandia | 30% | +30% charge damage dealt by mounted troops in the formation. | 30% charge damage to mounted troops in your formation. |
| IncreasedMeleeDamage | 1 | Standard of Fury | neutral_culture | 5% | +5% melee damage dealt by troops in the formation. | 5% melee damage to troops in your formation. |
| IncreasedMeleeDamage | 2 | Standard of Rage | neutral_culture | 10% | +10% melee damage dealt by troops in the formation. | 10% melee damage to troops in your formation. |
| IncreasedMeleeDamage | 3 | Standard of Wrath | neutral_culture | 15% | +15% melee damage dealt by troops in the formation. | 15% melee damage to troops in your formation. |
| IncreasedMeleeDamageAgainstMountedTroops | 1 | Deer Bane Flag | battania | 10% | +10% melee damage dealt by troops in the formation against cavalry or mounted targets. | 10% melee damage by troops in your formation against cavalry. |
| IncreasedMeleeDamageAgainstMountedTroops | 1 | Spear Bracing Banner | vlandia | 10% | +10% melee damage dealt by troops in the formation against cavalry or mounted targets. | 10% melee damage by troops in your formation against cavalry. |
| IncreasedMeleeDamageAgainstMountedTroops | 2 | Boar Bane Flag | battania | 20% | +20% melee damage dealt by troops in the formation against cavalry or mounted targets. | 20% melee damage by troops in your formation against cavalry. |
| IncreasedMeleeDamageAgainstMountedTroops | 2 | Spear Wall Banner | vlandia | 20% | +20% melee damage dealt by troops in the formation against cavalry or mounted targets. | 20% melee damage by troops in your formation against cavalry. |
| IncreasedMeleeDamageAgainstMountedTroops | 3 | Horse Bane Flag | battania | 30% | +30% melee damage dealt by troops in the formation against cavalry or mounted targets. | 30% melee damage by troops in your formation against cavalry. |
| IncreasedMeleeDamageAgainstMountedTroops | 3 | Pike Wall Banner | vlandia | 30% | +30% melee damage dealt by troops in the formation against cavalry or mounted targets. | 30% melee damage by troops in your formation against cavalry. |
| IncreasedMountMovementSpeed | 1 | Tug of the Roaming Horse | khuzait | 5% | +5% mount movement speed in the formation. | 5% movement speed to mounts in your formation. |
| IncreasedMountMovementSpeed | 2 | Tug of the Boundless Horde | khuzait | 8% | +8% mount movement speed in the formation. | 8% movement speed to mounts in your formation. |
| IncreasedMountMovementSpeed | 3 | Tug of the Endless Steppe | khuzait | 10% | +10% mount movement speed in the formation. | 10% movement speed to mounts in your formation. |
| IncreasedRangedDamage | 1 | Archer's Flag | neutral_culture | 4% | +4% ranged damage dealt by troops in the formation. | 4% ranged damage to troops in your formation. |
| IncreasedRangedDamage | 2 | Bowman's Flag | neutral_culture | 6% | +6% ranged damage dealt by troops in the formation. | 6% ranged damage to troops in your formation. |
| IncreasedRangedDamage | 3 | Marksman's Flag | neutral_culture | 8% | +8% ranged damage dealt by troops in the formation. | 8% ranged damage to troops in your formation. |
| IncreasedTroopMovementSpeed | 1 | Banner of Desert Winds | aserai | 15% | +15% infantry movement speed in the formation. | 15% movement speed to infantry in your formation. |
| IncreasedTroopMovementSpeed | 1 | Scout's Flag | battania | 15% | +15% infantry movement speed in the formation. | 15% movement speed to infantry in your formation. |
| IncreasedTroopMovementSpeed | 2 | Banner of Shifting Sands | aserai | 25% | +25% infantry movement speed in the formation. | 25% movement speed to infantry in your formation. |
| IncreasedTroopMovementSpeed | 2 | Ranger's Flag | battania | 25% | +25% infantry movement speed in the formation. | 25% movement speed to infantry in your formation. |
| IncreasedTroopMovementSpeed | 3 | Banner of Dust Devils | aserai | 30% | +30% infantry movement speed in the formation. | 30% movement speed to infantry in your formation. |
| IncreasedTroopMovementSpeed | 3 | Strider's Flag | battania | 30% | +30% infantry movement speed in the formation. | 30% movement speed to infantry in your formation. |
