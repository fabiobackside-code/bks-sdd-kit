# Prova que a reformatacao de um script SQL mudou so o layout: compara os tokens do HEAD com os da copia de trabalho.
# EXEC vale pela forma nomeada; DECLARE vale pelo conjunto de variaveis, com o valor inicial como SET no lugar.
# Uso: Comparar-Layout.ps1 [-Raizes app/sql] [-Arquivos <caminho>...] [-Referencia HEAD]
# Saida: uma linha por arquivo (igual | DIVERGE no token | SEM CR) e o total; codigo 1 quando algum nao confere.
param(
    [string[]]$Raizes = @('app/sql'),
    [string[]]$Arquivos,
    [string]$Referencia = 'HEAD'
)

$ErrorActionPreference = 'Stop'
$root = (git rev-parse --show-toplevel).Trim()
$sqlRoots = $Raizes

$tokenPattern = [regex]'(?s)(?<c>/\*.*?\*/|--[^\n]*)|(?<s>N?''(?:[^'']|'''')*'')|(?<b>\[[^\]]*\])|(?<w>@@?\w+|#{0,2}\w+(?:\.\d+)?)|(?<o><>|<=|>=|!=|\S)'

function Get-Tokens([string]$Text) {
    $list = New-Object System.Collections.Generic.List[string]
    foreach ($m in $tokenPattern.Matches($Text)) {
        if ($m.Groups['c'].Success) { continue }
        if ($m.Groups['s'].Success -or $m.Groups['b'].Success) { $list.Add($m.Value) }
        else { $list.Add($m.Value.ToUpperInvariant()) }
    }
    return , $list
}

function Get-HeadText([string]$RelativePath) {
    $text = git -C $root show "${Referencia}:$RelativePath" 2>$null
    if ($LASTEXITCODE -ne 0) { return $null }
    return ($text -join "`n")
}

# Assinaturas: nome da procedure -> parametros na ordem declarada, lidos dos scripts da referencia.
$signatures = @{}
foreach ($dir in $sqlRoots) {
    foreach ($path in (git -C $root ls-tree -r --name-only $Referencia -- $dir | Where-Object { $_ -like '*.sql' })) {
        $t = Get-Tokens (Get-HeadText $path)
        for ($i = 0; $i -lt $t.Count - 2; $i++) {
            if ($t[$i] -ne 'CREATE' -or ($t[$i + 1] -ne 'PROCEDURE' -and $t[$i + 1] -ne 'PROC')) { continue }
            $j = $i + 2
            $name = $t[$j]
            while ($t[$j + 1] -eq '.') { $j += 2; $name = $t[$j] }
            $params = New-Object System.Collections.Generic.List[string]
            $depth = 0; $expectParam = $true
            for ($k = $j + 1; $k -lt $t.Count -and $t[$k] -ne 'AS'; $k++) {
                if ($t[$k] -eq '(') { $depth++; continue }
                if ($t[$k] -eq ')') { $depth--; continue }
                if ($depth -eq 0 -and $t[$k] -eq ',') { $expectParam = $true; continue }
                if ($expectParam -and $t[$k].StartsWith('@')) { $params.Add($t[$k]); $expectParam = $false }
            }
            $signatures[$name] = $params
        }
    }
}

function Test-ArgumentStart([string]$Token) {
    if ($Token -eq 'NULL' -or $Token -eq 'DEFAULT') { return $true }
    return $Token -match "^(@|N?'|[-+]|\d)"
}

# Reescreve cada EXEC na forma canonica: retorno, nome e argumentos nomeados em ordem alfabetica.
function ConvertTo-Canonical([System.Collections.Generic.List[string]]$t) {
    $out = New-Object System.Collections.Generic.List[string]
    $i = 0
    while ($i -lt $t.Count) {
        if ($t[$i] -ne 'EXEC' -and $t[$i] -ne 'EXECUTE') { $out.Add($t[$i]); $i++; continue }
        $j = $i + 1
        $ret = ''
        if ($t[$j].StartsWith('@') -and $t[$j + 1] -eq '=') { $ret = $t[$j]; $j += 2 }
        if ($t[$j] -eq '(' -or $t[$j].StartsWith('@') -or $t[$j] -match "^N?'") { $out.Add($t[$i]); $i++; continue }
        $name = $t[$j]
        while ($t[$j + 1] -eq '.') { $j += 2; $name = $t[$j] }
        $j++
        $signature = $signatures[$name]
        $arguments = New-Object System.Collections.Generic.List[string]
        $position = 0
        if ($j -lt $t.Count -and (Test-ArgumentStart $t[$j])) {
            while ($true) {
                $argName = $null
                if ($t[$j].StartsWith('@') -and $t[$j + 1] -eq '=') { $argName = $t[$j]; $j += 2 }
                $value = $t[$j]; $j++
                if (($value -eq '-' -or $value -eq '+') -and $j -lt $t.Count) { $value += $t[$j]; $j++ }
                $output = ''
                if ($j -lt $t.Count -and ($t[$j] -eq 'OUTPUT' -or $t[$j] -eq 'OUT')) { $output = ' OUTPUT'; $j++ }
                if (-not $argName) {
                    $argName = if ($signature -and $position -lt $signature.Count) { $signature[$position] } else { "#$position" }
                }
                $arguments.Add("$argName=$value$output")
                $position++
                if ($j -lt $t.Count -and $t[$j] -eq ',') { $j++ } else { break }
            }
        }
        $sorted = $arguments | Sort-Object
        $out.Add("EXEC{$ret|$name|$($sorted -join ';')}")
        $i = $j
    }
    return , $out
}

# Separa as declaracoes: cada DECLARE vira o par (variavel:tipo) num conjunto, e o valor inicial vira SET no lugar.
$statementStart = @('SELECT', 'SET', 'IF', 'ELSE', 'EXEC', 'EXECUTE', 'DECLARE', 'BEGIN', 'END', 'RETURN', 'WHILE',
    'INSERT', 'UPDATE', 'DELETE', 'MERGE', 'THROW', 'RAISERROR', 'PRINT', 'COMMIT', 'ROLLBACK', 'WITH', 'OPEN',
    'FETCH', 'CLOSE', 'DEALLOCATE', 'GOTO', 'BREAK', 'CONTINUE', 'TRUNCATE', 'GO')
function Split-Declarations([System.Collections.Generic.List[string]]$t) {
    $out = New-Object System.Collections.Generic.List[string]
    $declared = New-Object System.Collections.Generic.List[string]
    $i = 0
    while ($i -lt $t.Count) {
        if ($t[$i] -ne 'DECLARE' -or -not $t[$i + 1].StartsWith('@')) {
            if ($t[$i] -ne ';') { $out.Add($t[$i]) }
            $i++; continue
        }
        $i++
        while ($true) {
            $name = $t[$i]; $i++
            if ($t[$i] -eq 'AS') { $i++ }
            $type = New-Object System.Collections.Generic.List[string]
            $type.Add($t[$i]); $i++
            if ($i -lt $t.Count -and $t[$i] -eq '(') {
                $d = 0
                do { if ($t[$i] -eq '(') { $d++ } elseif ($t[$i] -eq ')') { $d-- }; $type.Add($t[$i]); $i++ } while ($d -gt 0)
            }
            $declared.Add("${name}:$($type -join ' ')")
            if ($i -lt $t.Count -and $t[$i] -eq '=') {
                $i++
                $out.Add('SET'); $out.Add($name); $out.Add('=')
                $d = 0; $case = 0
                while ($i -lt $t.Count) {
                    $tok = $t[$i]
                    if ($d -eq 0 -and $case -eq 0 -and ($tok -eq ',' -or $tok -eq ';' -or $statementStart -contains $tok)) { break }
                    if ($tok -eq '(') { $d++ } elseif ($tok -eq ')') { $d-- }
                    elseif ($tok -eq 'CASE') { $case++ } elseif ($tok -eq 'END' -and $case -gt 0) { $case-- }
                    $out.Add($tok); $i++
                }
            }
            if ($i -lt $t.Count -and $t[$i] -eq ',') { $i++; continue }
            break
        }
    }
    $out.Add('DECLARADAS{' + (($declared | Sort-Object) -join ';') + '}')
    return , $out
}

if (-not $Arquivos) {
    $Arquivos = git -C $root diff --name-only $Referencia -- $sqlRoots | Where-Object { $_ -like '*.sql' }
}

$failures = 0
foreach ($file in $Arquivos) {
    $full = if ([IO.Path]::IsPathRooted($file)) { $file } else { Join-Path $root $file }
    $full = [IO.Path]::GetFullPath($full)
    $relative = $full.Substring([IO.Path]::GetFullPath($root).TrimEnd('\', '/').Length + 1).Replace('\', '/')
    $work = [IO.File]::ReadAllText($full)
    $head = Get-HeadText $relative
    if ($null -eq $head) { "{0,-70} NOVO (sem referencia)" -f $relative; continue }

    $bareLf = ([regex]::Matches($work, '(?<!\r)\n')).Count
    $a = Split-Declarations (ConvertTo-Canonical (Get-Tokens $head))
    $b = Split-Declarations (ConvertTo-Canonical (Get-Tokens $work))
    $n = [Math]::Min($a.Count, $b.Count)
    $diff = -1
    for ($k = 0; $k -lt $n; $k++) { if ($a[$k] -cne $b[$k]) { $diff = $k; break } }
    if ($diff -lt 0 -and $a.Count -ne $b.Count) { $diff = $n }

    if ($diff -ge 0) {
        $failures++
        $left = ($a | Select-Object -Skip $diff -First 3) -join ' '
        $right = ($b | Select-Object -Skip $diff -First 3) -join ' '
        "{0,-70} DIVERGE no token {1}: HEAD [{2}] x trabalho [{3}]" -f $relative, $diff, $left, $right
    }
    elseif ($bareLf -gt 0) { $failures++; "{0,-70} SEM CR em {1} linha(s)" -f $relative, $bareLf }
    else { "{0,-70} igual" -f $relative }
}
"TOTAL: $($Arquivos.Count) arquivo(s), $failures sem conferir"
if ($failures -gt 0) { exit 1 }
