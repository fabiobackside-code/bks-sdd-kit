# Confere o formato das procedures e functions: um item por linha em DECLARE, SELECT de atribuicao e EXEC nomeado.
# Uso: Conferir-Formato.ps1 [-Pasta app/sql] [-Arquivos <caminho>...]
# Saida: uma linha por achado (arquivo:linha [regra] trecho) e o total; codigo 1 quando ha achado.
param(
    [string]$Pasta = 'app/sql',
    [string[]]$Arquivos
)

$ErrorActionPreference = 'Stop'
$root = (git rev-parse --show-toplevel).Trim().Replace('/', '\')
if (-not $Arquivos) {
    $Arquivos = Get-ChildItem (Join-Path $root $Pasta) -Recurse -Filter *.sql |
        Where-Object { $_.FullName -match '\\(procedures|functions)\\' } | ForEach-Object { $_.FullName }
}

$type = '[A-Za-z]+(\s*\(\s*(\d+|MAX)\s*(,\s*\d+\s*)?\))?'
$rules = @(
    @{ Nome = 'DECLARE com mais de uma variavel na linha'; Padrao = "@\w+\s+$type(\s*=\s*[^,;]+?)?\s*,\s*@\w+\s+$type" },
    @{ Nome = 'mais de uma atribuicao ou argumento nomeado na linha'; Padrao = '@\w+\s*=\s*[^,;=]+?(\s+OUTPUT)?\s*,\s*@\w+\s*=' },
    @{ Nome = 'EXEC posicional'; Padrao = '\bEXEC(UTE)?\s+(@\w+\s*=\s*)?(dbo\.)?\w+\s+(@\w+|-?\d+|NULL|'''')\s*(OUTPUT\s*)?(,|;|$)' },
    @{ Nome = 'argumento posicional de saida'; Padrao = '@\w+\s+OUTPUT\s*,\s*@\w+(\s+OUTPUT)?\s*[,;]' }
)

$setRule = '(^|[^@\w])\[?\w+\]?\s*=\s*[^,;=]+?\s*,\s*\[?\w+\]?\s*=(?!=)'

$total = 0
foreach ($file in $Arquivos) {
    $inList = $false
    $depth = 0
    $full = [IO.Path]::GetFullPath($file)
    $relative = if ($full.StartsWith($root, [StringComparison]::OrdinalIgnoreCase)) { $full.Substring($root.Length + 1).Replace('\', '/') } else { $full }
    $inBlock = $false
    $n = 0
    foreach ($raw in [IO.File]::ReadAllLines($full)) {
        $n++
        $line = $raw
        if ($inBlock) {
            if ($line -match '\*/') { $inBlock = $false; $line = $line.Substring($line.IndexOf('*/') + 2) } else { continue }
        }
        if ($line -match '/\*' -and $line -notmatch '\*/') { $inBlock = $true; $line = $line.Substring(0, $line.IndexOf('/*')) }
        $line = ($line -replace "N?'(?:[^']|'')*'", "''") -replace '--.*$', ''

        # Lista de colunas do INSERT e linha do VALUES: um item por linha.
        if (-not $inList -and $line -match '\b(INSERT\s+(INTO\s+)?[\w.\[\]#@]+|VALUES)\s*\(' -and $line -notmatch '\(\s*VALUES') { $inList = $true; $depth = 0 }
        if ($inList) {
            $flat = $line -replace '\([^()]*\)', ''
            if (($flat -replace '^\s*,', '') -match '\S\s*,\s*\S') {
                $total++
                "{0}:{1} [{2}] {3}" -f $relative, $n, 'lista de INSERT ou VALUES com mais de um item na linha', $raw.Trim()
            }
            $depth += ([regex]::Matches($line, '\(')).Count - ([regex]::Matches($line, '\)')).Count
            if ($depth -le 0) { $inList = $false }
            continue
        }

        # SET de UPDATE com mais de uma coluna na linha.
        if ($line -match $setRule -and $line -notmatch '@\w+\s*=') {
            $total++
            "{0}:{1} [{2}] {3}" -f $relative, $n, 'SET de UPDATE com mais de uma coluna na linha', $raw.Trim()
            continue
        }

        if ($line -match '^\s*,?\s*(SET|IF|WHEN|THEN|AND|OR|WHERE|ON|RETURN)\b') { continue }
        if ($line -match '\b(ISNULL|COALESCE|CONCAT|JSON_MODIFY|DATEDIFF|FORMAT|NULLIF|IIF)\s*\(') { continue }
        foreach ($rule in $rules) {
            if ($line -match $rule.Padrao) {
                $total++
                "{0}:{1} [{2}] {3}" -f $relative, $n, $rule.Nome, $raw.Trim()
                break
            }
        }
    }
}
"TOTAL: $total achado(s) em $(@($Arquivos).Count) arquivo(s)"
if ($total -gt 0) { exit 1 }
