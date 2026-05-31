# Personal Combat Perks

This note summarizes perks whose main value is making the player character fight better in live battles. It uses the current perk export plus the direct skill-effect constants in the generated guide stat extract.

## Main Takeaways

- Personal combat perks should be judged against how the player actually fights. A huge mounted bonus is dead weight for an infantry captain, and a shield perk is dead weight for a two-handed duelist.
- Weapon skill itself matters, but perks are usually the bigger breakpoints. For example, +80 One Handed skill is about +5.6% weapon speed and +12% damage, while a single perk can add +20% one-handed duelist damage.
- Movement and handling perks are real combat comfort, but they are harder to value than damage, ammo, reload speed, armor penetration, or HP.
- High-skill epic perks are not always weak. Many are small per skill point, but some start counting from 200 or 250 skill and can be large if the build already reaches the high tier.
- Do not treat every 275 perk the same. Bow/Crossbow/Throwing epics start counting above 200; One Handed/Polearm start above 250; Two Handed unlocks at 250 but also starts above 250.

## Direct Skill Effects

Skill levels add baseline combat stats even before perks:

| Skill | Per skill point | +80 skill |
| --- | --- | --- |
| One Handed | +0.07% speed, +0.15% damage | +5.6% speed, +12% damage |
| Two Handed | +0.06% speed, +0.16% damage | +4.8% speed, +12.8% damage |
| Polearm | +0.06% speed, +0.07% damage | +4.8% speed, +5.6% damage |
| Bow | +0.11% damage, +0.09% accuracy effect | +8.8% damage, +7.2% accuracy effect |
| Crossbow | +0.07% reload, +0.05% accuracy effect | +5.6% reload, +4% accuracy effect |
| Throwing | +0.07% ready speed, +0.06% damage, +0.06% accuracy effect | +5.6% ready speed, +4.8% damage, +4.8% accuracy effect |

This makes attribute and focus investment more valuable when the player uses several skills under the same attribute. Vigor helps One Handed, Two Handed, and Polearm together; Control helps Bow, Crossbow, and Throwing together.

## Investment Lens

Using the additive cost model from `perk-investment-costs.md`:

| Tier | Raw allocation above 2 attribute baseline | Weighted cost |
| ---: | --- | ---: |
| 200 | 0 attribute + 5 focus | 5 |
| 225 | 1 attribute + 5 focus | 9 |
| 250 | 3 attribute + 5 focus | 17 |
| 275 | 5 attribute + 5 focus | 25 |

So level 225 perks are not "free." They still spend an attribute point that could have raised another attribute group. They become much more efficient when two or three skills in the same attribute are being pushed together.

## Vigor Weapons

### One Handed

One Handed is the flexible shield/duelist tree.

Strong low and mid picks:

- `Wrapped Handles`: +20% handling is a very noticeable early feel perk.
- `Shield Bearer`: removes the shield movement penalty, which is excellent for shield infantry play.
- `Duelist`: +20% damage without a shield. Very strong, but it pushes the character away from the defensive shield package.
- `Arrow Catcher`, `Shieldwall`, and `Steel Core Shields`: strong if the player actually blocks with shields often.
- `Deadly Purpose`: +5% one-handed damage at 225 is modest for the attribute cost unless Vigor is already being raised.
- `Chink in the Armor`: +10% melee armor penetration at 250 is more attractive than another small flat damage perk because it helps into armored targets.

High tier:

| Perk | Unlock | At 275 skill | At 330 skill |
| --- | ---: | ---: | ---: |
| `Way of the Sword` | 275 | +5% attack speed, +12.5% damage | +16% attack speed, +40% damage |

This is good if One Handed is a true main weapon and Vigor is already high. It is expensive as a splash.

### Two Handed

Two Handed is the clearest personal damage tree.

Strong picks:

- `Strong Grip`: +10% handling is a clean early quality perk.
- `Head Basher`: +10% damage with axes and maces. Excellent if those are the chosen weapons.
- `On the Edge`: +3% swing speed is small but always useful.
- `Berserker` and `Confidence`: big conditional damage perks. They reward either aggressive low-HP play or controlled high-HP play.
- `Projectile Deflection`: unique defensive utility for two-handed swords. This is build-defining if the player wants to fight without a shield.
- `Reckless Charge`: +20% speed-damage bonus while on foot. Strongest when the player actively uses movement to hit harder.
- `Blade Master` and `Vandal`: both are strong level 225 payoffs. `Vandal` is especially good into armor.

High tier:

| Perk | Unlock | At 250 skill | At 275 skill | At 330 skill |
| --- | ---: | ---: | ---: | ---: |
| `Way Of The Great Axe` | 250 | no benefit yet | +5% attack speed, +12.5% damage | +16% attack speed, +40% damage |

The perk unlocks at 250, but the formula starts above 250. It is a commitment perk, not an immediate payoff at exactly 250.

### Polearm

Polearm splits sharply between foot spear, mounted lance, and anti-cavalry utility.

Strong picks:

- `Pikeman` vs `Cavalry`: choose based on foot or mounted play. The bonuses are small, but they are very early.
- `Braced`: dismount support is useful if fighting cavalry directly.
- `Clean Thrust` vs `Swift Swing`: pick for weapon mode. `Swift Swing` is much better for swingable polearm builds.
- `Footwork`: +2% movement speed is minor, but it is always-on for polearm foot play.
- `Lancer`: +20% speed-damage bonus while mounted can be very strong in the playstyle it supports.
- `Steed Killer`: +70% damage to mounts is very specialized but very large.
- `Guards`: +50% polearm headshot damage is a strong skill-reward perk.
- `Sure Footed`: -40% charge damage taken is useful if fighting cavalry on foot.
- `Counterweight`: +15% handling for swingable polearms is a real quality upgrade.

High tier:

| Perk | Unlock | At 275 skill | At 330 skill |
| --- | ---: | ---: | ---: |
| `Way of the Spear` | 275 | +5% attack speed, +12.5% damage | +16% attack speed, +40% damage |

Polearm's normal skill damage scaling is lower than One Handed and Two Handed, so the high-tier damage perk matters if polearm is the player's main weapon.

## Control Weapons

### Bow

Bow has a very clean personal progression: remove accuracy penalties, then add reload, ammo, and high-skill scaling.

Strong picks:

- `Bow Control`: -30% movement accuracy penalty. Great for skirmish play.
- `Dead Aim`: +30% headshot damage. Excellent if the player can aim for heads reliably.
- `Nocking Point`: reduces the movement-speed penalty while reloading.
- `Quick Adjustments`: -50% rotating accuracy penalty. Very good in messy field fights.
- `Rapid Fire`: +25% reload speed is one of the clearest early ranged DPS perks.
- `Mounted Archery`: important if shooting from horseback.
- `Discipline`: longer aiming duration before losing accuracy.
- `Eagle Eye`: zoom is utility, but it is very practical.
- `Skirmish Phase Master`: -10% projectile damage taken. Personal survivability, not just captain value.
- `Horse Master`: use all bows on horseback. This is classified as unique, but it is a major combat unlock.
- `Ranger's Swiftness`: equipped bows do not slow the player down.

High tier:

| Perk | Unlock | At 275 skill | At 330 skill |
| --- | ---: | ---: | ---: |
| `Deadshot` | 275 | +15% reload speed, +37.5% bow damage | +26% reload speed, +65% bow damage |

Because this starts counting above 200, it is one of the more attractive 275 personal combat epics for a dedicated archer.

### Crossbow

Crossbow perks emphasize reload, accuracy comfort, anti-cavalry, and defensive utility.

Strong picks:

- `Marksmen`: faster aiming with crossbows.
- `Piercer`: ignores armor below 20. Strong early and especially good against lightly armored targets.
- `Wind Winder`: +25% reload speed.
- `Donkey's Swiftness`: reduced moving accuracy loss.
- `Sheriff`: +50% headshot damage.
- `Fletcher`: +4 bolts per quiver is very practical for long fights.
- `Deft Hands`: stagger resistance while reloading.
- `Loose and Move`: equipped crossbows do not slow the player down.
- `Mounted Crossbowman`: reload any crossbow on horseback. Major unique combat unlock.
- `Counter Fire`: -10% projectile damage while equipped with a crossbow.
- `Hammer Bolts`: dismounts and ignores 50% dismount resistance against cavalry.
- `Pavise`: 75% chance to block projectiles from behind with a shield on the back.

High tier:

| Perk | Unlock | At 275 skill | At 330 skill |
| --- | ---: | ---: | ---: |
| `Mighty Pull` | 275 | +15% reload speed, +37.5% crossbow damage | +26% reload speed, +65% crossbow damage |

This is another strong dedicated-ranged payoff. The question is whether Crossbow itself is worth pushing that high compared with Bow or Throwing.

### Throwing

Throwing has unusually high tactical perks: ammo, dismount, shield breaking, shield penetration, and big hit-condition damage.

Strong picks:

- `Quick Draw`: +20% draw speed.
- `Shield Breaker`: +40% shield damage.
- `Flexible Fighter`: +10% melee damage when using thrown weapons as melee. Niche, but useful for hybrid skirmishers.
- `Hunter`: +40% damage to mounts.
- `Mounted Skirmisher`: reduced mounted accuracy penalty.
- `Well Prepared`, `Saddlebags`, and `Resourceful`: ammo is extremely valuable because thrown weapons are limited.
- `Knock Off`: thrown weapons can dismount and ignore 25% dismount resistance.
- `Running Throw`: +25% speed-damage bonus.
- `Skirmisher`: -10% ranged damage taken while holding a throwing weapon.
- `Last Hit`: +50% damage to enemies below half HP.
- `Head Hunter`: +50% headshot damage.
- `Splinters`: triple damage against shields with throwing axes.
- `Perfect Technique`: +25% travel speed to thrown weapons.
- `Impale`: javelins penetrate shields. Classified as unique, but it is absolutely a personal combat unlock.
- `Weak Spot`: +30% armor penetration.

High tier:

| Perk | Unlock | At 275 skill | At 330 skill |
| --- | ---: | ---: | ---: |
| `Unstoppable Force` | 275 | +15% projectile speed, +37.5% throwing damage | +26% projectile speed, +65% throwing damage |

Throwing's high tier is expensive, but the tree has enough strong tactical perks that a Control-heavy skirmisher build can justify it.

## Support Skills

### Athletics

Athletics is a universal personal combat support skill for foot characters.

Notable perks:

- `Morning Exercise`: +3% combat movement speed.
- `Well Built`: +5 HP.
- `Fury`: +10% weapon handling while on foot.
- `Powerful`: +4% melee weapon damage.
- `Sprint`: +5% combat movement speed when no shields or ranged weapons are equipped.
- `Surging Blow`: +30% speed-damage bonus while on foot.
- `Ignore Pain`: +10% armor while on foot.
- `Spartan`: +50% stagger resistance while on foot.
- `Mighty Blow`: longer stun after enemies block, plus +1 HP per skill point above 250.

At 275 Athletics, `Mighty Blow` is already +25 personal HP from the secondary effect. At 330, it is +80 HP. That makes high Athletics much more than a small combat-feel upgrade.

### Riding

Riding is the mounted-combat support skill.

Notable perks:

- `Full Speed`: +20% charge damage.
- `Veterinary`: +20% HP to the player's mount.
- `Sagittarius`: reduced mounted accuracy penalty.
- `Horse Archer`: +10% ranged damage while mounted.
- `Mounted Warrior`: +5% mounted melee damage.
- `Thunderous Charge` and `Annoying Buzz`: morale penalties from mounted kills.
- `Dauntless Steed`: +50% stagger resistance while mounted.
- `Tough Steed`: +20% armor to the player's mount.

Riding is not just a travel skill for mounted builds. It protects the mount, improves mounted weapon use, and adds morale pressure.

### Roguery, Medicine, Smithing, Engineering

These are smaller personal-combat support sources:

- `Roguery Carver`: +10% damage with civilian weapons.
- `Roguery Dirty Fighting`: +50% kick stun duration.
- `Roguery Dash and Slash`: +50% speed-damage bonus while on foot.
- `Roguery Fleet Footed`: +10% movement speed while no weapons or shields are equipped.
- `Medicine Preventive Medicine`, `Doctor's Oath`, and `Fortitude Tonic`: small personal HP boosts.
- `Medicine Self Medication`: +2% combat movement speed and healing-rate support.
- `Smithing Sharpened Edge` / `Sharpened Tip`: +2% damage on crafted weapons. This is modest as a combat reason to push Smithing, but it stacks with the fact that crafted weapons can be extremely valuable and strong.
- `Engineering Torsion Engines`: +3 damage to equipped crossbows.
- `Engineering Scaffolds`: +30% shield hitpoints.

## Practical Build Reads

### Low Investment

Most level 25-200 personal combat perks can be reached with focus points alone from the 2-attribute baseline. This is where splash value is highest.

Good examples:

- One Handed shield comfort: `Wrapped Handles`, `Shield Bearer`, `Arrow Catcher`, `Shieldwall`.
- Two Handed offense: `Strong Grip`, `Head Basher`, `On the Edge`, `Projectile Deflection`, `Reckless Charge`.
- Bow comfort: `Bow Control`, `Rapid Fire`, `Mounted Archery`, `Eagle Eye`.
- Crossbow comfort: `Wind Winder`, `Donkey's Swiftness`, `Loose and Move`, `Counter Fire`.
- Throwing tactics: `Quick Draw`, `Knock Off`, `Running Throw`, `Head Hunter`, `Resourceful`.
- Foot combat support: Athletics up to 125 or 150 is broadly useful.

### Medium Investment

Level 225 and 250 perks require attribute investment. They make sense when the player is already raising that attribute group.

Standouts:

- Control: Bow/Crossbow/Throwing all have strong 225-250 perks, so a broad ranged build uses Control efficiently.
- Vigor: Two Handed 225 and Polearm 225 are strong; One Handed 250 is good if melee armor penetration matters.
- Endurance: Athletics and Riding 250 defensive perks are useful; Smithing 250 is not a strong combat-only reason by itself.

### High Investment

Level 275 perks should be for true identity skills, not casual splashes.

Most appealing high personal combat targets:

- Bow, Crossbow, or Throwing 275 if the build lives on that weapon.
- Athletics 275 if the player wants the personal HP scaling and foot-combat support.
- One Handed or Polearm 275 if Vigor is already being pushed and that weapon is a mainstay.

Be cautious with:

- Pushing a single weapon to 275 while ignoring the other two skills in its attribute group. The attribute cost is much more efficient when shared.
- Taking high-tier perks only for tiny numeric text. The total scaling can be good, but only if the skill will keep climbing.

## Open Follow-Ups

- Add exact live formulas for handling, movement speed, and stagger resistance if we extract their final driven-property paths in the same detail as XP formulas.
- Compare personal high-tier epics using actual expected skill levels: at unlock, at 300, and at 330.
- Link this guide to a future build-rater that scores perk value against weighted allocation cost and shared attribute usage.
