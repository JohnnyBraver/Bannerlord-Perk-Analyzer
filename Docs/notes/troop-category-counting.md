# Troop Category Counting

This note checks how Bannerlord counts ranged, foot, mounted, infantry, cavalry, and horse-archer troops for perk-style filters.

Sources used for this pass:

- `TaleWorlds.Core.TroopUsageFlags`
- `TaleWorlds.Core.FormationClassExtensions.GetTroopUsageFlags`
- `Helpers.PerkHelper.GetCaptainPerksForTroopUsages`
- `TaleWorlds.MountAndBlade.QueryLibrary.IsInfantry`
- `TaleWorlds.MountAndBlade.QueryLibrary.IsRanged`
- `TaleWorlds.MountAndBlade.QueryLibrary.IsCavalry`
- `TaleWorlds.MountAndBlade.QueryLibrary.IsRangedCavalry`
- `TaleWorlds.Core.BasicCharacterObject`
- `TaleWorlds.CampaignSystem.CharacterObject`

## Raw Flags

`TroopUsageFlags` is not a four-way formation enum. It is a bitmask:

| Value | Flag |
| ---: | --- |
| 0 | None |
| 1 | OnFoot |
| 2 | Mounted |
| 4 | Melee |
| 8 | Ranged |
| 16 | OneHandedUser |
| 32 | ShieldUser |
| 64 | TwoHandedUser |
| 128 | PolearmUser |
| 256 | BowUser |
| 512 | ThrownUser |
| 1024 | CrossbowUser |
| 65535 | Undefined |

In our generated data, `65535` is still written as `all` because `PerkHelper.GetCaptainPerksForTroopUsages` treats it as the special unfiltered value rather than as a normal mask.

## Formation Masks

The regular formation classes map onto those flags like this:

| Formation class | Flags | Numeric mask |
| --- | --- | ---: |
| Infantry | `OnFoot`, `Melee`, `OneHandedUser`, `ShieldUser`, `TwoHandedUser`, `PolearmUser` | 245 |
| Ranged | `OnFoot`, `Ranged`, `BowUser`, `ThrownUser`, `CrossbowUser` | 1801 |
| Cavalry | `Mounted`, `Melee`, `OneHandedUser`, `ShieldUser`, `TwoHandedUser`, `PolearmUser` | 246 |
| HorseArcher | `Mounted`, `Ranged`, `BowUser`, `ThrownUser`, `CrossbowUser` | 1802 |

Captain perk lookup uses `HasAllFlags`, not "has any flag." That makes combined masks strict:

| Perk mask | Matches by formation flags |
| --- | --- |
| `OnFoot` | Infantry and foot ranged |
| `Mounted` | Cavalry and horse archers |
| `Melee` | Infantry and cavalry |
| `Ranged` | Foot ranged and horse archers |
| `ThrownUser` | Troops classified as throwing-weapon users; this does not by itself imply `Ranged` |
| `OnFoot`, `Ranged` | Foot ranged only |
| `Mounted`, `Ranged` | Horse archers only |
| `Mounted`, `Melee` | Cavalry only |
| `Mounted`, `ThrownUser` | Mounted troops with throwing weapons |

## Live-Agent Queries

Live mission queries use a different set of predicates:

| Query | Meaning |
| --- | --- |
| `IsInfantry(agent)` | no mount and not ranged |
| `IsRanged(agent)` | no mount and ranged |
| `IsCavalry(agent)` | has mount and not ranged |
| `IsRangedCavalry(agent)` | has mount and ranged |

So live-agent `IsRanged` means foot ranged only. That differs from the `TroopUsageFlags.Ranged` bit, which is shared by foot ranged and horse archers when formation masks are used.

## Regular Troops And Heroes

For regular troop records, `BasicCharacterObject.IsRanged` and `BasicCharacterObject.IsMounted` are stored character flags, and `BasicCharacterObject.IsInfantry` is calculated as not ranged and not mounted.

Thrown weapons are tracked separately. `AgentOriginUtilities.GetDefaultTraitsMask` reads `BasicCharacterObject.IsRanged` for the ranged-vs-melee side, then separately reads `IAgentOriginBase.HasThrownWeapon`. A melee troop carrying javelins or throwing axes can therefore be a throwing-weapon user without becoming a ranged troop.

For heroes, `CharacterObject` overrides the stored flags from equipment:

- Mounted means the hero has an item in the horse slot.
- Ranged checks the first four equipment slots for bow, crossbow, or sling item types. In the inspected getter, thrown-only equipment did not count as ranged.
- Hero formation class is then derived from mounted plus ranged: infantry, ranged, cavalry, or horse archer.

## Practical Read

- "Foot troops" should be read as `OnFoot`: infantry plus foot ranged, unless the consuming code uses a stricter live-agent query.
- "Infantry" is not the same as "foot troops." In the core/live predicates, infantry means not ranged and not mounted.
- "Ranged troops" is context-dependent. A `TroopUsageFlags.Ranged` perk can include horse archers; a `QueryLibrary.IsRanged` check excludes mounted ranged troops.
- "Throwing weapon users" are not automatically "ranged troops." Check for `ThrownUser` masks separately.
- "Mounted troops" should be read as `Mounted`: melee cavalry plus horse archers, unless the code also requires `Melee` or uses `IsCavalry`.
- "Cavalry" as a formation class is mounted melee. A plain `Mounted` mask is broader than that.
