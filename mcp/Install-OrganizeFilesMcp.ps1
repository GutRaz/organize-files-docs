# Install the Organize Files MCP connector for AI assistants (Claude, Cursor, VS Code, etc.) on
# Windows, in a Python environment of its own. Running it again upgrades that environment.
#
#   ORGANIZE_FILES_MCP_HOME  where the environment goes (default %LOCALAPPDATA%\OrganizeFilesMcp\venv)
param(
    [string]$CliPath = "",
    [string]$ReadToken = "",
    [string]$JobsFile = ""
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot

# Runs a program with its output on screen and returns its exit code. Windows PowerShell 5.1 turns a
# program's stderr into a terminating error under "Stop", and pip writes notices there.
function Invoke-Program([string]$Exe, [string[]]$Arguments) {
    $previous = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        & $Exe @Arguments | Out-Host
        return $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $previous
    }
}

# Returns the interpreter's own full path when it is Python 3.10 or newer, otherwise $null. The
# version comes from the interpreter itself; the Microsoft Store placeholder for python.exe fails here.
function Find-Python([string]$Name, [string[]]$Prefix) {
    $command = Get-Command $Name -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $command) {
        return $null
    }
    $previous = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $output = & $command.Source @Prefix -c "import sys; print(sys.executable if sys.version_info >= (3, 10) else '')" 2>$null
        $code = $LASTEXITCODE
    } catch {
        return $null
    } finally {
        $ErrorActionPreference = $previous
    }
    if ($code -ne 0 -or -not $output) {
        return $null
    }
    $path = ([string]($output | Select-Object -Last 1)).Trim()
    if ($path -and (Test-Path -LiteralPath $path -PathType Leaf)) {
        return $path
    }
    return $null
}

$Python = Find-Python "py" @("-3")
if (-not $Python) {
    $Python = Find-Python "python" @()
}
if (-not $Python) {
    Write-Host ""
    Write-Host "Organize Files MCP needs Python 3.10 or newer, and none was found."
    Write-Host "Next step: install Python 3.12 from https://www.python.org/downloads/windows/ and tick Add python.exe to PATH, then run this script again."
    exit 1
}

$VenvHome = $env:ORGANIZE_FILES_MCP_HOME
if (-not $VenvHome) {
    $VenvHome = Join-Path $env:LOCALAPPDATA "OrganizeFilesMcp\venv"
}
$VenvHome = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($VenvHome)
$VenvPython = Join-Path $VenvHome "Scripts\python.exe"

if ((Test-Path -LiteralPath $VenvHome) -and
    -not (Test-Path -LiteralPath (Join-Path $VenvHome "pyvenv.cfg")) -and
    (Get-ChildItem -LiteralPath $VenvHome -Force | Select-Object -First 1)) {
    Write-Host "$VenvHome exists and is not a Python environment. Set ORGANIZE_FILES_MCP_HOME to another folder."
    exit 1
}

$reuse = $false
if (Test-Path -LiteralPath $VenvPython -PathType Leaf) {
    $previous = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        & $VenvPython -m pip --version *> $null
        $reuse = ($LASTEXITCODE -eq 0)
    } finally {
        $ErrorActionPreference = $previous
    }
}

if ($reuse) {
    Write-Host "Upgrading the environment at $VenvHome"
} else {
    $existed = Test-Path -LiteralPath $VenvHome
    Write-Host "Creating the environment at $VenvHome with $Python"
    if ((Invoke-Program $Python @("-m", "venv", "--clear", $VenvHome)) -ne 0) {
        if (-not $existed) {
            Remove-Item -LiteralPath $VenvHome -Recurse -Force -ErrorAction SilentlyContinue
        }
        Write-Host ""
        Write-Host "Python could not create the environment. The error is above."
        exit 1
    }
}

if ((Invoke-Program $VenvPython @("-m", "pip", "install", "--upgrade", "--prefer-binary", "--disable-pip-version-check", $Root)) -ne 0) {
    Write-Host ""
    Write-Host "pip could not install the connector. The error is above."
    exit 1
}

# Load the server itself, with -I so the source folder next to this script cannot stand in for the
# installed copy. Importing cli_runner alone passed on installs whose MCP library could not load it.
if ((Invoke-Program $VenvPython @("-I", "-c", "import organize_files_mcp.server")) -ne 0) {
    Write-Host ""
    Write-Host "The connector was installed but does not load. The error is above."
    exit 1
}

$JsonPython = $VenvPython.Replace("\", "/")
Write-Host ""
Write-Host "Organize Files MCP is installed in $VenvHome"
Write-Host ""
Write-Host "The AI app starts it with this Python, by its full path:"
Write-Host "  `"command`": `"$JsonPython`","
Write-Host "  `"args`": [`"-m`", `"organize_files_mcp`"]"
Write-Host ""
Write-Host "Configure the AI client from MCP setup in the Organize Files app. The AI assistant (MCP) chapter of its Documentation has every step."
Write-Host "Examples: $Root\examples\"
Write-Host ""
Write-Host "Check the install at any time:"
Write-Host "  & `"$VenvPython`" -I -c `"import organize_files_mcp.server; print('ok')`""
if ($CliPath) {
    Write-Host ""
    Write-Host "Suggested MCP env:"
    Write-Host "  ORGANIZE_FILES_CLI=$CliPath"
}
if ($ReadToken) {
    Write-Host "  ORGANIZE_FILES_MCP_READ_TOKEN=(set in your MCP config, not echoed here)"
}
if ($JobsFile) {
    Write-Host "  ORGANIZE_FILES_JOBS_FILE=$JobsFile"
}
