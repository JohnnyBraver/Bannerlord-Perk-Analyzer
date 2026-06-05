# Battania Start Focus Leak Analysis

Generated: 2026-06-05T16:19:11+03:00

This report brute-forces Battania story-campaign character creation choices, prunes starts that exceed the current commander attribute target, and classifies where unavoidable focus leaks land.

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
| Bow | core | 2 | Bow 100 Merry Men under assisted Control 4. |
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
| Crossbow | side_plan | 0 | Side plan only; crossbow formations. |
| Engineering | side_plan | 0 | Side plan only; usually delegate engineer. |
| Roguery | side_plan | 0 | Side plan only; loot/crime build. |
| Tactics | soft | 5 | Soft leak unless Tactics 200 is planned. |

## Summary

- Attribute-valid paths after pruning: 15800
- Minimum default focus leaks: 2 across 390 paths
- Zero default focus leak paths: 0
- Paths with no side-plan focus and no cap overflow: 280
- Paths with no hard focus leak and no Tactics focus: 0
- Paths with no hard focus leak and at most 2 Tactics focus: 51
- Attribute branches pruned while walking: control_attribute 7673, other_attribute_overflow 9306, social_attribute 6945

Default focus leaks count side-plan focus, focus cap overflow, and Tactics soft focus. Optional one-focus QoL sinks such as Trade and Charm, plus planned Leadership, are not counted as leaks.

Main read: after dropping purchased Control, Battania campaign starts can avoid hard side-plan focus leaks, but they may or may not avoid Tactics focus depending on the culture-specific family choices. Treat Tactics as a soft leak unless Tactics 200 is deliberately part of the commander plan.

## Default Focus Leak Distribution

| Default Focus Leaks | Paths |
| ---: | ---: |
| 2 | 390 |
| 3 | 2140 |
| 4 | 4684 |
| 5 | 4850 |
| 6 | 2788 |
| 7 | 844 |
| 8 | 104 |

## No-Hard-Leak Tactics Distribution

| Tactics Focus | Paths |
| ---: | ---: |
| 2 | 51 |
| 3 | 128 |
| 4 | 89 |
| 5 | 12 |

## Side-Plan Leak Sources

These choices push focus into skills that are not part of the default shock-infantry commander plan.

| Skill | Stage | Choice | Attribute-valid Paths Affected |
| --- | --- | --- | ---: |
| Engineering | youth | stood guard with the garrisons. | 7280 |
| Engineering | escape | you threw up makeshift fortifications. | 5816 |
| Engineering | childhood | your aptitude for numbers. | 5816 |
| Roguery | escape | you tricked the raiders. | 5808 |
| Crossbow | youth | stood guard with the garrisons. | 3640 |
| Engineering | education | repaired projects. | 2908 |
| Engineering | education | studied with your private tutor. | 2908 |
| Roguery | education | hung out with the gangs in the alleys. | 2904 |
| Roguery | youth | marched with the camp followers. | 1816 |
| Roguery | adulthood | you had a famous escapade in town. | 704 |
| Roguery | adulthood | you had a famous escapade. | 704 |

## Focus Overflow

Overflow means the start grants more focus than the default plan can use before a skill becomes a variant choice.

- Overflow path counts: Bow 160, Trade 2432

## Best Minimum-Leak Paths

| Leaks | Start Attributes | Level-Up Attributes | Side-Plan Leaks | Overflow | Soft Leaks | Optional Sinks | Core Sinks | Path |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Trade 1 | Bow 1, Medicine 1, Riding 1, Scouting 1, Smithing 1, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> hunted small game. -> were a chieftain's servant. -> you invested some money in land. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Trade 1 | Bow 1, Medicine 1, Riding 1, Scouting 1, Smithing 1, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> hunted small game. -> were a chieftain's servant. -> you invested some money in a workshop. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Trade 1 | Bow 1, Medicine 1, Riding 1, Scouting 1, Smithing 1, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> hunted small game. -> joined a commander's staff. -> you invested some money in land. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Trade 1 | Bow 1, Medicine 1, Riding 1, Scouting 1, Smithing 1, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> hunted small game. -> joined a commander's staff. -> you invested some money in a workshop. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Trade 1 | Athletics 1, Bow 1, Medicine 2, One Handed 1, Riding 1, Smithing 1, Steward 1 | Healers -> your skill with horses. -> hunted small game. -> were a chieftain's servant. -> you invested some money in land. -> you subdued a raider. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Trade 1 | Athletics 1, Bow 1, Medicine 2, One Handed 1, Riding 1, Smithing 1, Steward 1 | Healers -> your skill with horses. -> hunted small game. -> were a chieftain's servant. -> you invested some money in a workshop. -> you subdued a raider. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Trade 1 | Athletics 1, Bow 1, Medicine 2, One Handed 1, Riding 1, Smithing 1, Steward 1 | Healers -> your skill with horses. -> hunted small game. -> joined a commander's staff. -> you invested some money in land. -> you subdued a raider. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Trade 1 | Athletics 1, Bow 1, Medicine 2, One Handed 1, Riding 1, Smithing 1, Steward 1 | Healers -> your skill with horses. -> hunted small game. -> joined a commander's staff. -> you invested some money in a workshop. -> you subdued a raider. |
| 2 | 3 - 2 - 3 - 5 - 2 - 3 | Cunning 2, Intelligence 4 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Bow 1, Medicine 1, Riding 1, Scouting 1, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> hunted small game. -> were a chieftain's servant. -> you led a caravan. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 5 - 2 - 3 | Cunning 2, Intelligence 4 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Bow 1, Medicine 1, Riding 1, Scouting 1, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> hunted small game. -> joined a commander's staff. -> you led a caravan. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 5 - 2 - 3 | Cunning 2, Intelligence 4 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Bow 1, Medicine 2, One Handed 1, Riding 1, Steward 1 | Healers -> your skill with horses. -> hunted small game. -> were a chieftain's servant. -> you led a caravan. -> you subdued a raider. |
| 2 | 3 - 2 - 3 - 5 - 2 - 3 | Cunning 2, Intelligence 4 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Bow 1, Medicine 2, One Handed 1, Riding 1, Steward 1 | Healers -> your skill with horses. -> hunted small game. -> joined a commander's staff. -> you led a caravan. -> you subdued a raider. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 1, Riding 1, Scouting 1, Smithing 2, Steward 1 | Healers -> your leadership skills. -> helped at building sites. -> were a chieftain's servant. -> you invested some money in land. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 1, Riding 1, Scouting 1, Smithing 2, Steward 1 | Healers -> your leadership skills. -> helped at building sites. -> were a chieftain's servant. -> you invested some money in a workshop. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 1, Riding 1, Scouting 1, Smithing 2, Steward 1 | Healers -> your leadership skills. -> helped at building sites. -> joined a commander's staff. -> you invested some money in land. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 1, Riding 1, Scouting 1, Smithing 2, Steward 1 | Healers -> your leadership skills. -> helped at building sites. -> joined a commander's staff. -> you invested some money in a workshop. -> you rode off on a fast horse. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 2, One Handed 1, Scouting 1, Smithing 1, Steward 1 | Healers -> your leadership skills. -> gathered herbs in the wild. -> were a chieftain's servant. -> you invested some money in land. -> you subdued a raider. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 2, One Handed 1, Scouting 1, Smithing 1, Steward 1 | Healers -> your leadership skills. -> gathered herbs in the wild. -> were a chieftain's servant. -> you invested some money in a workshop. -> you subdued a raider. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 2, One Handed 1, Scouting 1, Smithing 1, Steward 1 | Healers -> your leadership skills. -> gathered herbs in the wild. -> joined a commander's staff. -> you invested some money in land. -> you subdued a raider. |
| 2 | 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | none | none | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 2, One Handed 1, Scouting 1, Smithing 1, Steward 1 | Healers -> your leadership skills. -> gathered herbs in the wild. -> joined a commander's staff. -> you invested some money in a workshop. -> you subdued a raider. |

## Best No-Hard-Leak Paths

| Start Attributes | Level-Up Attributes | Soft Leaks | Optional Sinks | Core Sinks | Path |
| --- | --- | --- | --- | --- | --- |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Trade 1 | Bow 1, Medicine 1, Riding 1, Scouting 1, Smithing 1, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> hunted small game. -> were a chieftain's servant. -> you invested some money in land. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Trade 1 | Bow 1, Medicine 1, Riding 1, Scouting 1, Smithing 1, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> hunted small game. -> were a chieftain's servant. -> you invested some money in a workshop. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Trade 1 | Bow 1, Medicine 1, Riding 1, Scouting 1, Smithing 1, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> hunted small game. -> joined a commander's staff. -> you invested some money in land. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Trade 1 | Bow 1, Medicine 1, Riding 1, Scouting 1, Smithing 1, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> hunted small game. -> joined a commander's staff. -> you invested some money in a workshop. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Trade 1 | Athletics 1, Bow 1, Medicine 2, One Handed 1, Riding 1, Smithing 1, Steward 1 | Healers -> your skill with horses. -> hunted small game. -> were a chieftain's servant. -> you invested some money in land. -> you subdued a raider. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Trade 1 | Athletics 1, Bow 1, Medicine 2, One Handed 1, Riding 1, Smithing 1, Steward 1 | Healers -> your skill with horses. -> hunted small game. -> were a chieftain's servant. -> you invested some money in a workshop. -> you subdued a raider. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Trade 1 | Athletics 1, Bow 1, Medicine 2, One Handed 1, Riding 1, Smithing 1, Steward 1 | Healers -> your skill with horses. -> hunted small game. -> joined a commander's staff. -> you invested some money in land. -> you subdued a raider. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Trade 1 | Athletics 1, Bow 1, Medicine 2, One Handed 1, Riding 1, Smithing 1, Steward 1 | Healers -> your skill with horses. -> hunted small game. -> joined a commander's staff. -> you invested some money in a workshop. -> you subdued a raider. |
| 3 - 2 - 3 - 5 - 2 - 3 | Cunning 2, Intelligence 4 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Bow 1, Medicine 1, Riding 1, Scouting 1, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> hunted small game. -> were a chieftain's servant. -> you led a caravan. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 5 - 2 - 3 | Cunning 2, Intelligence 4 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Bow 1, Medicine 1, Riding 1, Scouting 1, Steward 1, Throwing 1, Two Handed 1 | Healers -> your brawn. -> hunted small game. -> joined a commander's staff. -> you led a caravan. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 5 - 2 - 3 | Cunning 2, Intelligence 4 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Bow 1, Medicine 2, One Handed 1, Riding 1, Steward 1 | Healers -> your skill with horses. -> hunted small game. -> were a chieftain's servant. -> you led a caravan. -> you subdued a raider. |
| 3 - 2 - 3 - 5 - 2 - 3 | Cunning 2, Intelligence 4 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Bow 1, Medicine 2, One Handed 1, Riding 1, Steward 1 | Healers -> your skill with horses. -> hunted small game. -> joined a commander's staff. -> you led a caravan. -> you subdued a raider. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 1, Riding 1, Scouting 1, Smithing 2, Steward 1 | Healers -> your leadership skills. -> helped at building sites. -> were a chieftain's servant. -> you invested some money in land. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 1, Riding 1, Scouting 1, Smithing 2, Steward 1 | Healers -> your leadership skills. -> helped at building sites. -> were a chieftain's servant. -> you invested some money in a workshop. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 1, Riding 1, Scouting 1, Smithing 2, Steward 1 | Healers -> your leadership skills. -> helped at building sites. -> joined a commander's staff. -> you invested some money in land. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 1, Riding 1, Scouting 1, Smithing 2, Steward 1 | Healers -> your leadership skills. -> helped at building sites. -> joined a commander's staff. -> you invested some money in a workshop. -> you rode off on a fast horse. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 2, One Handed 1, Scouting 1, Smithing 1, Steward 1 | Healers -> your leadership skills. -> gathered herbs in the wild. -> were a chieftain's servant. -> you invested some money in land. -> you subdued a raider. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 2, One Handed 1, Scouting 1, Smithing 1, Steward 1 | Healers -> your leadership skills. -> gathered herbs in the wild. -> were a chieftain's servant. -> you invested some money in a workshop. -> you subdued a raider. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 2, One Handed 1, Scouting 1, Smithing 1, Steward 1 | Healers -> your leadership skills. -> gathered herbs in the wild. -> joined a commander's staff. -> you invested some money in land. -> you subdued a raider. |
| 3 - 2 - 3 - 4 - 2 - 4 | Cunning 3, Intelligence 3 | Tactics 2 | Charm 1, Leadership 1, Trade 1 | Athletics 1, Medicine 2, One Handed 1, Scouting 1, Smithing 1, Steward 1 | Healers -> your leadership skills. -> gathered herbs in the wild. -> joined a commander's staff. -> you invested some money in a workshop. -> you subdued a raider. |

## Common Leak Profiles

| Paths | Profile |
| ---: | --- |
| 184 | side=Engineering 2; overflow=none; tactics=2; optional=Leadership 1, Trade 1 |
| 156 | side=Engineering 1, Roguery 1; overflow=none; tactics=2; optional=Leadership 1, Trade 1 |
| 141 | side=Engineering 1, Roguery 1; overflow=none; tactics=3; optional=Leadership 1, Trade 1 |
| 139 | side=Engineering 1, Roguery 1; overflow=none; tactics=3; optional=Leadership 2 |
| 138 | side=Engineering 2, Roguery 1; overflow=none; tactics=2; optional=Leadership 1, Trade 1 |
| 134 | side=Engineering 1; overflow=none; tactics=3; optional=Leadership 2 |
| 121 | side=Engineering 2; overflow=none; tactics=1; optional=Charm 1, Leadership 1, Trade 1 |
| 114 | side=Engineering 1, Roguery 1; overflow=none; tactics=3; optional=Leadership 1 |
| 113 | side=Engineering 1; overflow=none; tactics=2; optional=Leadership 1, Trade 1 |
| 105 | side=Engineering 1; overflow=none; tactics=3; optional=Leadership 1, Trade 1 |
| 98 | side=Engineering 2; overflow=none; tactics=2; optional=Leadership 2 |
| 96 | side=Engineering 1, Roguery 1; overflow=none; tactics=2; optional=Charm 1, Leadership 1, Trade 1 |
| 89 | side=Engineering 1; overflow=none; tactics=3; optional=Leadership 1 |
| 88 | side=Engineering 1, Roguery 1; overflow=none; tactics=2; optional=Charm 1, Leadership 1 |
| 86 | side=Engineering 1, Roguery 1; overflow=none; tactics=1; optional=Charm 1, Leadership 1, Trade 1 |
| 85 | side=Engineering 2; overflow=none; tactics=2; optional=Leadership 1 |
| 85 | side=Engineering 1; overflow=none; tactics=2; optional=Charm 1, Leadership 1, Trade 1 |
| 83 | side=Engineering 2; overflow=none; tactics=1; optional=Leadership 1, Trade 1 |
| 83 | side=Engineering 2; overflow=none; tactics=3; optional=Leadership 2 |
| 83 | side=Engineering 2; overflow=none; tactics=3; optional=Leadership 1, Trade 1 |
