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

## Final Perk Level Distribution
Below is the distribution of the highest level perk in each skill. We track how this distribution shifts under two exclusion filters:
1. **Strict Exclusion**: Excludes perks that scale the exact same passive attribute that the skill natively scales (e.g. One Handed speed/damage).
2. **Broad Exclusion**: Excludes any final perk that acts as a linear passive scaling extension of any basic stat (e.g. Medicine scaling troop HP).

### Distribution Summary Table
| Final Perk Level | Raw (No Exclusions) | Strict Exclusion | Broad Exclusion (Passive Scale) |
| :--- | :---: | :---: | :---: |
| Level 225 | 0 skills | 1 skills | 1 skills |
| Level 250 | 1 skills | 10 skills | 14 skills |
| Level 275 | 16 skills | 6 skills | 2 skills |
| Level 300 | 1 skills | 1 skills | 1 skills |

### Skill-by-Skill Active Cap Table
| Skill | Raw Final Perk | Level | Base Passive Leveling Effect | Strict Exclude | Broad Exclude | Active Cap Level | New Last Perk(s) |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| Athletics | Mighty Blow | 275 | Increases running speed (+0.06% per level) | Keep | Exclude | **250** | Ignore Pain / Spartan |
| Bow | Deadshot | 275 | Increases damage (+0.11% per level) and accuracy (+0.09% per level) | Exclude | Exclude | **250** | Quick Draw / Ranger's Swiftness |
| Charm | Immortal Charm | 275 | Increases relation gain speed (+0.5% per level) | Keep | Keep | **275** | Immortal Charm |
| Crossbow | Mighty Pull | 275 | Increases reload speed (+0.07% per level) and accuracy (+0.09% per level) | Exclude | Exclude | **250** | Picked Shots / Terror |
| Engineering | Masterwork | 275 | Increases siege engine build speed (+0.9% per level) and wall repair speed (+0.9% per level) | Exclude | Exclude | **250** | Architectural Commissions / Clockwork |
| Leadership | Ultimate Leader | 275 | Increases party morale (+0.05% per level) and troop XP gain (+0.1% per level) | Keep | Exclude | **250** | Talent Magnet / We Pledge our Swords |
| Medicine | Minister of Health | 275 | Increases recovery rate of sick/wounded (+10% per level) and casualty survival (+0.08% per level) | Keep | Exclude | **250** | Battle Hardened / Helping Hands |
| One Handed | Way of the Sword | 275 | Increases attack speed and damage (+0.07% speed, +0.15% damage per level) | Exclude | Exclude | **250** | Chink in the Armor / Prestige |
| Polearm | Way of the Spear | 275 | Increases attack speed and damage (+0.07% speed, +0.15% damage per level) | Exclude | Exclude | **250** | Counterweight / Sharpen the Tip |
| Riding | The Way Of The Saddle | 275 | Increases mount speed (+0.2% per level) and mount maneuverability (+0.04% per level) | Exclude | Exclude | **250** | Dauntless Steed / Tough Steed |
| Roguery | Rogue Extraordinaire | 275 | Increases loot amount (+0.25% per level) and raid speed (+0.25% per level) | Exclude | Exclude | **250** | Dash and Slash / Fleet Footed |
| Scouting | Uncanny Insight | 275 | Increases track detection, tracking details, and party map speed (+0.07% map speed per level) | Exclude | Exclude | **250** | Rearguard / Vanguard |
| Smithing | Legendary Smith | 275 | Increases learning rate of parts and stamina recovery speed (+0.5% per level) | Keep | Keep | **275** | Legendary Smith |
| Steward | Price of Loyalty | 275 | Increases party size limit (+0.25 party size per level) | Keep | Exclude | **250** | Master of Planning / Master of Warcraft |
| Tactics | Tactical Mastery | 275 | Increases battle simulation advantage (+0.1% per level) | Exclude | Exclude | **250** | Counter Offensive / Gens d'armes |
| Throwing | Unstoppable Force | 275 | Increases damage (+0.13% per level) and accuracy (+0.06% per level) | Exclude | Exclude | **250** | Impale / Weak Spot |
| Trade | Everything Has a Price | 300 | Reduces trade penalty (+0.4% per level) | Keep | Keep | **300** | Everything Has a Price |
| Two Handed | Way Of The Great Axe | 250 | Increases attack speed and damage (+0.07% speed, +0.15% damage per level) | Exclude | Exclude | **225** | Blade Master / Vandal |
