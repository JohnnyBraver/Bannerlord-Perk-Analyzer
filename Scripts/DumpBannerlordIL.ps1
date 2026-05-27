$ErrorActionPreference = 'Stop'

$gameRoot = 'E:\SteamLibrary\steamapps\common\Mount & Blade II Bannerlord'
$bin = Join-Path $gameRoot 'bin\Win64_Shipping_Client'

[System.AppDomain]::CurrentDomain.add_AssemblyResolve({
    param($sender, $args)
    $name = New-Object System.Reflection.AssemblyName($args.Name)
    $candidate = Join-Path $bin ($name.Name + '.dll')
    if (Test-Path -LiteralPath $candidate) {
        return [System.Reflection.Assembly]::LoadFrom($candidate)
    }
    return $null
})

$coreAsm = [System.Reflection.Assembly]::LoadFrom((Join-Path $bin 'TaleWorlds.Core.dll'))
$campaignAsm = [System.Reflection.Assembly]::LoadFrom((Join-Path $bin 'TaleWorlds.CampaignSystem.dll'))

$singleByte = @{}
$doubleByte = @{}
[System.Reflection.Emit.OpCodes].GetFields([System.Reflection.BindingFlags]'Public,Static') | ForEach-Object {
    $op = $_.GetValue($null)
    $value = [int]$op.Value
    if ($value -lt 0) { $value = $value + 65536 }
    if ($value -le 0xff) { $singleByte[$value] = $op } else { $doubleByte[$value -band 0xff] = $op }
}

function Format-Operand {
    param(
        $OpCode,
        [byte[]]$Bytes,
        [ref]$Index
    )
    $module = $script:ResolveModule
    switch ($OpCode.OperandType.ToString()) {
        'InlineNone' { return '' }
        'ShortInlineI' { $v = [sbyte]$Bytes[$Index.Value]; $Index.Value += 1; return $v }
        'InlineI' { $v = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4; return $v }
        'InlineI8' { $v = [BitConverter]::ToInt64($Bytes, $Index.Value); $Index.Value += 8; return $v }
        'ShortInlineR' { $v = [BitConverter]::ToSingle($Bytes, $Index.Value); $Index.Value += 4; return $v }
        'InlineR' { $v = [BitConverter]::ToDouble($Bytes, $Index.Value); $Index.Value += 8; return $v }
        'ShortInlineBrTarget' { $v = [sbyte]$Bytes[$Index.Value]; $Index.Value += 1; return $v }
        'InlineBrTarget' { $v = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4; return $v }
        'InlineSwitch' {
            $count = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            $targets = @()
            for ($n = 0; $n -lt $count; $n++) {
                $targets += [BitConverter]::ToInt32($Bytes, $Index.Value)
                $Index.Value += 4
            }
            return ($targets -join ',')
        }
        'InlineString' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            return '"' + $module.ResolveString($token) + '"'
        }
        'InlineField' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            return $module.ResolveField($token)
        }
        'InlineMethod' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            return $module.ResolveMethod($token)
        }
        'InlineType' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            return $module.ResolveType($token)
        }
        'InlineTok' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            return $module.ResolveMember($token)
        }
        'InlineSig' {
            $token = [BitConverter]::ToInt32($Bytes, $Index.Value); $Index.Value += 4
            return ('sig:' + $token)
        }
        'ShortInlineVar' { $v = $Bytes[$Index.Value]; $Index.Value += 1; return $v }
        'InlineVar' { $v = [BitConverter]::ToUInt16($Bytes, $Index.Value); $Index.Value += 2; return $v }
        default { return '?' }
    }
}

function Dump-Method($type, $methodName) {
    $method = $type.GetMethod($methodName, [System.Reflection.BindingFlags]'Public,NonPublic,Static,Instance')
    Write-Output "METHOD $($type.FullName).$methodName"
    $body = $method.GetMethodBody()
    $bytes = $body.GetILAsByteArray()
    $i = 0
    while ($i -lt $bytes.Length) {
        $offset = $i
        $b = $bytes[$i]
        $i++
        if ($b -eq 0xfe) {
            $op = $doubleByte[[int]$bytes[$i]]
            $i++
        } else {
            $op = $singleByte[[int]$b]
        }
        if ($null -eq $op) {
            '{0:x4}: <unknown {1}>' -f $offset, $b
            continue
        }
        $refI = [ref]$i
        $script:ResolveModule = $method.Module
        $operand = Format-Operand -OpCode $op -Bytes $bytes -Index $refI
        $i = $refI.Value
        '{0:x4}: {1,-14} {2}' -f $offset, $op.Name, $operand
    }
    Write-Output ''
}

Dump-Method ($coreAsm.GetType('TaleWorlds.Core.DefaultSkills', $true)) 'Create'
Dump-Method ($coreAsm.GetType('TaleWorlds.Core.DefaultSkills', $true)) 'get_Instance'
Dump-Method ($coreAsm.GetType('TaleWorlds.Core.DefaultSkills', $true)) 'RegisterAll'
Dump-Method ($coreAsm.GetType('TaleWorlds.Core.DefaultSkills', $true)) 'InitializeAll'
Dump-Method ($campaignAsm.GetType('TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultPerks', $true)) 'Create'
Dump-Method ($campaignAsm.GetType('TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultPerks', $true)) 'get_Instance'
Dump-Method ($campaignAsm.GetType('TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultPerks', $true)) 'RegisterAll'
Dump-Method ($campaignAsm.GetType('TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultPerks', $true)) 'InitializeAll'
Dump-Method ($campaignAsm.GetType('TaleWorlds.CampaignSystem.CharacterDevelopment.DefaultPerks+OneHanded', $true)) 'get_Basher'
