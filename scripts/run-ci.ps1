param(
    [string]$Python,
    [switch]$SkipRequirementsInstall
)

$ErrorActionPreference = "Stop"
$isWindowsPlatform = $env:OS -eq "Windows_NT"
$repoRoot = Split-Path -Parent $PSScriptRoot
$smokeScript = "0,4,8"

function Get-AppVersion {
    $pyproject = Join-Path $repoRoot "pyproject.toml"
    if (-not (Test-Path $pyproject)) {
        return "0.0.0"
    }
    foreach ($line in Get-Content -Path $pyproject) {
        if ($line -match '^version\s*=\s*"(?<ver>[^"]+)"') {
            return $Matches['ver']
        }
    }
    return "0.0.0"
}

$appVersion = Get-AppVersion
$installDirName = "yourapp-starter-$appVersion"
$ciInstallDir = Join-Path ([System.IO.Path]::GetTempPath()) $installDirName

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

Push-Location $repoRoot
try {
    if (-not $SkipRequirementsInstall) {
        Invoke-Step -Label "Syncing requirements (installs -e . automatically)" -Operation {
            Invoke-PythonModule -Module pip -Arguments @("install", "-r", "requirements.txt")
        }
    }

    Invoke-Step -Label "Formatting (black --check)" -Operation {
        Invoke-PythonModule -Module black -Arguments @("--check", "src", "tests")
    }

    Invoke-Step -Label "Linting (ruff check)" -Operation {
        Invoke-PythonModule -Module ruff -Arguments @("check", "src", "tests")
    }

    Invoke-Step -Label "Type checking (mypy)" -Operation {
        Invoke-PythonModule -Module mypy -Arguments @("src")
    }

    Invoke-Step -Label "Pytest (non-GUI markers)" -Operation {
        Invoke-PythonModule -Module pytest -Arguments @("tests", "-m", "not gui", "--maxfail=1", "--disable-warnings", "-q")
    }

    Invoke-Step -Label "Pytest (GUI markers)" -Operation {
        Invoke-PythonModule -Module pytest -Arguments @("tests/test_gui.py", "-m", "gui", "-q")
    }

    if ($isWindowsPlatform) {
        Invoke-Step -Label "Build installer bundle" -Operation {
            & (Join-Path $repoRoot "wheel-builder.bat") "--ci" "--no-pause"
            if ($LASTEXITCODE -ne 0) {
                throw "wheel-builder.bat failed with exit code $LASTEXITCODE"
            }
        }

        Invoke-Step -Label "installation.bat smoke test" -Operation {
            & cmd /c (Join-Path $repoRoot "dist\installation.bat")
            if ($LASTEXITCODE -ne 0) {
                throw "installation.bat failed with exit code $LASTEXITCODE"
            }
        }

        Invoke-Step -Label "Cleanup CI install directory" -Operation {
            if (Test-Path $ciInstallDir) {
                Remove-Item -LiteralPath $ciInstallDir -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
    }
    else {
        Invoke-Step -Label "Build wheel bundle" -Operation {
            Invoke-PythonModule -Module build -Arguments @("--wheel")
        }

        $wheelPath = Get-ChildItem -Path (Join-Path $repoRoot "dist") -Filter *.whl | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if (-not $wheelPath) {
            throw "Wheel artifact not found in dist after build step."
        }

        $sandboxRoot = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())

        Invoke-Step -Label "Create sandbox virtual environment" -Operation {
            Invoke-PythonModule -Module venv -Arguments @($sandboxRoot)
        }

        $sandboxPython = Join-Path $sandboxRoot "bin/python"

        Invoke-Step -Label "Install wheel into sandbox" -Operation {
            & $sandboxPython -m pip install $wheelPath.FullName
            if ($LASTEXITCODE -ne 0) {
                throw "pip install of $($wheelPath.Name) failed with exit code $LASTEXITCODE"
            }
        }

        Invoke-Step -Label "Installer smoke test (service UI)" -Operation {
            & $sandboxPython -m tictactoe --ui service --script $smokeScript --quiet --label ci-smoke
            if ($LASTEXITCODE -ne 0) {
                throw "Service UI smoke test failed with exit code $LASTEXITCODE"
            }
        }

        Invoke-Step -Label "Cleanup sandbox" -Operation {
            if (Test-Path $sandboxRoot) {
                Remove-Item -LiteralPath $sandboxRoot -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
    }
}
finally {
    Pop-Location
}

Write-Host "`nAll local CI checks completed successfully." -ForegroundColor Green
