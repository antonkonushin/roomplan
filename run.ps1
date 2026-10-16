param([int]$Port = 8765)
$ErrorActionPreference = 'Stop'
$pythonPath = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (!(Test-Path -LiteralPath $pythonPath)) {
    $bundledPython = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
    if (Test-Path -LiteralPath $bundledPython) { $pythonPath = $bundledPython } else { $pythonPath = 'python' }
}
Push-Location $PSScriptRoot
try { & $pythonPath server.py --port $Port } finally { Pop-Location }
