# Kingdom Management and Policies Manual

This manual covers the mechanics of kingdom-level governance, diplomacy, army assembly, and the voting processes of Bannerlord. It details how the influence economy operates, how ruler overrides are calculated, and how the A/O/E (Authoritarian, Oligarchic, Egalitarian) voting weights shape noble council decisions.

---

## 1. The Influence Economy & Proposal Costs

Influence is the primary currency of statecraft. It is expended to propose laws, veto council decisions, annex fiefs, summon lords to war, and maintain cohesion.

### Base Decision Costs
The base cost to propose a kingdom-level action or decision is dictated by the campaign diplomacy model:

| Action / Proposal | Base Cost | Strategic Modifiers |
| :--- | ---: | :--- |
| **Propose or Disavow Policy** | 100 Influence | `Firebrand` (Charm 125) reduces proposal cost by $25\%$. |
| **Propose Peace** | 100 Influence | `Firebrand` reduces cost by $25\%$. |
| **Propose War** | 200 Influence | Doubled for the ruling clan if `War Tax` policy is active. |
| **Annex Fief** | 200 Influence | Doubled by `Feudal Inheritance`. Halved for ruler by `Precarial Land Tenure`. |
| **Expel Clan** | 200 Influence | `Firebrand` reduces cost by $25\%$. |

### Council Voting Support
When a proposal goes to vote, clans can back their stance at three strength tiers:

| Support Strength | Cost (Influence) | Personal Modifiers |
| :--- | ---: | :--- |
| **Low Support** | 20 | `Flexible Ethics` (Charm 125) reduces vote costs. |
| **Medium Support** | 60 | `Flexible Ethics` reduces vote costs. |
| **High Support** | 150 | `Flexible Ethics` reduces vote costs. |

> [!TIP]
> The perk `Good Natured` (Charm 175) refunds spent influence if a proposal you supported fails to pass. This provides significant political safety when attempting to sway hostile councils.

### Influence and Relation Perks
Several Charm perks assist in building influence and managing lord relations during council sessions:
* **Charm (Level 25) - `Self Promoter`**: Earn $+1$ influence per tournament win.
* **Charm (Level 50) - `Warlord`**: Earn $+30\%$ influence from combat victories.
* **Charm (Level 75) - `Forgivable Grievances`**: Prevents relations decay with other lords when voting against them in council decisions.
* **Charm (Level 75) - `Meaningful Favors`**: Generates $+1$ relation per day with a random clan leader of your faction if your influence exceeds theirs.
* **Charm (Level 150) - `Effort For The People`**: Reduces overall influence vote cost by $-10\%$ during kingdom proposals.
* **Charm (Level 175) - `Tribute`**: Generates $+10\%$ influence from owned fief tariffs.
* **Charm (Level 225) - `Public Speaker`**: Generates $+10\%$ influence from owned town taxes.
* **Charm (Level 225) - `Parade`**: Visiting a town you own gives $+5$ loyalty to that town (once per town visit).

### Ruler Overrides
The ruler can overrule any council vote by spending influence proportional to the support gap.
* **Cost formula**: The cost scales quadratically based on the percentage support gap between the ruler's choice and the popular choice.
* **Override discount**: The policy `Royal Privilege` applies a flat $20\%$ discount to all ruler override costs, enabling the ruler to force centralization over vassal objections.

---

## 2. Policy Voting Tendencies & Hidden Ideologies

Voting clans are not purely random. Every kingdom policy has hidden ideology weights across three vectors: Authoritarian (A), Oligarchic (O), and Egalitarian (E).

### Clan Decision-Making
A clan's support for a policy is determined by its cultural leanings and current situation:

| Clan Type / Situation | Voting Tendency | Ideological Focus |
| :--- | :--- | :--- |
| **Ruling Clan** | Favors policies that concentrate power/income at the top. | Strongly Authoritarian, Anti-Egalitarian. |
| **Minor Factions (Mercenaries)** | Favors clan autonomy, independence, and flat rights. | Strongly Egalitarian, Anti-Authoritarian. |
| **Tier 3+ Clans (Vassals)** | Favors noble privileges, vassal rights, and fief security. | Strongly Oligarchic, Anti-Authoritarian. |
| **Leader Traits** | Trait levels (Honor, Mercy, etc.) scale leans. | Trait levels align with A/O/E axes. |

---

## 3. Daily Influence & Military Coronae

Clans generate or lose influence daily based on active policies and owned holdings:

* **Sacred Majesty**: Ruler clan gains $+3$ daily influence; non-ruler clans lose $-0.5$ daily influence.
* **Royal Guard**: Ruler party size $+60$; non-ruler clans lose $-0.2$ daily influence.
* **Senate**: Tier 3+ clans gain $+0.5$ daily influence.
* **Lords' Privy Council**: Tier 5+ clans gain $+0.5$ daily influence.
* **Feudal Inheritance**: $+0.1$ daily influence per owned fief.
* **Serfdom**: $+0.2$ daily influence per owned village.
* **Bailiffs**: $+1$ daily influence per owned town with security $>60$.
* **Council of the Commons**: $+0.1$ daily influence per notable in owned settlements (extremely potent in well-populated territories).
* **Lawspeakers**: Leaders with Charm $>100$ gain $+1$ daily influence; leaders with Charm $<100$ lose $-1$ daily influence.

> [!IMPORTANT]
> The policy `Military Coronae` multiplies all combat-related influence gains by $+20\%$, but increases overall troop wages by $+10\%$. This policy should only be enacted by highly active, offensive clans that can offset the wage increase through constant combat victories.

---

## 4. Army Summoning & Cohesion Mechanics

 summons and army cohesion are governed by a strict model of relations, party size ratios, and distance:

* **Average Army Summon Baseline**: 20 Influence.
* **Size Eligibility (Player)**: A clan member's party must be at least $40\%$ full ($0.4$ ratio) to be summoned.
* **Size Eligibility (AI)**: An AI lord's party must be at least $60\%$ full ($0.6$ ratio) to be summoned.
* **Minimum Food Supply**: Called parties must carry at least 15 days of food reserves.
* **Cohesion Decay**: Cohesion decays by a baseline $-2$ points per day.
* **Dispersion Threshold**: When cohesion falls below $10$, the army automatically disperses.
* **Daily Influence Award**: Army members receive daily influence based on their party strength:
$$\text{Daily Influence Award} = \frac{\text{Party Strength} + 20}{200} \text{ (Before culture modifiers)}$$

### Army Cost Modifiers

| Source | Effect | Tactical Read |
| :--- | :--- | :--- |
| `Inspiring Leader` | Army leader pays $-20\%$ influence to call parties. | Essential Leadership perk for warfare. |
| `Call To Arms` | $-15\%$ summoning cost and called parties move faster. | Improves tactical response times. |
| `Encirclement` | $-10\%$ influence cost to boost army cohesion. | Extends army duration in long campaigns. |
| `Horde Leader` | Army leader loses $5\%$ less cohesion daily. | Reduces influence drain while sieging. |
| `Authority` | Army daily cohesion decay rate reduced by $-20\%$. | Leadership Level 75 army stabilizer. |
| `Royal Commissions` | Ruler army cost $-30\%$, Vassal army cost $+10\%$. | Restricts army-leading capabilities to the crown. |
| `Master of Planning` | Army daily cohesion decay rate reduced by $-5\%$ when traveling. | Steward Level 250 army stabilizer. |
| `Master of Warcraft` | Army daily cohesion decay rate reduced by $-5\%$ when sieging. | Steward Level 250 army siege stabilizer. |
| `Ultimate Leader` | Party size $+1$ for every Leadership level $>250$. | Late-game Leadership party-limit multiplier. |

---

## 5. Diplomacy & War Scoring

War and peace are calculated using a diplomatic evaluation score rather than simple military dominance. The key vectors include:
1. **Military Strength**: Relative total strength between kingdoms.
2. **Settlement Values**: The total prosperity and village status of owned lands. Losing prosperous towns drastically shifts a kingdom's peace evaluation.
3. **Casualties**: Cumulative battle casualties. High casualty counts trigger war fatigue.
4. **Frontage and Exposure**: Factions bordered by multiple hostile kingdoms become significantly more peace-inclined to avoid multi-front wars.
5. **Cultural Claims**: Factions prioritize reclaiming towns and castles that share their faction culture.

---

## 6. Vanilla Policies Encyclopedia

### Ruler Power & Revenue Policies

| Policy | Mechanical Effect | Strategic Implications | A/O/E |
| :--- | :--- | :--- | :---: |
| **Land Tax** | $+5\%$ village tax to ruler; $-5\%$ village tax to vassals. | Skims wealth from vassals to the crown. Punishes vassal economy. | `0.70 / 0.15 / -0.70` |
| **State Monopolies** | $+5\%$ workshop profits to ruler; $-10\%$ workshop speed. | Boosts royal coffers but degrades overall workshop productivity. | `0.75 / 0.10 / -0.60` |
| **Sacred Majesty** | Ruler $+3$ influence/day; Vassals $-0.5$ influence/day. | Excellent for locking down central rule; starves vassals of votes. | `0.85 / 0.10 / -0.90` |
| **Debasement of Currency** | Ruler $+100$ gold/day per town; Towns $-1$ loyalty/day. | Emergency crown cash at the cost of catastrophic loyalty decay. | `0.70 / 0.10 / -0.70` |
| **Crown Duty** | Ruler $+5\%$ tariffs; Town trade penalty $+5\%$; Prosperity $-1$/day. | Converts trade into royal income, but prosperity loss is costly. | `0.75 / 0.15 / -0.40` |
| **Imperial Towns** | Ruler towns $+1$ loyalty/prosperity; Vassal towns $-0.3$ loyalty. | Centralizes economic value under the crown's direct holdings. | `0.70 / 0.15 / -0.30` |
| **Royal Guard** | Ruler party size $+60$; Vassals $-0.2$ influence/day. | Drastically improves the ruler's personal army limit. | `0.75 / 0.00 / -0.50` |
| **War Tax** | Ruler $+5\%$ tax from settlements; Prosperity $-1$/day; War proposal cost doubled. | High war-funding tax, but hurts long-term development. | `0.70 / -0.10 / -0.65` |
| **Royal Privilege** | Ruler override costs reduced by $20\%$. | Enables cheap ruler overrides against popular votes. | `0.80 / -0.15 / -0.75` |
| **Precarial Land Tenure** | Ruler fief annexation proposal cost reduced by $50\%$. | Makes stripping vassals of fiefs significantly cheaper. | `0.75 / 0.00 / -0.60` |

---

### Armies & Noble Power Policies

| Policy | Mechanical Effect | Strategic Implications | A/O/E |
| :--- | :--- | :--- | :---: |
| **Royal Commissions** | Ruler army cost $-30\%$; Vassal army cost $+10\%$. | Prevents vassals from forming independent war hosts. | `0.65 / 0.00 / -0.45` |
| **Marshals** | Tier 5+ nobles army cost $-10\%$; Ruler $-1$ influence/day. | Delegates army coordination to senior vassal clans. | `-0.45 / 0.50 / 0.00` |
| **Senate** | Tier 3+ clans $+0.5$ influence/day; T2 army cost $+10\%$. | Empowers mid-tier noble clans. | `-0.70 / 0.85 / 0.70` |
| **Lords' Privy Council** | Tier 5+ clans $+0.5$ influence/day; T4 army cost $+20\%$. | Concentrates military and voting power within elite vassal clans. | `-0.50 / 0.70 / -0.15` |
| **Military Coronae** | Combat influence gains $+20\%$; Troop wages $+10\%$. | High-tempo military expansion policy; expensive in peacetime. | `-0.15 / 0.60 / 0.35` |
| **Feudal Inheritance** | Annexation cost doubled; Fiefs $+0.1$ influence/day. | Protects vassal fiefs from royal annexation. | `-0.75 / 0.75 / 0.65` |
| **Noble Retinues** | Tier 5+ clans leader party size $+40$; Influence $-1$/day. | Converts top-clan political weight into raw battlefield troops. | `-0.35 / 0.65 / -0.45` |
| **Castle Charters** | Castle upgrade construction costs reduced by $20\%$. | Accelerates defensive castle upgrades across the realm. | `-0.65 / 0.45 / 0.00` |

---

### Settlement Owners & Local Rule Policies

| Policy | Mechanical Effect | Strategic Implications | A/O/E |
| :--- | :--- | :--- | :---: |
| **Magistrates** | Town security $+1$/day; Town taxes $-5\%$. | Excellent for stabilizing conquered towns at a minor cost. | `0.60 / 0.35 / 0.10` |
| **Bailiffs** | Town security $+1$/day; Town owner $+1$ influence/day (if security $>60$); Taxes $-5\%$. | Rewards landed owners with influence for keeping order. | `0.00 / 0.40 / -0.10` |
| **Serfdom** | Owner $+0.2$ influence/day per village; Security $+1$/day; Militia $-1$/day. | Boosts owner influence, but weakens town defense counts. | `-0.40 / 0.50 / -0.25` |
| **Hunting Rights** | Town/Castle food production $+2$; Loyalty $-0.2$/day. | Excellent emergency food injection for sieged fiefs. | `-0.20 / 0.35 / -0.15` |
| **Road Tolls** | Owner trade tax $+3\%$; Prosperity $-0.2$/day. | Short-term cash injection for fief owners; restricts growth. | `-0.50 / 0.45 / -0.35` |
| **Council of Commons** | Owner $+0.1$ influence/day per notable; Taxes $-5\%$. | Massively scales vassal influence in highly populated towns. | `-0.50 / 0.10 / 0.70` |

---

### Commoner & Stability Policies

| Policy | Mechanical Effect | Strategic Implications | A/O/E |
| :--- | :--- | :--- | :---: |
| **Forgiveness of Debts** | Town loyalty $+2$/day; Workshop production $-5\%$. | The premier policy for stabilizing conquest-heavy kingdoms. | `-0.40 / -0.40 / 0.60` |
| **Citizenship** | Same-culture town loyalty $+0.5$; Wrong-culture town loyalty $-0.5$; Militia $+1$/day. | Excellent for culturally mono-realms; deadly for empires. | `-0.65 / -0.35 / 0.70` |
| **Tribunes of People** | Ruler town taxes $-5\%$; Town loyalty $+1$/day. | Reduces royal income to stabilize town loyalty. | `-0.60 / -0.20 / 0.55` |
| **Grazing Rights** | Settlement loyalty $+0.5$/day; Village hearth growth $-0.25$/day. | Minor loyalty boost, but degrades village production over time. | `-0.75 / -0.30 / 0.70` |
| **Trial by Jury** | Town loyalty $+0.5$/day; Security $-0.2$/day; Clans $-1$ influence/day. | Politically draining stability tool. | `-0.30 / 0.10 / 0.60` |
| **Cantons** | Militia production $+1$/day; Recruitment speed $+20\%$; Taxes $-10\%$. | Manpower-focused war mobilization policy. | `-0.20 / -0.10 / 0.40` |
| **Veterans' Land Grants**| Veteran militia rate $+10\%$; Village taxes $-5\%$. | Upgrades the defense quality of militias. | `-0.35 / -0.15 / 0.50` |

---

## 7. Strategic Policy Bundles

### Centralized Player Ruler Setup
This setup maximizes the ruler's influence, cash, and army limits while starving vassals of political power:
* **Core Policies**: `Sacred Majesty` (influence drain), `Royal Guard` (party size), `Royal Commissions` (army control), `Royal Privilege` (veto override discount), `Precarial Land Tenure` (cheap land confiscation).
* **Revenue Additions**: `Land Tax` (village skim), `State Monopolies` (workshop tax).

### Conquered Expansion Realm Setup
Designed to pacify newly captured fiefs of different cultures, preventing rebellions and stabilizing borders:
* **Core Policies**: `Forgiveness of Debts` ($+2$ loyalty), `Tribunes of the People` ($+1$ loyalty), `Magistrates` ($+1$ security), `Bailiffs` ($+1$ security).
* **Avoid**: `Debasement of the Currency` (loyalty decay), `War Tax` (prosperity decay).

### Democratic Vassal Coalition Setup
Enacted to empower senior vassal houses, maximizing noble cooperation and defense:
* **Core Policies**: `Senate` (nobility influence), `Feudal Inheritance` (fief security), `Council of the Commons` (notable-based influence), `Marshals` (vassal-led armies).

---

## 8. Political Traps to Avoid

* **Debasement of the Currency**: The $+100$ gold per town is negligible compared to the devastating $-1$ daily loyalty hit, which triggers rebellions and halts construction.
* **War Tax**: Restricts the ruler's ability to drive warfare by doubling war proposal costs, while degrading overall settlement prosperity.
* **Citizenship in Multi-Culture Kingdoms**: The $-0.5$ loyalty penalty to mismatching cultures will trigger massive rebellions in conquering realms.
* **Trial by Jury**: Starves small vassal clans of influence completely due to the global $-1$ daily influence drain.
