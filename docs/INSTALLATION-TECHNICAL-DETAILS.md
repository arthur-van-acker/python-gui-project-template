# Tic Tac Toe - Installation Technical Details

This document provides a comprehensive technical breakdown of the installation process for developers and advanced users who want to understand exactly what happens during installation.

---

## Installation Process - Step by Step

### 1. **Batch File Initialization**
   - `installation.bat` starts executing
   - `setlocal enabledelayedexpansion` - Enables variable expansion within loops/blocks
  - Sets `INSTALL_DIR` variable to `%LOCALAPPDATA%\Programs\yourapp-starter-<version>` (for example `yourapp-starter-0.1.0`)
  - In CI mode (`wheel-builder.bat --ci`) this instead points to `%TEMP%\yourapp-starter-<version>` so test runs never touch the real Programs folder

### 2. **Check for Existing Installation**
   - Checks if `%INSTALL_DIR%` folder exists
   - **If it exists:**
     - Displays message: "Found existing installation. Removing old version..."
     - Executes `rmdir /s /q "%INSTALL_DIR%"`
       - `/s` = removes all subdirectories and files
       - `/q` = quiet mode (no confirmation prompt)
     - Deletes the entire old installation directory including:
       - Old `.venv` virtual environment
       - Old wheel file
       - Old `tic-tac-toe-starter.vbs`
       - Old `favicon.ico`
     - Displays: "Old version removed."

### 3. **Create Installation Directory**
   - Executes `mkdir "%INSTALL_DIR%"` to create fresh installation folder
  - Creates: `C:\Users\[Username]\AppData\Local\Programs\yourapp-starter-0.1.0\`

### 4. **Copy Distribution Files**
   - Executes `xcopy /Y /Q "%~dp0*.*" "%INSTALL_DIR%\"`
     - `%~dp0` = directory where installation.bat is located (the dist folder)
     - `/Y` = overwrite without prompting
     - `/Q` = quiet mode (doesn't display filenames)
   - **Files copied:**
     - `tictactoe-<version>-py3-none-any.whl`
     - `installation.bat` (itself)
     - `tic-tac-toe-starter.vbs`
     - `how-to-install-me.txt`, `license.txt`, and future helper docs
     - `assets\` directory (icons, theme payloads)
     - `favicon.ico`

### 5. **Create Virtual Environment**
   - Executes `python -m venv "%INSTALL_DIR%\.venv"`
   - Python locates the global Python installation
   - Creates a `.venv` folder inside the installation directory
   - **Inside `.venv`, Python creates:**
     - `Scripts\` folder containing:
       - `python.exe` (copy of Python interpreter)
       - `pythonw.exe` (Python without console window)
       - `pip.exe` (package installer)
       - `activate.bat` (activation script)
       - Various other activation scripts
     - `Lib\` folder containing:
       - `site-packages\` (where packages will be installed)
       - Standard library links
     - `pyvenv.cfg` (configuration file pointing to base Python)
   - **If this fails:**
     - Displays error message
     - Pauses for user to read
     - Exits with error code 1

### 6. **Activate Virtual Environment**
   - Executes `call "%INSTALL_DIR%\.venv\Scripts\activate.bat"`
   - The activation script:
     - Modifies the `PATH` environment variable (in current session only)
     - Prepends `.venv\Scripts\` to PATH
     - Sets `VIRTUAL_ENV` variable to `.venv` path
     - Now when you run `python` or `pip`, it uses the venv versions

### 7. **Install Package with pip**
  - Executes `pip install "%INSTALL_DIR%\tictactoe-<version>-py3-none-any.whl"`
   - pip (from the virtual environment) processes the wheel file:
     
     **a. Read wheel metadata:**
     - Extracts package name, version, dependencies from wheel
     - Dependencies listed: `customtkinter>=5.2.2`, `darkdetect>=0.8.0`, `packaging>=25.0`, `pillow>=12.0.0`
     
     **b. Resolve and download dependencies:**
     - Connects to PyPI (Python Package Index) via internet
     - For each dependency:
       - Checks if it's already installed in the venv (it's not)
       - Downloads the wheel file from PyPI
       - **Downloads in order:**
         1. `pillow-12.0.0-cp313-cp313-win_amd64.whl` (~7 MB)
         2. `packaging-25.0-py3-none-any.whl` (~66 KB)
         3. `darkdetect-0.8.0-py3-none-any.whl` (~9 KB)
         4. `customtkinter-5.2.2-py3-none-any.whl` (~296 KB)
     
     **c. Install dependencies:**
     - Extracts each wheel to `.venv\Lib\site-packages\`
     - Creates folders:
       - `.venv\Lib\site-packages\PIL\` (Pillow)
       - `.venv\Lib\site-packages\packaging\`
       - `.venv\Lib\site-packages\darkdetect\`
       - `.venv\Lib\site-packages\customtkinter\`
     - Writes `.dist-info` folders for each package (metadata)
     
    **d. Install main package:**
    - Extracts `tictactoe-<version>-py3-none-any.whl`
    - Creates `.venv\Lib\site-packages\tictactoe\` folder
     - **Copies package contents:**
       - `__init__.py`
       - `__main__.py`
       - `assets\favicon.ico` (bundled with package)
       - `config\` folder with files
       - `domain\` folder with files
       - `ui\` folder with subfolders and files
    - Creates `.venv\Lib\site-packages\tictactoe-<version>.dist-info\`
     
     **e. Install entry point script:**
     - Reads `[project.scripts]` from package metadata
     - Creates `.venv\Scripts\tictactoe.exe`
     - This is a wrapper that executes `python -m tictactoe.__main__:main`

   - **Post-install smoke test:**
     - Executes `call "%INSTALL_DIR%\.venv\Scripts\python.exe" -m tictactoe --ui service --script 0,4,8 --quiet --label installer-smoke`
     - Verifies the automation/service frontend boots correctly using the freshly installed wheel
     - Any non-zero exit code aborts the installer before shortcuts or manifests are written
   
   - **If installation fails:**
     - Displays error message
     - Pauses
     - Exits with error code 1

### 8. **Get Desktop Path (OneDrive-compatible)**
   - Executes registry query:
     ```batch
     reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop
     ```
   - Reads the Desktop path from Windows registry
   - **Handles OneDrive scenarios:**
     - Standard: `C:\Users\[Username]\Desktop`
     - OneDrive: `C:\Users\[Username]\OneDrive\Desktop`
     - Enterprise: `D:\OneDrive\Documents\OneDrive\Desktop`
   - Stores result in `DESKTOP` variable
   - Removes trailing spaces from the path

### 9. **Expand Environment Variables**
   - Executes `call set DESKTOP=%DESKTOP%`
   - Expands any environment variables in the path (like `%USERPROFILE%`)
   - Final path is fully resolved

### 10. **Set Path Variables**
   - Sets `SCRIPT_DIR=%INSTALL_DIR%\` 
     - Example: `C:\Users\Arthur\AppData\Local\Programs\yourapp-starter-0.1.0\`
   - Sets `ICON_PATH=%SCRIPT_DIR%favicon.ico`
     - Full path to icon file
   - Sets `VBS_PATH=%SCRIPT_DIR%tic-tac-toe-starter.vbs`
     - Full path to VBS launcher

### 11. **Create VBScript for Shortcut**
  - Creates temporary VBScript file at `%TEMP%\create_yourapp_shortcut.vbs`
   - **VBScript contents (7 lines):**
     ```vbscript
     Set oWS = WScript.CreateObject("WScript.Shell")
    sLinkFile = "[Desktop Path]\YourApp Starter.lnk"
     Set oLink = oWS.CreateShortcut(sLinkFile)
     oLink.TargetPath = "[VBS_PATH]"
     oLink.IconLocation = "[ICON_PATH]"
     oLink.WorkingDirectory = "[SCRIPT_DIR]"
     oLink.Save
     ```
   - Each line is written using `echo` with output redirection (`>` and `>>`)

### 12. **Execute VBScript**
  - Runs `cscript //nologo "%TEMP%\create_yourapp_shortcut.vbs"`
   - `//nologo` suppresses the cscript banner
   - **VBScript execution:**
     - Creates Windows Script Host shell object
     - Creates shortcut object for `Desktop\YourApp Starter.lnk`
     - Sets shortcut properties:
      - **Target:** `C:\Users\...\yourapp-starter-0.1.0\tic-tac-toe-starter.vbs`
      - **Icon:** `C:\Users\...\yourapp-starter-0.1.0\favicon.ico`
      - **Working Directory:** `C:\Users\...\yourapp-starter-0.1.0\`
     - Saves the `.lnk` file to desktop
   - **Result:** Desktop shortcut appears with game icon

### 13. **Write Installation Manifest**
  - Executes `powershell -NoProfile` to emit `install-info.json` beside the application files
  - Captures `ProductName`, `Version`, `InstallDir`, and wheel filename for auditing or telemetry scripts
  - File is UTF-8 encoded JSON to simplify downstream tooling

### 14. **Cleanup Temporary Files**
  - Executes `del "%TEMP%\create_yourapp_shortcut.vbs"`
   - Removes the temporary VBScript file

### 15. **Display Completion**
   - Shows messages:
     - "Installation complete!"
     - "Desktop shortcut created successfully."
     - "You can now run the game from the desktop or by typing: tictactoe"
   - Executes `pause` - waits for user to press any key
   - Installer window closes

---

## Final Installation Structure

After installation completes, the directory structure is:

```
C:\Users\[Username]\AppData\Local\Programs\yourapp-starter-0.1.0\
├── .venv\
│   ├── Scripts\
│   │   ├── python.exe
│   │   ├── pythonw.exe
│   │   ├── pip.exe
│   │   ├── tictactoe.exe (entry point)
│   │   └── activate.bat
│   └── Lib\
│       └── site-packages\
│           ├── tictactoe\
│           │   ├── __init__.py
│           │   ├── __main__.py
│           │   ├── assets\
│           │   │   └── favicon.ico
│           │   ├── config\
│           │   ├── domain\
│           │   └── ui\
│           ├── customtkinter\
│           ├── PIL\
│           ├── darkdetect\
│           └── packaging\
├── tictactoe-0.1.0-py3-none-any.whl
├── installation.bat
├── tic-tac-toe-starter.vbs
└── favicon.ico

Desktop:
└── YourApp Starter.lnk (shortcut)
```

---

## Game Launch Sequence

When the user launches the game via the desktop shortcut:

### 1. **User Interaction**
  - User double-clicks `YourApp Starter.lnk` on desktop

### 2. **Windows Shortcut Resolution**
   - Windows reads the `.lnk` file
  - Resolves target: `C:\Users\...\yourapp-starter-0.1.0\tic-tac-toe-starter.vbs`
  - Sets working directory: `C:\Users\...\yourapp-starter-0.1.0\`

### 3. **VBScript Execution**
   - Windows launches `wscript.exe` to execute the VBS file
   - VBScript reads and executes:
     ```vbscript
     Set WshShell = CreateObject("WScript.Shell")
    WshShell.Run """C:\Users\...\yourapp-starter-0.1.0\.venv\Scripts\pythonw.exe"" -m tictactoe", 0
     Set WshShell = Nothing
     ```
   - The `0` parameter means: run hidden (no console window)

### 4. **Python Interpreter Launch**
   - `pythonw.exe` from the virtual environment starts
   - No console window appears (pythonw vs python)
   - Command line: `-m tictactoe`
   - Python looks for `tictactoe` package in `.venv\Lib\site-packages\`

### 5. **Python Module Execution**
  - Python finds the `tictactoe` package and executes `tictactoe/__main__.py`
  - The file now hosts a miniature CLI dispatcher built with `argparse`
  - Supported switches:
    - `--ui/--frontend`: choose `gui`, `headless`, or `cli`
    - `--list-frontends`: print the registry without launching anything
  - When no CLI flag is given, the dispatcher consults `TICTACTOE_UI` (if set) and falls back to the built-in default (`gui`).

### 6. **Frontend Registry**
  - `__main__.py` defines a `FRONTENDS` mapping of `FrontendSpec` objects
  - Each spec declares:
    - `target`: dotted import path + callable (e.g., `tictactoe.ui.gui.main:main`)
    - `description`: shown in `--list-frontends`
    - `env_overrides`: optional environment patches before launch
  - Available specs today:
    1. `gui` → CustomTkinter desktop app (default)
    2. `headless` → Same GUI widgets rendered via the shim so tests can run without Tk
    3. `cli` → Interactive / scripted terminal client

### 7. **Environment Overrides**
  - Specs can set additional variables before the frontend starts
  - The `headless` spec forces `TICTACTOE_HEADLESS=1`, which tells the GUI bootstrapper to import `tictactoe.ui.gui.headless_view` instead of the real CustomTkinter primitives
  - Installers can also pre-set `TICTACTOE_UI` globally (or per shortcut) to bias which frontend launches when users double-click

### 8. **Frontend Launch**
  - `FrontendSpec.load()` uses `importlib` to fetch the target callable lazily
  - The dispatcher simply invokes the callable; return codes propagate to the shell if the frontend returns an `int`
  - For the CLI path, control passes to `tictactoe.ui.cli.main` which handles `--script` and `--quiet` flags directly
  - The following steps describe the GUI/headless branch, which remains the default desktop experience

### 9. **GUI Module Import**
  - Imports `tictactoe.ui.gui.main`
  - Brings in dependencies:
    - `customtkinter` as `ctk`
    - `pathlib.Path`
    - `sys`
    - Domain layer symbols (`TicTacToe`, `GameState`)

### 10. **Windows-Specific Initialization**
  - Detects Windows via `platform.system()`
  - Calls `ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("TicTacToe.Game.v0.1.0")`
  - Ensures taskbar pinning and icons stay isolated from other Python apps

### 11. **TicTacToeGUI Class Initialization**
  - Instantiates `TicTacToeGUI`
  - Creates the domain model (`TicTacToe()`) and default view config if none supplied

### 12. **Game Logic Initialization**
  - Sets up an empty 3x3 board
  - Initializes the snapshot publisher used by both GUI widgets and headless adapters

### 13. **Window Creation**
  - `self.root = ctk.CTk()` to allocate the window (or shim equivalent when headless)
  - Applies title, geometry, and resizability constraints

### 14. **Icon Resolution**
  - Searches two locations for `favicon.ico`:
    1. Source tree: `src/tictactoe/assets` (editable installs)
    2. Installed path: `<venv>/Lib/site-packages/tictactoe/assets`
  - First match wins; stored in `self.icon_path`

### 15. **Icon Application**
  - Calls `self.root.iconbitmap(default=str(self.icon_path))`
  - Ties the favicon into the window chrome and Windows taskbar

### 16. **Theme Configuration**
  - Sets appearance mode and color theme (`light` / `blue` by default)
  - Additional theme hooks live in `tictactoe.config.gui`

### 17. **Widget Creation**
  - Builds the grid layout, status labels, and reset controls via `_create_widgets()`
  - Headless adapters reuse the same controller but render to stub widgets for tests

### 18. **Event Handler Binding**
  - Buttons invoke `_on_cell_click` with their position index
  - Reset button reinitializes the board via `_reset_game`

### 19. **Main Loop Start**
  - `self.root.mainloop()` (or the headless simulator) starts the event pump
  - Blocks until the window closes, processing redraws and input events

### 20. **Game Window Display**
  - GUI/headless visuals appear with correct icons and telemetry strings
  - CLI path instead stays inside `_interactive_session`, printing board states to stdout

---

## Key Technical Decisions

### Why Virtual Environment?
- **Isolation:** Dependencies don't conflict with user's other Python packages
- **Clean uninstall:** Delete one folder removes everything
- **Version control:** Each version can have its own dependencies
- **No permissions needed:** Installs to user directory, not system-wide

### Why pythonw.exe Instead of python.exe?
- `python.exe` opens a console window (black terminal)
- `pythonw.exe` runs without console (clean GUI experience)
- Essential for professional desktop applications

### Why VBScript Launcher?
- Direct `.exe` shortcuts would show Python logo in taskbar
- VBScript provides an intermediary that:
  - Hides console window (parameter `0`)
  - Launches with correct working directory
  - Allows custom icon via `.lnk` properties

### Why AppUserModelID?
- Windows groups taskbar buttons by executable
- All Python apps would show Python icon and group together
- Setting unique AppUserModelID tells Windows:
  - This is a separate application
  - Use this window's icon
  - Don't group with other Python apps

### Why Multiple Icon Path Checks?
- Development: Icon is in source tree at `src/tictactoe/assets/`
- Installed: Icon is in site-packages at `tictactoe/assets/`
- Ensures icon works in both scenarios
- Graceful fallback if neither path exists

### Why OneDrive Registry Query?
- Windows 10/11 Desktop can be:
  - Local: `C:\Users\[User]\Desktop`
  - OneDrive synced: `C:\Users\[User]\OneDrive\Desktop`
  - Enterprise OneDrive: Custom locations
- Registry always has the correct path
- Hardcoding would fail for OneDrive users

---

## Security Considerations

### Code Execution
- VBScript launcher executes arbitrary commands
- Hardcoded to only run pythonw.exe with specific module
- No user input is executed
- Limited attack surface

### File Permissions
- Installation to `%LOCALAPPDATA%`:
  - User-writable (no admin needed)
  - Per-user isolation
  - Protected from other users
- Virtual environment contains all code
- No system-wide modifications

### Network Access
- Only during pip install (downloading dependencies)
- Uses HTTPS to PyPI (encrypted)
- After installation, no network access required
- Game runs completely offline

### Registry Access
- Read-only query for Desktop path
- No registry modifications
- Standard Windows API usage

---

## Performance Characteristics

### Installation Time
- **Clean install:** 30-60 seconds
  - Virtual environment creation: 5-10 seconds
  - Dependency download: 10-30 seconds (network dependent)
  - Package installation: 10-20 seconds
  - Shortcut creation: <1 second

- **Reinstall/Update:** 20-40 seconds
  - Old folder deletion: 2-5 seconds
  - Rest same as clean install

### Disk Space Usage
- **Virtual environment:** ~30 MB
  - Python interpreter copy
  - Pip and setuptools
- **Dependencies:** ~15 MB
  - Pillow (largest at ~7 MB)
  - CustomTkinter (~3 MB)
  - Others (~5 MB)
- **Game package:** ~50 KB
- **Total:** ~50 MB

### Memory Usage (Running)
- Python interpreter: ~15 MB
- CustomTkinter/Tkinter: ~20 MB
- Game logic: <1 MB
- **Total:** ~35-40 MB RAM

### Startup Time
- VBScript launch: <100ms
- Python interpreter load: 200-500ms
- Module imports: 500-1000ms
- Window creation: 200-500ms
- **Total:** ~1-2 seconds from click to window

---

## Troubleshooting Reference

### Installation Fails at Virtual Environment Creation
**Cause:** Python not installed or not in PATH  
**Fix:** Install Python, ensure "Add to PATH" was checked

### Installation Fails at pip install
**Cause:** No internet connection or PyPI unreachable  
**Fix:** Check internet, try again, or use cached wheels

### Desktop Shortcut Not Created
**Cause:** Desktop path query failed or OneDrive sync issues  
**Fix:** Manually create shortcut pointing to `tic-tac-toe-starter.vbs`

### Icons Not Showing
**Cause:** `.ico` file missing or corrupted  
**Fix:** Verify `favicon.ico` exists in installation folder and package

### Game Won't Start
**Cause:** Virtual environment corrupted  
**Fix:** Delete installation folder and reinstall

### Taskbar Shows Python Icon
**Cause:** AppUserModelID not set (old version)  
**Fix:** Update to version with AppUserModelID support

---

## File Format Specifications

### Wheel File (.whl)
- **Format:** ZIP archive with specific structure
- **Naming:** `{package}-{version}-{python}-{abi}-{platform}.whl`
- **Example:** `tictactoe-0.1.0-py3-none-any.whl`
  - `py3` = Python 3
  - `none` = No ABI requirement
  - `any` = Any platform
- **Contents:**
  - Package source code
  - Metadata in `.dist-info`
  - Entry point scripts

### VBScript File (.vbs)
- **Format:** Plain text VBScript code
- **Encoding:** ASCII or UTF-8
- **Purpose:** Launch Python without console
- **Execution:** Windows Script Host (wscript.exe)

### Windows Shortcut (.lnk)
- **Format:** Binary file (Windows shell link)
- **Created by:** Windows Shell COM API
- **Properties stored:**
  - Target path
  - Working directory
  - Icon location
  - Window state (normal/minimized/maximized)
  - Hotkey (if any)

### Icon File (.ico)
- **Format:** Multi-resolution bitmap container
- **This project:** 16x16, 32x32, 48x48, 64x64, 128x128, 256x256
- **Color depth:** 32-bit RGBA
- **Usage:** Windows expects specific sizes for different UI elements

---

## Development Notes

### Building Distribution Package
```batch
.\wheel-builder.bat
```
- Activates virtual environment
- Cleans old builds
- Builds wheel with `python -m build --wheel`
- Copies assets to dist
- Generates installer scripts

### Testing Installation Locally
1. Run `wheel-builder.bat`
2. Navigate to `dist\`
3. Run `installation.bat`
4. Test desktop shortcut
5. Verify icon display

### Updating Version
1. Edit `pyproject.toml`: Change `version = "0.1.0"` to new version
2. Update `INSTALL_DIR` in `wheel-builder.bat` to match
3. Update documentation references
4. Rebuild wheel

### Adding Dependencies
1. Edit `pyproject.toml`: Add to `dependencies` list
2. Rebuild wheel
3. Test installation (pip will auto-download new deps)

---

## Architectural Overview

```
Distribution Package (ZIP)
    │
    ├── tictactoe-0.1.0-py3-none-any.whl  ← Python package
    ├── installation.bat                   ← Installer script
    ├── tic-tac-toe-starter.vbs            ← Launch wrapper
    └── favicon.ico                        ← Icon file
         
         ↓ [User runs installation.bat]
         
Installation Directory
    │
    ├── .venv\                             ← Isolated Python
  │   ├── Scripts\pythonw.exe            ← GUI Python interpreter
    │   └── Lib\site-packages\
    │       └── tictactoe\                 ← Installed package
    │           ├── __main__.py            ← Entry point
    │           ├── assets\favicon.ico     ← Bundled icon
    │           ├── domain\logic.py        ← Game logic
  │           └── ui\                    ← Presentation layer
  │               ├── gui\main.py        ← CustomTkinter frontend
  │               └── cli\main.py        ← Terminal frontend
    │
    └── tic-tac-toe-starter.vbs            ← Launcher
         
         ↓ [User clicks desktop shortcut]
         
Runtime Stack
    │
    Desktop Shortcut (.lnk)
         ↓
    wscript.exe
         ↓
    tic-tac-toe-starter.vbs
         ↓
    .venv\Scripts\pythonw.exe -m tictactoe
         ↓
    tictactoe\__main__.py:main()
      ↓
    Frontend dispatcher (FRONTENDS registry)
      ↓
    ├─ gui/headless → tictactoe.ui.gui.main:TicTacToeGUI() → CustomTkinter window or shim widgets
    └─ cli          → tictactoe.ui.cli.main:main()       → Text-based session in the terminal
```

---

**Document Version:** 1.1  
**Last Updated:** November 16, 2025  
**Target Audience:** Developers, Advanced Users, System Administrators
