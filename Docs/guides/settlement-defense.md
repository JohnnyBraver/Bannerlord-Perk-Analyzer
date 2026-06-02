# Settlement Defense

This note covers settlement defense as a governor and management category: security, garrison strength, militia gain and quality, siege food pressure, walls, siege engines, and bombardment resilience. It focuses on settlement-facing effects, not field-battle captain perks.

## Main Takeaways

- Security is both defense and economy. It affects loyalty and tax behavior, and it drifts naturally toward `50`.
- The security model uses garrison strength, not just headcount. Unwounded troops contribute through troop power, and ranged/mounted sub-strength is tracked separately.
- Ranged and mounted security perks use the troop's data flags. Mounted ranged troops can contribute to both mounted and ranged strength in the security calculation.
- Militia quantity and militia quality are separate. `Drills` looks terrible as party XP, but its governor veteran-militia side appears to be real.
- Siege defense is a stack of food, wall HP, attrition reduction, fortification, bombardment, ballista accuracy, and garrison/militia strength.

## Security Drift

The extracted security drift formula is:

```text
dailySecurityDrift = -1 * (security - 50) / 15
```

Examples:

| Current security | Daily drift |
| ---: | ---: |
| 20 | +2.00 |
| 35 | +1.00 |
| 50 | 0.00 |
| 65 | -1.00 |
| 80 | -2.00 |

The settlement wants to return to `50` unless other forces keep pushing it. That makes flat security perks useful, but it also means very high security needs ongoing support.

High prosperity also pushes security down:

```text
prosperitySecurityEffect = max(-5, -0.0005 * prosperity)
```

So a very prosperous town needs more defense management than a poor town.

## Garrison Strength And Troop Categories

The extracted `CalculateStrengthOfGarrisonParty` walks the garrison and uses `MilitaryPowerModel.GetTroopPower` on unwounded troops. It separately totals:

| Bucket | What the model appears to count | Practical read |
| --- | --- | --- |
| Total strength | All unwounded garrison troops by troop power | Elite troops count more than weak troops. |
| Ranged strength | Troops with the ranged flag | Archer and crossbow security perks scale with ranged power. |
| Mounted strength | Troops with the mounted flag | Cavalry security perks scale with mounted power. |

Because ranged and mounted are separate checks, mounted ranged units can contribute to both mounted and ranged security buckets. This is settlement-security logic, not the exact same thing as every live-battle perk filter.

## Defense Governor Perks

### Security

| Skill | Level | Perk | Effect | Read |
| --- | ---: | --- | --- | --- |
| One Handed | 50 | `To Be Blunt` | +0.5 security/day. | Cheap flat security. |
| One Handed | 175 | `Stand United` | +30% security from garrison. | Scales with total garrison power. |
| Bow | 100 | `Mounted Archery` | +20% security from archers. | Scales with ranged/archer garrison power. |
| Bow | 250 | `Ranger's Swiftness` | +20% security from archers. | Late ranged-garrison security. |
| Crossbow | 100 | `Renowned Marksmen` | +30% security from ranged garrison. | Strong if the garrison has real ranged power. |
| Leadership | 75 | `Authority` | +20% security from town garrison. | Good broad garrison-scaling perk. |
| Riding | 125 | `Relief Force` | +20% security from mounted troops. | Better with cavalry or mounted-ranged garrisons. |
| Roguery | 75 | `Know-How` | +1 security/day. | Strong flat security from Roguery. |
| Polearm | 150 | `Skewer` | +1 security/day. | Strong flat security. |
| Tactics | 250 | `Gens d'armes` | +1 security/day. | Late Tactics governor payoff. |
| Throwing | 150 | `Focus` | +1 security/day. | Strong flat security. |

### Militia Gain And Quality

| Skill | Level | Perk | Effect | Read |
| --- | ---: | --- | --- | --- |
| Bow | 100 | `Merry Men` | +1 militia recruitment/day. | Simple militia growth. |
| Crossbow | 200 | `Long Shots` | +1 daily militia. | Later ranged-skill militia growth. |
| One Handed | 50 | `Swift Strike` | +1 militia/day. | Cheap militia growth. |
| Polearm | 50 | `Keep at Bay` | +1 militia/day. | Cheap militia growth. |
| Roguery | 225 | `Arms Dealer` | +200% militia/day in besieged settlement. | Emergency siege-side militia growth. |
| Steward | 50 | `Seven Veterans` | +10% veteran militia rate. | Early quality increase. |
| Leadership | 150 | `Citizen Militia` | +20% veteran militia rate. | Good quality layer. |
| Polearm | 200 | `Drills` | +100% veteran militia spawn rate. | Governor side appears real, unlike its rounded-to-zero party XP side. |

The model has a dedicated veteran militia spawn chance path, so these should be evaluated as militia-quality perks rather than generic troop XP perks.

### Garrison Size And XP

| Skill | Level | Perk | Effect | Read |
| --- | ---: | --- | --- | --- |
| Leadership | 25 | `Raise The Meek` | +3 daily XP to garrison troops. | Early garrison training. |
| Bow | 200 | `Bulls Eye` | +3 daily XP to garrison troops. | Ranged-skill path to garrison training. |
| Polearm | 150 | `Guards` | +20% garrisoned cavalry XP. | Cavalry-specific garrison training. |
| Two Handed | 150 | `Projectile Deflection` | +10% garrison troop XP. | Broad garrison XP boost. |
| One Handed | 150 | `Corps-a-corps` | +30 garrison size. | Larger defensive roster. |
| Leadership | 150 | `Veteran's Respect` | +20 garrison size. | Smaller but in Leadership. |

### Siege Food And Attrition

| Skill | Level | Perk | Effect | Read |
| --- | ---: | --- | --- | --- |
| Athletics | 225 | `Strong Legs` | -20% food consumption under siege. | Major siege endurance perk. |
| Medicine | 50 | `Triage Tent` | -5% besieged settlement food consumption. | Small but early. |
| Steward | 175 | `Gourmet` | -10% garrison food consumption during sieges. | Good with large garrisons. |
| Roguery | 225 | `Dirty Fighting` | +2 random food items smuggled to besieged settlement. | Strange but useful siege sustain. |
| Medicine | 250 | `Battle Hardened` | -25% siege attrition loss. | High-end anti-attrition layer. |

### Walls, Siege Engines, And Bombardment

| Skill | Level | Perk | Effect | Read |
| --- | ---: | --- | --- | --- |
| Engineering | 75 | `Military Planner` | +25% projects in governed castle. | Castle-development defense. |
| Engineering | 125 | `Salvager` | +0.1% siege engine build speed per militia. | Militia helps engine building. |
| Engineering | 150 | `Stonecutters` | +30% fortification, aqueduct, and barrack projects. | Defensive construction speed. |
| Engineering | 200 | `Engineering Guilds` | +25% wall hit points. | Direct siege durability. |
| Crossbow | 225 | `Pavise` | +30% ballista accuracy. | Active siege-defense tool. |
| Tactics | 150 | `On The March` | +20% fortification bonus. | Defensive autoresolve/siege value. |
| Tactics | 175 | `Make Them Pay` | +25% damage to besieging siege engines. | Better bombardment pressure. |
| Tactics | 175 | `Pick Them Off The Walls` | +25% chance for double damage to besieging troops in bombardment. | Improves pre-assault attrition. |
| Two Handed | 125 | `Confidence` | +30% military project build speed. | Helps defensive project queue. |

## Practical Defense Builds

For a security governor:

- `Leadership 75 Authority`, `One Handed 175 Stand United`, and the ranged/mounted security perks scale with actual garrison strength.
- Flat `+1 security/day` perks are excellent for keeping a town above bad thresholds, especially conquered towns with high prosperity.
- Ranged or mounted security perks are best when the garrison is intentionally built around those troop types.

For a siege governor:

- Engineering is the central tree: wall HP, construction speed, fortification projects, and siege engines all live there.
- Steward and Athletics food-consumption reductions can matter as much as walls if the settlement is going to be starved out.
- Medicine 250 `Battle Hardened` is a serious high-end defensive perk because it reduces siege attrition loss.

For militia:

- Quantity perks get bodies into the settlement.
- Veteran militia perks improve the quality of the spawned militia.
- `Drills` deserves a split evaluation: avoid it for party XP, but do not dismiss the governor militia-quality side.

## Evidence

Primary local evidence:

- `Data/generated/settlement-methods.json`: extracted `DefaultSettlementSecurityModel`, `DefaultSettlementMilitiaModel`, food, construction, and siege-adjacent settlement methods.
- `Data/export/perk-effects.json`: postprocessed governor perk effects and custom classifications.
- `Docs/notes/troop-category-counting.md`: broader troop category notes for ranged, mounted, foot, infantry, and cavalry wording.
- `Docs/notes/party-management.md`: notes on the `Drills` party XP bug, separate from the governor militia-quality side.
