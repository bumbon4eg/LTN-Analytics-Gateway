param(
    [string]$PythonVersion = "3.12",
    [string]$IconPath = "assets\LTN_Analytics_Gateway.ico"
)

$ErrorActionPreference = "Stop"
$repositoryRoot = $PSScriptRoot
$environmentPath = Join-Path $repositoryRoot ".venv"
$pythonPath = Join-Path $environmentPath "Scripts\python.exe"
$requirementsPath = Join-Path $repositoryRoot "requirements-build.txt"
$entryPoint = Join-Path $repositoryRoot "main.py"
$distPath = Join-Path $repositoryRoot "dist"
$buildPath = Join-Path $repositoryRoot "build"

if (-not [System.IO.Path]::IsPathRooted($IconPath)) {
    $IconPath = Join-Path $repositoryRoot $IconPath
}

if (-not (Test-Path -LiteralPath $IconPath -PathType Leaf)) {
    throw "Application icon not found: $IconPath"
}
if ([System.IO.Path]::GetExtension($IconPath) -ine ".ico") {
    throw "Application icon must be an .ico file: $IconPath"
}

if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
    $launcher = Get-Command py -ErrorAction SilentlyContinue
    if (-not $launcher) {
        throw "Python Launcher for Windows was not found. Install Python $PythonVersion and retry."
    }

    & $launcher.Source "-$PythonVersion" -m venv $environmentPath
    if ($LASTEXITCODE -ne 0) {
        throw "Could not create the project virtual environment with Python $PythonVersion."
    }
}

$installedVersion = & $pythonPath -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
if ($LASTEXITCODE -ne 0) {
    throw "Could not inspect the project virtual environment's Python version."
}
if ($installedVersion.Trim() -ne $PythonVersion) {
    throw "The project .venv uses Python $($installedVersion.Trim()); Python $PythonVersion is required. Remove .venv and retry."
}

& $pythonPath -m pip install -r $requirementsPath
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install the pinned application and build dependencies."
}

Push-Location $repositoryRoot
try {
    & $pythonPath -m PyInstaller `
        --noconfirm `
        --clean `
        --onefile `
        --windowed `
        --name "LTN_Analytics_Gateway" `
        --icon $IconPath `
        --paths $repositoryRoot `
        --hidden-import ui.app `
        --collect-all asyncpg `
        --distpath $distPath `
        --workpath $buildPath `
        --specpath $buildPath `
        $entryPoint

    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller failed to build the release executable."
    }
}
finally {
    Pop-Location
}

$executablePath = Join-Path $distPath "LTN_Analytics_Gateway.exe"
if (-not (Test-Path -LiteralPath $executablePath -PathType Leaf)) {
    throw "Build finished without producing the expected executable: $executablePath"
}

Write-Host "Release executable created: $executablePath"
