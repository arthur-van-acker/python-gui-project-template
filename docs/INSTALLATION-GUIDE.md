# Tic Tac Toe - Installation Guide

This guide provides step-by-step instructions for installing the Tic Tac Toe game on your Windows computer.

## System Requirements

- **Operating System:** Windows 10 or later
- **Python:** Python 3.8 or higher (must be installed on your system)
- **Internet Connection:** Required for downloading dependencies during installation

> **Note:** The game installs in its own isolated virtual environment, so it won't interfere with any other Python packages you may have installed.

## Installation Steps

### Step 1: Download the Game

Download the `tic-tac-toe.zip` file to your computer.

### Step 2: Extract the ZIP File

1. Locate the downloaded `tic-tac-toe.zip` file (usually in your Downloads folder)
2. Right-click on the ZIP file
3. Select **"Extract All..."** from the context menu
4. Choose a destination folder (or keep the default)
5. Click **"Extract"**

A new folder will be created containing the game files.

### Step 3: Run the Installer

1. Open the extracted folder
2. Locate the file named **`installation.bat`**
3. **Double-click** on `installation.bat` to run it

   > **Note:** If Windows SmartScreen appears, click **"More info"** and then **"Run anyway"**

### Step 4: Installation Process

The installer will automatically:

1. **Check for and remove any existing installation** (if present)
   - This ensures a clean installation every time
   - You don't need to manually uninstall old versions

2. Create an installation directory at:
   ```
   C:\Users\YourUsername\AppData\Local\Programs\ttt.v0.1.0
   ```

3. Copy all game files to this directory

4. Create an isolated virtual environment (Python sandbox)

5. Download and install required dependencies into the virtual environment:
   - CustomTkinter (for modern UI)
   - Pillow (for image handling)
   - darkdetect (for theme detection)
   - packaging (for version management)

6. Install the Tic Tac Toe game package

7. Create a desktop shortcut named **"Tic Tac Toe"** with the game icon

> **What is a virtual environment?** It's an isolated Python installation that keeps the game's dependencies separate from your system Python. This prevents conflicts and makes uninstallation cleaner.

### Step 5: Wait for Completion

- The installation process may take a minute or two
- You'll see progress messages in the command window
- Wait for the message: **"Installation complete! Desktop shortcut created successfully."**
- Press any key to close the installer window

## Launching the Game

After installation, you have two ways to launch the game:

### Method 1: Desktop Shortcut (Recommended)

1. Locate the **"Tic Tac Toe"** icon on your desktop
2. **Double-click** the icon to launch the game

### Method 2: Command Line (Frontend Picker)

> **Heads up:** The command-line launcher respects the same isolated virtual environment as the desktop shortcut, so remember to activate `.venv` first. The shortcut is still the fastest way to reach the GUI, but the CLI gives you extra control when scripting or testing.

1. Open PowerShell or Command Prompt
2. Navigate to the installation folder:
   ```
   cd %LOCALAPPDATA%\Programs\ttt.v0.1.0
   ```
3. Activate the virtual environment:
   ```
   .venv\Scripts\activate
   ```
4. Inspect the available frontends (GUI, CLI, headless):
   ```
   python -m tictactoe --list-frontends
   ```
5. Launch the frontend you want:
   ```
   python -m tictactoe --ui gui      # CustomTkinter desktop (default)
   python -m tictactoe --ui cli      # Terminal experience
   python -m tictactoe --ui headless # GUI rendered with the shim for CI smoke tests
   ```
6. Need to automate the CLI? Call it directly so you can pass CLI-only switches:
   ```
   python -m tictactoe.ui.cli.main --script 0,4,8 --quiet
   ```

#### Environment Overrides

Set these variables before launching if you prefer zero-touch automation (PowerShell syntax shown):

| Variable | Purpose | Example |
| --- | --- | --- |
| `TICTACTOE_UI` | Forces the default frontend when `--ui` is omitted. | `$env:TICTACTOE_UI = "cli"` |
| `TICTACTOE_HEADLESS` | Tells the GUI bootstrapper to load shim widgets (no Tk required). Automatically set to `1` when you choose the `headless` frontend. | `$env:TICTACTOE_HEADLESS = "1"` |

Unset the variables (or close the terminal) to return to the desktop default.

## Troubleshooting

### Python Not Found

**Error:** `'python' is not recognized as an internal or external command`

**Solution:**
1. Install Python from [python.org](https://www.python.org/downloads/)
2. During installation, **make sure to check** "Add Python to PATH"
3. Restart your computer
4. Run the installer again

### Installation Failed

**Error:** `Installation failed!`

**Solution:**
1. Make sure you have an internet connection
2. Try running the installer as Administrator:
   - Right-click on `installation.bat`
   - Select **"Run as administrator"**

### Desktop Shortcut Not Working

**Solution:**
1. Navigate to: `C:\Users\YourUsername\AppData\Local\Programs\ttt.v0.1.0`
2. Double-click `tic-tac-toe-starter.vbs` to launch the game
3. If that doesn't work, try running directly:
   - Navigate to: `C:\Users\YourUsername\AppData\Local\Programs\ttt.v0.1.0\.venv\Scripts`
   - Double-click `pythonw.exe`
   - This won't work directly, but you can create a shortcut with target:
     ```
     "C:\Users\YourUsername\AppData\Local\Programs\ttt.v0.1.0\.venv\Scripts\pythonw.exe" -m tictactoe
     ```

### Game Won't Start

**Solution:**
1. Make sure the virtual environment was created successfully during installation
2. Check that this folder exists: `C:\Users\YourUsername\AppData\Local\Programs\ttt.v0.1.0\.venv`
3. If not, run the installer again
4. If the folder exists but the game still won't start, try reinstalling:
   - Delete the folder: `C:\Users\YourUsername\AppData\Local\Programs\ttt.v0.1.0`
   - Run the installer again

### Uninstalling Older Versions

**Note:** You don't need to manually uninstall old versions before installing! The installer automatically removes the previous installation.

If you want to manually clean up old installations or versions installed differently:

1. Check for old installation folders:
   - Navigate to: `C:\Users\YourUsername\AppData\Local\Programs`
   - Delete any old `ttt.*` folders (the installer handles this automatically for you)

2. If you installed a very old version globally (without virtual environment):
   - Open Command Prompt
   - Type: `pip uninstall tictactoe`
   - Press `y` to confirm

## Uninstalling the Game

### When to Uninstall

You only need to manually uninstall if you want to **completely remove** the game from your system.

**Note:** If you're updating to a newer version, you don't need to uninstall - just run the new installer and it will automatically replace the old version.

### Complete Uninstall (Manual Removal)

Since the game is installed in an isolated virtual environment, uninstallation is very simple:

1. **Delete the installation folder:**
   - Navigate to: `C:\Users\YourUsername\AppData\Local\Programs`
   - Delete the `ttt.v0.1.0` folder
   - This removes the game and all its dependencies

2. **Remove the desktop shortcut:**
   - Right-click on the "Tic Tac Toe" desktop icon
   - Select **"Delete"**

That's it! The game is completely removed from your system.

## Files Included

The distribution package contains:

- **`tictactoe-0.1.0-py3-none-any.whl`** - The game package
- **`installation.bat`** - Automated installer script
- **`tic-tac-toe-starter.vbs`** - Silent launcher (no console window)
- **`favicon.ico`** - Game icon (used for desktop shortcut)

## Privacy & Security

- The game does **not** collect any personal data
- The game does **not** require internet access to play (only during installation)
- All files are stored locally on your computer
- No information is sent to external servers

## Getting Help

If you encounter any issues not covered in this guide:

1. Check that Python is properly installed and in your PATH
2. Verify you have an active internet connection during installation
3. Try running the installer as Administrator
4. Make sure your antivirus isn't blocking the installation

## Additional Information

- **Version:** 0.1.0
- **Installation Size:** ~50 MB (including virtual environment and dependencies)
- **Isolation:** Installed in its own virtual environment - won't affect other Python packages
- **License:** Zero-Clause BSD (0BSD)

---

**Enjoy playing Tic Tac Toe!** 🎮
