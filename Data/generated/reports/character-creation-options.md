# Bannerlord Character Creation Choices

Generated: 2026-05-28T06:53:36.3263624+03:00

This report is extracted from local compiled assemblies. It covers the initial player character creation option effects exposed through `NarrativeMenuOptionArgs`.

## Reading Notes

- The standard non-age options use constructor defaults: +1 focus per affected skill, +10 skill levels per affected skill, and +1 attribute level.
- `Smithing` appears as `Crafting` in the compiled `DefaultSkills` API; this report displays the player-facing skill name.
- Age choices add unspent points rather than assigning them to a specific skill or attribute.
- Story-mode escape choices are included because they use the same character creation option effect path.

## Stage Summary

| Stage | Options |
| --- | ---: |
| Family | 36 |
| Childhood | 6 |
| Education | 12 |
| Youth | 17 |
| Adulthood | 12 |
| Age | 4 |
| Escape | 6 |

## Skill Coverage

| Skill | Choice count |
| --- | ---: |
| One Handed | 8 |
| Two Handed | 8 |
| Polearm | 14 |
| Bow | 13 |
| Crossbow | 7 |
| Throwing | 10 |
| Riding | 15 |
| Athletics | 11 |
| Smithing | 9 |
| Scouting | 10 |
| Tactics | 13 |
| Roguery | 10 |
| Charm | 15 |
| Leadership | 8 |
| Trade | 10 |
| Steward | 4 |
| Medicine | 5 |
| Engineering | 8 |

## Attribute Coverage

| Attribute | Choice count |
| --- | ---: |
| Control | 14 |
| Cunning | 17 |
| Endurance | 16 |
| Intelligence | 16 |
| Social | 14 |
| Vigor | 12 |

## Options

### Family

| Culture | Choice | Effects | Option id |
| --- | --- | --- | --- |
| Aserai | Urban back-alley thugs | +1 Control; +1 focus and +10 skill to Polearm, Roguery | `aserai_artisan_option` |
| Aserai | Oasis farmers | +1 Endurance; +1 focus and +10 skill to One Handed, Athletics | `aserai_farmer_option` |
| Aserai | Bedouin | +1 Cunning; +1 focus and +10 skill to Bow, Scouting | `aserai_herder_option` |
| Aserai | Kinsfolk of an emir | +1 Social; +1 focus and +10 skill to Throwing, Riding | `aserai_kinsfolk_option` |
| Aserai | Physician | +1 Intelligence; +1 focus and +10 skill to Charm, Medicine | `aserai_physician_option` |
| Aserai | Warrior-slaves | +1 Vigor; +1 focus and +10 skill to Polearm, Riding | `aserai_slave_option` |
| Battania | Smiths | +1 Endurance; +1 focus and +10 skill to Two Handed, Smithing | `battania_artisan_option` |
| Battania | Bards | +1 Social; +1 focus and +10 skill to Roguery, Charm | `battania_bard_option` |
| Battania | Tribespeople | +1 Control; +1 focus and +10 skill to Throwing, Athletics | `battania_farmer_option` |
| Battania | Healers | +1 Intelligence; +1 focus and +10 skill to Charm, Medicine | `battania_healer_option` |
| Battania | Foresters | +1 Cunning; +1 focus and +10 skill to Scouting, Tactics | `battania_hunter_option` |
| Battania | Members of the chieftain's hearthguard | +1 Vigor; +1 focus and +10 skill to Two Handed, Bow | `battania_retainer_option` |
| Empire | Urban artisans | +1 Intelligence; +1 focus and +10 skill to Crossbow, Smithing | `empire_artisan_option` |
| Empire | Freeholders | +1 Endurance; +1 focus and +10 skill to Polearm, Athletics | `empire_farmer_option` |
| Empire | Foresters | +1 Control; +1 focus and +10 skill to Bow, Scouting | `empire_hunter_option` |
| Empire | A landlord's retainers | +1 Vigor; +1 focus and +10 skill to Polearm, Riding | `empire_lanlord_option` |
| Empire | Urban merchants | +1 Social; +1 focus and +10 skill to Charm, Trade | `empire_merchant_option` |
| Empire | Urban vagabonds | +1 Cunning; +1 focus and +10 skill to Throwing, Roguery | `empire_vagabond_option` |
| Khuzait | Farmers | +1 Vigor; +1 focus and +10 skill to Polearm, Throwing | `khuzait_farmer_option` |
| Khuzait | Shamans | +1 Intelligence; +1 focus and +10 skill to Charm, Medicine | `khuzait_healer_option` |
| Khuzait | Nomads | +1 Cunning; +1 focus and +10 skill to Riding, Scouting | `khuzait_herder_option` |
| Khuzait | Tribespeople | +1 Control; +1 focus and +10 skill to Bow, Riding | `khuzait_mercenary_option` |
| Khuzait | Merchants | +1 Social; +1 focus and +10 skill to Charm, Trade | `khuzait_merhant_option` |
| Khuzait | A noyan's kinsfolk | +1 Endurance; +1 focus and +10 skill to Polearm, Riding | `khuzait_retainer_option` |
| Sturgia | Urban artisans | +1 Intelligence; +1 focus and +10 skill to One Handed, Smithing | `sturgia_artisan_option` |
| Sturgia | A boyar's companions | +1 Social; +1 focus and +10 skill to Two Handed, Riding | `sturgia_companion_option` |
| Sturgia | Free farmers | +1 Endurance; +1 focus and +10 skill to Polearm, Athletics | `sturgia_farmer_option` |
| Sturgia | Hunters | +1 Vigor; +1 focus and +10 skill to Bow, Scouting | `sturgia_hunter_option` |
| Sturgia | Urban traders | +1 Cunning; +1 focus and +10 skill to Tactics, Trade | `sturgia_trader_option` |
| Sturgia | Vagabonds | +1 Control; +1 focus and +10 skill to Throwing, Roguery | `sturgia_vagabond_option` |
| Vlandia | Urban blacksmith | +1 Vigor; +1 focus and +10 skill to Two Handed, Smithing | `vlandia_blacksmith_option` |
| Vlandia | Yeomen | +1 Endurance; +1 focus and +10 skill to Polearm, Crossbow | `vlandia_farmer_option` |
| Vlandia | Hunters | +1 Control; +1 focus and +10 skill to Crossbow, Scouting | `vlandia_hunter_option` |
| Vlandia | Mercenaries | +1 Cunning; +1 focus and +10 skill to Crossbow, Roguery | `vlandia_mercenary_option` |
| Vlandia | Urban merchants | +1 Intelligence; +1 focus and +10 skill to Charm, Trade | `vlandia_merchant_option` |
| Vlandia | A baron's retainers | +1 Social; +1 focus and +10 skill to Polearm, Riding | `vlandia_retainer_option` |

### Childhood

| Culture | Choice | Effects | Option id |
| --- | --- | --- | --- |
|  | your brawn. | +1 Vigor; +1 focus and +10 skill to Two Handed, Throwing | `childhood_brawn_option` |
|  | your attention to detail. | +1 Control; +1 focus and +10 skill to Bow, Athletics | `childhood_detail_option` |
|  | your skill with horses. | +1 Endurance; +1 focus and +10 skill to Riding, Medicine | `childhood_horse_option` |
|  | your way with people. | +1 Social; +1 focus and +10 skill to Charm, Leadership | `childhood_leader_option` |
|  | your leadership skills. | +1 Cunning; +1 focus and +10 skill to Tactics, Leadership | `childhood_leadership_option` |
|  | your aptitude for numbers. | +1 Intelligence; +1 focus and +10 skill to Trade, Engineering | `childhood_smart_option` |

### Education

| Culture | Choice | Effects | Option id |
| --- | --- | --- | --- |
|  | helped at building sites. | +1 Vigor; +1 focus and +10 skill to Athletics, Smithing | `education_docker_option` |
|  | gathered herbs in the wild. | +1 Endurance; +1 focus and +10 skill to Scouting, Medicine | `education_doctor_option` |
|  | repaired projects. | +1 Intelligence; +1 focus and +10 skill to Smithing, Engineering | `education_engineer_option` |
|  | hung out with the gangs in the alleys. | +1 Cunning; +1 focus and +10 skill to One Handed, Roguery | `education_ganger_option` |
|  | herded the sheep. | +1 Control; +1 focus and +10 skill to Throwing, Athletics | `education_herder_option` |
|  | cared for the horses. | +1 Endurance; +1 focus and +10 skill to Riding, Steward | `education_horser_option` |
|  | hunted small game. | +1 Cunning; +1 focus and +10 skill to Bow, Tactics | `education_hunter_option` |
|  | worked in the markets and caravanserais. | +1 Social; +1 focus and +10 skill to Charm, Trade | `education_marketer_option` |
|  | sold product at the market. | +1 Social; +1 focus and +10 skill to Charm, Trade | `education_merchant_option` |
|  | worked in the village smithy. | +1 Vigor; +1 focus and +10 skill to Two Handed, Smithing | `education_smith_option` |
|  | studied with your private tutor. | +1 Intelligence; +1 focus and +10 skill to Leadership, Engineering | `education_tutor_option` |
|  | watched the militia training. | +1 Control; +1 focus and +10 skill to Polearm, Tactics | `education_watcher_option` |

### Youth

| Culture | Choice | Effects | Option id |
| --- | --- | --- | --- |
|  | marched with the camp followers. | +1 Cunning; +1 focus and +10 skill to Throwing, Roguery | `youth_camp_option` |
|  | trained with the cavalry. | +1 Endurance; +1 focus and +10 skill to Polearm, Riding | `youth_cavalry_option` |
|  | served in an envoy's entourage | +1 Social; +1 focus and +10 skill to Scouting, Charm | `youth_envoys_guard_first_option` |
|  | served in an envoy's entourage | +1 Social; +1 focus and +10 skill to Scouting, Charm | `youth_envoys_guard_second_option` |
|  | served as a baron's groom. | +1 Social; +1 focus and +10 skill to Tactics, Charm | `youth_groom_option` |
|  | stood guard with the garrisons. | +1 Intelligence; +1 focus and +10 skill to Crossbow, Engineering | `youth_guard_empire_register_option` |
|  | stood guard with the garrisons. | +1 Intelligence; +1 focus and +10 skill to Bow, Engineering | `youth_guard_garrisons_register_option` |
|  | stood guard with the garrisons. | +1 Intelligence; +1 focus and +10 skill to Crossbow, Engineering | `youth_guard_high_register_option` |
|  | stood guard with the garrisons. | +1 Intelligence; +1 focus and +10 skill to Bow, Engineering | `youth_guard_low_register_option` |
|  | trained with the hearth guard. | +1 Endurance; +1 focus and +10 skill to Polearm, Riding | `youth_hearth_option` |
|  | trained with the infantry. | +1 Vigor; +1 focus and +10 skill to One Handed, Polearm | `youth_infantry_option` |
|  | joined the kern. | +1 Control; +1 focus and +10 skill to One Handed, Throwing | `youth_kern_option` |
|  | rode with the scouts. | +1 Endurance; +1 focus and +10 skill to Bow, Riding | `youth_rider_high_register_option` |
|  | rode with the scouts. | +1 Endurance; +1 focus and +10 skill to Bow, Riding | `youth_rider_low_register_option` |
|  | were a chieftain's servant. | +1 Cunning; +1 focus and +10 skill to Tactics, Steward | `youth_servant_second_option` |
|  | joined the skirmishers. | +1 Control; +1 focus and +10 skill to One Handed, Throwing | `youth_skirmisher_option` |
|  | joined a commander's staff. | +1 Cunning; +1 focus and +10 skill to Tactics, Steward | `youth_staff_second_option` |

### Adulthood

| Culture | Choice | Effects | Option id |
| --- | --- | --- | --- |
|  | you led a caravan. | +1 Cunning; +1 focus and +10 skill to Leadership, Trade; +1 Calculating trait; +10 renown | `adulthood_caravan_leader_option` |
|  | you defeated an enemy in battle. | +1 Vigor; +1 focus and +10 skill to One Handed, Two Handed; +1 Valor trait; +20 renown | `adulthood_defeated_enemy_option` |
|  | you had a famous escapade in town. | +1 Endurance; +1 focus and +10 skill to Athletics, Roguery; +1 Valor trait; +5 renown | `adulthood_escapade_high_register_option` |
|  | you had a famous escapade. | +1 Endurance; +1 focus and +10 skill to Athletics, Roguery; +1 Valor trait; +5 renown | `adulthood_escapade_low_register_option` |
|  | you hunted a dangerous animal. | +1 Control; +1 focus and +10 skill to Polearm, Athletics; +1 Valor trait; +5 renown | `adulthood_hunter_option` |
|  | you invested some money in land. | +1 Intelligence; +1 focus and +10 skill to Smithing, Trade; +1 Calculating trait; +10 renown | `adulthood_investor_option` |
|  | you led a successful manhunt. | +1 Cunning; +1 focus and +10 skill to Tactics, Leadership; +1 Calculating trait; +10 renown | `adulthood_manhunt_option` |
|  | you treated people well. | +1 Social; +1 focus and +10 skill to Charm, Steward; +1 Generosity trait; +1 Honor trait; +1 Mercy trait; +5 renown | `adulthood_nice_person_option` |
|  | you saved your city quarter from a fire. | +1 Cunning; +1 focus and +10 skill to Tactics, Leadership; +1 Calculating trait; +10 renown | `adulthood_saved_city_option` |
|  | you saved your village from a flood. | +1 Cunning; +1 focus and +10 skill to Tactics, Leadership; +1 Valor trait; +10 renown | `adulthood_saved_village_option` |
|  | you survived a siege. | +1 Control; +1 focus and +10 skill to Bow, Crossbow; +5 renown | `adulthood_siege_survivor_option` |
|  | you invested some money in a workshop. | +1 Intelligence; +1 focus and +10 skill to Smithing, Trade; +1 Calculating trait; +10 renown | `adulthood_workshop_option` |

### Age

| Culture | Choice | Effects | Option id |
| --- | --- | --- | --- |
|  | 30 | +4 unspent focus; +2 unspent attribute | `age_selection_adult_option` |
|  | 50 | +8 unspent focus; +4 unspent attribute | `age_selection_elder_option` |
|  | 40 | +6 unspent focus; +3 unspent attribute | `age_selection_middle_age_option` |
|  | 20 | +2 unspent focus; +1 unspent attribute | `age_selection_young_adult_option` |

### Escape

| Culture | Choice | Effects | Option id |
| --- | --- | --- | --- |
|  | you drove them off with arrows. | +1 Control; +1 focus and +10 skill to Bow, Tactics | `escape_arrow_option` |
|  | you organized the travelers to break out. | +1 Social; +1 focus and +10 skill to Charm, Leadership | `escape_breakout_option` |
|  | you rode off on a fast horse. | +1 Endurance; +1 focus and +10 skill to Riding, Scouting | `escape_horse_option` |
|  | you threw up makeshift fortifications. | +1 Intelligence; +1 focus and +10 skill to Two Handed, Engineering | `escape_makeshift_fortification_option` |
|  | you subdued a raider. | +1 Vigor; +1 focus and +10 skill to One Handed, Athletics | `escape_subdued_raider_option` |
|  | you tricked the raiders. | +1 Cunning; +1 focus and +10 skill to Tactics, Roguery | `escape_tricked_option` |

## Outputs

- JSON: `Data\generated\character-creation-options.json`
- Report: `Data\generated\reports\character-creation-options.md`
