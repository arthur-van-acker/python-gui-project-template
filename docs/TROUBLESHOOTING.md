# Troubleshooting & FAQ

Use this FAQ to resolve the most common issues reported when adopting or installing the template.

## Virtual Environment Creation Fails
**Symptom:** `python -m venv .venv` or the installer prints "Failed to create virtual environment".
- Ensure Python 3.11+ is installed and accessible in `PATH`.
- On Windows, install the "Python 3.x (64-bit)" MSI with the "Add to PATH" option enabled.
- Delete partially created `.venv/` folders before retrying.

## `pip install` Cannot Reach the Internet
- Pre-download dependencies and place wheels next to the installer. Update `installation.bat` to pass `--no-index --find-links` as described in `docs/INSTALLER-CUSTOMIZATION.md`.
- Provide a corporate mirror via `pip.ini` or environment variables (e.g., `PIP_INDEX_URL`).

## CustomTkinter/Tk Errors (e.g., `tkinter.TclError`)
- Install the Tk runtime packages (`sudo apt install python3-tk` on Debian/Ubuntu).
- For CI, rely on `HeadlessGameView` by running tests with `-m "not gui"` or setting `TICTACTOE_HEADLESS=1`.
- When shipping to macOS/Linux, ensure the target machines include a GUI subsystem or stick to the CLI frontend.

## OneDrive Desktop Detection Issues
**Symptom:** No shortcut created because the Desktop path contains spaces or OneDrive placeholders.
- The installer already reads `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders`. If that registry path is missing, add a fallback to `%USERPROFILE%\Desktop` in `wheel-builder.bat`.
- Users can manually create a shortcut pointing to `%LOCALAPPDATA%\Programs\ttt.vX.Y.Z\tic-tac-toe-starter.vbs`.

## Headless Tests Crash with `HeadlessGameView has not been built yet`
- Ensure `view.build()` is called before rendering. When writing custom views, follow the `GameViewPort` contract: `build()`, `is_ready()`, then `render()`.
- In tests, construct `TicTacToeGUI(view_factory=HeadlessGameView)` so the controller wiring remains intact.

## Wheel Builder Cannot Find `python`
- Activate the project virtual environment before running `wheel-builder.bat` (`.venv\Scripts\activate`).
- If you prefer a system interpreter, edit the script to call an absolute path (`C:\Python313\python.exe`).

## Desktop Shortcut Uses Old Name/Icon
- Update `wheel-builder.bat` (shortcut creation block) and rebuild. Deleting `%TEMP%\create_ttt_shortcut.vbs` between runs helps avoid stale scripts.

## Installer Leaves Behind Old Versions
- The default installer removes any existing `INSTALL_DIR`. If you need side-by-side installs, comment out the `rmdir /s /q` block and communicate manual cleanup instructions.

## GUI Window Too Small or Fonts Misaligned
- Modify `config/gui.py` (`WindowConfig.geometry`, `FontConfig`, `LayoutConfig`).
- Regenerate the installer if you embed default configs anywhere else.

Still stuck? Open an issue on GitHub with logs (`dist\installation.log` if you add logging) and specify Windows version, Python version, and whether the problem occurs during build, install, or runtime.
