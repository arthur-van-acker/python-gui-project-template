param(
    [string]$Python,
    [switch]$SkipRequirementsInstall
)

$ErrorActionPreference = "Stop"
$isWindowsPlatform = $env:OS -eq "Windows_NT"
$repoRoot = Split-Path -Parent $PSScriptRoot

function Get-DefaultPython {
    if ($env:VIRTUAL_ENV) {
        if ($isWindowsPlatform) {
            return (Join-Path $env:VIRTUAL_ENV "Scripts\python.exe")
        }
        return (Join-Path $env:VIRTUAL_ENV "bin/python")
    }
    $embeddedVenv = Join-Path $repoRoot ".venv"
    if (Test-Path $embeddedVenv) {
        $winCandidate = Join-Path $embeddedVenv "Scripts\python.exe"
        $posixCandidate = Join-Path $embeddedVenv "bin/python"
        if ($isWindowsPlatform -and (Test-Path $winCandidate)) {
            return $winCandidate
        }
        if (-not $isWindowsPlatform -and (Test-Path $posixCandidate)) {
            return $posixCandidate
        }
        if (Test-Path $winCandidate) {
            return $winCandidate
        }
        if (Test-Path $posixCandidate) {
            return $posixCandidate
        }
    }
    return "python"
}

if (-not $PSBoundParameters.ContainsKey('Python') -or [string]::IsNullOrWhiteSpace($Python)) {
    $Python = Get-DefaultPython
}

function Invoke-Step {
    param(
        [string]$Label,
        [scriptblock]$Operation
    )

    Write-Host "`n>>> $Label" -ForegroundColor Cyan
    & $Operation
}

function Invoke-PythonModule {
    param(
        [string]$Module,
        [string[]]$Arguments = @()
    )

    & $Python -m $Module @Arguments
    if ($LASTEXITCODE -ne 0) {
        $joinedArgs = if ($Arguments.Length -gt 0) { [string]::Join(' ', $Arguments) } else { '' }
        throw "Command '$Python -m $Module $joinedArgs' failed with exit code $LASTEXITCODE"
    }
}

Write-Host "Running local CI checks with $Python" -ForegroundColor Green

if (-not $SkipRequirementsInstall) {
    Invoke-Step -Label "Syncing requirements (installs -e . automatically)" -Operation {
        Invoke-PythonModule -Module pip -Arguments @("install", "-r", "requirements.txt")
    }
}

Invoke-Step -Label "Tox lint/type/test matrix" -Operation {
    Invoke-PythonModule -Module tox -Arguments @("-e", "lint,type,py313")
}

Write-Host "`nAll local CI checks completed successfully." -ForegroundColor Green
