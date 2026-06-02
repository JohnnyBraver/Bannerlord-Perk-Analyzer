# Kingdom Management

This note covers the kingdom-level layer: influence, policy voting, ruler overrides, armies, war and peace decisions, clan politics, and the policies that make those systems tilt. Read this together with `kingdom-policies.md`, which has the full policy table.

The extraction source for this pass is `Data/generated/kingdom-management-methods.json`.

## Main Takeaways

- Kingdom management is mostly an influence economy. Influence buys proposals, votes, army summons, cohesion, ruler overrides, clan support, and political pressure.
- Policies are not just passive bonuses. Many of them redistribute money, influence, loyalty, prosperity, troop access, or army control between the ruler, high-tier nobles, settlement owners, and commoners.
- Being the ruler is a different game from being a vassal. Ruler-favoring policies are powerful, but several of them directly drain vassal influence, loyalty, prosperity, workshop output, or trade value.
- Voting has hidden ideology weights. Each policy has authoritarian, oligarchic, and egalitarian weights; clan tier, ruler status, minor-faction status, and leader traits change which weights a clan tends to support.
- War and peace are scored from strength, settlement value, war progress, exposure, relations, culture claims, tribute, alliances, and trade agreements. Winning fights is only part of the diplomatic picture.

## Influence Costs

The extracted `DefaultDiplomacyModel` gives these base proposal costs:

| Decision | Base cost | Important modifiers |
| --- | ---: | --- |
| Propose or disavow policy | 100 influence | `Firebrand` reduces kingdom decision proposal cost by 25%. |
| Propose peace | 100 influence | `Firebrand` applies. |
| Propose war | 200 influence | `War Tax` doubles this for the ruling clan. `Firebrand` applies. |
| Propose fief annexation | 200 influence | `Feudal Inheritance` doubles it. `Precarial Land Tenure` halves it for the ruling clan. `Firebrand` applies. |
| Expel clan | 200 influence | `Firebrand` applies. |

Voting support uses the familiar three strengths:

| Support strength | Cost |
| --- | ---: |
| Low | 20 influence |
| Medium | 60 influence |
| High | 150 influence |

`Flexible Ethics` reduces the influence cost of voting for kingdom proposals made by others. `Good Natured` refunds influence when a supported proposal fails. Those are easy to underestimate because they do not create influence directly, but they make your political budget stretch much further.

## Ruler Overrides

The ruler can override the council outcome by paying influence. The extracted `DefaultClanPoliticsModel.GetInfluenceRequiredToOverrideKingdomDecision` scales the cost from the support-point gap and rounds to a multiple of 5. `Royal Privilege` applies a 20% reduction when the ruler is overriding the popular decision.

The practical read is simple:

- If you are the ruler, influence is your emergency brake.
- If you want to govern democratically, `Royal Privilege` is optional.
- If you want to force through hostile ruler policies, `Royal Privilege`, `Sacred Majesty`, `Firebrand`, and daily influence generation matter a lot.

## Policy Voting

`KingdomPolicyDecision.DetermineSupport` starts each clan with hidden lean values for authoritarian, oligarchic, and egalitarian policies, then adjusts them:

| Clan situation | Voting tendency from extraction |
| --- | --- |
| Ruling clan | More authoritarian, less oligarchic and egalitarian. |
| Minor faction | More egalitarian, less oligarchic and authoritarian. |
| Tier 3+ clan | More oligarchic, less authoritarian and egalitarian. Higher tier strengthens the oligarchic pull. |
| Tier 2 clan | Slightly more oligarchic, less authoritarian and egalitarian. |
| Leader traits | Authoritarian, Oligarchic, and Egalitarian trait levels push the matching policy weights. |

That means a ruler-heavy kingdom can push ruler laws, a high-tier noble bloc likes noble privileges, and commoner/settlement-stability laws can face resistance from the people who actually have votes.

See `kingdom-policies.md` for the full A/O/E weight table.

## Daily Influence

Policy influence income is scattered across several systems:

| Source | Effect |
| --- | --- |
| `Sacred Majesty` | Ruler clan +3 influence/day; non-ruler clans -0.5/day. |
| `Royal Guard` | Non-ruling clans -0.2/day. |
| `Marshals` | Ruling clan -1/day. |
| `Senate` | Tier 3+ clans +0.5/day. |
| `Lords' Privy Council` | Tier 5+ clans +0.5/day. |
| `Noble Retinues` | Tier 5+ clans -1/day, but their leaders gain party size. |
| `Feudal Inheritance` | +0.1 influence/day per owned fief. |
| `Serfdom` | +0.2 influence/day per owned village. |
| `Bailiffs` | +1 influence/day per owned town with security above 60. |
| `Council of the Commons` | +0.1 influence/day per notable in owned settlements. |
| `Trial by Jury` | All clans -1 influence/day. |
| `Lawspeakers` | Clan leader with Charm above 100 gains +1/day; otherwise loses -1/day. |

`Military Coronae` multiplies many military influence awards by 20%, but raises troop wages by 10%. It is best when your kingdom actually fights enough for the extra influence to matter.

## Armies

The extracted army model has a few useful constants:

| Army rule | Extracted value |
| --- | ---: |
| Average call-to-army cost baseline | 20 influence |
| Player party size ratio used for call eligibility | 0.4 |
| AI party size ratio used for call eligibility | 0.6 |
| Minimum food days to call a party | 15 days |
| Maximum wait time while gathering | 3 days |
| Cohesion threshold for dispersion | 10 |
| AI influence budget while creating army | 70% of clan influence |
| Base daily cohesion change | -2 cohesion/day |
| Army-member influence award | `(party strength + 20) / 200` per day before culture modifiers |

Army summon cost is not a flat price. It scales with relation to the target leader, target party strength, target party size readiness, distance, random leader variation, policies, perks, and culture.

Important army modifiers:

| Source | Effect |
| --- | --- |
| `Royal Commissions` | Ruler army creation cost -30%; ruler army cohesion boost cost -30%; non-ruler army creation cost +10%. |
| `Marshals` | Tier 5+ nobles pay 10% less to lead armies; ruler clan loses 1 influence/day. |
| `Lords' Privy Council` | Calling Tier 4 or lower parties costs 20% more. |
| `Senate` | Calling Tier 2 or lower parties costs 10% more. |
| `Inspiring Leader` | Army leader pays 20% less influence to call parties. |
| `Call To Arms` | Army leader pays 15% less influence to call parties and called parties move faster. |
| `Encirclement` | Army leader pays 10% less influence to boost cohesion. |
| `Horde Leader` | Army leader loses 5% less army cohesion. |

`Royal Commissions` is the clean ruler army policy. `Marshals` is the high-tier noble army policy. The names are easy to mentally merge, but the formulas treat them differently.

## Diplomacy And War Score

The diplomacy extraction is too wide to reduce to one clean formula, but the important inputs are visible:

- Relative strength and enemy strength.
- Value of settlements, including town prosperity and bound villages.
- War progress, including casualties and settlement outcomes.
- Exposure to other factions.
- Same-culture towns held by the target.
- Relations between leaders/clans.
- Tribute direction and amount.
- Alliances, trade agreements, and constant-war rules.

Practical implications:

- Taking towns changes diplomacy more than farming small parties.
- Bleeding enemy parties matters because war progress includes casualties, but settlement value is a huge diplomatic lever.
- A kingdom that is exposed on multiple fronts becomes more peace-inclined.
- Relations and culture claims can bend the score around the raw military math.

## Clan Politics

Clan recruitment and retention are not only about cash. The diplomacy model looks at settlement value, culture, relation, clan strength, war-party limit, current fiefs, reliability, and the value of joining or leaving a kingdom.

For a player kingdom, the management loop is:

1. Keep influence generation positive before forcing votes.
2. Use ruler policies only when the kingdom can survive the loyalty, prosperity, or vassal-influence loss.
3. Build relations with major clans before you need their votes.
4. Give clans enough fief value that leaving is unattractive.
5. Use war wins to gain fiefs and tribute leverage, not just loot.

## Strong Kingdom Build Pieces

| Area | Picks |
| --- | --- |
| Proposal economy | `Charm 125 Firebrand`, `Charm 125 Flexible Ethics`, `Charm 175 Good Natured`. |
| Daily influence | `Charm 275 Immortal Charm`, `Sacred Majesty`, `Lawspeakers` if the ruler and vassals have high Charm. |
| Battle influence | `Charm 50 Warlord`, `Tactics 225 Pre Battle Maneuvers`, `Tactics 225 Besieged`, `Military Coronae`. |
| Army control | `Leadership 175 Inspiring Leader`, `Tactics 150 Call To Arms`, `Tactics 200 Encirclement`, `Royal Commissions`. |
| Troop donation influence | `Steward 150 Relocation`. |
| Stable rule | `Citizenship`, `Forgiveness of Debts`, `Tribunes of the People`, `Bailiffs`, with care around taxes and production. |

The cleanest ruler setup is influence first, armies second, taxes third. Money policies are tempting, but unstable towns and angry vassals can turn short-term income into a long-term governance tax.
