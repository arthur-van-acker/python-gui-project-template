@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ---------------------------------------------------------------------------
REM Argument parsing
REM ---------------------------------------------------------------------------
set "CI_MODE=0"
set "INSTALL_ROOT_OVERRIDE="
set "SKIP_PAUSE="

:parse_args
if "%~1"=="" goto args_done
if /I "%~1"=="--ci" (
    set "CI_MODE=1"
    set "SKIP_PAUSE=1"
) else if /I "%~1"=="--install-root" (
    shift
    if "%~1"=="" (
        echo --install-root requires a path to follow it.
        exit /b 1
    )
    set "INSTALL_ROOT_OVERRIDE=%~1"
) else if /I "%~1"=="--no-pause" (
    set "SKIP_PAUSE=1"
) else (
    echo Unknown option %~1
    exit /b 1
)
shift
goto parse_args

:args_done

REM ---------------------------------------------------------------------------
REM Metadata
REM ---------------------------------------------------------------------------
set "APP_VERSION="
for /f "tokens=3 delims== " %%v in ('findstr /R /C:"^version = " pyproject.toml') do (
    set "APP_VERSION=%%~v"
    goto version_found
)
:version_found
if not defined APP_VERSION set "APP_VERSION=0.0.0"

set "PRODUCT_NAME=YourApp Starter"
set "APP_SLUG=yourapp-starter"
set "INSTALL_DIR_NAME=%APP_SLUG%-%APP_VERSION%"
set "SHORTCUT_NAME=YourApp Starter.lnk"
set "SMOKE_SCRIPT=0,4,8"

if defined INSTALL_ROOT_OVERRIDE (
    set "INSTALL_ROOT=%INSTALL_ROOT_OVERRIDE%"
) else if "%CI_MODE%"=="1" (
    set "INSTALL_ROOT=%TEMP%\%INSTALL_DIR_NAME%"
) else if defined LOCALAPPDATA (
    set "INSTALL_ROOT=%LOCALAPPDATA%\Programs\%INSTALL_DIR_NAME%"
) else (
    set "INSTALL_ROOT=%USERPROFILE%\AppData\Local\Programs\%INSTALL_DIR_NAME%"
)

echo Building wheel for %PRODUCT_NAME% v%APP_VERSION%
echo Installation target: %INSTALL_ROOT%
echo.

REM ---------------------------------------------------------------------------
REM Setup environment
REM ---------------------------------------------------------------------------
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist src\tictactoe.egg-info rmdir /s /q src\tictactoe.egg-info

python -m build --wheel
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

if not exist dist (
    echo ERROR: dist folder missing after build.
    exit /b 1
)

for %%f in (dist\*.whl) do set "WHEEL_FILE=%%~nxf"
if not defined WHEEL_FILE (
    echo ERROR: Wheel artifact not found.
    exit /b 1
)

if exist src\tictactoe\assets (
    if exist dist\assets rmdir /s /q dist\assets
    xcopy /E /I /Y "src\tictactoe\assets" "dist\assets" >nul
    echo Copied assets folder into dist\assets
) else (
    echo WARNING: src\tictactoe\assets missing.
)

if exist src\tictactoe\assets\favicon.ico (
    copy /Y src\tictactoe\assets\favicon.ico dist\ >nul
)

REM ---------------------------------------------------------------------------
REM Write installation.bat
REM ---------------------------------------------------------------------------
(
echo @echo off
echo setlocal enabledelayedexpansion
echo set "PRODUCT_NAME=%PRODUCT_NAME%"
echo set "PRODUCT_VERSION=%APP_VERSION%"
echo set "INSTALL_DIR=%INSTALL_ROOT%"
echo set "SHORTCUT_NAME=%SHORTCUT_NAME%"
echo set "WHEEL_FILE=%WHEEL_FILE%"
echo set "ASSET_SOURCE=%%~dp0assets"
echo.
echo echo Installing !PRODUCT_NAME! v!PRODUCT_VERSION!
echo echo Target directory: !INSTALL_DIR!
echo echo.
echo if exist "!INSTALL_DIR!" ^(
echo     echo Found prior installation. Removing it...
echo     rmdir /s /q "!INSTALL_DIR!"
echo ^)
echo mkdir "!INSTALL_DIR!"
echo.
echo echo Copying release bundle...
echo xcopy /E /I /Y "%%~dp0*.*" "!INSTALL_DIR!\" ^>nul
echo.
echo echo Creating isolated virtual environment...
echo python -m venv "!INSTALL_DIR!\.venv"
echo if errorlevel 1 ^(
echo     echo Failed to create the virtual environment. Aborting install.
echo     exit /b 1
echo ^)
echo call "!INSTALL_DIR!\.venv\Scripts\activate.bat"
echo echo Installing wheel package...
echo pip install "!INSTALL_DIR!\!WHEEL_FILE!"
echo if errorlevel 1 ^(
echo     echo Package installation failed.
echo     exit /b 1
echo ^)
echo.
echo if exist "!ASSET_SOURCE!" ^(
echo     echo Copying assets...
echo     xcopy /E /I /Y "!ASSET_SOURCE!" "!INSTALL_DIR!\assets" ^>nul
echo ^)
echo.
echo echo Running post-install smoke test...
echo call "!INSTALL_DIR!\.venv\Scripts\python.exe" -m tictactoe --ui service --script %SMOKE_SCRIPT% --quiet --label installer-smoke
echo if errorlevel 1 ^(
echo     echo Smoke test failed. Installation aborted.
echo     exit /b 1
echo ^)
echo echo Smoke test passed.
echo.
echo echo Creating desktop shortcut...
echo for /f "usebackq tokens=3*" %%%%A in ^(`reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop`^) do set DESKTOP=%%%%A %%%%B
echo set DESKTOP=%%DESKTOP:~0,-1%%
echo if "%%DESKTOP:~-1%%"==" " set DESKTOP=%%DESKTOP:~0,-1%%
echo call set DESKTOP=%%DESKTOP%%
echo set SCRIPT_DIR=!INSTALL_DIR!\
echo set ICON_PATH=%%SCRIPT_DIR%%favicon.ico
echo set VBS_PATH=%%SCRIPT_DIR%%tic-tac-toe-starter.vbs
echo echo Set oWS = CreateObject("WScript.Shell"^) ^> "%%TEMP%%\create_yourapp_shortcut.vbs"
echo echo sLinkFile = "%%DESKTOP%%\!SHORTCUT_NAME!" ^>^> "%%TEMP%%\create_yourapp_shortcut.vbs"
echo echo Set oLink = oWS.CreateShortcut(sLinkFile^) ^>^> "%%TEMP%%\create_yourapp_shortcut.vbs"
echo echo oLink.TargetPath = "%%VBS_PATH%%" ^>^> "%%TEMP%%\create_yourapp_shortcut.vbs"
echo echo oLink.IconLocation = "%%ICON_PATH%%" ^>^> "%%TEMP%%\create_yourapp_shortcut.vbs"
echo echo oLink.WorkingDirectory = "%%SCRIPT_DIR%%" ^>^> "%%TEMP%%\create_yourapp_shortcut.vbs"
echo echo oLink.Save ^>^> "%%TEMP%%\create_yourapp_shortcut.vbs"
echo cscript //nologo "%%TEMP%%\create_yourapp_shortcut.vbs"
echo del "%%TEMP%%\create_yourapp_shortcut.vbs"
echo.
echo echo Writing install manifest...
echo powershell -NoProfile -Command "$manifest = @{ ProductName = '!PRODUCT_NAME!'; Version = '!PRODUCT_VERSION!'; InstallDir = '!INSTALL_DIR!'; Wheel = '!WHEEL_FILE!' }; $manifest | ConvertTo-Json -Depth 2 | Set-Content -Path '!INSTALL_DIR!\install-info.json' -Encoding UTF8"
echo.
echo echo Installation complete!
echo echo Shortcut created: !SHORTCUT_NAME!
echo echo To uninstall, remove !INSTALL_DIR! and the desktop shortcut.
echo exit /b 0
) > dist\installation.bat

REM ---------------------------------------------------------------------------
REM Write launcher script (relative paths)
REM ---------------------------------------------------------------------------
(
echo Dim fso, root, shell
echo Set fso = CreateObject("Scripting.FileSystemObject")
echo root = fso.GetParentFolderName(WScript.ScriptFullName)
echo Set shell = CreateObject("WScript.Shell")
echo shell.Run """" ^& root ^& "\\.venv\\Scripts\\pythonw.exe"" -m tictactoe", 0
echo Set shell = Nothing
echo Set fso = Nothing
) > dist\tic-tac-toe-starter.vbs

REM ---------------------------------------------------------------------------
REM Documentation artifacts
REM ---------------------------------------------------------------------------
(
echo %PRODUCT_NAME% Template
echo Copyright (c) 2025 Arthur van Acker
echo.
echo Permission to use, copy, modify, and/or distribute this software for any
echo purpose with or without fee is hereby granted.
echo.
echo THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
echo WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
echo MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
echo ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
echo WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
echo ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR
echo IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
) > dist\license.txt

(
echo How to install %PRODUCT_NAME%
echo ================================
echo.
echo 1. Unzip the release bundle.
echo 2. Double-click `installation.bat`.
echo 3. Wait for the smoke test to pass.
echo 4. Launch the "!SHORTCUT_NAME!" shortcut.
echo.
echo What the installer does
echo -----------------------
echo - Installs into %%LOCALAPPDATA%%\Programs\%INSTALL_DIR_NAME% by default.
echo - Creates a private virtual environment and installs %WHEEL_FILE%.
echo - Copies assets (icons, JSON, etc.) beside the binaries.
echo - Runs a non-interactive smoke test (`python -m tictactoe --ui service`).
echo - Drops a JSON manifest (`install-info.json`) for inventory scripts.
echo.
echo Need screenshots or troubleshooting tips?
echo https://github.com/arthur-van-acker/tic-tac-toe/blob/main/docs/INSTALLATION-GUIDE.md
) > dist\how-to-install-me.txt

echo.
echo Build complete! Artifacts available in the dist\ folder.
echo Wheel: %WHEEL_FILE%
echo Installer: dist\installation.bat
echo Launcher: dist\tic-tac-toe-starter.vbs
echo.

if not defined SKIP_PAUSE pause
