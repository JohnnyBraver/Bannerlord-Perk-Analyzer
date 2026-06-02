# Alley Appendix

This appendix covers alley holdings. Alleys are settlement-adjacent, but they are closer to the crime/Roguery loop than normal town development, so they get their own note instead of being buried under settlement economy.

## Main Takeaways

- Alleys are criminal holdings, not normal settlement improvements.
- A player-owned alley requires between `5` and `10` troops.
- The extracted daily income is `50` gold.
- The extracted daily crime rating is `+0.5`.
- Alley XP is real and sizable: clearing, holding, assigning a clan member, and defending an alley all have separate XP values.
- If the alley leader dies, the model destroys the alley after `4` days.

## Extracted Alley Constants

| Model value | Extracted value | Practical read |
| --- | ---: | --- |
| Minimum troops in player-owned alley | `5` | Required garrison floor. |
| Maximum troops in player-owned alley | `10` | Small holding, not a full garrison. |
| Daily income | `50` gold | Low passive income. |
| Daily crime rating | `+0.5` | The income has a crime cost. |
| Destroy after leader death | `4` days | Replace the leader quickly. |
| Initial main hero XP | `1500` | Reward for taking the alley. |
| Daily main hero XP | `40` | Passive owner XP. |
| Daily assigned clan member XP | `200` | Clan member gains faster than main hero daily trickle. |
| Successful defense main hero XP | `6000` | Large defense payout. |

The attack response time method includes `4`, `8`, and `12` day constants, so troop strength/roster appears to affect how long the player has to answer an attack. That path deserves a deeper extraction before turning it into a rule-of-thumb table.

## Practical Alley Read

Alleys are not a normal investment property:

- The passive gold is modest.
- The crime rating cost is persistent.
- The troop requirement is small but still real.
- The XP and Roguery/crime loop are the main reasons to care.
- The assigned clan member gains meaningful daily XP, so alleys can double as a companion/family-member development tool.

This makes alleys closer to a crime build appendix than a settlement economy staple. A clean lawful trading build probably does not want them. A Roguery build, bandit build, or companion-development experiment might.

## Open Follow-Ups

- Decode the alley attack response-time thresholds.
- Extract the troop generation logic for AI-owned alleys and attack missions.
- Cross-link this with a future dedicated crime/Roguery guide.

## Evidence

Primary local evidence:

- `Data/generated/settlement-methods.json`: extracted `DefaultAlleyModel`, alley XP, income, troop limits, crime rating, and attack-response methods.
- `Data/generated/reports/xp-formulas.md`: broader XP-source report that includes alley XP.
- `Data/export/perk-effects.json`: postprocessed Roguery and settlement-adjacent perk effects.
