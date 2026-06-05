# Battanian Character Creation and Commander Progression Guide

This guide tracks Battanian character creation choices for the elite one-party commander build after dropping the purchased Control point:

$$\text{Purchased Target} = \text{VIG 3 | CTR 2 | END 3 | CNG 7 | SOC 2 | INT 7}$$

The physical training windows are still better than the purchased line suggests:

$$\text{Training Windows} = \text{VIG 3(5) | CTR 2(4) | END 3(5)}$$

The values in parentheses are not all live at the same time. Athletics and Smithing attribute perks can be selected, used to train a physical group, and later changed at the arena once the skill levels are already banked. The important change is Control: the default shock-infantry commander does not buy Control 3 anymore. `Controlled Smith` plus `Steady` can make effective Control 4, which reaches Bow 100 and Throwing 125 with two focus points each.

---

## 1. What Changed

The older Battanian starts were built around:

$$\text{VIG 3 | CTR 3 | END 3 | CNG 7 | SOC 2 | INT 7}$$

That made Control-raising starts look clean. Under the current commander doctrine, that Control attribute is wasted unless the character is specifically becoming an archer, crossbow, or throwing specialist. The default shock-infantry plan wants:

- **No purchased Control attribute**: stay at base Control 2 and use the Endurance trick for effective Control 4 when training Bow and Throwing.
- **Cunning 7 and Intelligence 7 by level 24**: campaign character creation gives six fixed attribute choices, then level-up attributes at levels 4, 8, 12, 16, 20, and 24 provide the six points needed to finish the target.
- **Permanent focus in real sinks**: Scouting, Medicine, and Steward are all 5-focus destinations. Athletics and Smithing are 5-focus enablers. Riding is only a 1-focus sink. Bow and Throwing are 2-focus Control sinks. Crossbow is normally 0.

This means old Control starts such as `Tribespeople` or `attention to detail` should no longer be treated as default-compatible.

---

## 2. Focus Target Layout

Use this layout when judging whether a creation focus point is useful or wasted.

The generated [Battanian start focus leak report](../reports/battanian-start-leaks.md) brute-forces the full story-campaign choice grid against this target. Current headline: **15,800** starts survive the no-Control/no-Social attribute pruning, the best Battanian starts have **2** default focus leaks across **390** paths, and **0** paths are completely leak-free. Those best paths are clean on hard side-plan focus and only leak into Tactics.

The generated [culture start focus leak comparison](../reports/culture-start-leaks.md) runs the same target across every culture. Under this exact policy, **no culture** has a zero-default-leak path. **Aserai, Battania, Khuzait, and Sturgia** can bottom out at **2** default focus leaks; **Empire and Vlandia** bottom out at **3**. Attribute leaks are pruned rather than scored, so this comparison is only about focus leakage among starts that can still hit the target attribute line.

| Skill Group | Default Focus Read | Notes |
| --- | ---: | --- |
| Scouting | 5 | Core target for `Uncanny Insight` at 275. |
| Medicine | 5 | Core troop durability target for `Minister of Health`. |
| Steward | 5 | Core party scaling/logistics target if the player is quartermaster. |
| Athletics | 5 | Endurance/Vigor/Control enabler; Athletics 200 and sometimes 250 matter. |
| Smithing | 5 | Attribute/focus engine and economy engine. |
| One Handed | 5 or less | Strong Vigor sink if shield infantry is central. |
| Polearm | 5 or less | Strong Vigor sink if polearm infantry is central. |
| Two Handed | 3 by default | Stop at 175 unless personally using two-handers or spending spare focus. |
| Riding | 1 | `Sweeping Wind` at 100; extra Riding focus is usually waste for infantry. |
| Bow | 2 | `Merry Men` at 100 under assisted Control 4. |
| Throwing | 2 | `Skirmisher` at 125 under assisted Control 4. |
| Leadership | 2 to 5 | Useful party-size stretch, but Social stays at 2. |
| Charm | 1 | Optional QoL/renown pickup. |
| Trade | 1 | Excellent QoL for price marking. |
| Tactics | 0 or 5 | Free to 75 from Cunning 7; only keep focus here if planning the Tactics 200 stretch. |
| Engineering | 0 by default | Delegate to a companion unless the player is deliberately the engineer. |
| Roguery | 0 by default | Loot/crime side plan, not a commander-core sink. |
| Crossbow | 0 by default | `Counter Fire` is crossbow-user mitigation, not infantry protection. |

The strict filter "no Control, no Social, no Engineering, no Roguery, no Crossbow, and no Tactics focus" has no complete Battanian campaign path. Battanian Cunning choices usually bring Tactics or Roguery with them. The clean practical filter is therefore:

- Avoid Control and Social attributes.
- Avoid Crossbow, Engineering, and Roguery focus unless the build has a specific side plan.
- Treat Tactics focus as acceptable only if the build plans to push Tactics toward 200 for `Elite Reserves`; otherwise it is soft waste.

The common hard leaks are:

| Leak | Main Sources | Default Read |
| --- | --- | --- |
| Engineering | `stood guard with the garrisons`, `makeshift fortifications`, `aptitude for numbers`, `repaired projects`, `private tutor` | Only for player-engineer variants; otherwise delegate. |
| Roguery | `tricked the raiders`, `hung out with the gangs`, `marched with the camp followers`, `famous escapade` | Only for loot/crime variants. |
| Crossbow | Some `stood guard with the garrisons` variants | Only for crossbow formations. |
| Bow overflow | Stacking too many Bow-granting no-Control picks | Becomes archer-heavy value after Bow 100; not default shock-infantry value. |
| Trade overflow | More than one Trade focus | QoL is great at one focus; extra Trade is an economy-side plan. |

---

## 3. Battanian No-Control Choice Filter

### Clean Picks

These do not raise Control and put focus into skills the default commander can naturally use.

| Stage | Choice | Attribute | Focus Skills | Read |
| --- | --- | --- | --- | --- |
| Family | Smiths | Endurance | Two Handed, Smithing | Clean if the build wants early Smithing and Two Handed support. |
| Family | Healers | Intelligence | Charm, Medicine | Clean Medicine start; Charm is a one-focus QoL sink. |
| Family | Members of the chieftain's hearthguard | Vigor | Two Handed, Bow | Clean physical start, but no Cunning/Intelligence. |
| Childhood | your brawn. | Vigor | Two Handed, Throwing | Clean if using Throwing 125. |
| Childhood | your skill with horses. | Endurance | Riding, Medicine | Clean, but remember Riding only wants one focus total. |
| Education | helped at building sites. | Vigor | Athletics, Smithing | Very clean physical-engine start. |
| Education | gathered herbs in the wild. | Endurance | Scouting, Medicine | Very clean commander start. |
| Education | cared for the horses. | Endurance | Riding, Steward | Clean if this is the only Riding focus. |
| Education | worked in the village smithy. | Vigor | Two Handed, Smithing | Clean Vigor/Smithing start. |
| Youth | trained with the cavalry. | Endurance | Polearm, Riding | Clean if this is the only Riding focus. |
| Youth | trained with the hearth guard. | Endurance | Polearm, Riding | Same as cavalry; good Polearm/Riding seed. |
| Youth | trained with the infantry. | Vigor | One Handed, Polearm | Very clean Vigor start. |
| Youth | rode with the scouts. | Endurance | Bow, Riding | Clean if this is the only Riding focus. |
| Adulthood | you defeated an enemy in battle. | Vigor | One Handed, Two Handed | Clean combat start. |
| Adulthood | you invested some money in land. | Intelligence | Smithing, Trade | Clean if using Trade 50 QoL. |
| Adulthood | you invested some money in a workshop. | Intelligence | Smithing, Trade | Same as land; choose by roleplay/trait preference. |
| Escape | you rode off on a fast horse. | Endurance | Riding, Scouting | Clean if this is the only Riding focus. |
| Escape | you subdued a raider. | Vigor | One Handed, Athletics | Clean physical-engine escape. |

### Conditional Picks

These avoid Control but only stay zero-waste if their secondary skill is deliberately part of the final plan.

| Stage | Choice | Attribute | Focus Skills | Condition |
| --- | --- | --- | --- | --- |
| Family | Foresters | Cunning | Scouting, Tactics | Good if Tactics 200 is planned; otherwise the Tactics focus is soft waste. |
| Childhood | your leadership skills. | Cunning | Tactics, Leadership | Good if Tactics 200 and/or Leadership 175 are planned. |
| Education | hunted small game. | Cunning | Bow, Tactics | Good if Bow 100 and Tactics 200 are planned. |
| Youth | were a chieftain's servant. | Cunning | Tactics, Steward | Good if Tactics 200 is planned; Steward is excellent. |
| Youth | joined a commander's staff. | Cunning | Tactics, Steward | Same as chieftain's servant. |
| Adulthood | you led a caravan. | Cunning | Leadership, Trade | Good low-waste Cunning pick if Leadership and Trade are in the plan. |
| Adulthood | you led a successful manhunt. | Cunning | Tactics, Leadership | Good if Tactics 200 and Leadership are in the plan. |
| Adulthood | you saved your city quarter from a fire. | Cunning | Tactics, Leadership | Same as manhunt. |
| Adulthood | you saved your village from a flood. | Cunning | Tactics, Leadership | Same as manhunt. |

### Avoid By Default

These are not default-compatible after dropping the purchased Control point.

| Stage | Choice | Why |
| --- | --- | --- |
| Family | Tribespeople | Raises Control. The Throwing/Athletics focus is nice, but the attribute is now wasted. |
| Childhood | your attention to detail. | Raises Control. This was part of the old Cunning start and should be dropped. |
| Education | herded the sheep. | Raises Control. |
| Education | watched the militia training. | Raises Control. |
| Youth | joined the kern / joined the skirmishers | Raises Control. |
| Adulthood | you hunted a dangerous animal | Raises Control. |
| Adulthood | you survived a siege | Raises Control and adds Crossbow. |
| Escape | you drove them off with arrows | Raises Control. |
| Any stage | Bards / way with people / envoy / market/social choices | Raise Social; Social 3 is not part of this commander baseline. |
| Youth | stood guard with the garrisons | Adds Engineering, and sometimes Crossbow. Only use if player-engineer is a deliberate side plan. |
| Education | repaired projects / private tutor | Adds Engineering. Use only for player-engineer variants. |
| Escape | makeshift fortifications | Adds Engineering. Use only for player-engineer variants. |
| Escape | tricked the raiders | Adds both Tactics and Roguery; acceptable only for a Cunning/Roguery side plan. |

---

## 4. Recommended Campaign Starts

These starts avoid the wasted Control attribute. They both reach the purchased target by level 24.

### A. Balanced Intelligence/Cunning Commander

This is the cleanest no-Control path if Tactics 200 is accepted as the Cunning-side focus sink. It avoids Engineering, Crossbow, and Roguery entirely.

| Stage | Choice | Attribute | Focus and Skill Effects |
| --- | --- | ---: | --- |
| Family | Healers | +1 Intelligence | +1 focus and +10 skill: Charm, Medicine |
| Childhood | your leadership skills. | +1 Cunning | +1 focus and +10 skill: Tactics, Leadership |
| Education | gathered herbs in the wild. | +1 Endurance | +1 focus and +10 skill: Scouting, Medicine |
| Youth | were a chieftain's servant. / joined a commander's staff. | +1 Cunning | +1 focus and +10 skill: Tactics, Steward |
| Adulthood | you invested some money in land / workshop. | +1 Intelligence | +1 focus and +10 skill: Smithing, Trade |
| Escape | you subdued a raider. | +1 Vigor | +1 focus and +10 skill: One Handed, Athletics |

Starting attributes after creation:

$$\text{VIG 3 | CTR 2 | END 3 | CNG 4 | SOC 2 | INT 4}$$

Level-up allocation to level 24:

- Buy **+3 Cunning**.
- Buy **+3 Intelligence**.

Final purchased line at level 24:

$$\text{VIG 3 | CTR 2 | END 3 | CNG 7 | SOC 2 | INT 7}$$

Creation focus profile:

| Skill | Starting Focus | Read |
| --- | ---: | --- |
| Medicine | 2 | Excellent. This is a 5-focus target. |
| Tactics | 2 | Non-waste only if planning the Tactics 200 stretch. |
| Steward | 1 | Excellent. This is a 5-focus target. |
| Scouting | 1 | Excellent. This is a 5-focus target. |
| Smithing | 1 | Excellent. This is a 5-focus enabler. |
| Athletics | 1 | Excellent. This is a 5-focus enabler. |
| One Handed | 1 | Useful Vigor combat seed. |
| Leadership | 1 | Useful if Leadership 75/175 is planned. |
| Charm | 1 | Optional QoL; do not add more by default. |
| Trade | 1 | Strong QoL for price marking. |

### B. Scouting-Forward Cunning Commander

This version starts faster on Scouting and the cheap Control-combat pickups, but it leans harder into Tactics focus and starts lower in Intelligence.

| Stage | Choice | Attribute | Focus and Skill Effects |
| --- | --- | ---: | --- |
| Family | Foresters | +1 Cunning | +1 focus and +10 skill: Scouting, Tactics |
| Childhood | your brawn. | +1 Vigor | +1 focus and +10 skill: Two Handed, Throwing |
| Education | hunted small game. | +1 Cunning | +1 focus and +10 skill: Bow, Tactics |
| Youth | were a chieftain's servant. / joined a commander's staff. | +1 Cunning | +1 focus and +10 skill: Tactics, Steward |
| Adulthood | you invested some money in land / workshop. | +1 Intelligence | +1 focus and +10 skill: Smithing, Trade |
| Escape | you rode off on a fast horse. | +1 Endurance | +1 focus and +10 skill: Riding, Scouting |

Starting attributes after creation:

$$\text{VIG 3 | CTR 2 | END 3 | CNG 5 | SOC 2 | INT 3}$$

Level-up allocation to level 24:

- Buy **+2 Cunning**.
- Buy **+4 Intelligence**.

Final purchased line at level 24:

$$\text{VIG 3 | CTR 2 | END 3 | CNG 7 | SOC 2 | INT 7}$$

Creation focus profile:

| Skill | Starting Focus | Read |
| --- | ---: | --- |
| Scouting | 2 | Excellent. This is the main reason to like this path. |
| Tactics | 3 | Only clean if Tactics 200 is part of the plan. |
| Steward | 1 | Excellent. This is a 5-focus target. |
| Smithing | 1 | Excellent. This is a 5-focus enabler. |
| Riding | 1 | Perfect count for Riding 100. Do not add more. |
| Bow | 1 | Useful toward Bow 100; one more focus later reaches the target under assisted Control 4. |
| Throwing | 1 | Useful toward Throwing 125; one more focus later reaches the target under assisted Control 4. |
| Two Handed | 1 | Useful if stopping at 100 or 175. |
| Trade | 1 | Strong QoL for price marking. |

---

## 5. Deprecated Old Starts

The old starts are no longer default-compatible because they begin at Control 3.

| Old Path | Problem |
| --- | --- |
| Tribespeople -> skill with horses -> repaired projects -> guard with garrison -> defeated enemy | `Tribespeople` adds Control, and the guard/engineering picks are only clean for a player-engineer variant. |
| Foresters -> attention to detail -> repaired projects -> hearth guard -> defeated enemy | `attention to detail` adds Control, and `repaired projects` adds Engineering. |

The old starts were good under a `CTR 3(5)` model. Under `CTR 2(4)`, the Control point should be treated as an avoidable attribute tax.
