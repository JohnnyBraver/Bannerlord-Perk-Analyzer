using System.Reflection;
using System.Reflection.Emit;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Text.RegularExpressions;

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
                "xp-methods" => ExtractXpMethods(options),
                "dump-il" => DumpIl(options),
                "find-methods" => FindMethods(options),
                _ => Fail($"Unknown command: {command}"),
            };
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine(ex.Message);
            return 1;
        }
    }

    private static void PrintHelp()
    {
        Console.WriteLine("BannerlordExtractor");
        Console.WriteLine();
        Console.WriteLine("Commands:");
        Console.WriteLine("  perks --game-root <path> --output <json>");
        Console.WriteLine("  xp-methods --game-root <path> --json-output <json> [--assembly <name>] [--include-il] [--deep-scan-callers] [--include-contracts]");
        Console.WriteLine("  dump-il --game-root <path> --assembly <name> --type <full type> --method <name> [--output <txt>]");
        Console.WriteLine("  find-methods --game-root <path> --query <text> [--assembly <name>] [--all-game-assemblies] [--include-il] [--output <json>]");
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
        if ((value & 1) != 0) parts.Add("infantry");
        if ((value & 2) != 0) parts.Add("ranged");
        if ((value & 4) != 0) parts.Add("cavalry");
        if ((value & 8) != 0) parts.Add("horse_archer");
        if ((value & 16) != 0) parts.Add("heroes");
        if ((value & 32) != 0) parts.Add("non_hero");
        if ((value & 64) != 0) parts.Add("formation");
        if ((value & 128) != 0) parts.Add("melee");
        if ((value & 256) != 0) parts.Add("mounted");
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
