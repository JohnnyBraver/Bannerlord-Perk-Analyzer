param(
    [string]$GameRoot = $env:BANNERLORD_GAME_ROOT
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($GameRoot)) {
    throw 'Bannerlord game root is required. Pass -GameRoot or set BANNERLORD_GAME_ROOT.'
}
$GameRoot = (Resolve-Path -LiteralPath $GameRoot).Path
$bin = Join-Path $GameRoot 'bin\Win64_Shipping_Client'
$campaignDll = Join-Path $bin 'TaleWorlds.CampaignSystem.dll'
$objectSystemDll = Join-Path $bin 'TaleWorlds.ObjectSystem.dll'
$coreDll = Join-Path $bin 'TaleWorlds.Core.dll'
if (-not (Test-Path -LiteralPath $campaignDll) -or -not (Test-Path -LiteralPath $objectSystemDll) -or -not (Test-Path -LiteralPath $coreDll)) {
    throw "Could not find Bannerlord assemblies under '$bin'. Check -GameRoot."
}

[System.AppDomain]::CurrentDomain.add_AssemblyResolve({
    param($sender, $args)
    $name = New-Object System.Reflection.AssemblyName($args.Name)
    $candidate = Join-Path $bin ($name.Name + '.dll')
    if (Test-Path -LiteralPath $candidate) {
        return [System.Reflection.Assembly]::LoadFrom($candidate)
    }
    return $null
})

$asm = [System.Reflection.Assembly]::LoadFrom($campaignDll)
$objectSystemAsm = [System.Reflection.Assembly]::LoadFrom($objectSystemDll)
$coreAsm = [System.Reflection.Assembly]::LoadFrom($coreDll)

$objectManagerType = $objectSystemAsm.GetType('TaleWorlds.ObjectSystem.MBObjectManager', $true)
try {
    $objectManagerType.GetMethod('Init', [System.Reflection.BindingFlags]'Public,Static').Invoke($null, $null)
    Write-Output 'MBObjectManager.Init OK'
} catch {
    $inner = $_.Exception.InnerException
    if ($inner) {
        Write-Output "MBObjectManager.Init ERROR $($inner.GetType().FullName): $($inner.Message)"
    } else {
        Write-Output "MBObjectManager.Init ERROR $($_.Exception.GetType().FullName): $($_.Exception.Message)"
    }
}
$objectManager = $objectManagerType.GetProperty('Instance', [System.Reflection.BindingFlags]'Public,Static').GetValue($null)

$gameType = $coreAsm.GetType('TaleWorlds.Core.Game', $true)
try {
    $game = [System.Runtime.Serialization.FormatterServices]::GetUninitializedObject($gameType)
    $gameType.GetProperty('ObjectManager', [System.Reflection.BindingFlags]'Public,Instance').SetValue($game, $objectManager)
    $gameType.GetProperty('Current', [System.Reflection.BindingFlags]'Public,Static').SetValue($null, $game)
    Write-Output 'Minimal Game.Current OK'
} catch {
    $inner = $_.Exception.InnerException
    if ($inner) {
        Write-Output "Minimal Game.Current ERROR $($inner.GetType().FullName): $($inner.Message)"
    } else {
        Write-Output "Minimal Game.Current ERROR $($_.Exception.GetType().FullName): $($_.Exception.Message)"
    }
}

$defaultSkillsType = $coreAsm.GetType('TaleWorlds.Core.DefaultSkills', $true)
$defaultCharacterAttributesType = $coreAsm.GetType('TaleWorlds.Core.DefaultCharacterAttributes', $true)

Write-Output 'DefaultCharacterAttributes methods:'
$defaultCharacterAttributesType.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly') |
    Select-Object Name, IsStatic, IsPublic, IsPrivate |
    Format-Table -AutoSize
try {
    $attributesInstance = [System.Runtime.Serialization.FormatterServices]::GetUninitializedObject($defaultCharacterAttributesType)
    $gameType.GetProperty('DefaultCharacterAttributes', [System.Reflection.BindingFlags]'Public,Instance').SetValue($game, $attributesInstance)
    Write-Output 'Game.DefaultCharacterAttributes set'
    foreach ($methodName in @('RegisterAll')) {
        $method = $defaultCharacterAttributesType.GetMethod($methodName, [System.Reflection.BindingFlags]'NonPublic,Instance')
        if ($method) {
            try {
                $method.Invoke($attributesInstance, $null)
                Write-Output "DefaultCharacterAttributes.$methodName OK"
            } catch {
                $inner = $_.Exception.InnerException
                if ($inner) {
                    Write-Output "DefaultCharacterAttributes.$methodName ERROR $($inner.GetType().FullName): $($inner.Message)"
                    Write-Output $inner.StackTrace
                } else {
                    Write-Output "DefaultCharacterAttributes.$methodName ERROR $($_.Exception.GetType().FullName): $($_.Exception.Message)"
                }
            }
        }
    }
} catch {
    Write-Output "DefaultCharacterAttributes bootstrap ERROR $($_.Exception.Message)"
}

Write-Output 'DefaultSkills methods:'
$defaultSkillsType.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly') |
    Select-Object Name, IsStatic, IsPublic, IsPrivate |
    Format-Table -AutoSize
try {
    $skillsInstance = [System.Runtime.Serialization.FormatterServices]::GetUninitializedObject($defaultSkillsType)
    $gameType.GetProperty('DefaultSkills', [System.Reflection.BindingFlags]'Public,Instance').SetValue($game, $skillsInstance)
    Write-Output 'Game.DefaultSkills set'
    foreach ($methodName in @('RegisterAll')) {
        $method = $defaultSkillsType.GetMethod($methodName, [System.Reflection.BindingFlags]'NonPublic,Instance')
        if ($method) {
            try {
                $method.Invoke($skillsInstance, $null)
                Write-Output "DefaultSkills.$methodName OK"
            } catch {
                $inner = $_.Exception.InnerException
                if ($inner) {
                    Write-Output "DefaultSkills.$methodName ERROR $($inner.GetType().FullName): $($inner.Message)"
                    Write-Output $inner.StackTrace
                } else {
                    Write-Output "DefaultSkills.$methodName ERROR $($_.Exception.GetType().FullName): $($_.Exception.Message)"
                }
            }
        }
    }
} catch {
    Write-Output "DefaultSkills bootstrap ERROR $($_.Exception.Message)"
}

$defaultPerksType = $asm.GetType('TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultPerks', $true)
$perkObjectType = $asm.GetType('TaleWorlds.CampaignSystem.CharacterDevelopment.PerkObject', $true)

Write-Output 'DefaultPerks methods:'
$defaultPerksType.GetMethods([System.Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly') |
    Select-Object Name, IsStatic, IsPublic, IsPrivate |
    Format-Table -AutoSize

Write-Output 'PerkObject properties:'
$perkObjectType.GetProperties([System.Reflection.BindingFlags]'Public,Instance') |
    Select-Object Name, @{Name='Type'; Expression={$_.PropertyType.FullName}} |
    Format-Table -AutoSize

try {
    $campaignType = $asm.GetType('TaleWorlds.CampaignSystem.Campaign', $true)
    $campaign = [System.Runtime.Serialization.FormatterServices]::GetUninitializedObject($campaignType)
    $campaignType.GetProperty('CurrentGame', [System.Reflection.BindingFlags]'Public,Instance').SetValue($campaign, $game)
    $campaignType.GetProperty('Current', [System.Reflection.BindingFlags]'Public,Static').SetValue($null, $campaign)
    Write-Output 'Minimal Campaign.Current OK'
} catch {
    $inner = $_.Exception.InnerException
    if ($inner) {
        Write-Output "Minimal Campaign.Current ERROR $($inner.GetType().FullName): $($inner.Message)"
    } else {
        Write-Output "Minimal Campaign.Current ERROR $($_.Exception.GetType().FullName): $($_.Exception.Message)"
    }
}

try {
    $instance = [Activator]::CreateInstance($defaultPerksType)
    Write-Output 'DefaultPerks constructor OK'
} catch {
    $inner = $_.Exception.InnerException
    if ($inner) {
        Write-Output "DefaultPerks constructor ERROR $($inner.GetType().FullName): $($inner.Message)"
    } else {
        Write-Output "DefaultPerks constructor ERROR $($_.Exception.GetType().FullName): $($_.Exception.Message)"
    }
    $instance = [System.Runtime.Serialization.FormatterServices]::GetUninitializedObject($defaultPerksType)
    Write-Output 'Using uninitialized DefaultPerks object'
}
try {
    $campaignType.GetProperty('DefaultPerks', [System.Reflection.BindingFlags]'Public,Instance').SetValue($campaign, $instance)
    Write-Output 'Campaign.DefaultPerks set'
} catch {
    Write-Output "Campaign.DefaultPerks set ERROR $($_.Exception.Message)"
}
foreach ($methodName in @('RegisterAll')) {
    try {
        $method = $defaultPerksType.GetMethod($methodName, [System.Reflection.BindingFlags]'NonPublic,Instance')
        $method.Invoke($instance, $null)
        Write-Output "$methodName OK"
    } catch {
        $inner = $_.Exception.InnerException
        if ($inner) {
            Write-Output "$methodName ERROR $($inner.GetType().FullName): $($inner.Message)"
            Write-Output $inner.StackTrace
        } else {
            Write-Output "$methodName ERROR $($_.Exception.GetType().FullName): $($_.Exception.Message)"
        }
    }
}

$oneHandedType = $asm.GetType('TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultPerks+OneHanded', $true)
$basherProperty = $oneHandedType.GetProperty('Basher', [System.Reflection.BindingFlags]'Public,Static')
try {
    $basher = $basherProperty.GetValue($null)
    if ($null -eq $basher) {
        Write-Output 'Basher is null'
    } else {
        Write-Output 'Basher object:'
        $basher |
            Format-List StringId,Name,RequiredSkillValue,PrimaryRole,SecondaryRole,PrimaryBonus,SecondaryBonus,PrimaryIncrementType,SecondaryIncrementType,PrimaryTroopUsageMask,SecondaryTroopUsageMask,PrimaryDescription,SecondaryDescription
    }
} catch {
    $inner = $_.Exception.InnerException
    if ($inner) {
        Write-Output "Basher ERROR $($inner.GetType().FullName): $($inner.Message)"
        Write-Output $inner.StackTrace
    } else {
        Write-Output "Basher ERROR $($_.Exception.GetType().FullName): $($_.Exception.Message)"
    }
}
