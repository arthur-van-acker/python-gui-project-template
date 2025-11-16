# Installer Customization Guide

`wheel-builder.bat` generates two scripts per build:
- `installation.bat` — interactive installer that deploys to `%LOCALAPPDATA%\Programs\ttt.v0.1.0` and provisions a virtual environment.
- `tic-tac-toe-starter.vbs` — silent launcher that runs `pythonw.exe -m tictactoe` without a console window.

This document explains how to tailor those scripts for new product names, install paths, or deployment requirements.

## Where to Edit
- **Primary edits** belong in `wheel-builder.bat`. The batch file templates the installer/launcher with `echo` statements so changes survive regeneration.
- Only adjust the generated `dist/installation.bat` or `tic-tac-toe-starter.vbs` for quick experiments; otherwise, re-run `wheel-builder.bat` to avoid manual drift.

## Common Customizations

### 1. Installation Directory
- Change `set INSTALL_DIR=%LOCALAPPDATA%\Programs\ttt.v0.1.0` near the top of the generated installer block.
- When templating via `wheel-builder.bat`, update the `echo set INSTALL_DIR=...` line so future builds use the new path.
- For machine-wide installs, point to `%ProgramFiles%\YourApp` and run the installer from an elevated prompt.

### 2. Shortcut Names & Icons
- Modify `echo oLink.TargetPath`, `echo oLink.IconLocation`, and the `sLinkFile` name in the shortcut creation block to match your branding.
- Update `favicon.ico` inside `src/tictactoe/assets` and ensure `wheel-builder.bat` copies any new icon files (PNG, ICO) into `dist/`.

### 3. Post-Install Steps
Insert additional commands in the installer template:
- Registry entries (`reg add ...`) for protocol handlers.
- Configuration files copied to `%PROGRAMDATA%` or `%APPDATA%`.
- Telemetry opt-in prompts (write text files or set env vars).
Always guard optional steps with informative echo statements and error handling so failures are clear.

### 4. Offline or Portable Installs
- Replace the `pip install` line with `pip install --no-index --find-links "%%INSTALL_DIR%%\wheels"` and pre-seed a `wheels/` folder copied alongside the installer.
- Skip virtual environment creation by removing the `python -m venv` block and calling the system Python instead (not recommended unless you control the environment).

### 5. Launcher Behavior
- `tic-tac-toe-starter.vbs` calls `pythonw.exe -m tictactoe`. To pass arguments (e.g., force headless UI), append them: `"""...pythonw.exe"" -m tictactoe --ui headless"`.
- To launch CLI instead of GUI, change the module to `tictactoe.ui.cli.main` or call a custom entry point.

### 6. Enterprise Deployment
For SCCM/Intune packaging:
- Wrap `installation.bat` inside a PowerShell script that runs silently (`start /wait installation.bat > install.log`).
- Configure the script to accept `INSTALL_DIR` overrides through environment variables so IT can redirect to network locations.
- Document exit codes; the current script exits `1` on failure inside `wheel-builder.bat`’s template.

## Testing Changes
1. Re-run `wheel-builder.bat` after editing templates.
2. Inspect the generated scripts in `dist/` to confirm your changes.
3. Execute the installer on a clean user profile; verify:
   - Shortcut names/icon updates.
   - New files or registry keys exist.
   - Uninstall instructions still work (delete install folder + shortcut).

## Versioning the Installer
When bumping the application version:
- Update `INSTALL_DIR` suffix (`ttt.v0.1.0`) in `wheel-builder.bat` to the new semantic version or a channel name (`myapp.v1`).
- Consider preserving previous installs by including the version (`ttt.v1.2.0`) so users can test side-by-side builds.

By funneling all installer edits through `wheel-builder.bat`, you guarantee every distribution pack remains consistent and traceable in git, removing guesswork for future template adopters.
