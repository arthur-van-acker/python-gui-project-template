# YourApp Starter – Installation Guide

This guide walks you through installing the published YourApp Starter bundle so you can evaluate the template packaging flow. The GUI still looks like the Tic Tac Toe sample, but the domain layer is intentionally left as a stub—clicking the board raises `NotImplementedError` to remind adopters to plug in their own business rules.

## System Requirements

- **Operating System:** Windows 10 or Windows 11 (64-bit)
- **Python:** Version 3.8 or later available on `PATH` (the installer bootstraps its own virtual environment using whichever `python` it finds)
- **Internet Connection:** Required the first time the installer downloads dependencies from PyPI

> This installer is Windows-only by design—the batch/VBScript pair depends on Explorer, PowerShell, and the Windows desktop shell. For macOS/Linux evaluations, install the package via `pip install -r requirements.txt` and launch `python -m tictactoe` directly.

> The installer creates an isolated `.venv` inside the install directory so nothing leaks into your global Python environment.

## Installation Steps

### Step 1: Download the Bundle

- Grab the latest `yourapp-starter-artifacts.zip` from the GitHub Releases page **or** run `wheel-builder.bat` locally and copy everything under `dist/` to your target machine.

### Step 2: Extract the ZIP File

1. Right-click the ZIP file and select **Extract All...**
2. Choose a destination folder. After extraction you should see `installation.bat`, `tic-tac-toe-starter.vbs`, the wheel file, and the `assets/` directory.

### Step 3: Run the Installer

1. Open the extracted folder
2. Double-click **`installation.bat`**
3. If Windows SmartScreen appears, choose **More info → Run anyway** (the script is unsigned by design so adopters can add their own signing step)

Expected console log excerpt:
```
Creating %LOCALAPPDATA%\Programs\yourapp-starter-<version>
Bootstrapping virtual environment (.venv)
Installing wheel tictactoe-<version>-py3-none-any.whl
Running smoke test: python -m tictactoe --ui service --script 0,4,8 --quiet --label installer-smoke
Desktop shortcut created: YourApp Starter.lnk
Installation complete! Shortcut created.
```

### Step 4: What the Installer Does

During the run you will see status messages for each of these actions:

1. Remove any previous install directory automatically (no manual uninstall required)
2. Create `%LOCALAPPDATA%\Programs\yourapp-starter-<version>` (or `%TEMP%\yourapp-starter-<version>` when the bundle was built with `--ci`)
3. Copy every file from the extracted folder into that directory, including `assets/`
4. Create a private virtual environment inside `<install>\.venv`
5. Install the wheel (`tictactoe-<version>-py3-none-any.whl`) plus runtime dependencies (CustomTkinter, Pillow, darkdetect, packaging)
6. Run a smoke test via `python -m tictactoe --ui service --script 0,4,8 --quiet --label installer-smoke`
7. Drop a desktop shortcut named **YourApp Starter.lnk** that launches `tic-tac-toe-starter.vbs`
8. Write `install-info.json`, `license.txt`, and `how-to-install-me.txt` beside the binaries for inventory purposes

### Step 5: Wait for Confirmation

Leave the console window open until it prints **Installation complete! Shortcut created.** Press any key to exit.

## Launching the Template

### Method 1: Desktop Shortcut (Recommended)

Double-click **YourApp Starter** on the desktop. The shortcut launches `pythonw.exe -m tictactoe` inside the isolated environment, so no console window flashes.

### Method 2: Command Line (Frontend Picker)

1. Open PowerShell or Command Prompt
2. Navigate to the install directory (replace `<version>` with the number printed by the installer):
   ```pwsh
   cd "$env:LOCALAPPDATA\Programs\yourapp-starter-<version>"
   ```
3. Activate the virtual environment:
   ```pwsh
   .\.venv\Scripts\activate
   ```
4. Inspect available frontends:
   ```pwsh
   python -m tictactoe --list-frontends
   ```
5. Launch one:
   ```pwsh
   python -m tictactoe --ui gui      # CustomTkinter desktop (default)
   python -m tictactoe --ui headless # GUI rendered with the shim (for CI)
   python -m tictactoe --ui cli      # Terminal automation demo
   python -m tictactoe --ui service  # Env-driven automation/service mode
   ```
6. Need CLI-only switches? Call the module directly:
   ```pwsh
   python -m tictactoe.ui.cli.main --script 0,4,8 --quiet --output-json artifacts/summary.json
   ```

#### Environment Overrides

Set these variables before launching if you prefer zero-touch automation (PowerShell syntax shown):

| Variable | Purpose | Example |
| --- | --- | --- |
| `TICTACTOE_UI` | Forces the default frontend when `--ui` is omitted. | `$env:TICTACTOE_UI = "cli"`
| `TICTACTOE_HEADLESS` | Forces the GUI bootstrapper to use the shim widgets. Automatically set to `1` when you choose the `headless` frontend. | `$env:TICTACTOE_HEADLESS = "1"`
| `TICTACTOE_LOGGING` | Enables shared telemetry hooks for **all** frontends via `ControllerHooks.logging_hooks()`. | `$env:TICTACTOE_LOGGING = "1"`

Close the terminal (or `Remove-Item Env:VARIABLE`) to restore defaults.

```bash
export TICTACTOE_UI=cli
python -m tictactoe
unset TICTACTOE_UI
```

> **Tip:** Per-frontend aliases such as `TICTACTOE_GUI_LOGGING`, `TICTACTOE_CLI_LOGGING`, and `TICTACTOE_SERVICE_LOGGING` still work if you only want diagnostics for a single surface.

### What to Expect from the Sample

The bundled domain layer is a teaching stub—it publishes snapshots but intentionally raises `NotImplementedError` when you click the board or run automation scripts. This is normal and highlights where you need to wire in your own business logic when adopting the template.

## Troubleshooting

### Python Not Found
`'python' is not recognized...`

- Install Python 3.8+ from [python.org](https://www.python.org/downloads/) and select **Add Python to PATH** during setup
- Re-open the terminal (PATH changes propagate to new shells only)
- Run `installation.bat` again

### Installation Failed Midway

- Confirm you have internet access (pip pulls CustomTkinter, Pillow, etc.)
- Re-run the installer from an elevated PowerShell session (**Run as administrator**) if corporate policies restrict `%LOCALAPPDATA%`

### Desktop Shortcut Not Working

1. Navigate to `%LOCALAPPDATA%\Programs\yourapp-starter-<version>`
2. Double-click `tic-tac-toe-starter.vbs`
3. If needed, create a manual shortcut to:
   ```
   "%LOCALAPPDATA%\Programs\yourapp-starter-<version>\.venv\Scripts\pythonw.exe" -m tictactoe --ui gui
   ```

### Template Fails to Launch

- Ensure `<install>\.venv` exists; if not, rerun `installation.bat`
- Delete `%LOCALAPPDATA%\Programs\yourapp-starter-<version>` and reinstall to reset the environment

### Cleaning Up Old Builds

- The installer deletes the previous directory automatically. If you want to keep multiple versions, rename the folder before running a new installer.
- To remove obsolete installs manually, delete `%LOCALAPPDATA%\Programs\yourapp-starter-*` and the corresponding desktop shortcuts.

## Uninstalling the Template

1. Delete `%LOCALAPPDATA%\Programs\yourapp-starter-<version>`
2. Remove **YourApp Starter.lnk** from the desktop

That’s it—no registry keys or global packages remain.

## Files Included in the Release ZIP

- `tictactoe-<version>-py3-none-any.whl` – the Python package
- `installation.bat` – interactive installer
- `tic-tac-toe-starter.vbs` – silent launcher used by the shortcut
- `assets/` – icons, theme JSON, and other resources copied beside the binaries
- `license.txt`, `how-to-install-me.txt`, `install-info.json` – helper documents generated by `wheel-builder.bat`

## Privacy & Security

- No telemetry or personal data collection
- No internet access required after installation completes
- All code runs from `%LOCALAPPDATA%` under your user account

## Getting Help

- Re-run the installer with the console window visible and collect the logs
- File an issue on GitHub with Windows + Python versions and any error output
- When adapting the template, document your own org-specific steps here so future teammates can follow along

---

**Happy prototyping with YourApp Starter!**
