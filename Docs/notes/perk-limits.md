# Perk Limits

Bannerlord uses the same skill limit and peak learning range formulas for every skill:

`limit = 4 + 14 * (attribute - 1) + 40 * focus`

`peak learning range = 10 * (attribute - 1) + 30 * focus`

The limit is where learning rate reaches zero. Peak learning range is the lower threshold where the over-limit penalty starts. The planner optimizes against the limit because that is what matters for reaching perks.

Attribute points apply to every skill in the same attribute group. For example, raising Control helps Bow, Crossbow, and Throwing together.

The build planner treats 2 attribute and 0 focus as the default practical floor, but the full grid below includes 1 attribute because it explains the formula.

## Skill Limit Grid

Cells are `limit (peak learning range)`.

| Attribute | Focus 0 | Focus 1 | Focus 2 | Focus 3 | Focus 4 | Focus 5 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4 (0) | 44 (30) | 84 (60) | 124 (90) | 164 (120) | 204 (150) |
| 2 | 18 (10) | 58 (40) | 98 (70) | 138 (100) | 178 (130) | 218 (160) |
| 3 | 32 (20) | 72 (50) | 112 (80) | 152 (110) | 192 (140) | 232 (170) |
| 4 | 46 (30) | 86 (60) | 126 (90) | 166 (120) | 206 (150) | 246 (180) |
| 5 | 60 (40) | 100 (70) | 140 (100) | 180 (130) | 220 (160) | 260 (190) |
| 6 | 74 (50) | 114 (80) | 154 (110) | 194 (140) | 234 (170) | 274 (200) |
| 7 | 88 (60) | 128 (90) | 168 (120) | 208 (150) | 248 (180) | 288 (210) |
| 8 | 102 (70) | 142 (100) | 182 (130) | 222 (160) | 262 (190) | 302 (220) |
| 9 | 116 (80) | 156 (110) | 196 (140) | 236 (170) | 276 (200) | 316 (230) |
| 10 | 130 (90) | 170 (120) | 210 (150) | 250 (180) | 290 (210) | 330 (240) |

## Minimum Target Splits

These are the non-dominated attribute/focus splits for each perk tier. A split is omitted when another split reaches the same tier with no more attribute and no more focus.

| Perk Level | Non-dominated target splits |
|---:|---|
| 25 | 2 attribute + 1 focus, 3 attribute |
| 50 | 2 attribute + 1 focus, 5 attribute |
| 75 | 2 attribute + 2 focus, 4 attribute + 1 focus, 7 attribute |
| 100 | 2 attribute + 3 focus, 3 attribute + 2 focus, 5 attribute + 1 focus, 8 attribute |
| 125 | 2 attribute + 3 focus, 4 attribute + 2 focus, 7 attribute + 1 focus, 10 attribute |
| 150 | 2 attribute + 4 focus, 3 attribute + 3 focus, 6 attribute + 2 focus, 9 attribute + 1 focus |
| 175 | 2 attribute + 4 focus, 5 attribute + 3 focus, 8 attribute + 2 focus |
| 200 | 2 attribute + 5 focus, 4 attribute + 4 focus, 7 attribute + 3 focus, 10 attribute + 2 focus |
| 225 | 3 attribute + 5 focus, 6 attribute + 4 focus, 9 attribute + 3 focus |
| 250 | 5 attribute + 5 focus, 8 attribute + 4 focus, 10 attribute + 3 focus |
| 275 | 7 attribute + 5 focus, 9 attribute + 4 focus |

## Player Point Budget

Every player level grants 1 focus point. Every 4 player levels grant 1 attribute point. For point-budget planning, the minimum level-ups needed for a build are `max(total focus points spent, total attribute points spent * 4)`.
