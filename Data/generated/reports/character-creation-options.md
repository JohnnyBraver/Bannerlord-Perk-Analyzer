# Bannerlord Character Creation Choices

Generated: 2026-05-28T06:53:36.3263624+03:00

This report is extracted from local compiled assemblies. It covers the initial player character creation option effects exposed through `NarrativeMenuOptionArgs`.

## Reading Notes

- The standard non-age options use constructor defaults: +1 focus per affected skill, +10 skill levels per affected skill, and +1 attribute level.
- `Smithing` appears as `Crafting` in the compiled `DefaultSkills` API; this report displays the player-facing skill name.
- Sandbox age choices add unspent points rather than assigning them to a specific skill or attribute.
- Story campaign deletes the sandbox age-selection menu. Its final escape choice replaces age 20: the same +1 attribute and +2 focus budget is fixed to one attribute and two skills, and it also adds +10 starting levels to those two skills.
- Story campaign also has a larger family context than sandbox. Those relatives do not inherit the player's character creation attribute/focus/skill choices; they use fixed StoryMode templates plus the normal HeroCreator/HeroDeveloper initialization flow.

## Stage Summary

| Stage | Availability | Point allocation | Options |
| --- | --- | --- | ---: |
| Family | campaign, sandbox | fixed_choice | 36 |
| Childhood | campaign, sandbox | fixed_choice | 6 |
| Education | campaign, sandbox | fixed_choice | 12 |
| Youth | campaign, sandbox | fixed_choice | 17 |
| Adulthood | campaign, sandbox | fixed_choice | 12 |
| Age | sandbox | sandbox_flexible_age_points | 4 |
| Escape | campaign | campaign_fixed_age_20_equivalent | 6 |

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

## Campaign Family Mechanics

Story campaign family attributes, focus, and skill values are not allocated from the player's character creation choices. Family members are registered through HeroCreator.CreateBasicHero from fixed StoryMode character objects. Creation menus can later change family culture, names, appearance, equipment, and home settlement, but not their underlying template-driven stat source.

DefaultHeroCreationModel.GetDefaultSkillsForHero reads CharacterObject.GetDefaultCharacterSkills(). For adult heroes it adds a random +5 to +9 to each nonzero template skill before the hero developer derives level, focus, attributes, and perks from those skill values. Underage siblings defer this until they pass the game's coming-of-age check.

HeroDeveloper.InitializeHeroDeveloper and DefaultCharacterDevelopmentModel distribute unspent focus and attribute points toward skills that are over their current learning limits. This can vary slightly with the random skill noise, but it is not driven by the selected family/background/escape options.

| Family member | Character id | Skill source |
| --- | --- | --- |
| Father | `main_hero_father` | `SkillSet.spc_cavalry_skills_rookie` |
| Mother | `main_hero_mother` | `SkillSet.spc_matriarch_skills_rookie` |
| Elder Brother | `tutorial_npc_brother` | `SkillSet.spc_cavalry_skills_rookie` |
| Younger Brother | `storymode_little_brother` | `SkillSet.spc_cavalry_skills_rookie` |
| Younger Sister | `storymode_little_sister` | `SkillSet.spc_cavalry_skills_rookie` |

## Hero Creation Flow

HeroCreation is the game's generic hero factory plus initializer. It creates or finds a Hero, builds HeroInitializationArgs, then asks HeroCreationModel for defaults such as born settlement, culture, traits, skills, body properties, and equipment.

StoryModeHeroes.RegisterAll calls HeroCreator.CreateBasicHero for the player's parents, elder brother, younger brother, and younger sister. Parents are registered as not alive and StoryMode assigns their birth/death days; siblings are registered alive. StoryMode then links siblings to the fixed mother and father heroes. The elder brother gets ResetCharacterStats after that link; younger siblings defer skill setup until the story rescue/load/coming-of-age helper sees they need it.

CreateBasicHero first tries to find an existing hero by string id. If none exists, it asks HeroCreationModel.GetBirthAndDeathDay for dates, creates a Hero from the exact CharacterObject, wraps it in HeroInitializationArgs with isOffspring=false, and calls InitializeHeroFromSettings.

CreateSpecialHero is the dynamic NPC path: it clones the template CharacterObject, enables generated first/full names, optionally sets born settlement, clan, and supporter clan, then uses the same InitializeHeroFromSettings initializer. The campaign family path does not use this clone path.

| Step | Effect |
| --- | --- |
| Family And Identity | Applies mother, father, gender, level, occupation, supporter clan, body build/weight, names, born settlement, clan, culture, and preferred formation from args or HeroCreationModel defaults. |
| Traits | Calls HeroCreationModel.GetTraitsForHero and writes the returned trait levels. For campaign family this is still model/template driven, not one of the player creation choices. |
| Skills | Calls HeroCreationModel.GetDefaultSkillsForHero and writes those skill values onto the hero. For adults this reads the character skill template and adds +5 to +9 noise to nonzero skills. |
| Developer | Initializes HeroDeveloper immediately for offspring, or for non-offspring heroes only when they are at or above the coming-of-age threshold. This derives level, attributes, focus, and perks from skill values. |
| Equipment | Assigns civilian and battle equipment from HeroCreationModel. Underage heroes get delivered-offspring/civilian-derived equipment; adults keep their current civilian and battle equipment. |

## Options

### Family

| Availability | Culture | Choice | Effects | Option id |
| --- | --- | --- | --- | --- |
| campaign, sandbox | Aserai | Urban back-alley thugs | +1 Control; +1 focus and +10 skill to Polearm, Roguery | `aserai_artisan_option` |
| campaign, sandbox | Aserai | Oasis farmers | +1 Endurance; +1 focus and +10 skill to One Handed, Athletics | `aserai_farmer_option` |
| campaign, sandbox | Aserai | Bedouin | +1 Cunning; +1 focus and +10 skill to Bow, Scouting | `aserai_herder_option` |
| campaign, sandbox | Aserai | Kinsfolk of an emir | +1 Social; +1 focus and +10 skill to Throwing, Riding | `aserai_kinsfolk_option` |
| campaign, sandbox | Aserai | Physician | +1 Intelligence; +1 focus and +10 skill to Charm, Medicine | `aserai_physician_option` |
| campaign, sandbox | Aserai | Warrior-slaves | +1 Vigor; +1 focus and +10 skill to Polearm, Riding | `aserai_slave_option` |
| campaign, sandbox | Battania | Smiths | +1 Endurance; +1 focus and +10 skill to Two Handed, Smithing | `battania_artisan_option` |
| campaign, sandbox | Battania | Bards | +1 Social; +1 focus and +10 skill to Roguery, Charm | `battania_bard_option` |
| campaign, sandbox | Battania | Tribespeople | +1 Control; +1 focus and +10 skill to Throwing, Athletics | `battania_farmer_option` |
| campaign, sandbox | Battania | Healers | +1 Intelligence; +1 focus and +10 skill to Charm, Medicine | `battania_healer_option` |
| campaign, sandbox | Battania | Foresters | +1 Cunning; +1 focus and +10 skill to Scouting, Tactics | `battania_hunter_option` |
| campaign, sandbox | Battania | Members of the chieftain's hearthguard | +1 Vigor; +1 focus and +10 skill to Two Handed, Bow | `battania_retainer_option` |
| campaign, sandbox | Empire | Urban artisans | +1 Intelligence; +1 focus and +10 skill to Crossbow, Smithing | `empire_artisan_option` |
| campaign, sandbox | Empire | Freeholders | +1 Endurance; +1 focus and +10 skill to Polearm, Athletics | `empire_farmer_option` |
| campaign, sandbox | Empire | Foresters | +1 Control; +1 focus and +10 skill to Bow, Scouting | `empire_hunter_option` |
| campaign, sandbox | Empire | A landlord's retainers | +1 Vigor; +1 focus and +10 skill to Polearm, Riding | `empire_lanlord_option` |
| campaign, sandbox | Empire | Urban merchants | +1 Social; +1 focus and +10 skill to Charm, Trade | `empire_merchant_option` |
| campaign, sandbox | Empire | Urban vagabonds | +1 Cunning; +1 focus and +10 skill to Throwing, Roguery | `empire_vagabond_option` |
| campaign, sandbox | Khuzait | Farmers | +1 Vigor; +1 focus and +10 skill to Polearm, Throwing | `khuzait_farmer_option` |
| campaign, sandbox | Khuzait | Shamans | +1 Intelligence; +1 focus and +10 skill to Charm, Medicine | `khuzait_healer_option` |
| campaign, sandbox | Khuzait | Nomads | +1 Cunning; +1 focus and +10 skill to Riding, Scouting | `khuzait_herder_option` |
| campaign, sandbox | Khuzait | Tribespeople | +1 Control; +1 focus and +10 skill to Bow, Riding | `khuzait_mercenary_option` |
| campaign, sandbox | Khuzait | Merchants | +1 Social; +1 focus and +10 skill to Charm, Trade | `khuzait_merhant_option` |
| campaign, sandbox | Khuzait | A noyan's kinsfolk | +1 Endurance; +1 focus and +10 skill to Polearm, Riding | `khuzait_retainer_option` |
| campaign, sandbox | Sturgia | Urban artisans | +1 Intelligence; +1 focus and +10 skill to One Handed, Smithing | `sturgia_artisan_option` |
| campaign, sandbox | Sturgia | A boyar's companions | +1 Social; +1 focus and +10 skill to Two Handed, Riding | `sturgia_companion_option` |
| campaign, sandbox | Sturgia | Free farmers | +1 Endurance; +1 focus and +10 skill to Polearm, Athletics | `sturgia_farmer_option` |
| campaign, sandbox | Sturgia | Hunters | +1 Vigor; +1 focus and +10 skill to Bow, Scouting | `sturgia_hunter_option` |
| campaign, sandbox | Sturgia | Urban traders | +1 Cunning; +1 focus and +10 skill to Tactics, Trade | `sturgia_trader_option` |
| campaign, sandbox | Sturgia | Vagabonds | +1 Control; +1 focus and +10 skill to Throwing, Roguery | `sturgia_vagabond_option` |
| campaign, sandbox | Vlandia | Urban blacksmith | +1 Vigor; +1 focus and +10 skill to Two Handed, Smithing | `vlandia_blacksmith_option` |
| campaign, sandbox | Vlandia | Yeomen | +1 Endurance; +1 focus and +10 skill to Polearm, Crossbow | `vlandia_farmer_option` |
| campaign, sandbox | Vlandia | Hunters | +1 Control; +1 focus and +10 skill to Crossbow, Scouting | `vlandia_hunter_option` |
| campaign, sandbox | Vlandia | Mercenaries | +1 Cunning; +1 focus and +10 skill to Crossbow, Roguery | `vlandia_mercenary_option` |
| campaign, sandbox | Vlandia | Urban merchants | +1 Intelligence; +1 focus and +10 skill to Charm, Trade | `vlandia_merchant_option` |
| campaign, sandbox | Vlandia | A baron's retainers | +1 Social; +1 focus and +10 skill to Polearm, Riding | `vlandia_retainer_option` |

### Childhood

| Availability | Culture | Choice | Effects | Option id |
| --- | --- | --- | --- | --- |
| campaign, sandbox |  | your brawn. | +1 Vigor; +1 focus and +10 skill to Two Handed, Throwing | `childhood_brawn_option` |
| campaign, sandbox |  | your attention to detail. | +1 Control; +1 focus and +10 skill to Bow, Athletics | `childhood_detail_option` |
| campaign, sandbox |  | your skill with horses. | +1 Endurance; +1 focus and +10 skill to Riding, Medicine | `childhood_horse_option` |
| campaign, sandbox |  | your way with people. | +1 Social; +1 focus and +10 skill to Charm, Leadership | `childhood_leader_option` |
| campaign, sandbox |  | your leadership skills. | +1 Cunning; +1 focus and +10 skill to Tactics, Leadership | `childhood_leadership_option` |
| campaign, sandbox |  | your aptitude for numbers. | +1 Intelligence; +1 focus and +10 skill to Trade, Engineering | `childhood_smart_option` |

### Education

| Availability | Culture | Choice | Effects | Option id |
| --- | --- | --- | --- | --- |
| campaign, sandbox |  | helped at building sites. | +1 Vigor; +1 focus and +10 skill to Athletics, Smithing | `education_docker_option` |
| campaign, sandbox |  | gathered herbs in the wild. | +1 Endurance; +1 focus and +10 skill to Scouting, Medicine | `education_doctor_option` |
| campaign, sandbox |  | repaired projects. | +1 Intelligence; +1 focus and +10 skill to Smithing, Engineering | `education_engineer_option` |
| campaign, sandbox |  | hung out with the gangs in the alleys. | +1 Cunning; +1 focus and +10 skill to One Handed, Roguery | `education_ganger_option` |
| campaign, sandbox |  | herded the sheep. | +1 Control; +1 focus and +10 skill to Throwing, Athletics | `education_herder_option` |
| campaign, sandbox |  | cared for the horses. | +1 Endurance; +1 focus and +10 skill to Riding, Steward | `education_horser_option` |
| campaign, sandbox |  | hunted small game. | +1 Cunning; +1 focus and +10 skill to Bow, Tactics | `education_hunter_option` |
| campaign, sandbox |  | worked in the markets and caravanserais. | +1 Social; +1 focus and +10 skill to Charm, Trade | `education_marketer_option` |
| campaign, sandbox |  | sold product at the market. | +1 Social; +1 focus and +10 skill to Charm, Trade | `education_merchant_option` |
| campaign, sandbox |  | worked in the village smithy. | +1 Vigor; +1 focus and +10 skill to Two Handed, Smithing | `education_smith_option` |
| campaign, sandbox |  | studied with your private tutor. | +1 Intelligence; +1 focus and +10 skill to Leadership, Engineering | `education_tutor_option` |
| campaign, sandbox |  | watched the militia training. | +1 Control; +1 focus and +10 skill to Polearm, Tactics | `education_watcher_option` |

### Youth

| Availability | Culture | Choice | Effects | Option id |
| --- | --- | --- | --- | --- |
| campaign, sandbox |  | marched with the camp followers. | +1 Cunning; +1 focus and +10 skill to Throwing, Roguery | `youth_camp_option` |
| campaign, sandbox |  | trained with the cavalry. | +1 Endurance; +1 focus and +10 skill to Polearm, Riding | `youth_cavalry_option` |
| campaign, sandbox |  | served in an envoy's entourage | +1 Social; +1 focus and +10 skill to Scouting, Charm | `youth_envoys_guard_first_option` |
| campaign, sandbox |  | served in an envoy's entourage | +1 Social; +1 focus and +10 skill to Scouting, Charm | `youth_envoys_guard_second_option` |
| campaign, sandbox |  | served as a baron's groom. | +1 Social; +1 focus and +10 skill to Tactics, Charm | `youth_groom_option` |
| campaign, sandbox |  | stood guard with the garrisons. | +1 Intelligence; +1 focus and +10 skill to Crossbow, Engineering | `youth_guard_empire_register_option` |
| campaign, sandbox |  | stood guard with the garrisons. | +1 Intelligence; +1 focus and +10 skill to Bow, Engineering | `youth_guard_garrisons_register_option` |
| campaign, sandbox |  | stood guard with the garrisons. | +1 Intelligence; +1 focus and +10 skill to Crossbow, Engineering | `youth_guard_high_register_option` |
| campaign, sandbox |  | stood guard with the garrisons. | +1 Intelligence; +1 focus and +10 skill to Bow, Engineering | `youth_guard_low_register_option` |
| campaign, sandbox |  | trained with the hearth guard. | +1 Endurance; +1 focus and +10 skill to Polearm, Riding | `youth_hearth_option` |
| campaign, sandbox |  | trained with the infantry. | +1 Vigor; +1 focus and +10 skill to One Handed, Polearm | `youth_infantry_option` |
| campaign, sandbox |  | joined the kern. | +1 Control; +1 focus and +10 skill to One Handed, Throwing | `youth_kern_option` |
| campaign, sandbox |  | rode with the scouts. | +1 Endurance; +1 focus and +10 skill to Bow, Riding | `youth_rider_high_register_option` |
| campaign, sandbox |  | rode with the scouts. | +1 Endurance; +1 focus and +10 skill to Bow, Riding | `youth_rider_low_register_option` |
| campaign, sandbox |  | were a chieftain's servant. | +1 Cunning; +1 focus and +10 skill to Tactics, Steward | `youth_servant_second_option` |
| campaign, sandbox |  | joined the skirmishers. | +1 Control; +1 focus and +10 skill to One Handed, Throwing | `youth_skirmisher_option` |
| campaign, sandbox |  | joined a commander's staff. | +1 Cunning; +1 focus and +10 skill to Tactics, Steward | `youth_staff_second_option` |

### Adulthood

| Availability | Culture | Choice | Effects | Option id |
| --- | --- | --- | --- | --- |
| campaign, sandbox |  | you led a caravan. | +1 Cunning; +1 focus and +10 skill to Leadership, Trade; +1 Calculating trait; +10 renown | `adulthood_caravan_leader_option` |
| campaign, sandbox |  | you defeated an enemy in battle. | +1 Vigor; +1 focus and +10 skill to One Handed, Two Handed; +1 Valor trait; +20 renown | `adulthood_defeated_enemy_option` |
| campaign, sandbox |  | you had a famous escapade in town. | +1 Endurance; +1 focus and +10 skill to Athletics, Roguery; +1 Valor trait; +5 renown | `adulthood_escapade_high_register_option` |
| campaign, sandbox |  | you had a famous escapade. | +1 Endurance; +1 focus and +10 skill to Athletics, Roguery; +1 Valor trait; +5 renown | `adulthood_escapade_low_register_option` |
| campaign, sandbox |  | you hunted a dangerous animal. | +1 Control; +1 focus and +10 skill to Polearm, Athletics; +1 Valor trait; +5 renown | `adulthood_hunter_option` |
| campaign, sandbox |  | you invested some money in land. | +1 Intelligence; +1 focus and +10 skill to Smithing, Trade; +1 Calculating trait; +10 renown | `adulthood_investor_option` |
| campaign, sandbox |  | you led a successful manhunt. | +1 Cunning; +1 focus and +10 skill to Tactics, Leadership; +1 Calculating trait; +10 renown | `adulthood_manhunt_option` |
| campaign, sandbox |  | you treated people well. | +1 Social; +1 focus and +10 skill to Charm, Steward; +1 Generosity trait; +1 Honor trait; +1 Mercy trait; +5 renown | `adulthood_nice_person_option` |
| campaign, sandbox |  | you saved your city quarter from a fire. | +1 Cunning; +1 focus and +10 skill to Tactics, Leadership; +1 Calculating trait; +10 renown | `adulthood_saved_city_option` |
| campaign, sandbox |  | you saved your village from a flood. | +1 Cunning; +1 focus and +10 skill to Tactics, Leadership; +1 Valor trait; +10 renown | `adulthood_saved_village_option` |
| campaign, sandbox |  | you survived a siege. | +1 Control; +1 focus and +10 skill to Bow, Crossbow; +5 renown | `adulthood_siege_survivor_option` |
| campaign, sandbox |  | you invested some money in a workshop. | +1 Intelligence; +1 focus and +10 skill to Smithing, Trade; +1 Calculating trait; +10 renown | `adulthood_workshop_option` |

### Age

| Availability | Culture | Choice | Effects | Option id |
| --- | --- | --- | --- | --- |
| sandbox |  | 30 | +4 unspent focus; +2 unspent attribute | `age_selection_adult_option` |
| sandbox |  | 50 | +8 unspent focus; +4 unspent attribute | `age_selection_elder_option` |
| sandbox |  | 40 | +6 unspent focus; +3 unspent attribute | `age_selection_middle_age_option` |
| sandbox |  | 20 | +2 unspent focus; +1 unspent attribute | `age_selection_young_adult_option` |

### Escape

| Availability | Culture | Choice | Effects | Option id |
| --- | --- | --- | --- | --- |
| campaign |  | you drove them off with arrows. | +1 Control; +1 focus and +10 skill to Bow, Tactics | `escape_arrow_option` |
| campaign |  | you organized the travelers to break out. | +1 Social; +1 focus and +10 skill to Charm, Leadership | `escape_breakout_option` |
| campaign |  | you rode off on a fast horse. | +1 Endurance; +1 focus and +10 skill to Riding, Scouting | `escape_horse_option` |
| campaign |  | you threw up makeshift fortifications. | +1 Intelligence; +1 focus and +10 skill to Two Handed, Engineering | `escape_makeshift_fortification_option` |
| campaign |  | you subdued a raider. | +1 Vigor; +1 focus and +10 skill to One Handed, Athletics | `escape_subdued_raider_option` |
| campaign |  | you tricked the raiders. | +1 Cunning; +1 focus and +10 skill to Tactics, Roguery | `escape_tricked_option` |

## Outputs

- JSON: `Data\generated\character-creation-options.json`
- Report: `Data\generated\reports\character-creation-options.md`
