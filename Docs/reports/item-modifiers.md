# Item Quality Modifiers

Generated: 2026-06-07T07:32:41.3044166+03:00

This report documents Bannerlord's item quality modifiers (prefixes for weapons, armor, shields, and mounts) parsed from the native game XML files.

## Inputs

- JSON: `Data\raw\item-modifiers.json`
- Modifiers XML: `Modules\Native\ModuleData\item_modifiers.xml`
- Groups XML: `Modules\Native\ModuleData\item_modifiers_groups.xml`

## Modifier Spawning Mechanics

When an item is spawned as battle loot or in a town's production inventory, it has a chance to receive a quality modifier based on its assigned `ItemModifierGroup`.
Each group has a weight for spawning with no modifier, and each possible modifier in the group has its own weight (drop score).

The probabilities are calculated as:
- **Loot Spawn Chance**: `loot_drop_score / (no_modifier_loot_score + sum(all_modifier_loot_drop_scores))`
- **Production Spawn Chance**: `production_drop_score / (no_modifier_production_score + sum(all_modifier_production_drop_scores))`

---

### Modifier Group: Arrows (`arrow`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Large Bag of [Item] | 2.00x | 0 Damage, +5 Stack Count | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| Legendary [Item] | 1.80x | +3 Damage, +5 Stack Count | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Balanced [Item] | 1.50x | +2 Damage | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Bent [Item] | 0.60x | -1 Damage | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Splintered [Item] | 0.30x | -3 Damage | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Axes (`axe`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +7 Damage, +3 Speed | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Masterwork [Item] | 1.50x | +5 Damage, +2 Speed | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Quality [Item] | 1.20x | +3 Damage, +1 Speed | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Dented [Item] | 0.60x | -1 Damage, -1 Speed | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Rusty [Item] | 0.30x | -4 Damage, 0 Speed | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Bolts (`bolt`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +3 Damage, +4 Stack Count | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Balanced [Item] | 1.50x | +2 Damage | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Large Bag of [Item] | 1.20x | 0 Damage, +2 Stack Count | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Bent [Item] | 0.60x | -1 Damage | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Splintered [Item] | 0.30x | -5 Damage | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Bows (`bow`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +7 Damage, +4 Missile Speed, +4 Speed | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Masterwork [Item] | 1.50x | +5 Damage, +3 Missile Speed, +3 Speed | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Balanced [Item] | 1.20x | +1 Damage, +2 Missile Speed, +2 Speed | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Cracked [Item] | 0.60x | -8 Damage, -6 Missile Speed, -4 Speed | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Splintered [Item] | 0.30x | -15 Damage, 0 Missile Speed, -2 Speed | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Chain Armor (`chain`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +9 Armor | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Lordly [Item] | 1.50x | +6 Armor | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Fine [Item] | 1.20x | +3 Armor | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Loose [Item] | 0.60x | -6 Armor | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Rusty [Item] | 0.30x | -8 Armor | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Cheap Weapons (`cheap_weapon`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +7 Damage, +3 Speed | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Fine [Item] | 1.50x | +5 Damage, +2 Speed | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Well made [Item] | 1.20x | +2 Damage, +1 Speed | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Bent [Item] | 0.60x | -5 Damage, -1 Speed | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Cracked [Item] | 0.40x | -10 Damage, -2 Speed | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Cloth Armor (`cloth`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +5 Armor | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Fine [Item] | 1.50x | +3 Armor | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Tailored [Item] | 1.20x | +1 Armor | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Worn [Item] | 0.60x | -1 Armor | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Ripped [Item] | 0.30x | -2 Armor | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Companions (`companion`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| [Normal / No Modifier] | 1.00x | None | normal | 1 / 1 (100.00%) | 1 / 1 (100.00%) |
| Old [Item] | 0.20x | +0.8 Charge Damage, +0.9 Horse Hit Points, +0.8 Horse Speed, +0.95 Maneuver | poor | 0 / 1 (0.00%) | 0 / 1 (0.00%) |
| Rusty [Item] | 0.20x | -10 Damage | poor | 0 / 1 (0.00%) | 0 / 1 (0.00%) |
| Worn [Item] | 0.20x | -6 Armor | poor | 0 / 1 (0.00%) | 0 / 1 (0.00%) |

### Modifier Group: Crossbows (`crossbow`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +4 Damage, +15 Missile Speed, +4 Speed | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Masterwork [Item] | 1.50x | +3 Damage, +9 Missile Speed, +3 Speed | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Tuned [Item] | 1.20x | 0 Damage, +3 Missile Speed, 0 Speed | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Bent [Item] | 0.60x | -5 Damage, -1 Missile Speed, -1 Speed | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Cracked [Item] | 0.30x | -10 Damage, -6 Missile Speed, -2 Speed | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Horses / Mounts (`horse`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| [Normal / No Modifier] | 1.00x | None | normal | 1 / 1 (100.00%) | 1 / 1 (100.00%) |
| Lame [Item] | 0.10x | +0.6 Charge Damage, +0.8 Horse Hit Points, +0.7 Horse Speed, +0.9 Maneuver | poor | 0 / 1 (0.00%) | 0 / 1 (0.00%) |

### Modifier Group: Leather Armor (`leather`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +7 Armor | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Fine [Item] | 1.50x | +5 Armor | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Waxed [Item] | 1.20x | +3 Armor | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Worn [Item] | 0.60x | -2 Armor | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Battered [Item] | 0.30x | -3 Armor | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Maces (`mace`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +7 Damage, +3 Speed | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Masterwork [Item] | 1.50x | +5 Damage, +2 Speed | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Balanced [Item] | 1.20x | +3 Damage, +1 Speed | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Unbalanced [Item] | 0.60x | -1 Damage, -1 Speed | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Splintered [Item] | 0.30x | -4 Damage, -2 Speed | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Plate Armor (`plate`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +12 Armor | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Lordly [Item] | 1.50x | +8 Armor | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Fine [Item] | 1.20x | +4 Armor | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Dented [Item] | 0.60x | -4 Armor | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Rusty [Item] | 0.30x | -6 Armor | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Polearms (`polearm`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +7 Damage, +3 Speed | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Masterwork [Item] | 1.50x | +5 Damage, +2 Speed | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Balanced [Item] | 1.20x | +3 Damage, +1 Speed | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Bent [Item] | 0.60x | -3 Damage, -1 Speed | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Cracked [Item] | 0.30x | -6 Damage, -3 Speed | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Shields (`shield`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +8 Armor, +210 Hit Points, 0 Speed | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Lordly [Item] | 1.50x | +5 Armor, +130 Hit Points, 0 Speed | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Thick [Item] | 1.20x | +3 Armor, +40 Hit Points, 0 Speed | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Battered [Item] | 0.60x | -2 Armor, -70 Hit Points, 0 Speed | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Cracked [Item] | 0.30x | -4 Armor, -110 Hit Points, -1 Speed | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Swords (`sword`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +7 Damage, +3 Speed | legendary | 2 / 102 (1.96%) | 5 / 107 (4.67%) |
| Masterwork [Item] | 1.50x | +5 Damage, +2 Speed | masterwork | 5 / 102 (4.90%) | 10 / 107 (9.35%) |
| Balanced [Item] | 1.20x | +3 Damage, +1 Speed | fine | 10 / 102 (9.80%) | 15 / 107 (14.02%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 102 (44.12%) | 75 / 107 (70.09%) |
| Dull [Item] | 0.60x | -10 Damage, -10 Speed | inferior | 15 / 102 (14.71%) | 1 / 107 (0.93%) |
| Rusty [Item] | 0.30x | -15 Damage, -5 Speed | poor | 25 / 102 (24.51%) | 1 / 107 (0.93%) |

### Modifier Group: Throwing Axes (`axe_throwing`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +3 Missile Speed, +4 Stack Count | legendary | 2 / 107 (1.87%) | 2 / 99 (2.02%) |
| Large Bag of [Item] | 1.50x | 0 Missile Speed, +2 Stack Count | masterwork | 10 / 107 (9.35%) | 5 / 99 (5.05%) |
| Balanced [Item] | 1.20x | +5 Missile Speed | fine | 10 / 107 (9.35%) | 15 / 99 (15.15%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 107 (42.06%) | 75 / 99 (75.76%) |
| Bent [Item] | 0.60x | -3 Missile Speed | inferior | 15 / 107 (14.02%) | 1 / 99 (1.01%) |
| Splintered [Item] | 0.30x | -6 Missile Speed | poor | 25 / 107 (23.36%) | 1 / 99 (1.01%) |

### Modifier Group: Throwing Knives (`knife_throwing`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +8 Missile Speed, +4 Stack Count | legendary | 2 / 107 (1.87%) | 2 / 99 (2.02%) |
| Balanced [Item] | 1.50x | 0 Damage, +4 Missile Speed, 0 Speed | masterwork | 10 / 107 (9.35%) | 5 / 99 (5.05%) |
| Large Bag of [Item] | 1.20x | 0 Damage, 0 Missile Speed, 0 Speed, +2 Stack Count | fine | 10 / 107 (9.35%) | 15 / 99 (15.15%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 107 (42.06%) | 75 / 99 (75.76%) |
| Bent [Item] | 0.60x | 0 Damage, -2 Missile Speed, 0 Speed | inferior | 15 / 107 (14.02%) | 1 / 99 (1.01%) |
| Rusty [Item] | 0.30x | 0 Damage, -2 Missile Speed, 0 Speed | poor | 25 / 107 (23.36%) | 1 / 99 (1.01%) |

### Modifier Group: Throwing Spears / Darts (`spear_dart_throwing`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +3 Damage, +6 Missile Speed, +2 Speed | legendary | 2 / 107 (1.87%) | 2 / 99 (2.02%) |
| Balanced [Item] | 1.50x | +2 Damage, +3 Missile Speed, +1 Speed | masterwork | 10 / 107 (9.35%) | 5 / 99 (5.05%) |
| Large Bag of [Item] | 1.20x | 0 Damage, 0 Missile Speed, 0 Speed, +2 Stack Count | fine | 10 / 107 (9.35%) | 15 / 99 (15.15%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 107 (42.06%) | 75 / 99 (75.76%) |
| Bent [Item] | 0.60x | -2 Damage, -1 Missile Speed, 0 Speed | inferior | 15 / 107 (14.02%) | 1 / 99 (1.01%) |
| Cracked [Item] | 0.30x | -5 Damage, -2 Missile Speed, 0 Speed | poor | 25 / 107 (23.36%) | 1 / 99 (1.01%) |

### Modifier Group: Unarmored Cloth (`cloth_unarmoured`)

| Modifier Prefix | Price Factor | Stat Adjustments | Quality Rank | Loot Spawn Chance | Production Spawn Chance |
| :--- | :---: | :--- | :---: | :---: | :---: |
| Legendary [Item] | 1.80x | +3 Armor | legendary | 2 / 107 (1.87%) | 5 / 102 (4.90%) |
| Fine [Item] | 1.50x | +2 Armor | masterwork | 10 / 107 (9.35%) | 5 / 102 (4.90%) |
| Tailored [Item] | 1.20x | +1 Armor | fine | 10 / 107 (9.35%) | 15 / 102 (14.71%) |
| [Normal / No Modifier] | 1.00x | None | normal | 45 / 107 (42.06%) | 75 / 102 (73.53%) |
| Worn [Item] | 0.60x | -1 Armor | inferior | 15 / 107 (14.02%) | 1 / 102 (0.98%) |
| Ripped [Item] | 0.30x | -2 Armor | poor | 25 / 107 (23.36%) | 1 / 102 (0.98%) |

