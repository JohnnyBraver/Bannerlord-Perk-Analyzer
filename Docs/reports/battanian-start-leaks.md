# Battania Start Focus Leak Analysis

Generated: 2026-06-12T18:46:25+03:00

This report brute-forces Battania story-campaign character creation choices, applies the game's parent-occupation and culture option gates, prunes starts that exceed the current commander attribute target, and classifies where unavoidable focus leaks land.

## Assumptions

- Culture: Battania
- Stage order: family, childhood, education, youth, adulthood, escape
- Base attributes: Control 2, Cunning 2, Endurance 2, Intelligence 2, Social 2, Vigor 2
- Target attributes: Control 2, Cunning 7, Endurance 3, Intelligence 7, Social 2, Vigor 3
- Total combinations before pruning: 528768

## Focus Buckets

| Skill | Bucket | Cap | Read |
| --- | --- | ---: | --- |
| Athletics | core | 5 | Physical attribute and foot-party enabler. |
| Medicine | core | 5 | Core 275 troop-survival target. |
| One Handed | core | 5 | Core Vigor infantry package. |
| Polearm | core | 5 | Core Vigor infantry package. |
| Riding | core | 1 | Only needs one focus for Riding 100 in infantry doctrine. |
| Scouting | core | 5 | Core 275 engagement-control target. |
| Smithing | core | 5 | Attribute/focus engine and money engine. |
| Steward | core | 5 | Core party-scaling target if the player is quartermaster. |
| Throwing | core | 2 | Throwing 125 Skirmisher under assisted Control 4. |
| Two Handed | core | 3 | Default stop is 175; later focus is optional. |
| Charm | optional | 1 | One-focus QoL or renown pickup. |
| Leadership | optional | 5 | Useful party-size stretch; Social still stays at 2. |
| Trade | optional | 1 | One-focus price-marking QoL pickup. |
| Bow | side_plan | 0 | Ranged-side plan only; Bow 100 Merry Men costs two focus under assisted Control 4 and is too thin for default infantry. |
| Crossbow | side_plan | 0 | Side plan only; crossbow formations. |
| Engineering | side_plan | 0 | Convertible hard leak: delegate by default, but Engineering 225 Metallurgy can justify a late player-engineer stretch. |
| Roguery | side_plan | 0 | Side plan only; loot/crime build. |
| Tactics | soft | 5 | Soft leak unless Tactics 200 is planned. |

## Summary

- Attribute-valid paths after pruning: 926
- Minimum default focus leaks: 2 across 12 paths
- Zero default focus leak paths: 0
- Paths with no side-plan focus and no cap overflow: 8
- Paths with no hard focus leak and no Tactics focus: 0
- Paths with no hard focus leak and at most 2 Tactics focus: 2
- Attribute branches pruned while walking: adulthood_condition 768, control_attribute 543, education_condition 84, other_attribute_overflow 704, social_attribute 543, youth_condition 484

Default focus leaks count side-plan focus, focus cap overflow, and Tactics soft focus. Optional one-focus QoL sinks such as Trade and Charm, plus planned Leadership, are not counted as leaks.

Main read: after dropping purchased Control, Battania campaign starts can avoid hard side-plan focus leaks, but they may or may not avoid Tactics focus depending on the culture-specific family choices. Treat Tactics as a soft leak unless Tactics 200 is deliberately part of the commander plan.

## Default Focus Leak Distribution

| Default Focus Leaks | Paths |
| ---: | ---: |
| 2 | 12 |
| 3 | 76 |
| 4 | 196 |
| 5 | 269 |
| 6 | 219 |
| 7 | 114 |
| 8 | 35 |
| 9 | 5 |

## No-Hard-Leak Tactics Distribution

| Tactics Focus | Paths |
| ---: | ---: |
| 2 | 2 |
| 3 | 4 |
| 4 | 2 |

## Side-Plan Leak Sources

These choices push focus into skills that are not part of the default shock-infantry commander plan.

| Skill | Stage | Choice | Attribute-valid Paths Affected |
| --- | --- | --- | ---: |
| Bow | youth | stood guard with the garrisons. | 351 |
| Engineering | youth | stood guard with the garrisons. | 351 |
| Engineering | escape | you threw up makeshift fortifications. | 351 |
| Roguery | escape | you tricked the raiders. | 351 |
| Engineering | childhood | your aptitude for numbers. | 351 |
| Engineering | education | repaired projects. | 255 |
| Bow | education | hunted small game. | 255 |
| Bow | family | Members of the chieftain's hearthguard | 112 |
| Roguery | education | hung out with the gangs in the alleys. | 96 |
| Engineering | education | studied with your private tutor. | 96 |
| Roguery | adulthood | you had a famous escapade in town. | 96 |
| Roguery | adulthood | you had a famous escapade. | 16 |

## Focus Overflow

Overflow means the start grants more focus than the default plan can use before a skill becomes a variant choice.

- Overflow path counts: Trade 127

## Best Minimum-Leak Paths

| Leaks | Start Attributes | Level-Up Attributes | Side-Plan Leaks | Overflow | Soft Leaks | Optional Sinks | Core Sinks | Path |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 2, One Handed 1, Scouting 1, Smithing 1, Steward 1 | Healers -> your leadership skills. -> gathered herbs in the wild. -> were a chieftain's servant. -> you invested some money in land. -> you subdued a raider. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Medicine 1, Riding 1, Scouting 1, Smithing 2, Steward 1, Two Handed 1 | Healers -> your leadership skills. -> worked in the village smithy. -> were a chieftain's servant. -> you invested some money in land. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 3 - 2 - 5 | Cunning 4, Intelligence 2 | Engineering 1 | none | Tactics 1 | Charm 1, Trade 1 | Medicine 2, Scouting 1, Smithing 1, Steward 1, Throwing 1, Two Handed 2 | Healers -> your brawn. -> gathered herbs in the wild. -> were a chieftain's servant. -> you invested some money in land. -> you threw up makeshift fortifications. |
| 2 | 3 - 2 - 3 - 3 - 2 - 5 | Cunning 4, Intelligence 2 | Engineering 1 | none | Tactics 1 | Charm 1, Trade 1 | Medicine 1, Riding 1, Scouting 1, Smithing 2, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> repaired projects. -> were a chieftain's servant. -> you invested some money in land. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 3 - 2 - 5 | Cunning 4, Intelligence 2 | Engineering 1 | none | Tactics 1 | Charm 1, Trade 1 | Athletics 1, Medicine 2, One Handed 1, Riding 1, Smithing 2, Steward 1 | Healers -> your skill with horses. -> repaired projects. -> were a chieftain's servant. -> you invested some money in land. -> you subdued a raider. |
| 2 | 3 - 2 - 3 - 3 - 2 - 5 | Cunning 4, Intelligence 2 | Engineering 1 | none | Tactics 1 | Charm 1, Trade 1 | Medicine 2, Riding 1, Smithing 2, Steward 1, Two Handed 2 | Healers -> your skill with horses. -> worked in the village smithy. -> were a chieftain's servant. -> you invested some money in land. -> you threw up makeshift fortifications. |
| 2 | 3 - 2 - 3 - 3 - 2 - 5 | Cunning 4, Intelligence 2 | Engineering 1 | none | Tactics 1 | Charm 1, Leadership 1, Trade 1 | Medicine 2, One Handed 1, Polearm 1, Scouting 1, Smithing 1, Two Handed 1 | Healers -> your leadership skills. -> gathered herbs in the wild. -> trained with the infantry. -> you invested some money in land. -> you threw up makeshift fortifications. |
| 2 | 3 - 2 - 3 - 3 - 2 - 5 | Cunning 4, Intelligence 2 | Engineering 1 | none | Tactics 1 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 1, One Handed 1, Polearm 1, Riding 1, Smithing 2 | Healers -> your leadership skills. -> repaired projects. -> trained with the hearth guard. -> you invested some money in land. -> you subdued a raider. |
| 2 | 3 - 2 - 3 - 3 - 2 - 5 | Cunning 4, Intelligence 2 | Engineering 1 | none | Tactics 1 | Charm 1, Leadership 1, Trade 1 | Medicine 1, One Handed 1, Polearm 1, Riding 1, Scouting 1, Smithing 2 | Healers -> your leadership skills. -> repaired projects. -> trained with the infantry. -> you invested some money in land. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 3 - 2 - 5 | Cunning 4, Intelligence 2 | Engineering 1 | none | Tactics 1 | Charm 1, Leadership 1, Trade 1 | Medicine 1, Polearm 1, Riding 1, Smithing 2, Two Handed 2 | Healers -> your leadership skills. -> worked in the village smithy. -> trained with the hearth guard. -> you invested some money in land. -> you threw up makeshift fortifications. |
| 2 | 3 - 2 - 3 - 2 - 2 - 6 | Cunning 5, Intelligence 1 | Engineering 2 | none | none | Charm 1, Trade 1 | Medicine 1, Polearm 1, Riding 1, Smithing 2, Throwing 1, Two Handed 2 | Healers -> your brawn. -> repaired projects. -> trained with the hearth guard. -> you invested some money in land. -> you threw up makeshift fortifications. |
| 2 | 3 - 2 - 3 - 2 - 2 - 6 | Cunning 5, Intelligence 1 | Engineering 2 | none | none | Charm 1, Trade 1 | Medicine 2, One Handed 1, Polearm 1, Riding 1, Smithing 2, Two Handed 1 | Healers -> your skill with horses. -> repaired projects. -> trained with the infantry. -> you invested some money in land. -> you threw up makeshift fortifications. |

## Best No-Hard-Leak Paths

| Start Attributes | Level-Up Attributes | Soft Leaks | Optional Sinks | Core Sinks | Path |
| --- | --- | --- | --- | --- | --- |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 2, One Handed 1, Scouting 1, Smithing 1, Steward 1 | Healers -> your leadership skills. -> gathered herbs in the wild. -> were a chieftain's servant. -> you invested some money in land. -> you subdued a raider. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Medicine 1, Riding 1, Scouting 1, Smithing 2, Steward 1, Two Handed 1 | Healers -> your leadership skills. -> worked in the village smithy. -> were a chieftain's servant. -> you invested some money in land. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 5 - 2 - 3 | Cunning 2, Intelligence 4 | Tactics 3 | Leadership 1, Trade 1 | Athletics 1, Medicine 1, One Handed 1, Scouting 2, Smithing 1, Steward 1 | Foresters -> your leadership skills. -> gathered herbs in the wild. -> were a chieftain's servant. -> you invested some money in land. -> you subdued a raider. |
| 3 - 2 - 3 - 5 - 2 - 3 | Cunning 2, Intelligence 4 | Tactics 3 | Leadership 1, Trade 1 | Riding 1, Scouting 2, Smithing 2, Steward 1, Two Handed 1 | Foresters -> your leadership skills. -> worked in the village smithy. -> were a chieftain's servant. -> you invested some money in land. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 5 - 2 - 3 | Cunning 2, Intelligence 4 | Tactics 3 | Charm 1, Leadership 2 | Athletics 1, Medicine 2, One Handed 1, Scouting 1, Steward 1 | Healers -> your leadership skills. -> gathered herbs in the wild. -> were a chieftain's servant. -> you led a successful manhunt. -> you subdued a raider. |
| 3 - 2 - 3 - 5 - 2 - 3 | Cunning 2, Intelligence 4 | Tactics 3 | Charm 1, Leadership 2 | Medicine 1, Riding 1, Scouting 1, Smithing 1, Steward 1, Two Handed 1 | Healers -> your leadership skills. -> worked in the village smithy. -> were a chieftain's servant. -> you led a successful manhunt. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 6 - 2 - 2 | Cunning 1, Intelligence 5 | Tactics 4 | Leadership 2 | Athletics 1, Medicine 1, One Handed 1, Scouting 2, Steward 1 | Foresters -> your leadership skills. -> gathered herbs in the wild. -> were a chieftain's servant. -> you led a successful manhunt. -> you subdued a raider. |
| 3 - 2 - 3 - 6 - 2 - 2 | Cunning 1, Intelligence 5 | Tactics 4 | Leadership 2 | Riding 1, Scouting 2, Smithing 1, Steward 1, Two Handed 1 | Foresters -> your leadership skills. -> worked in the village smithy. -> were a chieftain's servant. -> you led a successful manhunt. -> you rode off on a fast horse. |

## Common Leak Profiles

| Paths | Profile |
| ---: | --- |
| 7 | side=Engineering 2; overflow=none; tactics=2; optional=Leadership 1, Trade 1 |
| 7 | side=Bow 1, Engineering 2; overflow=none; tactics=2; optional=Leadership 1, Trade 1 |
| 6 | side=Bow 1, Engineering 2; overflow=none; tactics=1; optional=Charm 1, Leadership 1 |
| 6 | side=Engineering 1; overflow=none; tactics=2; optional=Charm 1, Leadership 1 |
| 6 | side=Bow 1, Engineering 2; overflow=none; tactics=1; optional=Charm 1, Leadership 1, Trade 1 |
| 6 | side=Engineering 1; overflow=none; tactics=2; optional=Charm 1, Leadership 1, Trade 1 |
| 6 | side=Engineering 2; overflow=none; tactics=1; optional=Charm 1, Leadership 1, Trade 1 |
| 6 | side=Bow 1, Engineering 2; overflow=none; tactics=2; optional=Leadership 1 |
| 6 | side=Engineering 1; overflow=none; tactics=3; optional=Leadership 1 |
| 6 | side=Engineering 1; overflow=none; tactics=3; optional=Leadership 1, Trade 1 |
| 5 | side=Engineering 1; overflow=none; tactics=3; optional=Leadership 2 |
| 5 | side=Engineering 1; overflow=none; tactics=2; optional=Leadership 1, Trade 1 |
| 5 | side=Engineering 1, Roguery 1; overflow=none; tactics=3; optional=Leadership 1, Trade 1 |
| 5 | side=Engineering 2; overflow=Trade 1; tactics=1; optional=Trade 2 |
| 5 | side=Engineering 1, Roguery 1; overflow=none; tactics=2; optional=Charm 1, Leadership 1 |
| 5 | side=Bow 1, Engineering 3; overflow=none; tactics=1; optional=Charm 1, Leadership 1, Trade 1 |
| 5 | side=Engineering 2; overflow=none; tactics=2; optional=Charm 1, Leadership 1, Trade 1 |
| 5 | side=Engineering 1, Roguery 1; overflow=none; tactics=3; optional=Leadership 1 |
| 5 | side=Bow 1, Engineering 3; overflow=none; tactics=2; optional=Leadership 1, Trade 1 |
| 5 | side=Engineering 2; overflow=none; tactics=3; optional=Leadership 1, Trade 1 |
