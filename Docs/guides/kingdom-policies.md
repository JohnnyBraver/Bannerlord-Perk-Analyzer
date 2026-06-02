# Kingdom Policies

This note is a policy-focused appendix for `kingdom-management.md`. It lists every extracted vanilla policy, its main mechanical effect, and its hidden voting weights.

The A/O/E column is `Authoritarian / Oligarchic / Egalitarian`. Positive values make that ideology more likely to support passing the policy; negative values push against it. Actual support also depends on clan tier, ruler status, minor-faction status, and leader traits.

## Ruler Power And Revenue

| Policy | Main effect | Practical read | A/O/E |
| --- | --- | --- | ---: |
| `Land Tax` | 5% of village income is paid to the ruler clan; non-ruler clan village income is reduced by 5%. | Direct ruler skim from villages. Stronger in a large kingdom, hostile to vassal income. | `0.70 / 0.15 / -0.70` |
| `State Monopolies` | Ruler income gains 5% of workshop profits from ruler-owned towns; workshop production is reduced by 10%. | Ruler money at the cost of workshop economy. Bad if you care about workshop owners and town production. | `0.75 / 0.10 / -0.60` |
| `Sacred Majesty` | Ruler clan +3 influence/day; non-ruler clans -0.5 influence/day. | One of the strongest ruler snowball policies, but it starves vassals politically. | `0.85 / 0.10 / -0.90` |
| `Debasement Of The Currency` | Ruler clan gains 100 denars/day per town in the kingdom; settlements lose 1 loyalty/day. | Emergency ruler income. The loyalty hit is brutal in newly conquered or wrong-culture towns. | `0.70 / 0.10 / -0.70` |
| `Crown Duty` | 5% tariff tax is paid to ruler clan; higher town trade penalty; town prosperity -1/day. | Turns trade into royal income, but prosperity loss is expensive over time. | `0.75 / 0.15 / -0.40` |
| `Imperial Towns` | Ruler-owned towns gain +1 loyalty and +1 prosperity/day; non-ruler towns lose 0.3 loyalty/day. | Excellent if the ruler owns the key towns. Politically ugly if vassals own most towns. | `0.70 / 0.15 / -0.30` |
| `Royal Guard` | Ruler party size +60; non-ruling clans -0.2 influence/day. | Great personal ruler power. Another slow drain on vassal political strength. | `0.75 / 0.00 / -0.50` |
| `War Tax` | Ruler gains 5% tax from all settlements; towns lose 1 prosperity/day; ruler's war proposal cost is doubled. | A wartime cash lever with a long-term prosperity cost. The doubled war proposal cost matters if the ruler drives diplomacy. | `0.70 / -0.10 / -0.65` |
| `Royal Privilege` | Ruler override cost is reduced by 20%. | Lets the ruler force outcomes more cheaply. Best when you plan to overrule the council. | `0.80 / -0.15 / -0.75` |
| `Precarial Land Tenure` | Ruler clan pays 50% less influence to propose fief annexation. | Makes revoking fiefs much cheaper for the ruler, especially if `Feudal Inheritance` is not active. | `0.75 / 0.00 / -0.60` |

## Armies And Noble Power

| Policy | Main effect | Practical read | A/O/E |
| --- | --- | --- | ---: |
| `Royal Commissions` | Ruler army creation cost -30%; ruler army cohesion boost cost -30%; non-ruler army creation cost +10%. | The ruler army-control policy. Very good for a player ruler who personally leads wars. | `0.65 / 0.00 / -0.45` |
| `Marshals` | Tier 5+ nobles pay 10% less influence to lead armies; ruler clan -1 influence/day. | The high-tier noble army policy. Good for empowering great clans, not for centralizing power. | `-0.45 / 0.50 / 0.00` |
| `Senate` | Tier 3+ clans +0.5 influence/day; calling Tier 2 or lower parties to armies costs 10% more. | Broad noble council. Good for medium and large vassals, mildly worse for recruiting small clan parties into armies. | `-0.70 / 0.85 / 0.70` |
| `Lords' Privy Council` | Tier 5+ clans +0.5 influence/day; calling Tier 4 or lower parties to armies costs 20% more. | Concentrates power in top clans. Strong for entrenched great houses, bad for smaller clans. | `-0.50 / 0.70 / -0.15` |
| `Military Coronae` | Military influence awards +20%; troop wages +10%. | Excellent for aggressive kingdoms if wages are manageable. It rewards constant fighting. | `-0.15 / 0.60 / 0.35` |
| `Feudal Inheritance` | Fief revocation cost is doubled; clans gain +0.1 influence/day per fief. | Vassal security policy. Makes the realm harder for the ruler to rearrange. | `-0.75 / 0.75 / 0.65` |
| `Noble Retinues` | Tier 5+ clans lose 1 influence/day; their leaders gain +40 party size. | Turns top-clan influence into larger elite parties. Better for battlefield strength than politics. | `-0.35 / 0.65 / -0.45` |
| `Castle Charters` | Castle upgrade costs are reduced by 20%. | Good if the realm has many castles to develop. Narrow but clean. | `-0.65 / 0.45 / 0.00` |

## Settlement Owners And Local Rule

| Policy | Main effect | Practical read | A/O/E |
| --- | --- | --- | ---: |
| `Magistrates` | Town security +1/day; town taxes -5%. | A strong security policy with a small tax cost. Often worth it for unstable towns. | `0.60 / 0.35 / 0.10` |
| `Bailiffs` | Town security +1/day; towns above 60 security give owner clan +1 influence/day; town taxes -5%. | Excellent owner influence if towns are already stable or can be pushed above 60 security. | `0.00 / 0.40 / -0.10` |
| `Serfdom` | Owned villages grant +0.2 influence/day; towns gain +1 security/day but lose 1 militia/day. | Better than its name suggests for landed clans, but the militia loss is real. | `-0.40 / 0.50 / -0.25` |
| `Hunting Rights` | Town and castle food production +2; town loyalty -0.2/day. | Useful for food-stressed fortifications. The loyalty loss is small but constant. | `-0.20 / 0.35 / -0.15` |
| `Road Tolls` | Town owner gains 3% more trade tax; town prosperity -0.2/day. | Owner income now, slower prosperity later. Safer than Crown Duty but still a growth tax. | `-0.50 / 0.45 / -0.35` |
| `Council of the Commons` | Each notable gives settlement owner +0.1 influence/day; fortification tax income -5%. | Good in notable-rich holdings. Politically egalitarian but still pays the owner. | `-0.50 / 0.10 / 0.70` |

## Commoner And Stability Policies

| Policy | Main effect | Practical read | A/O/E |
| --- | --- | --- | ---: |
| `Forgiveness of Debts` | Settlement loyalty +2/day; workshop production -5%. | Huge loyalty stabilizer. The production hit is often worth it in fragile towns. | `-0.40 / -0.40 / 0.60` |
| `Citizenship` | Same-culture owner settlements +0.5 loyalty/day; wrong-culture owner settlements -0.5 loyalty/day; militia production +1. | Great in culturally aligned realms, dangerous in a mixed conquest realm. | `-0.65 / -0.35 / 0.70` |
| `Tribunes of the People` | Town taxes paid to ruler -5%; town loyalty +1/day. | Clean anti-revolt policy if the ruler can afford lower town tax. | `-0.60 / -0.20 / 0.55` |
| `Grazing Rights` | Settlement loyalty +0.5/day; village hearth growth -0.25/day. | Mild loyalty support with a long-term village-growth cost. | `-0.75 / -0.30 / 0.70` |
| `Lawspeakers` | Clan leaders with Charm above 100 gain +1 influence/day; others lose -1/day. | Very strong in a high-Charm player realm, punishing for low-Charm clans. | `0.00 / 0.25 / 0.45` |
| `Trial by Jury` | Settlement loyalty +0.5/day; settlement security -0.2/day; all clans -1 influence/day. | Stability by loyalty, but politically expensive and slightly worse for security. | `-0.30 / 0.10 / 0.60` |
| `Cantons` | Militia production +1; recruits replenish 20% faster; settlement tax income -10%. | Recruit and defense policy, paid for with tax. Good for manpower-focused kingdoms. | `-0.20 / -0.10 / 0.40` |
| `Land Grants for Veterans` | Veteran militia spawn chance +10%; village tax income -5%. | Defensive quality policy for villages and militia, with a small village tax cost. | `-0.35 / -0.15 / 0.50` |

## Policy Bundles

### Centralized Player Ruler

Good core:

- `Sacred Majesty`
- `Royal Guard`
- `Royal Commissions`
- `Royal Privilege`
- `Precarial Land Tenure`

Add money policies only when stable:

- `Land Tax`
- `State Monopolies`
- `Crown Duty`
- `War Tax`
- `Debasement Of The Currency`

This is powerful but politically sharp. It makes the ruler stronger and richer while vassals lose influence or income.

### Stable Conquest Realm

Good core:

- `Forgiveness of Debts`
- `Tribunes of the People`
- `Magistrates`
- `Bailiffs`
- `Hunting Rights` if food is stressed

Conditional:

- `Citizenship` if settlement owners usually match settlement culture.
- Avoid `Debasement Of The Currency` and `War Tax` if loyalty/prosperity are already fragile.

### Noble Coalition

Good core:

- `Senate`
- `Feudal Inheritance`
- `Bailiffs`
- `Council of the Commons`
- `Military Coronae`

Conditional:

- `Lords' Privy Council` if you want top clans to dominate.
- `Noble Retinues` if you value larger top-clan parties more than their influence income.
- `Marshals` if Tier 5+ nobles should lead more armies and the ruler can eat -1 influence/day.

### Manpower And Defense

Good core:

- `Cantons`
- `Land Grants for Veterans`
- `Bailiffs`
- `Magistrates`
- `Castle Charters`
- `Hunting Rights`

This stack is about recruit flow, militia, security, castle development, and food. It is less flashy than the ruler-income laws, but it keeps the realm from hollowing out.

## Easy Traps

- `Debasement Of The Currency` looks like simple income, but -1 loyalty/day is huge.
- `War Tax` pays the ruler but taxes prosperity and doubles the ruler's war proposal cost.
- `Imperial Towns` is great if the ruler owns the towns, but quietly hurts vassal-owned towns.
- `Trial by Jury` gives loyalty, but all clans lose 1 influence/day.
- `Marshals` is not the same as `Royal Commissions`: `Marshals` favors Tier 5+ nobles and costs the ruler influence; `Royal Commissions` centralizes army control under the ruler.
