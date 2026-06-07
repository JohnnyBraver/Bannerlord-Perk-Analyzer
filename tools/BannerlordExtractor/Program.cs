using System.Reflection;
using System.Reflection.Emit;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Xml.Linq;
using System.Xml;

internal static class Program
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        WriteIndented = true,
        Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping,
    };

    public static int Main(string[] args)
    {
        try
        {
            if (args.Length == 0 || args[0] is "-h" or "--help")
            {
                PrintHelp();
                return 0;
            }

            var command = args[0];
            var options = CliOptions.Parse(args.Skip(1).ToArray());
            return command switch
            {
                "perks" => ExtractPerks(options),
                "banners" => ExtractBanners(options),
                "modifiers" => ExtractModifiers(options),
                "xp-methods" => ExtractXpMethods(options),
                "dump-il" => DumpIl(options),
                "find-methods" => FindMethods(options),
                "print-enum" => PrintEnum(options),
                "troops" => ExtractTroops(options),
                _ => Fail($"Unknown command: {command}"),
            };
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Unhandled exception: {ex}");
            if (ex.InnerException != null)
            {
                Console.Error.WriteLine($"Inner Exception: {ex.InnerException}");
            }
            return 1;
        }
    }

    private static void PrintHelp()
    {
        Console.WriteLine("BannerlordExtractor");
        Console.WriteLine();
        Console.WriteLine("Commands:");
        Console.WriteLine("  perks --game-root <path> --output <json>");
        Console.WriteLine("  banners --game-root <path> --output <json> [--include-mp]");
        Console.WriteLine("  modifiers --game-root <path> --output <json>");
        Console.WriteLine("  xp-methods --game-root <path> --json-output <json> [--assembly <name>] [--include-il] [--deep-scan-callers] [--include-contracts]");
        Console.WriteLine("  dump-il --game-root <path> --assembly <name> --type <full type> --method <name> [--output <txt>]");
        Console.WriteLine("  find-methods --game-root <path> --query <text> [--assembly <name>] [--all-game-assemblies] [--include-il] [--output <json>]");
        Console.WriteLine("  print-enum --game-root <path>");
        Console.WriteLine("  troops --game-root <path> --output <json>");
    }

    private static int PrintEnum(CliOptions options)
    {
        var gameRoot = options.RequiredPath("game-root");
        var bin = ResolveGameBin(gameRoot);
        var objectSystemDll = Path.Combine(bin, "TaleWorlds.ObjectSystem.dll");
        AddAssemblyResolver(ResolveAssemblySearchDirs(gameRoot));
        
        var objectSystemAsm = Assembly.LoadFrom(objectSystemDll);
        var xmlInfoType = objectSystemAsm.GetType("TaleWorlds.ObjectSystem.MbObjectXmlInformation", true);

        Console.WriteLine("=== MbObjectXmlInformation Fields & Properties ===");
        foreach (var f in xmlInfoType.GetFields(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static))
        {
            Console.WriteLine($"Field: {f.FieldType.Name} {f.Name}");
        }
        foreach (var p in xmlInfoType.GetProperties(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static))
        {
            Console.WriteLine($"Prop: {p.PropertyType.Name} {p.Name}");
        }

        Console.WriteLine("=== MbObjectXmlInformation Constructors ===");
        foreach (var c in xmlInfoType.GetConstructors(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance))
        {
            Console.WriteLine($"Ctor: ({string.Join(", ", c.GetParameters().Select(p => $"{p.ParameterType.Name} {p.Name}"))})");
        }

        return 0;
    }

    private static int Fail(string message)
    {
        Console.Error.WriteLine(message);
        return 1;
    }

    private static int ExtractPerks(CliOptions options)
    {
        var gameRoot = options.RequiredPath("game-root");
        var output = options.RequiredPath("output");
        var bin = ResolveGameBin(gameRoot);
        var campaignDll = Path.Combine(bin, "TaleWorlds.CampaignSystem.dll");
        var coreDll = Path.Combine(bin, "TaleWorlds.Core.dll");
        RequireFile(campaignDll, "Could not find TaleWorlds.CampaignSystem.dll.");
        RequireFile(coreDll, "Could not find TaleWorlds.Core.dll.");
        AddAssemblyResolver(ResolveAssemblySearchDirs(gameRoot));

        var campaignAsm = Assembly.LoadFrom(campaignDll);
        _ = Assembly.LoadFrom(coreDll);
        var defaultPerksType = campaignAsm.GetType("TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultPerks", throwOnError: true)
            ?? throw new InvalidOperationException("Could not load DefaultPerks type.");
        var register = defaultPerksType.GetMethod("RegisterAll", BindingFlags.NonPublic | BindingFlags.Instance)
            ?? throw new InvalidOperationException("Could not find DefaultPerks.RegisterAll.");
        var initialize = defaultPerksType.GetMethod("InitializeAll", BindingFlags.NonPublic | BindingFlags.Instance)
            ?? throw new InvalidOperationException("Could not find DefaultPerks.InitializeAll.");

        var createMap = GetPerkCreateMap(IlReader.ReadInstructions(register));
        var perks = GetPerkDefinitions(IlReader.ReadInstructions(initialize), createMap)
            .OrderBy(perk => perk.Skill)
            .ThenBy(perk => perk.Level)
            .ThenBy(perk => perk.Name)
            .Select(ConvertPerkToRawObject)
            .ToList();

        WriteJson(output, perks);
        Console.WriteLine($"Raw perks written: {perks.Count}");
        Console.WriteLine($"Output: {output}");
        return 0;
    }

    private static int ExtractBanners(CliOptions options)
    {
        var gameRoot = options.RequiredPath("game-root");
        var output = options.RequiredPath("output");
        var bin = ResolveGameBin(gameRoot);
        var coreDll = Path.Combine(bin, "TaleWorlds.Core.dll");
        RequireFile(coreDll, "Could not find TaleWorlds.Core.dll.");
        AddAssemblyResolver(ResolveAssemblySearchDirs(gameRoot));

        var coreAsm = Assembly.LoadFrom(coreDll);
        var defaultBannerEffectsType = coreAsm.GetType("TaleWorlds.Core.DefaultBannerEffects", throwOnError: true)
            ?? throw new InvalidOperationException("Could not load DefaultBannerEffects type.");
        var register = defaultBannerEffectsType.GetMethod("RegisterAll", BindingFlags.NonPublic | BindingFlags.Instance)
            ?? throw new InvalidOperationException("Could not find DefaultBannerEffects.RegisterAll.");
        var initialize = defaultBannerEffectsType.GetMethod("InitializeAll", BindingFlags.NonPublic | BindingFlags.Instance)
            ?? throw new InvalidOperationException("Could not find DefaultBannerEffects.InitializeAll.");

        var stringIdsByField = GetBannerEffectStringIds(IlReader.ReadInstructions(register));
        var effects = GetBannerEffectDefinitions(IlReader.ReadInstructions(initialize), stringIdsByField)
            .OrderBy(effect => effect.StringId)
            .ToList();
        var effectsByStringId = effects.ToDictionary(effect => effect.StringId, StringComparer.OrdinalIgnoreCase);
        var includeMultiplayer = options.Has("include-mp");
        var bannerXmlPaths = FindBannerXmlPaths(gameRoot, includeMultiplayer);
        var items = bannerXmlPaths
            .SelectMany(path => ReadBannerItems(gameRoot, path, effectsByStringId))
            .OrderBy(item => item.EffectStringId)
            .ThenBy(item => item.BannerLevel)
            .ThenBy(item => item.Id)
            .ToList();

        var payload = new Dictionary<string, object?>
        {
            ["generated_at"] = DateTimeOffset.Now.ToString("o"),
            ["inputs"] = new Dictionary<string, object?>
            {
                ["game_root"] = "<local Bannerlord install>",
                ["core_assembly"] = SanitizeLocalPath(coreDll, gameRoot),
                ["banner_xml"] = bannerXmlPaths.Select(path => SanitizeLocalPath(path, gameRoot)).ToList(),
            },
            ["effect_definitions"] = effects.Select(effect => new Dictionary<string, object?>
            {
                ["string_id"] = effect.StringId,
                ["field"] = effect.Field,
                ["name_raw"] = effect.NameRaw,
                ["name"] = effect.Name,
                ["description_raw"] = effect.DescriptionRaw,
                ["description"] = effect.Description,
                ["increment_type"] = effect.IncrementType,
                ["increment_value"] = effect.IncrementValue,
                ["tiers"] = effect.Tiers.Select(tier => new Dictionary<string, object?>
                {
                    ["level"] = tier.Level,
                    ["bonus"] = tier.Bonus,
                    ["bonus_percent"] = tier.Bonus * 100.0,
                    ["display_bonus"] = FormatPercent(tier.Bonus),
                    ["description"] = FormatBannerDescription(effect.Description, tier.Bonus),
                }).ToList(),
            }).ToList(),
            ["items"] = items.Select(item => new Dictionary<string, object?>
            {
                ["id"] = item.Id,
                ["name_raw"] = item.NameRaw,
                ["name"] = item.Name,
                ["culture"] = item.Culture,
                ["module"] = item.Module,
                ["source"] = item.Source,
                ["banner_level"] = item.BannerLevel,
                ["effect"] = item.EffectStringId,
                ["effect_name"] = item.EffectName,
                ["effect_description"] = item.EffectDescription,
                ["bonus"] = item.Bonus,
                ["bonus_percent"] = item.Bonus * 100.0,
                ["display_bonus"] = FormatPercent(item.Bonus),
                ["display_effect"] = FormatBannerDescription(item.EffectDescription, item.Bonus),
                ["weapon_class"] = item.WeaponClass,
                ["mesh"] = item.Mesh,
                ["prefab"] = item.Prefab,
                ["weight"] = item.Weight,
            }).ToList(),
            ["groups"] = items
                .GroupBy(item => item.EffectStringId, StringComparer.OrdinalIgnoreCase)
                .OrderBy(group => group.Key)
                .Select(group => new Dictionary<string, object?>
                {
                    ["effect"] = group.Key,
                    ["effect_name"] = group.First().EffectName,
                    ["items"] = group
                        .OrderBy(item => item.BannerLevel)
                        .ThenBy(item => item.Id)
                        .Select(item => item.Id)
                        .ToList(),
                    ["tiers"] = group
                        .GroupBy(item => item.BannerLevel)
                        .OrderBy(tierGroup => tierGroup.Key)
                        .Select(tierGroup => new Dictionary<string, object?>
                        {
                            ["level"] = tierGroup.Key,
                            ["bonus"] = tierGroup.First().Bonus,
                            ["bonus_percent"] = tierGroup.First().Bonus * 100.0,
                            ["display_bonus"] = FormatPercent(tierGroup.First().Bonus),
                            ["item_count"] = tierGroup.Count(),
                            ["items"] = tierGroup.Select(item => item.Id).OrderBy(id => id).ToList(),
                        })
                        .ToList(),
                })
                .ToList(),
        };

        WriteJson(output, payload);
        Console.WriteLine($"Banner effects extracted: {effects.Count}");
        Console.WriteLine($"Banner items extracted: {items.Count}");
        Console.WriteLine($"Output: {output}");
        return 0;
    }

    private static int ExtractModifiers(CliOptions options)
    {
        var gameRoot = options.RequiredPath("game-root");
        var output = options.RequiredPath("output");

        var modules = Path.Combine(Path.GetFullPath(gameRoot), "Modules");
        if (!Directory.Exists(modules))
        {
            return Fail($"Could not find Modules directory under game root: {modules}");
        }

        var modifiersPath = Path.Combine(modules, "Native", "ModuleData", "item_modifiers.xml");
        if (!File.Exists(modifiersPath))
        {
            modifiersPath = Directory.GetFiles(modules, "item_modifiers.xml", SearchOption.AllDirectories).FirstOrDefault();
        }
        if (string.IsNullOrEmpty(modifiersPath) || !File.Exists(modifiersPath))
        {
            return Fail("Could not find item_modifiers.xml.");
        }

        var groupsPath = Path.Combine(modules, "Native", "ModuleData", "item_modifiers_groups.xml");
        if (!File.Exists(groupsPath))
        {
            groupsPath = Directory.GetFiles(modules, "item_modifiers_groups.xml", SearchOption.AllDirectories).FirstOrDefault();
        }
        if (string.IsNullOrEmpty(groupsPath) || !File.Exists(groupsPath))
        {
            return Fail("Could not find item_modifiers_groups.xml.");
        }

        // Parse groups
        var groupsDoc = XDocument.Load(groupsPath);
        var groups = new List<ModifierGroupDefinition>();
        foreach (var groupEl in groupsDoc.Descendants("ItemModifierGroup"))
        {
            groups.Add(new ModifierGroupDefinition
            {
                Id = Attr(groupEl, "id"),
                NoModifierLootScore = ParseInt(Attr(groupEl, "no_modifier_loot_score")),
                NoModifierProductionScore = ParseInt(Attr(groupEl, "no_modifier_production_score")),
                Modifiers = new List<ModifierInGroup>()
            });
        }
        var groupsById = groups.ToDictionary(g => g.Id, StringComparer.OrdinalIgnoreCase);

        // Parse modifiers
        var modifiersDoc = XDocument.Load(modifiersPath);
        var modifiers = new List<ItemModifierDefinition>();

        foreach (var modEl in modifiersDoc.Descendants("ItemModifier"))
        {
            var rawGroup = Attr(modEl, "modifier_group");
            var groupName = rawGroup.Replace("ItemModifierGroup.", "", StringComparison.OrdinalIgnoreCase);

            var mod = new ItemModifierDefinition
            {
                Id = Attr(modEl, "id"),
                NameRaw = Attr(modEl, "name"),
                Name = StripLocPrefix(Attr(modEl, "name")),
                ModifierGroup = groupName,
                PriceFactor = ParseDouble(Attr(modEl, "price_factor")),
                Quality = Attr(modEl, "quality"),
                LootDropScore = ParseInt(Attr(modEl, "loot_drop_score")),
                ProductionDropScore = ParseInt(Attr(modEl, "production_drop_score"))
            };

            var metadataKeys = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
            {
                "id", "name", "modifier_group", "price_factor", "quality", "loot_drop_score", "production_drop_score"
            };

            foreach (var attr in modEl.Attributes())
            {
                if (!metadataKeys.Contains(attr.Name.LocalName))
                {
                    mod.Stats[attr.Name.LocalName] = attr.Value;
                }
            }

            modifiers.Add(mod);

            if (groupsById.TryGetValue(groupName, out var group))
            {
                group.Modifiers.Add(new ModifierInGroup
                {
                    Id = mod.Id,
                    LootDropScore = mod.LootDropScore,
                    ProductionDropScore = mod.ProductionDropScore
                });
            }
        }

        var payload = new Dictionary<string, object?>
        {
            ["generated_at"] = DateTimeOffset.Now.ToString("o"),
            ["inputs"] = new Dictionary<string, object?>
            {
                ["game_root"] = "<local Bannerlord install>",
                ["item_modifiers_xml"] = SanitizeLocalPath(modifiersPath, gameRoot),
                ["item_modifiers_groups_xml"] = SanitizeLocalPath(groupsPath, gameRoot)
            },
            ["modifiers"] = modifiers,
            ["groups"] = groups
        };

        WriteJson(output, payload);
        Console.WriteLine($"Extracted {modifiers.Count} modifiers and {groups.Count} modifier groups.");
        Console.WriteLine($"Output: {output}");
        return 0;
    }

    private static readonly string[] SlotNames = new[]
    {
        "Weapon0",
        "Weapon1",
        "Weapon2",
        "Weapon3",
        "ExtraWeaponSlot",
        "Head",
        "Body",
        "Leg",
        "Gloves",
        "Cape",
        "Horse",
        "HorseHarness"
    };

    private static int ExtractTroops(CliOptions options)
    {
        var gameRoot = options.RequiredPath("game-root");
        var output = options.RequiredPath("output");
        var bin = ResolveGameBin(gameRoot);

        var coreDll = Path.Combine(bin, "TaleWorlds.Core.dll");
        var campaignDll = Path.Combine(bin, "TaleWorlds.CampaignSystem.dll");
        var objectSystemDll = Path.Combine(bin, "TaleWorlds.ObjectSystem.dll");
        var moduleManagerDll = Path.Combine(bin, "TaleWorlds.ModuleManager.dll");

        RequireFile(coreDll, "Could not find TaleWorlds.Core.dll.");
        RequireFile(campaignDll, "Could not find TaleWorlds.CampaignSystem.dll.");
        RequireFile(objectSystemDll, "Could not find TaleWorlds.ObjectSystem.dll.");
        RequireFile(moduleManagerDll, "Could not find TaleWorlds.ModuleManager.dll.");

        AddAssemblyResolver(ResolveAssemblySearchDirs(gameRoot));

        var coreAsm = Assembly.LoadFrom(coreDll);
        var campaignAsm = Assembly.LoadFrom(campaignDll);
        var objectSystemAsm = Assembly.LoadFrom(objectSystemDll);
        var moduleManagerAsm = Assembly.LoadFrom(moduleManagerDll);

        // Initialize ModuleHelper & active modules
        Console.WriteLine("Initializing ModuleHelper and active modules...");
        try
        {
            var moduleHelperType = moduleManagerAsm.GetType("TaleWorlds.ModuleManager.ModuleHelper", true);
            var moduleInfoType = moduleManagerAsm.GetType("TaleWorlds.ModuleManager.ModuleInfo", true);
            
            var loadedModulesField = moduleHelperType.GetField("_loadedModules", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static);
            if (loadedModulesField != null)
            {
                var dictType = typeof(Dictionary<,>).MakeGenericType(typeof(string), moduleInfoType);
                var dictInstance = Activator.CreateInstance(dictType);
                loadedModulesField.SetValue(null, dictInstance);
                Console.WriteLine("ModuleHelper._loadedModules initialized to empty dictionary.");
                
                var initializeSingleModuleMethod = moduleHelperType.GetMethod("InitializeSingleModule", BindingFlags.Public | BindingFlags.Static);
                if (initializeSingleModuleMethod != null)
                {
                    var modDir = Path.Combine(gameRoot, "Modules");
                    if (Directory.Exists(modDir))
                    {
                        var loadedModulesDict = (System.Collections.IDictionary)dictInstance;
                        foreach (var dir in Directory.GetDirectories(modDir))
                        {
                            var moduleInfo = initializeSingleModuleMethod.Invoke(null, new object[] { dir });
                            if (moduleInfo != null)
                            {
                                var moduleIdProp = moduleInfoType.GetProperty("Id", BindingFlags.Public | BindingFlags.Instance);
                                var id = moduleIdProp?.GetValue(moduleInfo)?.ToString();
                                if (!string.IsNullOrEmpty(id))
                                {
                                    // Set IsActive = true and IsSelected = true
                                    SetPrivateFieldOrProperty(moduleInfo, "IsActive", true);
                                    SetPrivateFieldOrProperty(moduleInfo, "IsSelected", true);
                                    
                                    loadedModulesDict[id.ToLowerInvariant()] = moduleInfo;
                                    Console.WriteLine($"Loaded module: {id} from {dir}");
                                }
                            }
                        }
                    }
                }
            }
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Error initializing ModuleHelper/Modules: {ex.Message}");
            if (ex.InnerException != null)
            {
                Console.Error.WriteLine($"Inner Exception: {ex.InnerException.Message}");
            }
        }

        // Initialize GameTexts
        Console.WriteLine("Initializing GameTexts...");
        try
        {
            var gameTextsType = coreAsm.GetType("TaleWorlds.Core.GameTexts", true);
            var gameTextManagerType = coreAsm.GetType("TaleWorlds.Core.GameTextManager", true);
            var gameTextManagerInstance = Activator.CreateInstance(gameTextManagerType);
            
            try
            {
                var loadDefaultTextsMethod = gameTextManagerType.GetMethod("LoadDefaultTexts", BindingFlags.Public | BindingFlags.Instance);
                if (loadDefaultTextsMethod != null)
                {
                    loadDefaultTextsMethod.Invoke(gameTextManagerInstance, null);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Warning: Failed to load default texts: {ex.Message}");
            }
            
            var initializeMethod = gameTextsType.GetMethod("Initialize", BindingFlags.Public | BindingFlags.Static);
            if (initializeMethod != null)
            {
                initializeMethod.Invoke(null, new[] { gameTextManagerInstance });
                Console.WriteLine("GameTexts initialized successfully.");
            }
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Error initializing GameTexts: {ex.Message}");
        }

        var objectManagerType = objectSystemAsm.GetType("TaleWorlds.ObjectSystem.MBObjectManager", true)
            ?? throw new InvalidOperationException("Could not load MBObjectManager type.");
        var initMethod = objectManagerType.GetMethod("Init", BindingFlags.Public | BindingFlags.Static)
            ?? throw new InvalidOperationException("Could not find MBObjectManager.Init.");
        var loadXmlMethod = objectManagerType.GetMethod("LoadXml", new[] { typeof(XmlDocument), typeof(bool) })
            ?? throw new InvalidOperationException("Could not find MBObjectManager.LoadXml.");

        Console.WriteLine("Initializing MBObjectManager...");
        var manager = initMethod.Invoke(null, null);
        if (manager == null)
        {
            return Fail("Failed to initialize MBObjectManager instance.");
        }

        // Types
        var monsterType = coreAsm.GetType("TaleWorlds.Core.Monster", true);
        var bodyPropertyType = coreAsm.GetType("TaleWorlds.Core.MBBodyProperty", true);
        var itemType = coreAsm.GetType("TaleWorlds.Core.ItemObject", true);
        var itemModifierType = coreAsm.GetType("TaleWorlds.Core.ItemModifier", true);
        var itemModifierGroupType = coreAsm.GetType("TaleWorlds.Core.ItemModifierGroup", true);
        var characterAttributeType = coreAsm.GetType("TaleWorlds.Core.CharacterAttribute", true);
        var skillType = coreAsm.GetType("TaleWorlds.Core.SkillObject", true);
        var itemCategoryType = coreAsm.GetType("TaleWorlds.Core.ItemCategory", true);
        var craftingPieceType = coreAsm.GetType("TaleWorlds.Core.CraftingPiece", true);
        var craftingTemplateType = coreAsm.GetType("TaleWorlds.Core.CraftingTemplate", true);
        var weaponDescType = coreAsm.GetType("TaleWorlds.Core.WeaponDescription", true);
        var charType = campaignAsm.GetType("TaleWorlds.CampaignSystem.CharacterObject", true);
        var cultureType = campaignAsm.GetType("TaleWorlds.CampaignSystem.CultureObject", true);
        var siegeEngineType = coreAsm.GetType("TaleWorlds.Core.SiegeEngineType", true);
        var equipmentType = coreAsm.GetType("TaleWorlds.Core.Equipment", true);
        var equipmentElementType = coreAsm.GetType("TaleWorlds.Core.EquipmentElement", true);
        var equipmentRosterType = coreAsm.GetType("TaleWorlds.Core.MBEquipmentRoster", true);
        var skillSetType = coreAsm.GetType("TaleWorlds.Core.MBCharacterSkills", true);
        var bannerEffectType = coreAsm.GetType("TaleWorlds.Core.BannerEffect", true);
        var traitType = campaignAsm.GetType("TaleWorlds.CampaignSystem.CharacterDevelopment.TraitObject", true);

        var gameTypeType = coreAsm.GetType("TaleWorlds.Core.GameType", true);
        var gameManagerBaseType = coreAsm.GetType("TaleWorlds.Core.GameManagerBase", true);
        var gameType = coreAsm.GetType("TaleWorlds.Core.Game", true);

        Console.WriteLine("Registering types...");
        RegisterType(manager, monsterType, "Monster", "Monsters", 2U, true, false);
        RegisterType(manager, bodyPropertyType, "BodyProperty", "BodyProperties", 3U, true, false);
        RegisterType(manager, itemType, "Item", "Items", 4U, true, false);
        RegisterType(manager, itemModifierType, "ItemModifier", "ItemModifiers", 6U, true, false);
        RegisterType(manager, itemModifierGroupType, "ItemModifierGroup", "ItemModifierGroups", 7U, true, false);
        RegisterType(manager, characterAttributeType, "CharacterAttribute", "CharacterAttributes", 8U, true, false);
        RegisterType(manager, skillType, "Skill", "Skills", 9U, true, false);
        RegisterType(manager, itemCategoryType, "ItemCategory", "ItemCategories", 10U, true, false);
        RegisterType(manager, craftingPieceType, "CraftingPiece", "CraftingPieces", 11U, true, false);
        RegisterType(manager, craftingTemplateType, "CraftingTemplate", "CraftingTemplates", 12U, true, false);
        RegisterType(manager, weaponDescType, "WeaponDescription", "WeaponDescriptions", 14U, true, false);
        RegisterType(manager, charType, "NPCCharacter", "NPCCharacters", 16U, true, false);
        RegisterType(manager, cultureType, "Culture", "SPCultures", 17U, true, false);
        RegisterType(manager, traitType, "Trait", "Traits", 32U, true, false);
        RegisterType(manager, siegeEngineType, "SiegeEngineType", "SiegeEngineTypes", 50U, true, false);
        RegisterType(manager, equipmentRosterType, "EquipmentRoster", "EquipmentRosters", 51U, true, false);
        RegisterType(manager, skillSetType, "SkillSet", "SkillSets", 52U, true, false);
        RegisterType(manager, bannerEffectType, "BannerEffect", "BannerEffects", 53U, true, false);
        Console.WriteLine("Types registered.");

        Console.WriteLine("Initializing XmlResource...");
        try
        {
            var xmlResourceType = objectSystemAsm.GetType("TaleWorlds.ObjectSystem.XmlResource", true);
            var xmlInfoType = objectSystemAsm.GetType("TaleWorlds.ObjectSystem.MbObjectXmlInformation", true);

            var xmlInfoListType = typeof(List<>).MakeGenericType(xmlInfoType);
            var xmlInfoListInstance = (System.Collections.IList)Activator.CreateInstance(xmlInfoListType)!;

            var emptyStringList = new List<string>();

            var xmlInfoCtor = xmlInfoType.GetConstructor(new[] { typeof(string), typeof(string), typeof(string), typeof(List<string>) })
                ?? throw new InvalidOperationException("Could not find MbObjectXmlInformation constructor.");

            var info1 = xmlInfoCtor.Invoke(new object[] { "CoreParameters", "managed_core_parameters", "Native", emptyStringList });
            var info2 = xmlInfoCtor.Invoke(new object[] { "SiegeEngines", "siege_engine_types", "Native", emptyStringList });

            xmlInfoListInstance.Add(info1);
            xmlInfoListInstance.Add(info2);

            var initializeXmlInformationListMethod = xmlResourceType.GetMethod("InitializeXmlInformationList", BindingFlags.Public | BindingFlags.Static)
                ?? throw new InvalidOperationException("Could not find XmlResource.InitializeXmlInformationList method.");

            initializeXmlInformationListMethod.Invoke(null, new object[] { xmlInfoListInstance });
            Console.WriteLine("XmlResource initialized successfully.");

            var xmlInformationListField = xmlResourceType.GetField("XmlInformationList", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static);
            var currentList = xmlInformationListField?.GetValue(null) as System.Collections.IEnumerable;
            if (currentList != null)
            {
                int count = 0;
                foreach (var item in currentList) count++;
                Console.WriteLine($"Verify: XmlResource.XmlInformationList count = {count}");
            }
            else
            {
                Console.WriteLine("Verify: XmlResource.XmlInformationList is NULL!");
            }

            // Diagnostics
            if (currentList != null)
            {
                var moduleHelperType = moduleManagerAsm.GetType("TaleWorlds.ModuleManager.ModuleHelper", true);
                var isNativeActive = moduleHelperType.GetMethod("IsModuleActive", BindingFlags.Public | BindingFlags.Static)
                    ?.Invoke(null, new object[] { "Native" });
                Console.WriteLine($"Diagnostic: IsModuleActive(\"Native\") = {isNativeActive}");

                var getXmlPathMethod = moduleHelperType.GetMethod("GetXmlPath", BindingFlags.Public | BindingFlags.Static);
                var xmlPath = getXmlPathMethod?.Invoke(null, new object[] { "Native", "managed_core_parameters" })?.ToString();
                Console.WriteLine($"Diagnostic: GetXmlPath(\"Native\", \"managed_core_parameters\") = {xmlPath}");
                if (xmlPath != null)
                {
                    Console.WriteLine($"Diagnostic: File.Exists(xmlPath) = {File.Exists(xmlPath)}");
                }

                foreach (var item in currentList)
                {
                    var itemId = xmlInfoType.GetField("Id")?.GetValue(item)?.ToString();
                    var itemName = xmlInfoType.GetField("Name")?.GetValue(item)?.ToString();
                    var itemModuleName = xmlInfoType.GetField("ModuleName")?.GetValue(item)?.ToString();
                    var itemGameTypes = xmlInfoType.GetField("GameTypesIncluded")?.GetValue(item) as System.Collections.IEnumerable;
                    int gtCount = 0;
                    if (itemGameTypes != null) foreach (var gt in itemGameTypes) gtCount++;
                    Console.WriteLine($"Diagnostic XmlInfo: Id={itemId}, Name={itemName}, ModuleName={itemModuleName}, GameTypesCount={gtCount}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Error initializing XmlResource: {ex.Message}");
            if (ex.InnerException != null)
            {
                Console.Error.WriteLine($"Inner Exception: {ex.InnerException.Message}");
            }
        }

        Console.WriteLine("Initializing Game.Current with mocks...");
        object? gameInstance = null;
        try
        {
            var mockGameType = CreateMockSubclass(gameTypeType, "MockGameType");
            var mockGameManager = CreateMockSubclass(gameManagerBaseType, "MockGameManager");

            var dummyGameTypeObj = Activator.CreateInstance(mockGameType);
            var dummyGameManagerObj = Activator.CreateInstance(mockGameManager);

            var ctor = gameType.GetConstructor(
                BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic,
                null,
                new[] { gameTypeType, gameManagerBaseType, manager.GetType() },
                null
            ) ?? throw new InvalidOperationException("Game constructor not found.");

            gameInstance = ctor.Invoke(new object[] { dummyGameTypeObj, dummyGameManagerObj, manager });
            Console.WriteLine($"Game.Current set to instance: {gameInstance}");

            // Set BasicModels on gameInstance
            try
            {
                var basicGameModelsType = coreAsm.GetType("TaleWorlds.Core.BasicGameModels", true);
                var gameModelType = coreAsm.GetType("TaleWorlds.Core.GameModel", true);
                var listType = typeof(List<>).MakeGenericType(gameModelType);
                var emptyList = Activator.CreateInstance(listType);

                var basicModelsInstance = Activator.CreateInstance(basicGameModelsType, new object[] { emptyList });
                Console.WriteLine("BasicGameModels instance created.");

                var defaultRidingModelType = coreAsm.GetType("TaleWorlds.Core.DefaultRidingModel", true);
                var defaultItemCategorySelectorType = coreAsm.GetType("TaleWorlds.Core.DefaultItemCategorySelector", true);
                var defaultItemValueModelType = coreAsm.GetType("TaleWorlds.Core.DefaultItemValueModel", true);

                var ridingModelInstance = CreateInstanceSafe(defaultRidingModelType);
                var categorySelectorInstance = CreateInstanceSafe(defaultItemCategorySelectorType);
                var itemValueModelInstance = CreateInstanceSafe(defaultItemValueModelType);

                SetPrivateFieldOrProperty(basicModelsInstance, "RidingModel", ridingModelInstance);
                SetPrivateFieldOrProperty(basicModelsInstance, "ItemCategorySelector", categorySelectorInstance);
                SetPrivateFieldOrProperty(basicModelsInstance, "ItemValueModel", itemValueModelInstance);

                SetPrivateFieldOrProperty(gameInstance, "BasicModels", basicModelsInstance);
                Console.WriteLine("BasicModels set successfully on gameInstance.");
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"Error setting up BasicModels: {ex.Message}");
                if (ex.InnerException != null)
                {
                    Console.Error.WriteLine($"Inner Exception: {ex.InnerException.Message}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Error setting up Game.Current: {ex.Message}");
            if (ex.InnerException != null)
            {
                Console.Error.WriteLine($"Inner Exception: {ex.InnerException.Message}");
                Console.Error.WriteLine($"Stack Trace:\n{ex.InnerException.StackTrace}");
            }
        }

        Console.WriteLine("Instantiating default game objects...");
        var defaultTypes = new[]
        {
            ("DefaultCharacterAttributes", coreAsm.GetType("TaleWorlds.Core.DefaultCharacterAttributes", true)),
            ("DefaultSkills", coreAsm.GetType("TaleWorlds.Core.DefaultSkills", true)),
            ("DefaultItemCategories", coreAsm.GetType("TaleWorlds.Core.DefaultItemCategories", true)),
            ("DefaultBannerEffects", coreAsm.GetType("TaleWorlds.Core.DefaultBannerEffects", true)),
            ("DefaultSiegeEngineTypes", coreAsm.GetType("TaleWorlds.Core.DefaultSiegeEngineTypes", true))
        };

        foreach (var dt in defaultTypes)
        {
            try
            {
                var instance = CreateInstanceSafe(dt.Item2);
                Console.WriteLine($"Instantiated: {dt.Item1}");
                if (gameInstance != null)
                {
                    SetPrivateFieldOrProperty(gameInstance, dt.Item1, instance);
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"Error instantiating/setting {dt.Item1}: {ex.Message}");
                if (ex.InnerException != null)
                {
                    Console.Error.WriteLine($"Inner Exception: {ex.InnerException.Message}");
                    Console.Error.WriteLine($"Stack Trace:\n{ex.InnerException.StackTrace}");
                }
            }
        }
        Console.WriteLine("Default game objects instantiation pass finished.");

        Console.WriteLine("Initializing Campaign.Current...");
        try
        {
            var campaignType = campaignAsm.GetType("TaleWorlds.CampaignSystem.Campaign", true);
            var campaignGameModeType = campaignAsm.GetType("TaleWorlds.CampaignSystem.CampaignGameMode", true);
            var defaultTraitsType = campaignAsm.GetType("TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultTraits", true);

            var gameModeVal = Enum.ToObject(campaignGameModeType, 0);
            var campaignInstance = Activator.CreateInstance(campaignType, new object[] { gameModeVal });
            Console.WriteLine($"Campaign instance created: {campaignInstance}");

            var currentSetter = campaignType.GetMethod("set_Current", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static);
            if (currentSetter != null)
            {
                currentSetter.Invoke(null, new[] { campaignInstance });
                Console.WriteLine("Campaign.Current set successfully.");
            }

            var defaultTraitsInstance = CreateInstanceSafe(defaultTraitsType);
            Console.WriteLine("DefaultTraits instantiated successfully.");
            if (campaignInstance != null)
            {
                SetPrivateFieldOrProperty(campaignInstance, "DefaultTraits", defaultTraitsInstance);
            }

            // Setup Campaign models
            try
            {
                var gameModelType = coreAsm.GetType("TaleWorlds.Core.GameModel", true);
                var listType = typeof(List<>).MakeGenericType(gameModelType);
                var listInstance = (System.Collections.IList)Activator.CreateInstance(listType)!;

                var defaultCharacterStatsModelType = campaignAsm.GetType("TaleWorlds.CampaignSystem.GameComponents.DefaultCharacterStatsModel", true);
                var characterStatsModelInstance = CreateInstanceSafe(defaultCharacterStatsModelType);
                listInstance.Add(characterStatsModelInstance);
                Console.WriteLine("DefaultCharacterStatsModel instantiated and added to list.");

                var gameModelsType = campaignAsm.GetType("TaleWorlds.CampaignSystem.GameModels", true);
                var gameModelsInstance = Activator.CreateInstance(gameModelsType, new object[] { listInstance });
                Console.WriteLine("GameModels instance created.");
                SetPrivateFieldOrProperty(gameModelsInstance, "CharacterStatsModel", characterStatsModelInstance);

                if (campaignInstance != null)
                {
                    SetPrivateFieldOrProperty(campaignInstance, "_gameModels", gameModelsInstance);
                    Console.WriteLine("Campaign models initialized successfully.");
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"Error setting up Campaign models: {ex.Message}");
                if (ex.InnerException != null)
                {
                    Console.Error.WriteLine($"Inner Exception: {ex.InnerException.Message}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Error setting up Campaign.Current: {ex.Message}");
            if (ex.InnerException != null)
            {
                Console.Error.WriteLine($"Inner Exception: {ex.InnerException.Message}");
                Console.Error.WriteLine($"Stack Trace:\n{ex.InnerException.StackTrace}");
            }
        }

        var modulesDir = Path.Combine(gameRoot, "Modules");
        var relativeXmlPaths = new[]
        {
            "Native/ModuleData/skills.xml",
            "Native/ModuleData/monsters.xml",
            "Native/ModuleData/weapon_descriptions.xml",
            "Native/ModuleData/crafting_pieces.xml",
            "Native/ModuleData/crafting_templates.xml",
            "Native/ModuleData/item_modifiers.xml",
            "Native/ModuleData/item_modifiers_groups.xml",
            "Native/ModuleData/native_skill_sets.xml",
            "Native/ModuleData/native_equipment_sets.xml",
            "SandBoxCore/ModuleData/spcultures.xml",
            "SandBoxCore/ModuleData/sandboxcore_skill_sets.xml",
            "SandBoxCore/ModuleData/sandboxcore_equipment_sets.xml",
            "SandBoxCore/ModuleData/items/weapons.xml",
            "SandBoxCore/ModuleData/items/arm_armors.xml",
            "SandBoxCore/ModuleData/items/body_armors.xml",
            "SandBoxCore/ModuleData/items/head_armors.xml",
            "SandBoxCore/ModuleData/items/leg_armors.xml",
            "SandBoxCore/ModuleData/items/shoulder_armors.xml",
            "SandBoxCore/ModuleData/items/horses_and_others.xml",
            "SandBoxCore/ModuleData/items/shields.xml",
            "SandBoxCore/ModuleData/spnpccharactertemplates.xml",
            "SandBoxCore/ModuleData/spnpccharacters.xml",
            "SandBox/ModuleData/sandbox_skill_sets.xml",
            "SandBox/ModuleData/sandbox_equipment_sets.xml",
            "SandBox/ModuleData/spgenericcharacters.xml",
            "SandBox/ModuleData/spspecialcharacters.xml",
            "StoryMode/ModuleData/story_mode_characters.xml"
        };

        Console.WriteLine("Loading XML files...");
        foreach (var relPath in relativeXmlPaths)
        {
            var path = Path.Combine(modulesDir, relPath.Replace('/', Path.DirectorySeparatorChar));
            LoadXmlFile(manager, loadXmlMethod, path);
        }

        Console.WriteLine("Querying characters database...");
        var getObjectsMethod = objectManagerType.GetMethod("GetObjectTypeList", BindingFlags.Public | BindingFlags.Instance)
            ?? throw new InvalidOperationException("Could not find GetObjectTypeList method.");

        var concreteGetObjects = getObjectsMethod.MakeGenericMethod(charType);
        var charList = (System.Collections.IEnumerable)concreteGetObjects.Invoke(manager, null);

        var concreteGetSkills = getObjectsMethod.MakeGenericMethod(skillType);
        var skillList = (System.Collections.IEnumerable)concreteGetSkills.Invoke(manager, null);

        var troopsData = new List<Dictionary<string, object?>>();

        // Properties we need from character
        var idProp = GetPropertySafe(charType, "StringId") ?? throw new InvalidOperationException("Could not find StringId property.");
        var nameProp = GetPropertySafe(charType, "Name") ?? throw new InvalidOperationException("Could not find Name property.");
        var tierProp = GetPropertySafe(charType, "Tier") ?? throw new InvalidOperationException("Could not find Tier property.");
        var levelProp = GetPropertySafe(charType, "Level") ?? throw new InvalidOperationException("Could not find Level property.");
        var cultureProp = GetPropertySafe(charType, "Culture") ?? throw new InvalidOperationException("Could not find Culture property.");
        var occupationProp = GetPropertySafe(charType, "Occupation") ?? throw new InvalidOperationException("Could not find Occupation property.");
        var isHeroProp = GetPropertySafe(charType, "IsHero") ?? throw new InvalidOperationException("Could not find IsHero property.");
        var isRegularProp = GetPropertySafe(charType, "IsRegular") ?? throw new InvalidOperationException("Could not find IsRegular property.");
        var getSkillValueMethod = charType.GetMethod("GetSkillValue", new[] { skillType }) ?? throw new InvalidOperationException("Could not find GetSkillValue method.");
        var battleEquipsProp = GetPropertySafe(charType, "BattleEquipments") ?? throw new InvalidOperationException("Could not find BattleEquipments property.");

        // Properties/Indexer on equipment
        var equipmentIndexer = equipmentType.GetProperties()
            .FirstOrDefault(p => p.GetIndexParameters().Length == 1 && p.GetIndexParameters()[0].ParameterType == typeof(int))
            ?? throw new InvalidOperationException("Could not find Equipment indexer.");
        var itemPropInElement = equipmentElementType.GetProperty("Item") ?? throw new InvalidOperationException("Could not find Item property in EquipmentElement.");
        var isEmptyPropInElement = equipmentElementType.GetProperty("IsEmpty") ?? throw new InvalidOperationException("Could not find IsEmpty property in EquipmentElement.");

        foreach (var character in charList)
        {
            var isHero = (bool)isHeroProp.GetValue(character);
            var isRegular = (bool)isRegularProp.GetValue(character);

            if (isHero || !isRegular) continue;

            var id = (string)idProp.GetValue(character);
            var name = nameProp.GetValue(character)?.ToString() ?? "";
            var tier = (int)tierProp.GetValue(character);
            var level = (int)levelProp.GetValue(character);
            var cultureVal = cultureProp.GetValue(character);
            var culture = cultureVal != null ? GetPropertySafe(cultureVal.GetType(), "StringId")?.GetValue(cultureVal)?.ToString() : "";
            var occupation = occupationProp.GetValue(character)?.ToString() ?? "";

            var troopDict = new Dictionary<string, object?>
            {
                ["id"] = id,
                ["name"] = name,
                ["tier"] = tier,
                ["level"] = level,
                ["culture"] = culture,
                ["occupation"] = occupation
            };

            // Skills
            var skillsDict = new Dictionary<string, int>();
            var skillsField = character.GetType().GetField("DefaultCharacterSkills", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance)
                ?? character.GetType().BaseType?.GetField("DefaultCharacterSkills", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
            var skillsVal = skillsField?.GetValue(character);

            if (skillsVal != null)
            {
                foreach (var skillObj in skillList)
                {
                    var skillId = (string)GetPropertySafe(skillObj.GetType(), "StringId")?.GetValue(skillObj);
                    var skillValue = (int)getSkillValueMethod.Invoke(character, new[] { skillObj });
                    if (skillValue > 0 && skillId != null)
                    {
                        skillsDict[skillId] = skillValue;
                    }
                }
            }
            troopDict["skills"] = skillsDict;

            // Equipment sets
            var battleEquips = (System.Collections.IEnumerable)battleEquipsProp.GetValue(character);
            var setsList = new List<Dictionary<string, object?>>();

            foreach (var equip in battleEquips)
            {
                var setDict = new Dictionary<string, object?>();
                for (int i = 0; i <= 11; i++)
                {
                    var element = equipmentIndexer.GetValue(equip, new object[] { i });
                    var isEmpty = (bool)isEmptyPropInElement.GetValue(element);
                    if (isEmpty) continue;

                    var itemObj = itemPropInElement.GetValue(element);
                    if (itemObj == null) continue;

                    var slotName = SlotNames[i];
                    var itemDict = DumpItem(itemObj);
                    setDict[slotName] = itemDict;
                }
                if (setDict.Count > 0)
                {
                    setsList.Add(setDict);
                }
            }
            troopDict["equipment_sets"] = setsList;

            troopsData.Add(troopDict);
        }

        Console.WriteLine($"Extracted {troopsData.Count} troops.");
        WriteJson(output, troopsData);
        Console.WriteLine($"Output written to: {output}");

        return 0;
    }

    private static object CreateInstanceSafe(Type type)
    {
        var ctor = type.GetConstructor(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic, null, Type.EmptyTypes, null);
        if (ctor != null)
        {
            return ctor.Invoke(null);
        }
        return Activator.CreateInstance(type);
    }

    private static void SetPrivateFieldOrProperty(object obj, string name, object value)
    {
        var type = obj.GetType();
        var field = type.GetField(name, BindingFlags.NonPublic | BindingFlags.Instance);
        if (field == null)
        {
            field = type.GetField($"<{name}>k__BackingField", BindingFlags.NonPublic | BindingFlags.Instance);
        }
        if (field != null)
        {
            field.SetValue(obj, value);
            Console.WriteLine($"Successfully set field: {field.Name}");
            return;
        }

        var prop = type.GetProperty(name, BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
        if (prop != null && prop.CanWrite)
        {
            prop.SetValue(obj, value);
            Console.WriteLine($"Successfully set property: {prop.Name}");
            return;
        }

        var setter = type.GetMethod($"set_{name}", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
        if (setter != null)
        {
            setter.Invoke(obj, new[] { value });
            Console.WriteLine($"Successfully invoked setter: set_{name}");
        }
        else
        {
            Console.WriteLine($"Warning: Field or Property {name} not found on {type.FullName}");
        }
    }

    private static PropertyInfo? GetPropertySafe(Type type, string name)
    {
        var prop = type.GetProperty(name, BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly);
        if (prop != null) return prop;

        var currentType = type.BaseType;
        while (currentType != null)
        {
            prop = currentType.GetProperty(name, BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly);
            if (prop != null) return prop;
            currentType = currentType.BaseType;
        }

        return type.GetProperty(name, BindingFlags.Public | BindingFlags.Instance);
    }

    private static Type CreateMockSubclass(Type baseType, string className)
    {
        var assemblyName = new AssemblyName("MockAssembly_" + className);
        var assemblyBuilder = AssemblyBuilder.DefineDynamicAssembly(assemblyName, AssemblyBuilderAccess.Run);
        var moduleBuilder = assemblyBuilder.DefineDynamicModule("MockModule");
        var typeBuilder = moduleBuilder.DefineType(className, TypeAttributes.Public, baseType);

        var ctor = typeBuilder.DefineConstructor(MethodAttributes.Public, CallingConventions.Standard, Type.EmptyTypes);
        var il = ctor.GetILGenerator();
        il.Emit(OpCodes.Ldarg_0);
        var baseCtor = baseType.GetConstructor(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic, null, Type.EmptyTypes, null)
            ?? throw new InvalidOperationException($"Base type {baseType.FullName} does not have a parameterless constructor.");
        il.Emit(OpCodes.Call, baseCtor);
        il.Emit(OpCodes.Ret);

        // Implement all abstract methods
        foreach (var method in baseType.GetMethods(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance).Where(m => m.IsAbstract))
        {
            var parameterTypes = method.GetParameters().Select(p => p.ParameterType).ToArray();
            var methodBuilder = typeBuilder.DefineMethod(
                method.Name,
                (method.Attributes & ~MethodAttributes.Abstract) | MethodAttributes.Virtual,
                method.CallingConvention,
                method.ReturnType,
                parameterTypes
            );

            var mil = methodBuilder.GetILGenerator();
            if (method.ReturnType != typeof(void))
            {
                if (method.ReturnType.IsValueType)
                {
                    var local = mil.DeclareLocal(method.ReturnType);
                    mil.Emit(OpCodes.Ldloca_S, local);
                    mil.Emit(OpCodes.Initobj, method.ReturnType);
                    mil.Emit(OpCodes.Ldloc, local);
                }
                else
                {
                    mil.Emit(OpCodes.Ldnull);
                }
            }
            mil.Emit(OpCodes.Ret);
            typeBuilder.DefineMethodOverride(methodBuilder, method);
        }

        return typeBuilder.CreateType();
    }

    private static void RegisterType(object manager, Type type, string prefix, string plural, uint id, bool autoCreate, bool isTemp)
    {
        var registerTypeMethod = manager.GetType().GetMethod("RegisterType", BindingFlags.Public | BindingFlags.Instance)
            ?? throw new InvalidOperationException("Could not find RegisterType method.");
        var concrete = registerTypeMethod.MakeGenericMethod(type);
        concrete.Invoke(manager, new object[] { prefix, plural, id, autoCreate, isTemp });
    }

    private static void LoadXmlFile(object manager, MethodInfo loadXmlMethod, string path)
    {
        if (!File.Exists(path))
        {
            Console.WriteLine($"Warning: File not found: {path}");
            return;
        }

        try
        {
            var doc = new XmlDocument();
            doc.Load(path);
            loadXmlMethod.Invoke(manager, new object[] { doc, false });
            Console.WriteLine($"Successfully loaded: {Path.GetFileName(path)}");
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Error loading {path}: {ex.Message}");
            if (ex.InnerException != null)
            {
                Console.Error.WriteLine($"Inner Exception: {ex.InnerException.Message}");
                Console.Error.WriteLine($"Stack Trace:\n{ex.InnerException.StackTrace}");
            }
        }
    }

    private static Dictionary<string, object?> DumpItem(object itemObj)
    {
        var dict = DumpSimpleProperties(itemObj);

        // Weapons
        var weaponsProp = GetPropertySafe(itemObj.GetType(), "Weapons");
        if (weaponsProp != null)
        {
            var weaponsList = (System.Collections.IEnumerable)weaponsProp.GetValue(itemObj);
            if (weaponsList != null)
            {
                var weaponModes = new List<Dictionary<string, object?>>();
                foreach (var mode in weaponsList)
                {
                    var modeDict = DumpSimpleProperties(mode);

                    // Add RelevantSkill string id
                    var relevantSkillProp = GetPropertySafe(mode.GetType(), "RelevantSkill");
                    if (relevantSkillProp != null)
                    {
                        var skillObj = relevantSkillProp.GetValue(mode);
                        if (skillObj != null)
                        {
                            var stringIdProp = GetPropertySafe(skillObj.GetType(), "StringId");
                            if (stringIdProp != null)
                            {
                                modeDict["RelevantSkill"] = stringIdProp.GetValue(skillObj)?.ToString() ?? "";
                            }
                        }
                    }
                    weaponModes.Add(modeDict);
                }
                if (weaponModes.Count > 0)
                {
                    dict["Weapons"] = weaponModes;
                }
            }
        }

        // Armor
        var armorCompProp = GetPropertySafe(itemObj.GetType(), "ArmorComponent");
        if (armorCompProp != null)
        {
            var armorComp = armorCompProp.GetValue(itemObj);
            if (armorComp != null)
            {
                dict["Armor"] = DumpSimpleProperties(armorComp);
            }
        }

        // Horse
        var horseCompProp = GetPropertySafe(itemObj.GetType(), "HorseComponent");
        if (horseCompProp != null)
        {
            var horseComp = horseCompProp.GetValue(itemObj);
            if (horseComp != null)
            {
                dict["Horse"] = DumpSimpleProperties(horseComp);
            }
        }

        return dict;
    }

    private static Dictionary<string, object?> DumpSimpleProperties(object obj)
    {
        var dict = new Dictionary<string, object?>(StringComparer.OrdinalIgnoreCase);
        if (obj == null) return dict;
        foreach (var prop in obj.GetType().GetProperties(BindingFlags.Public | BindingFlags.Instance))
        {
            try
            {
                var t = prop.PropertyType;
                var underlyingType = Nullable.GetUnderlyingType(t) ?? t;
                if (underlyingType.IsPrimitive || 
                    underlyingType.IsEnum || 
                    underlyingType == typeof(string) || 
                    underlyingType == typeof(decimal))
                {
                    var val = prop.GetValue(obj);
                    dict[prop.Name] = val?.ToString() ?? "";
                    if (underlyingType.IsPrimitive && val != null)
                    {
                        dict[prop.Name] = val; // keep numeric types as numbers
                    }
                }
                else if (underlyingType.Name == "TextObject" && prop.Name == "Name")
                {
                    dict[prop.Name] = prop.GetValue(obj)?.ToString() ?? "";
                }
            }
            catch {}
        }
        return dict;
    }

    private static int ExtractXpMethods(CliOptions options)
    {
        var gameRoot = options.RequiredPath("game-root");
        var output = options.RequiredPath("json-output");
        var bin = ResolveGameBin(gameRoot);
        var searchDirs = ResolveAssemblySearchDirs(gameRoot);
        AddAssemblyResolver(searchDirs);

        var assemblyNames = options.All("assembly").ToList();
        if (assemblyNames.Count == 0)
        {
            assemblyNames.Add("TaleWorlds.Core");
            assemblyNames.Add("TaleWorlds.CampaignSystem");
        }

        var includeIl = options.Has("include-il");
        var includeContracts = options.Has("include-contracts");
        var deepScanCallers = options.Has("deep-scan-callers");
        var loadedAssemblies = new List<Assembly>();
        var loadErrors = new List<string>();

        foreach (var assemblyName in assemblyNames)
        {
            var dll = FindAssemblyPath(assemblyName, searchDirs);
            if (!File.Exists(dll))
            {
                loadErrors.Add($"Missing assembly: {dll}");
                continue;
            }
            try
            {
                loadedAssemblies.Add(Assembly.LoadFrom(dll));
            }
            catch (Exception ex)
            {
                loadErrors.Add($"Could not load {dll}: {ex.Message}");
            }
        }

        if (loadedAssemblies.Count == 0)
        {
            throw new InvalidOperationException("No Bannerlord assemblies were loaded.");
        }

        var bindingFlags = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly;
        var methodsScanned = 0;
        var candidates = new List<Dictionary<string, object?>>();

        foreach (var assembly in loadedAssemblies)
        {
            foreach (var type in GetSafeTypes(assembly))
            {
                MethodBase[] methods;
                try
                {
                    methods = type.GetMethods(bindingFlags).Cast<MethodBase>()
                        .Concat(type.GetConstructors(bindingFlags))
                        .ToArray();
                }
                catch
                {
                    continue;
                }

                foreach (var method in methods)
                {
                    methodsScanned++;
                    var declaringTypeName = GetTypeDisplayName(method.DeclaringType);
                    if (method.IsConstructor)
                    {
                        continue;
                    }
                    if (declaringTypeName == "TaleWorlds.CampaignSystem.GameModels" && Regex.IsMatch(method.Name, "(Xp|XP|Experience)"))
                    {
                        continue;
                    }
                    if (method.Name.StartsWith("AutoGeneratedGetMemberValue_", StringComparison.Ordinal))
                    {
                        continue;
                    }

                    var nameCandidate = TestNameCandidate(method);
                    if (!nameCandidate && !deepScanCallers)
                    {
                        continue;
                    }

                    var ilInfo = IlReader.ReadMethodIl(method, includeIl);
                    if (!includeContracts && ilInfo.IlBytes == 0)
                    {
                        continue;
                    }
                    var xpRefs = GetXpMemberReferences(ilInfo.Members);
                    var callCandidate = xpRefs.Count > 0;
                    if (!nameCandidate && !callCandidate)
                    {
                        continue;
                    }

                    var reasons = new List<string>();
                    if (nameCandidate)
                    {
                        reasons.Add("name");
                    }
                    if (callCandidate)
                    {
                        reasons.Add("references-xp-member");
                    }

                    var parameters = method.GetParameters()
                        .Select(parameter => new Dictionary<string, object?>
                        {
                            ["name"] = parameter.Name ?? "",
                            ["type"] = GetTypeDisplayName(parameter.ParameterType),
                        })
                        .ToList();
                    var returnType = method is MethodInfo methodInfo ? GetTypeDisplayName(methodInfo.ReturnType) : "void";

                    candidates.Add(new Dictionary<string, object?>
                    {
                        ["category"] = GetXpCategory(method),
                        ["assembly"] = assembly.GetName().Name ?? "",
                        ["type"] = GetTypeDisplayName(method.DeclaringType),
                        ["method"] = method.Name,
                        ["signature"] = GetMethodSignature(method),
                        ["visibility"] = GetMethodVisibility(method),
                        ["is_static"] = method.IsStatic,
                        ["return_type"] = returnType,
                        ["parameters"] = parameters,
                        ["il_bytes"] = ilInfo.IlBytes,
                        ["match_reasons"] = reasons,
                        ["numeric_constants"] = ilInfo.Numbers,
                        ["string_literals"] = ilInfo.Strings,
                        ["xp_references"] = xpRefs,
                        ["referenced_members"] = ilInfo.Members,
                        ["il"] = ilInfo.Instructions,
                        ["errors"] = ilInfo.Errors,
                    });
                }
            }
        }

        candidates = candidates
            .OrderBy(row => row["category"])
            .ThenBy(row => row["type"])
            .ThenBy(row => row["method"])
            .ToList();

        var payload = new Dictionary<string, object?>
        {
            ["generated_at"] = DateTimeOffset.Now.ToString("o"),
            ["game_root"] = "<local path omitted>",
            ["bin"] = "<local path omitted>\\bin\\Win64_Shipping_Client",
            ["assemblies_requested"] = assemblyNames,
            ["assemblies_loaded"] = loadedAssemblies.Select(assembly => assembly.GetName().Name ?? "").ToList(),
            ["load_errors"] = loadErrors,
            ["deep_scan_callers"] = deepScanCallers,
            ["include_contracts"] = includeContracts,
            ["methods_scanned"] = methodsScanned,
            ["methods_matched"] = candidates.Count,
            ["methods"] = candidates,
        };

        WriteJson(output, payload);
        Console.WriteLine($"XP methods scanned: {methodsScanned}");
        Console.WriteLine($"XP methods matched: {candidates.Count}");
        Console.WriteLine($"JSON written: {output}");
        return 0;
    }

    private static int DumpIl(CliOptions options)
    {
        var gameRoot = options.RequiredPath("game-root");
        var assemblyName = options.Required("assembly");
        var typeName = options.Required("type");
        var methodName = options.Required("method");
        var output = options.Get("output");
        var bin = ResolveGameBin(gameRoot);
        var searchDirs = ResolveAssemblySearchDirs(gameRoot);
        AddAssemblyResolver(searchDirs);

        var dll = FindAssemblyPath(assemblyName, searchDirs);
        RequireFile(dll, $"Could not find assembly: {dll}");
        var assembly = Assembly.LoadFrom(dll);
        var type = assembly.GetType(typeName, throwOnError: true)
            ?? throw new InvalidOperationException($"Could not load type: {typeName}");
        var method = type.GetMethods(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.Instance)
            .Cast<MethodBase>()
            .Concat(type.GetConstructors(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.Instance))
            .FirstOrDefault(candidate => candidate.Name == methodName)
            ?? throw new InvalidOperationException($"Could not find method: {typeName}.{methodName}");
        var il = IlReader.ReadMethodIl(method, keepInstructions: true);
        var lines = new List<string>
        {
            $"METHOD {GetTypeDisplayName(method.DeclaringType)}.{method.Name}",
        };
        lines.AddRange(il.Instructions);

        if (string.IsNullOrWhiteSpace(output))
        {
            foreach (var line in lines)
            {
                Console.WriteLine(line);
            }
        }
        else
        {
            Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(output)) ?? ".");
            File.WriteAllLines(output, lines);
            Console.WriteLine($"IL written: {output}");
        }
        return 0;
    }

    private static int FindMethods(CliOptions options)
    {
        var gameRoot = options.RequiredPath("game-root");
        var queries = options.All("query").Select(query => query.ToLowerInvariant()).ToList();
        if (queries.Count == 0)
        {
            throw new ArgumentException("Missing required option --query.");
        }

        var searchDirs = ResolveAssemblySearchDirs(gameRoot);
        AddAssemblyResolver(searchDirs);
        var includeIl = options.Has("include-il");
        var assemblyPaths = new List<string>();
        foreach (var assemblyFile in options.All("assembly-file"))
        {
            assemblyPaths.Add(Path.GetFullPath(assemblyFile));
        }
        foreach (var assemblyName in options.All("assembly"))
        {
            assemblyPaths.Add(FindAssemblyPath(assemblyName, searchDirs));
        }
        if (options.Has("all-game-assemblies"))
        {
            assemblyPaths.AddRange(DiscoverGameAssemblyPaths(gameRoot));
        }
        if (assemblyPaths.Count == 0)
        {
            throw new ArgumentException("Pass at least one --assembly, --assembly-file, or --all-game-assemblies.");
        }

        var results = new List<Dictionary<string, object?>>();
        var loadErrors = new List<string>();
        var methodsScanned = 0;

        foreach (var assemblyPath in assemblyPaths.Distinct(StringComparer.OrdinalIgnoreCase))
        {
            if (!File.Exists(assemblyPath))
            {
                loadErrors.Add($"Missing assembly: {assemblyPath}");
                continue;
            }

            Assembly assembly;
            try
            {
                assembly = Assembly.LoadFrom(assemblyPath);
            }
            catch (Exception ex)
            {
                loadErrors.Add($"Could not load {assemblyPath}: {ex.Message}");
                continue;
            }

            foreach (var type in GetSafeTypes(assembly))
            {
                MethodBase[] methods;
                try
                {
                    methods = type.GetMethods(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly)
                        .Cast<MethodBase>()
                        .Concat(type.GetConstructors(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly))
                        .ToArray();
                }
                catch
                {
                    continue;
                }

                foreach (var method in methods)
                {
                    methodsScanned++;
                    var ilInfo = IlReader.ReadMethodIl(method, includeIl);
                    var parameters = method.GetParameters()
                        .Select(parameter => new Dictionary<string, object?>
                        {
                            ["name"] = parameter.Name ?? "",
                            ["type"] = GetTypeDisplayName(parameter.ParameterType),
                        })
                        .ToList();
                    var haystackParts = new List<string>
                    {
                        assembly.GetName().Name ?? "",
                        GetTypeDisplayName(method.DeclaringType),
                        method.Name,
                        GetMethodSignature(method),
                    };
                    haystackParts.AddRange(parameters.Select(parameter => $"{parameter["type"]} {parameter["name"]}"));
                    haystackParts.AddRange(ilInfo.Strings);
                    haystackParts.AddRange(ilInfo.Members);
                    if (includeIl)
                    {
                        haystackParts.AddRange(ilInfo.Instructions);
                    }

                    var haystack = string.Join("\n", haystackParts).ToLowerInvariant();
                    var matched = queries.Where(haystack.Contains).ToList();
                    if (matched.Count == 0)
                    {
                        continue;
                    }

                    results.Add(new Dictionary<string, object?>
                    {
                        ["matched_queries"] = matched,
                        ["assembly"] = assembly.GetName().Name ?? "",
                        ["assembly_path"] = SanitizeLocalPath(assemblyPath, gameRoot),
                        ["type"] = GetTypeDisplayName(method.DeclaringType),
                        ["method"] = method.Name,
                        ["signature"] = GetMethodSignature(method),
                        ["visibility"] = GetMethodVisibility(method),
                        ["is_static"] = method.IsStatic,
                        ["parameters"] = parameters,
                        ["il_bytes"] = ilInfo.IlBytes,
                        ["numeric_constants"] = ilInfo.Numbers,
                        ["string_literals"] = ilInfo.Strings,
                        ["referenced_members"] = ilInfo.Members,
                        ["il"] = ilInfo.Instructions,
                        ["errors"] = ilInfo.Errors,
                    });
                }
            }
        }

        results = results
            .OrderBy(row => row["assembly"])
            .ThenBy(row => row["type"])
            .ThenBy(row => row["method"])
            .ToList();

        var payload = new Dictionary<string, object?>
        {
            ["generated_at"] = DateTimeOffset.Now.ToString("o"),
            ["queries"] = queries,
            ["assemblies_scanned"] = assemblyPaths.Distinct(StringComparer.OrdinalIgnoreCase).Select(path => SanitizeLocalPath(path, gameRoot)).ToList(),
            ["load_errors"] = loadErrors,
            ["methods_scanned"] = methodsScanned,
            ["methods_matched"] = results.Count,
            ["methods"] = results,
        };

        var output = options.Get("output");
        if (!string.IsNullOrWhiteSpace(output))
        {
            WriteJson(output, payload);
            Console.WriteLine($"Methods scanned: {methodsScanned}");
            Console.WriteLine($"Methods matched: {results.Count}");
            Console.WriteLine($"JSON written: {output}");
        }
        else
        {
            Console.WriteLine(JsonSerializer.Serialize(payload, JsonOptions));
        }

        return 0;
    }

    private static string ResolveGameBin(string gameRoot)
    {
        var root = Path.GetFullPath(gameRoot);
        var bin = Path.Combine(root, "bin", "Win64_Shipping_Client");
        if (!Directory.Exists(bin))
        {
            throw new InvalidOperationException($"Could not find Bannerlord binary directory under '{root}'. Check --game-root.");
        }
        return bin;
    }

    private static List<string> ResolveAssemblySearchDirs(string gameRoot)
    {
        var dirs = new List<string> { ResolveGameBin(gameRoot) };
        var modules = Path.Combine(Path.GetFullPath(gameRoot), "Modules");
        if (Directory.Exists(modules))
        {
            dirs.AddRange(Directory.GetDirectories(modules)
                .Select(module => Path.Combine(module, "bin", "Win64_Shipping_Client"))
                .Where(Directory.Exists));
        }
        return dirs.Distinct(StringComparer.OrdinalIgnoreCase).ToList();
    }

    private static string FindAssemblyPath(string assemblyName, IEnumerable<string> searchDirs)
    {
        var fileName = assemblyName.EndsWith(".dll", StringComparison.OrdinalIgnoreCase) ? assemblyName : assemblyName + ".dll";
        if (Path.IsPathRooted(fileName))
        {
            return Path.GetFullPath(fileName);
        }
        foreach (var dir in searchDirs)
        {
            var candidate = Path.Combine(dir, fileName);
            if (File.Exists(candidate))
            {
                return candidate;
            }
        }
        return Path.Combine(searchDirs.First(), fileName);
    }

    private static List<string> DiscoverGameAssemblyPaths(string gameRoot)
    {
        return ResolveAssemblySearchDirs(gameRoot)
            .SelectMany(dir => Directory.GetFiles(dir, "*.dll"))
            .Where(path =>
            {
                var name = Path.GetFileName(path);
                return name.StartsWith("TaleWorlds.", StringComparison.OrdinalIgnoreCase)
                    || name.Equals("SandBox.dll", StringComparison.OrdinalIgnoreCase)
                    || name.Equals("StoryMode.dll", StringComparison.OrdinalIgnoreCase);
            })
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .ToList();
    }

    private static string SanitizeLocalPath(string path, string gameRoot)
    {
        try
        {
            return Path.GetRelativePath(Path.GetFullPath(gameRoot), Path.GetFullPath(path));
        }
        catch
        {
            return "<local path>";
        }
    }

    private static void RequireFile(string path, string message)
    {
        if (!File.Exists(path))
        {
            throw new FileNotFoundException(message, path);
        }
    }

    private static void AddAssemblyResolver(IEnumerable<string> searchDirs)
    {
        var dirs = searchDirs.ToList();
        AppDomain.CurrentDomain.AssemblyResolve += (_, args) =>
        {
            var name = new AssemblyName(args.Name).Name;
            if (string.IsNullOrWhiteSpace(name))
            {
                return null;
            }
            foreach (var dir in dirs)
            {
                var candidate = Path.Combine(dir, name + ".dll");
                if (File.Exists(candidate))
                {
                    return Assembly.LoadFrom(candidate);
                }
            }
            return null;
        };
    }

    private static void WriteJson(string path, object value)
    {
        Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(path)) ?? ".");
        File.WriteAllText(path, JsonSerializer.Serialize(value, JsonOptions) + Environment.NewLine, new System.Text.UTF8Encoding(false));
    }

    private static string StripLocPrefix(string? text)
    {
        return Regex.Replace(text ?? "", "^\\{=[^}]+\\}", "").Trim();
    }

    private static string ConvertRole(int value)
    {
        var map = new Dictionary<int, string>
        {
            [0] = "none",
            [1] = "role_1",
            [2] = "clan leader",
            [3] = "governor",
            [4] = "army leader",
            [5] = "party leader",
            [6] = "role 6",
            [7] = "surgeon",
            [8] = "engineer",
            [9] = "scout",
            [10] = "quartermaster",
            [11] = "player",
            [12] = "personal",
            [13] = "captain",
        };
        return map.TryGetValue(value, out var role) ? role : $"role {value}";
    }

    private static string ConvertIncrement(int value)
    {
        return value switch
        {
            0 => "add",
            1 => "add_factor",
            _ => $"increment_{value}",
        };
    }

    private static string ConvertTroopMask(int value)
    {
        if (value == 65535)
        {
            return "all";
        }

        var parts = new List<string>();
        if ((value & 1) != 0) parts.Add("on_foot");
        if ((value & 2) != 0) parts.Add("mounted");
        if ((value & 4) != 0) parts.Add("melee");
        if ((value & 8) != 0) parts.Add("ranged");
        if ((value & 16) != 0) parts.Add("one_handed_user");
        if ((value & 32) != 0) parts.Add("shield_user");
        if ((value & 64) != 0) parts.Add("two_handed_user");
        if ((value & 128) != 0) parts.Add("polearm_user");
        if ((value & 256) != 0) parts.Add("bow_user");
        if ((value & 512) != 0) parts.Add("thrown_user");
        if ((value & 1024) != 0) parts.Add("crossbow_user");
        return parts.Count == 0 ? "none" : string.Join(", ", parts);
    }

    private static string GetSkillAttribute(string skill)
    {
        var map = new Dictionary<string, string>
        {
            ["One Handed"] = "Vigor",
            ["Two Handed"] = "Vigor",
            ["Polearm"] = "Vigor",
            ["Bow"] = "Control",
            ["Crossbow"] = "Control",
            ["Throwing"] = "Control",
            ["Riding"] = "Endurance",
            ["Athletics"] = "Endurance",
            ["Smithing"] = "Endurance",
            ["Scouting"] = "Cunning",
            ["Tactics"] = "Cunning",
            ["Roguery"] = "Cunning",
            ["Charm"] = "Social",
            ["Leadership"] = "Social",
            ["Trade"] = "Social",
            ["Steward"] = "Intelligence",
            ["Medicine"] = "Intelligence",
            ["Engineering"] = "Intelligence",
        };
        return map.TryGetValue(skill, out var attribute) ? attribute : "";
    }

    private static Dictionary<string, string> GetBannerEffectStringIds(List<IlInstruction> instructions)
    {
        var stack = new List<StackValue?>();
        var map = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        foreach (var instruction in instructions)
        {
            switch (instruction.OpCode)
            {
                case "ldarg.0":
                    stack.Add(new StackValue("this"));
                    break;
                case "ldstr":
                    stack.Add(new StackValue("string", Value: instruction.Operand as string));
                    break;
                case "call":
                    if (instruction.Operand is MethodBase { Name: "Create" })
                    {
                        var arg = Pop(stack);
                        stack.Add(new StackValue("created_banner_effect", StringId: Convert.ToString(arg?.Value) ?? ""));
                    }
                    break;
                case "stfld":
                    var value = Pop(stack);
                    if (stack.Count > 0)
                    {
                        stack.RemoveAt(stack.Count - 1);
                    }
                    if (value?.Kind == "created_banner_effect" && instruction.Operand is FieldInfo field)
                    {
                        map[field.Name] = value.StringId ?? "";
                    }
                    break;
            }
        }
        return map;
    }

    private static List<BannerEffectDefinition> GetBannerEffectDefinitions(
        List<IlInstruction> instructions,
        Dictionary<string, string> stringIdsByField
    )
    {
        var stack = new List<object?>();
        var defs = new List<BannerEffectDefinition>();

        foreach (var instruction in instructions)
        {
            var op = instruction.OpCode;
            if (op == "ldarg.0")
            {
                stack.Add(new StackValue("this"));
            }
            else if (op == "ldstr")
            {
                stack.Add(instruction.Operand as string ?? "");
            }
            else if (op == "ldc.r4" || op == "ldc.r8")
            {
                stack.Add(Convert.ToDouble(instruction.Operand));
            }
            else if (op == "ldc.i4.m1")
            {
                stack.Add(-1);
            }
            else if (Regex.IsMatch(op, "^ldc\\.i4\\.[0-8]$"))
            {
                stack.Add(int.Parse(op[^1].ToString()));
            }
            else if (op is "ldc.i4.s" or "ldc.i4")
            {
                stack.Add(Convert.ToInt32(instruction.Operand));
            }
            else if (op == "ldfld")
            {
                if (stack.Count > 0)
                {
                    stack.RemoveAt(stack.Count - 1);
                }
                if (instruction.Operand is FieldInfo field)
                {
                    stringIdsByField.TryGetValue(field.Name, out var stringId);
                    stack.Add(new StackValue("field", Field: field.Name, StringId: stringId ?? ""));
                }
            }
            else if (op == "callvirt" && instruction.Operand is MethodBase method)
            {
                if (method.Name == "Initialize" && method.DeclaringType?.FullName == "TaleWorlds.Core.BannerEffect")
                {
                    var items = new List<object?>();
                    for (var i = 0; i < 7; i++)
                    {
                        items.Insert(0, PopAny(stack));
                    }
                    var effectField = (StackValue)items[0]!;
                    var tier1 = Convert.ToDouble(items[3]);
                    var tier2 = Convert.ToDouble(items[4]);
                    var tier3 = Convert.ToDouble(items[5]);
                    var incrementValue = Convert.ToInt32(items[6]);
                    defs.Add(new BannerEffectDefinition
                    {
                        Field = effectField.Field ?? "",
                        StringId = effectField.StringId ?? "",
                        NameRaw = Convert.ToString(items[1]) ?? "",
                        Name = StripLocPrefix(Convert.ToString(items[1])),
                        DescriptionRaw = Convert.ToString(items[2]) ?? "",
                        Description = StripLocPrefix(Convert.ToString(items[2])),
                        IncrementValue = incrementValue,
                        IncrementType = ConvertIncrement(incrementValue),
                        Tiers = new List<BannerEffectTier>
                        {
                            new() { Level = 1, Bonus = tier1 },
                            new() { Level = 2, Bonus = tier2 },
                            new() { Level = 3, Bonus = tier3 },
                        },
                    });
                }
            }
        }

        return defs;
    }

    private static List<string> FindBannerXmlPaths(string gameRoot, bool includeMultiplayer)
    {
        var modules = Path.Combine(Path.GetFullPath(gameRoot), "Modules");
        if (!Directory.Exists(modules))
        {
            return new List<string>();
        }
        var singleplayerPath = Path.Combine(modules, "SandBoxCore", "ModuleData", "items", "banners.xml");
        if (!includeMultiplayer && File.Exists(singleplayerPath))
        {
            return new List<string> { singleplayerPath };
        }
        return Directory.GetFiles(modules, "banners.xml", SearchOption.AllDirectories)
            .Where(path => Regex.IsMatch(path, @"ModuleData[\\/](items[\\/])?banners\.xml$", RegexOptions.IgnoreCase))
            .OrderBy(path => path, StringComparer.OrdinalIgnoreCase)
            .ToList();
    }

    private static List<BannerItemDefinition> ReadBannerItems(
        string gameRoot,
        string xmlPath,
        Dictionary<string, BannerEffectDefinition> effectsByStringId
    )
    {
        var document = XDocument.Load(xmlPath);
        var module = GetModuleName(gameRoot, xmlPath);
        var source = SanitizeLocalPath(xmlPath, gameRoot);
        var items = new List<BannerItemDefinition>();

        foreach (var item in document.Descendants("Item"))
        {
            var banner = item.Descendants("Banner").FirstOrDefault();
            if (banner is null)
            {
                continue;
            }

            var effectStringId = Attr(banner, "effect");
            var level = ParseInt(Attr(banner, "banner_level"));
            effectsByStringId.TryGetValue(effectStringId, out var effect);
            var bonus = effect?.Tiers.FirstOrDefault(tier => tier.Level == level)?.Bonus ?? 0;

            items.Add(new BannerItemDefinition
            {
                Id = Attr(item, "id"),
                NameRaw = Attr(item, "name"),
                Name = StripLocPrefix(Attr(item, "name")),
                Culture = Attr(item, "culture").Replace("Culture.", "", StringComparison.Ordinal),
                Module = module,
                Source = source,
                BannerLevel = level,
                EffectStringId = effectStringId,
                EffectName = effect?.Name ?? "",
                EffectDescription = effect?.Description ?? "",
                Bonus = bonus,
                WeaponClass = Attr(banner, "weapon_class"),
                Mesh = Attr(item, "mesh"),
                Prefab = Attr(item, "prefab"),
                Weight = ParseDouble(Attr(item, "weight")),
            });
        }

        return items;
    }

    private static string Attr(XElement element, string name) => element.Attribute(name)?.Value ?? "";

    private static int ParseInt(string text) => int.TryParse(text, out var value) ? value : 0;

    private static double ParseDouble(string text) => double.TryParse(text, out var value) ? value : 0;

    private static string GetModuleName(string gameRoot, string path)
    {
        var modules = Path.Combine(Path.GetFullPath(gameRoot), "Modules");
        var relative = Path.GetRelativePath(modules, Path.GetFullPath(path));
        var first = relative.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar).FirstOrDefault();
        return string.IsNullOrWhiteSpace(first) ? "" : first;
    }

    private static string FormatPercent(double value)
    {
        var percent = value * 100.0;
        var text = Math.Abs(percent - Math.Round(percent)) < 0.000001
            ? Math.Round(percent).ToString("0")
            : percent.ToString("0.####");
        return text + "%";
    }

    private static string FormatBannerDescription(string description, double bonus)
    {
        if (string.IsNullOrWhiteSpace(description))
        {
            return "";
        }
        return description.Replace("{BONUS_AMOUNT}", FormatPercent(bonus).TrimEnd('%'), StringComparison.Ordinal);
    }

    private static Dictionary<string, string> GetPerkCreateMap(List<IlInstruction> instructions)
    {
        var stack = new List<StackValue?>();
        var map = new Dictionary<string, string>();
        foreach (var instruction in instructions)
        {
            switch (instruction.OpCode)
            {
                case "ldarg.0":
                    stack.Add(new StackValue("this"));
                    break;
                case "ldstr":
                    stack.Add(new StackValue("string", Value: instruction.Operand as string));
                    break;
                case "call":
                    if (instruction.Operand is MethodBase { Name: "Create" })
                    {
                        var arg = Pop(stack);
                        stack.Add(new StackValue("created_perk", StringId: Convert.ToString(arg?.Value) ?? ""));
                    }
                    break;
                case "stfld":
                    var value = Pop(stack);
                    if (stack.Count > 0)
                    {
                        stack.RemoveAt(stack.Count - 1);
                    }
                    if (value?.Kind == "created_perk" && instruction.Operand is FieldInfo field)
                    {
                        map[field.Name] = value.StringId ?? "";
                    }
                    break;
            }
        }
        return map;
    }

    private static List<PerkDefinition> GetPerkDefinitions(List<IlInstruction> instructions, Dictionary<string, string> createMap)
    {
        var stack = new List<object?>();
        var defs = new List<PerkDefinition>();

        foreach (var instruction in instructions)
        {
            var op = instruction.OpCode;
            if (op == "ldarg.0")
            {
                stack.Add(new StackValue("this"));
            }
            else if (op == "ldnull")
            {
                stack.Add(null);
            }
            else if (op == "ldstr")
            {
                stack.Add(instruction.Operand as string ?? "");
            }
            else if (op == "ldc.r4" || op == "ldc.r8")
            {
                stack.Add(Convert.ToDouble(instruction.Operand));
            }
            else if (op == "ldc.i4.m1")
            {
                stack.Add(-1);
            }
            else if (Regex.IsMatch(op, "^ldc\\.i4\\.[0-8]$"))
            {
                stack.Add(int.Parse(op[^1].ToString()));
            }
            else if (op is "ldc.i4.s" or "ldc.i4")
            {
                stack.Add(Convert.ToInt32(instruction.Operand));
            }
            else if (op == "ldfld")
            {
                if (stack.Count > 0)
                {
                    stack.RemoveAt(stack.Count - 1);
                }
                if (instruction.Operand is FieldInfo field)
                {
                    createMap.TryGetValue(field.Name, out var stringId);
                    stack.Add(new StackValue("field", Field: field.Name, StringId: stringId ?? ""));
                }
            }
            else if (op == "call")
            {
                if (instruction.Operand is not MethodBase method)
                {
                    continue;
                }
                if (method.Name == "GetTierCost")
                {
                    var tier = Convert.ToInt32(PopAny(stack));
                    stack.Add(tier * 25);
                }
                else if (method.Name.StartsWith("get_", StringComparison.Ordinal) && method is MethodInfo methodInfo && methodInfo.ReturnType.FullName == "TaleWorlds.Core.SkillObject")
                {
                    var skill = method.Name[4..].Replace("Crafting", "Smithing", StringComparison.Ordinal);
                    skill = Regex.Replace(skill, "([a-z])([A-Z])", "$1 $2");
                    stack.Add(skill);
                }
                else if (method.Name == "Create")
                {
                    var arg = Convert.ToString(PopAny(stack)) ?? "";
                    stack.Add(new StackValue("created_perk", StringId: arg));
                }
            }
            else if (op == "callvirt")
            {
                if (instruction.Operand is not MethodBase method)
                {
                    continue;
                }
                if (method.Name == "Initialize" && method.DeclaringType?.FullName == "TaleWorlds.CampaignSystem.CharacterDevelopment.PerkObject")
                {
                    var items = new List<object?>();
                    for (var i = 0; i < 15; i++)
                    {
                        items.Insert(0, PopAny(stack));
                    }
                    var perkField = (StackValue)items[0]!;
                    var altField = items[4] as StackValue;
                    defs.Add(new PerkDefinition
                    {
                        Field = perkField.Field ?? "",
                        StringId = perkField.StringId ?? "",
                        NameRaw = Convert.ToString(items[1]) ?? "",
                        Name = StripLocPrefix(Convert.ToString(items[1])),
                        Skill = Convert.ToString(items[2]) ?? "",
                        Level = Convert.ToInt32(items[3]),
                        AlternativeField = altField?.Field ?? "",
                        AlternativeStringId = altField?.StringId ?? "",
                        PrimaryTemplate = Convert.ToString(items[5]) ?? "",
                        PrimaryRoleValue = Convert.ToInt32(items[6]),
                        PrimaryBonus = Convert.ToDouble(items[7]),
                        PrimaryIncrementValue = Convert.ToInt32(items[8]),
                        SecondaryTemplate = Convert.ToString(items[9]) ?? "",
                        SecondaryRoleValue = Convert.ToInt32(items[10]),
                        SecondaryBonus = Convert.ToDouble(items[11]),
                        SecondaryIncrementValue = Convert.ToInt32(items[12]),
                        PrimaryTroopMaskValue = Convert.ToInt32(items[13]),
                        SecondaryTroopMaskValue = Convert.ToInt32(items[14]),
                    });
                }
            }
        }

        return defs;
    }

    private static StackValue? Pop(List<StackValue?> stack)
    {
        if (stack.Count == 0)
        {
            return null;
        }
        var value = stack[^1];
        stack.RemoveAt(stack.Count - 1);
        return value;
    }

    private static object? PopAny(List<object?> stack)
    {
        if (stack.Count == 0)
        {
            return null;
        }
        var value = stack[^1];
        stack.RemoveAt(stack.Count - 1);
        return value;
    }

    private static Dictionary<string, object?> ConvertPerkToRawObject(PerkDefinition perk)
    {
        return new Dictionary<string, object?>
        {
            ["string_id"] = perk.StringId,
            ["name_raw"] = perk.NameRaw,
            ["name"] = perk.Name,
            ["attribute"] = GetSkillAttribute(perk.Skill),
            ["skill"] = perk.Skill,
            ["level"] = perk.Level,
            ["field"] = perk.Field,
            ["alternative_field"] = perk.AlternativeField,
            ["alternative_string_id"] = perk.AlternativeStringId,
            ["primary_effect"] = ConvertRawEffectSlot(perk, primary: true),
            ["secondary_effect"] = ConvertRawEffectSlot(perk, primary: false),
        };
    }

    private static Dictionary<string, object?> ConvertRawEffectSlot(PerkDefinition perk, bool primary)
    {
        var template = primary ? perk.PrimaryTemplate : perk.SecondaryTemplate;
        var roleValue = primary ? perk.PrimaryRoleValue : perk.SecondaryRoleValue;
        var bonus = primary ? perk.PrimaryBonus : perk.SecondaryBonus;
        var incrementValue = primary ? perk.PrimaryIncrementValue : perk.SecondaryIncrementValue;
        var maskValue = primary ? perk.PrimaryTroopMaskValue : perk.SecondaryTroopMaskValue;
        return new Dictionary<string, object?>
        {
            ["template_raw"] = template,
            ["template"] = StripLocPrefix(template),
            ["role"] = ConvertRole(roleValue),
            ["role_value"] = roleValue,
            ["bonus"] = bonus,
            ["increment_type"] = ConvertIncrement(incrementValue),
            ["increment_value"] = incrementValue,
            ["troop_usage"] = ConvertTroopMask(maskValue),
            ["troop_usage_value"] = maskValue,
        };
    }

    private static string GetTypeDisplayName(Type? type)
    {
        if (type is null)
        {
            return "void";
        }
        if (type.IsArray)
        {
            return GetTypeDisplayName(type.GetElementType()) + "[]";
        }
        if (type.IsGenericType)
        {
            var baseName = string.IsNullOrWhiteSpace(type.FullName) ? type.Name : type.FullName!;
            var tick = baseName.IndexOf('`');
            if (tick >= 0)
            {
                baseName = baseName[..tick];
            }
            var args = type.GetGenericArguments().Select(GetTypeDisplayName);
            return $"{baseName}<{string.Join(", ", args)}>";
        }
        return string.IsNullOrWhiteSpace(type.FullName) ? type.Name : type.FullName!;
    }

    private static string GetMemberDisplayName(object? member)
    {
        try
        {
            return member switch
            {
                MethodBase method => $"{GetTypeDisplayName(method.DeclaringType)}.{method.Name}({string.Join(", ", method.GetParameters().Select(parameter => GetTypeDisplayName(parameter.ParameterType)))})",
                FieldInfo field => $"{GetTypeDisplayName(field.DeclaringType)}.{field.Name}",
                Type type => GetTypeDisplayName(type),
                null => "",
                _ => member.ToString() ?? "",
            };
        }
        catch
        {
            return member?.ToString() ?? "";
        }
    }

    private static Type[] GetSafeTypes(Assembly assembly)
    {
        try
        {
            return assembly.GetTypes();
        }
        catch (ReflectionTypeLoadException ex)
        {
            return ex.Types.Where(type => type is not null).Cast<Type>().ToArray();
        }
    }

    private static string GetMethodVisibility(MethodBase method)
    {
        if (method.IsPublic) return "public";
        if (method.IsFamily) return "protected";
        if (method.IsAssembly) return "internal";
        if (method.IsFamilyOrAssembly) return "protected internal";
        if (method.IsPrivate) return "private";
        return "non-public";
    }

    private static string GetMethodSignature(MethodBase method)
    {
        var returnType = method is MethodInfo methodInfo ? GetTypeDisplayName(methodInfo.ReturnType) : "void";
        var parameters = method.GetParameters()
            .Select(parameter => $"{GetTypeDisplayName(parameter.ParameterType)} {parameter.Name}");
        return $"{returnType} {GetTypeDisplayName(method.DeclaringType)}.{method.Name}({string.Join(", ", parameters)})";
    }

    private static string GetXpCategory(MethodBase method)
    {
        var text = $"{GetTypeDisplayName(method.DeclaringType)}.{method.Name}";
        if (IsMatch(text, "DefaultCombatXpModel|CombatXp|GetXpFromHit|MapEvent.*CommitXp|SkillLevelingManager.OnBattleEnded")) return "combat xp";
        if (IsMatch(text, "PartyTraining|TroopRoster|FlattenedTroop|PartyAddSharedXp|CanTroopGainXp|GenerateSharedXp|TroopUpgrade|DailyTroopXpBonus|PartyBase.OnXpChanged|CampaignBattleRecoveryBehavior.GiveTroopXp|GarrisonRecruitment|ItemDiscard|InventoryLogic.*Xp|GetUpgradeXpCost|AddTroopsXp|AddPrisonersXp|GetMaximumXpAmountPartyCanGet")) return "troop xp";
        if (IsMatch(text, "Healing|Medicine|PartyHealing")) return "healing xp";
        if (IsMatch(text, "Smithing|Crafting|CraftingOrder")) return "crafting xp";
        if (IsMatch(text, "Diplomacy|Charm|Persuasion|Tournament|Workshop|Alley|Hideout|IncidentEffect|Issue")) return "activity xp";
        if (IsMatch(text, "GenericXp|Multiplier")) return "xp multiplier";
        if (IsMatch(text, "HeroDeveloper|CharacterDevelopment|Learning|SkillLevel|SkillXp|GainRawXp|AddSkillXp|XpRequiredForLevel|TraitXp")) return "hero progression";
        return "other xp";
    }

    private static bool TestNameCandidate(MethodBase method)
    {
        var text = $"{GetTypeDisplayName(method.DeclaringType)}.{method.Name}";
        return Regex.IsMatch(text, "(Xp|XP|Xpf|Experience(?!d)|LearningLimit|LearningRate|SkillLevelChange|SkillsRequiredForLevel|MaxSkillPoint|PartyAddSharedXp|CanTroopGainXp|AddSkillXp|GainRawXp|AddXpToTroop)");
    }

    private static List<string> GetXpMemberReferences(IEnumerable<string> members)
    {
        return members
            .Where(member => Regex.IsMatch(member, "(Xp|XP|Xpf|Experience(?!d)|Learning|SkillLevel|AddSkill|GainRaw|AddXpToTroop|PartyAddSharedXp|GenerateSharedXp|OnTroopGainXp|TroopRoster|HeroDeveloper)"))
            .Distinct()
            .OrderBy(member => member)
            .ToList();
    }

    private static bool IsMatch(string text, string pattern)
    {
        return Regex.IsMatch(text, pattern, RegexOptions.IgnoreCase);
    }

    private sealed record StackValue(
        string Kind,
        object? Value = null,
        string? Field = null,
        string? StringId = null
    );

    private sealed class PerkDefinition
    {
        public string Field { get; init; } = "";
        public string StringId { get; init; } = "";
        public string NameRaw { get; init; } = "";
        public string Name { get; init; } = "";
        public string Skill { get; init; } = "";
        public int Level { get; init; }
        public string AlternativeField { get; init; } = "";
        public string AlternativeStringId { get; init; } = "";
        public string PrimaryTemplate { get; init; } = "";
        public int PrimaryRoleValue { get; init; }
        public double PrimaryBonus { get; init; }
        public int PrimaryIncrementValue { get; init; }
        public string SecondaryTemplate { get; init; } = "";
        public int SecondaryRoleValue { get; init; }
        public double SecondaryBonus { get; init; }
        public int SecondaryIncrementValue { get; init; }
        public int PrimaryTroopMaskValue { get; init; }
        public int SecondaryTroopMaskValue { get; init; }
    }

    private sealed class BannerEffectTier
    {
        public int Level { get; init; }
        public double Bonus { get; init; }
    }

    private sealed class BannerEffectDefinition
    {
        public string Field { get; init; } = "";
        public string StringId { get; init; } = "";
        public string NameRaw { get; init; } = "";
        public string Name { get; init; } = "";
        public string DescriptionRaw { get; init; } = "";
        public string Description { get; init; } = "";
        public int IncrementValue { get; init; }
        public string IncrementType { get; init; } = "";
        public List<BannerEffectTier> Tiers { get; init; } = new();
    }

    private sealed class BannerItemDefinition
    {
        public string Id { get; init; } = "";
        public string NameRaw { get; init; } = "";
        public string Name { get; init; } = "";
        public string Culture { get; init; } = "";
        public string Module { get; init; } = "";
        public string Source { get; init; } = "";
        public int BannerLevel { get; init; }
        public string EffectStringId { get; init; } = "";
        public string EffectName { get; init; } = "";
        public string EffectDescription { get; init; } = "";
        public double Bonus { get; init; }
        public string WeaponClass { get; init; } = "";
        public string Mesh { get; init; } = "";
        public string Prefab { get; init; } = "";
        public double Weight { get; init; }
    }

    private sealed class ItemModifierDefinition
    {
        public string Id { get; init; } = "";
        public string Name { get; init; } = "";
        public string NameRaw { get; init; } = "";
        public string ModifierGroup { get; init; } = "";
        public double PriceFactor { get; init; }
        public string Quality { get; init; } = "";
        public int LootDropScore { get; init; }
        public int ProductionDropScore { get; init; }
        public Dictionary<string, string> Stats { get; init; } = new();
    }

    private sealed class ModifierInGroup
    {
        public string Id { get; init; } = "";
        public int LootDropScore { get; init; }
        public int ProductionDropScore { get; init; }
    }

    private sealed class ModifierGroupDefinition
    {
        public string Id { get; init; } = "";
        public int NoModifierLootScore { get; init; }
        public int NoModifierProductionScore { get; init; }
        public List<ModifierInGroup> Modifiers { get; init; } = new();
    }

    private sealed class CliOptions
    {
        private readonly Dictionary<string, List<string>> _values = new(StringComparer.OrdinalIgnoreCase);

        public static CliOptions Parse(string[] args)
        {
            var result = new CliOptions();
            for (var i = 0; i < args.Length; i++)
            {
                var token = args[i];
                if (!token.StartsWith("--", StringComparison.Ordinal))
                {
                    throw new ArgumentException($"Unexpected argument: {token}");
                }
                var name = token[2..];
                if (i + 1 < args.Length && !args[i + 1].StartsWith("--", StringComparison.Ordinal))
                {
                    result.Add(name, args[++i]);
                }
                else
                {
                    result.Add(name, "true");
                }
            }
            return result;
        }

        public bool Has(string name) => _values.ContainsKey(name);

        public string? Get(string name)
        {
            return _values.TryGetValue(name, out var values) && values.Count > 0 ? values[^1] : null;
        }

        public IEnumerable<string> All(string name)
        {
            return _values.TryGetValue(name, out var values) ? values : Array.Empty<string>();
        }

        public string Required(string name)
        {
            return Get(name) ?? throw new ArgumentException($"Missing required option --{name}.");
        }

        public string RequiredPath(string name)
        {
            return Path.GetFullPath(Required(name));
        }

        private void Add(string name, string value)
        {
            if (!_values.TryGetValue(name, out var values))
            {
                values = new List<string>();
                _values[name] = values;
            }
            values.Add(value);
        }
    }

    private sealed class IlInstruction
    {
        public int Offset { get; init; }
        public string OpCode { get; init; } = "";
        public object? Operand { get; init; }
    }

    private sealed class IlInfo
    {
        public int IlBytes { get; init; }
        public List<double> Numbers { get; } = new();
        public List<string> Strings { get; } = new();
        public List<string> Members { get; } = new();
        public List<string> Instructions { get; } = new();
        public List<string> Errors { get; } = new();
    }

    private static class IlReader
    {
        private static readonly Dictionary<int, OpCode> SingleByte;
        private static readonly Dictionary<int, OpCode> DoubleByte;

        static IlReader()
        {
            SingleByte = new Dictionary<int, OpCode>();
            DoubleByte = new Dictionary<int, OpCode>();
            foreach (var field in typeof(OpCodes).GetFields(BindingFlags.Public | BindingFlags.Static))
            {
                if (field.GetValue(null) is not OpCode op)
                {
                    continue;
                }
                var value = unchecked((ushort)op.Value);
                if (value <= 0xff)
                {
                    SingleByte[value] = op;
                }
                else
                {
                    DoubleByte[value & 0xff] = op;
                }
            }
        }

        public static List<IlInstruction> ReadInstructions(MethodBase method)
        {
            var body = method.GetMethodBody() ?? throw new InvalidOperationException($"Method has no IL body: {method.Name}");
            var bytes = body.GetILAsByteArray() ?? Array.Empty<byte>();
            var instructions = new List<IlInstruction>();
            var index = 0;
            while (index < bytes.Length)
            {
                var offset = index;
                var op = ReadOpCode(bytes, ref index);
                var operand = ReadOperand(method, op, bytes, ref index);
                instructions.Add(new IlInstruction
                {
                    Offset = offset,
                    OpCode = op.Name ?? "",
                    Operand = operand,
                });
            }
            return instructions;
        }

        public static IlInfo ReadMethodIl(MethodBase method, bool keepInstructions)
        {
            var info = new IlInfo();
            MethodBody? body;
            try
            {
                body = method.GetMethodBody();
            }
            catch (Exception ex)
            {
                info.Errors.Add(ex.Message);
                return info;
            }
            if (body is null)
            {
                return info;
            }

            var bytes = body.GetILAsByteArray() ?? Array.Empty<byte>();
            var numbers = new SortedSet<double>();
            var strings = new SortedSet<string>(StringComparer.Ordinal);
            var members = new SortedSet<string>(StringComparer.Ordinal);
            var objectInfo = new IlInfo { IlBytes = bytes.Length };
            var index = 0;

            while (index < bytes.Length)
            {
                var offset = index;
                OpCode op;
                try
                {
                    op = ReadOpCode(bytes, ref index);
                }
                catch (Exception ex)
                {
                    objectInfo.Errors.Add($"Unknown opcode at IL_{offset:x4}: {ex.Message}");
                    continue;
                }

                var operand = ReadOperand(method, op, bytes, ref index);
                var number = GetLdcNumber(op, operand);
                if (number.HasValue)
                {
                    numbers.Add(number.Value);
                }
                if (op.OperandType == OperandType.InlineString && operand is string stringValue)
                {
                    strings.Add(stringValue);
                }
                if (operand is MemberInfo or Type)
                {
                    var memberText = GetMemberDisplayName(operand);
                    if (!string.IsNullOrWhiteSpace(memberText))
                    {
                        members.Add(memberText);
                    }
                }
                else if (operand is string text && text.StartsWith("unresolved:", StringComparison.Ordinal))
                {
                    members.Add(text);
                }

                if (keepInstructions)
                {
                    var operandText = FormatOperandText(operand);
                    objectInfo.Instructions.Add($"IL_{offset:x4}: {op.Name,-14} {operandText}".TrimEnd());
                }
            }

            objectInfo.Numbers.AddRange(numbers);
            objectInfo.Strings.AddRange(strings);
            objectInfo.Members.AddRange(members);
            return objectInfo;
        }

        private static OpCode ReadOpCode(byte[] bytes, ref int index)
        {
            var b = bytes[index++];
            if (b == 0xfe)
            {
                return DoubleByte[bytes[index++]];
            }
            return SingleByte[b];
        }

        private static object? ReadOperand(MethodBase method, OpCode op, byte[] bytes, ref int index)
        {
            switch (op.OperandType)
            {
                case OperandType.InlineNone:
                    return null;
                case OperandType.ShortInlineI:
                    return unchecked((sbyte)bytes[index++]);
                case OperandType.InlineI:
                    var inlineI = BitConverter.ToInt32(bytes, index);
                    index += 4;
                    return inlineI;
                case OperandType.InlineI8:
                    var inlineI8 = BitConverter.ToInt64(bytes, index);
                    index += 8;
                    return inlineI8;
                case OperandType.ShortInlineR:
                    var shortR = BitConverter.ToSingle(bytes, index);
                    index += 4;
                    return shortR;
                case OperandType.InlineR:
                    var inlineR = BitConverter.ToDouble(bytes, index);
                    index += 8;
                    return inlineR;
                case OperandType.ShortInlineBrTarget:
                    return unchecked((sbyte)bytes[index++]);
                case OperandType.InlineBrTarget:
                    var branch = BitConverter.ToInt32(bytes, index);
                    index += 4;
                    return branch;
                case OperandType.InlineSwitch:
                    var count = BitConverter.ToInt32(bytes, index);
                    index += 4;
                    var targets = new int[count];
                    for (var i = 0; i < count; i++)
                    {
                        targets[i] = BitConverter.ToInt32(bytes, index);
                        index += 4;
                    }
                    return targets;
                case OperandType.InlineString:
                    var stringToken = BitConverter.ToInt32(bytes, index);
                    index += 4;
                    try
                    {
                        return method.Module.ResolveString(stringToken);
                    }
                    catch
                    {
                        return $"unresolved:String:0x{stringToken:x8}";
                    }
                case OperandType.InlineField:
                    var fieldToken = BitConverter.ToInt32(bytes, index);
                    index += 4;
                    return ResolveIlMember(method, fieldToken, "Field");
                case OperandType.InlineMethod:
                    var methodToken = BitConverter.ToInt32(bytes, index);
                    index += 4;
                    return ResolveIlMember(method, methodToken, "Method");
                case OperandType.InlineType:
                    var typeToken = BitConverter.ToInt32(bytes, index);
                    index += 4;
                    return ResolveIlMember(method, typeToken, "Type");
                case OperandType.InlineTok:
                    var memberToken = BitConverter.ToInt32(bytes, index);
                    index += 4;
                    return ResolveIlMember(method, memberToken, "Member");
                case OperandType.InlineSig:
                    var sigToken = BitConverter.ToInt32(bytes, index);
                    index += 4;
                    return $"sig:0x{sigToken:x8}";
                case OperandType.ShortInlineVar:
                    return bytes[index++];
                case OperandType.InlineVar:
                    var varToken = BitConverter.ToUInt16(bytes, index);
                    index += 2;
                    return varToken;
                default:
                    return null;
            }
        }

        private static object? ResolveIlMember(MethodBase method, int token, string kind)
        {
            var module = method.Module;
            var typeArgs = method.DeclaringType is { IsGenericType: true } declaringType ? declaringType.GetGenericArguments() : null;
            var methodArgs = method.IsGenericMethod ? method.GetGenericArguments() : null;
            try
            {
                return kind switch
                {
                    "Field" => module.ResolveField(token, typeArgs, methodArgs),
                    "Method" => module.ResolveMethod(token, typeArgs, methodArgs),
                    "Type" => module.ResolveType(token, typeArgs, methodArgs),
                    "Member" => module.ResolveMember(token, typeArgs, methodArgs),
                    _ => $"unresolved:{kind}:0x{token:x8}",
                };
            }
            catch
            {
                return $"unresolved:{kind}:0x{token:x8}";
            }
        }

        private static double? GetLdcNumber(OpCode op, object? operand)
        {
            return op.Name switch
            {
                "ldc.i4.m1" => -1,
                "ldc.i4.0" => 0,
                "ldc.i4.1" => 1,
                "ldc.i4.2" => 2,
                "ldc.i4.3" => 3,
                "ldc.i4.4" => 4,
                "ldc.i4.5" => 5,
                "ldc.i4.6" => 6,
                "ldc.i4.7" => 7,
                "ldc.i4.8" => 8,
                "ldc.i4.s" or "ldc.i4" or "ldc.i8" or "ldc.r4" or "ldc.r8" => Convert.ToDouble(operand),
                _ => null,
            };
        }

        private static string FormatOperandText(object? operand)
        {
            return operand switch
            {
                null => "",
                MemberInfo or Type => GetMemberDisplayName(operand),
                int[] values => string.Join(", ", values),
                _ => Convert.ToString(operand) ?? "",
            };
        }
    }
}
