# YourApp Starter – Python GUI Template

YourApp Starter is a CustomTkinter-based reference implementation that shows how to ship a polished Python desktop app with multiple frontends, theming hooks, and production-ready installers. The repo still bundles the Tic Tac Toe sample, but every file is structured so you can drop in your own domain logic without rewriting the infrastructure.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-0BSD-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

---

## 🎯 Project Goals

This project was created as a **reference template** for building professional Python GUI applications. It demonstrates:

- ✅ **Modern GUI Development** using CustomTkinter
- ✅ **Proper Project Structure** with separation of concerns
- ✅ **Python Packaging** with setuptools and wheel distribution
- ✅ **Isolated Virtual Environment** installation
- ✅ **Professional Windows Distribution** with automated installer
- ✅ **Desktop Integration** with shortcuts and icons
- ✅ **Clean Architecture** following best practices
- ✅ **Complete Documentation** for users and developers

**Use this as a starting point** for your own Python GUI projects!

---

## 🎮 Template Highlights

### What You Can Reuse Immediately
- **Multi-frontend dispatcher**: GUI, headless, CLI, and service entry points live behind `python -m tictactoe` so you can register more launchers without forking scripts.
- **Typed theme/config layer**: `tictactoe.config.gui` exposes dataclasses for fonts, colors, copy, and layout; presets can be loaded from JSON or environment variables.
- **Installer + launcher duo**: `wheel-builder.bat` outputs a version-stamped `installation.bat`, VBScript launcher, manifest, and helper docs with one command.
- **CI rehearsal scripts**: `scripts/run-ci.ps1` and `.sh` run formatting, linting, typing, pytest (GUI + non-GUI), and installer smoke tests locally or in automation.
- **Headless GUI adapter**: `HeadlessGameView` mirrors widget telemetry so GUI smoke tests run in CI without a Tk display.

### Why Teams Adopt It
- **Isolated installations** prevent global Python conflicts and mimic end-user environments.
- **Desktop integration** (shortcut, icon, VBScript launcher) demonstrates how to feel native on Windows.
- **Environment-driven configuration** keeps installers/CI in sync with runtime features like themes or automation scripts.
- **Docs-first approach** means README + deep dives already describe packaging, configuration, and adoption steps for your future contributors.

---

## 📁 Project Structure

```
yourapp-starter/
├── src/
│   └── tictactoe/
│       ├── __init__.py
│       ├── __main__.py              # Entry point
│       ├── assets/
│       │   └── favicon.ico          # Application icon
│       ├── config/                  # Configuration (future use)
│       ├── domain/
│       │   └── logic.py             # Game logic (model)
│       └── ui/
│           └── gui/
│               └── main.py          # GUI implementation (view)
├── tests/                           # Unit tests
├── docs/
│   ├── INSTALLATION-GUIDE.md        # User installation guide
│   └── INSTALLATION-TECHNICAL-DETAILS.md  # Technical deep-dive
├── dist/                            # Built distribution files
├── pyproject.toml                   # Project metadata & dependencies
├── requirements.txt                 # Development dependencies
├── wheel-builder.bat                # Build script
└── README.md

Architecture: MVC-inspired separation
- domain/: Business logic (Model)
- ui/: User interface (View)
- Future: Add controller layer if needed
```

---

## 🚀 Quick Start

### For Users

1. **Download** the latest sample release (`yourapp-starter.zip`)
2. **Extract** the ZIP file
3. **Run** `installation.bat`
4. **Launch** from desktop shortcut

See [INSTALLATION-GUIDE.md](docs/INSTALLATION-GUIDE.md) for detailed instructions.

### For Developers

#### Prerequisites
- Python 3.8 or higher
- Git (optional)

#### Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd yourapp-starter

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

#### Run in Development Mode

```bash
# Activate virtual environment first
.venv\Scripts\activate

# Run the bundled sample app
python -m tictactoe
# or
tictactoe
```

#### Choose a Frontend

`python -m tictactoe` now acts as a thin dispatcher so template users can plug in
different interfaces without forking the entry point. Pick a frontend at runtime:

```bash
# Launch the CustomTkinter GUI (default)
python -m tictactoe --ui gui

# Launch the GUI with the headless shim (CI or servers without Tk)
python -m tictactoe --ui headless

# Launch the terminal client
python -m tictactoe --ui cli

# Launch the headless automation/service runner
python -m tictactoe --ui service

# Launch the GUI with the bundled "dark" theme
python -m tictactoe --ui gui --theme dark

# Load a JSON theme config from disk
python -m tictactoe --ui gui --theme-file themes/enterprise.json

# List every registered frontend
python -m tictactoe --list-frontends
```

Environment variables offer zero-touch overrides for installers or CI:

| Variable | Accepted values | Notes |
| --- | --- | --- |
| `TICTACTOE_UI` | `gui`, `cli`, `headless`, `service` | Forces a frontend when no flag is provided. |
| `TICTACTOE_HEADLESS` | `0` / `1` | Still respected by the GUI to load the shim widgets in tests. |
| `TICTACTOE_THEME` | `default`, `light`, `dark`, `enterprise`, ... | Selects a named preset from `tictactoe.config.gui.NAMED_THEMES`. |
| `TICTACTOE_THEME_FILE` | filesystem path | Points to a JSON file containing `GameViewConfig` data. |
| `TICTACTOE_THEME_PAYLOAD` | JSON string (internal) | Automatically managed when using `--theme` / `--theme-file`; can be set manually for advanced flows. |
| `TICTACTOE_SCRIPT` | comma-separated moves | Consumed by the service frontend to drive automation runs. |
| `TICTACTOE_SCRIPT_FILE` | filesystem path | Alternative to `TICTACTOE_SCRIPT` if you store scripts in files. |
| `TICTACTOE_AUTOMATION_OUTPUT` | filesystem path | Where automation results are written as JSON. |
| `TICTACTOE_AUTOMATION_LABEL` | any string | Stored in the automation summary for traceability. |
| `TICTACTOE_AUTOMATION_QUIET` | `0` / `1` | Controls whether the service frontend prints to stdout. |
| `TICTACTOE_LOGGING` | `0` / `1` / `true` / `false` | Turns on telemetry/logging hooks for **all** frontends at once. Legacy `TICTACTOE_GUI_LOGGING`, `TICTACTOE_CLI_LOGGING`, and `TICTACTOE_SERVICE_LOGGING` still work for per-frontend overrides. |

Setting `TICTACTOE_UI=headless` automatically flips `TICTACTOE_HEADLESS=1`, which is
useful for CI smoke tests that still exercise the GUI bootstrap path without a Tk
runtime.

Need targeted diagnostics without editing code? Export `TICTACTOE_LOGGING=1` (or one
of the legacy `*_LOGGING` vars) before launching. Every frontend will automatically
use the built-in `ControllerHooks.logging_hooks()` helper so you can capture
controller telemetry in the terminal or installer logs.

Need scripted or fully automated CLI sessions? Invoke the CLI module directly so
you can access its own flags (such as `--script` and `--quiet`):

```bash
# Replay a deterministic move list and capture JSON output for CI
python -m tictactoe.ui.cli.main --script 0,4,8 --output-json artifacts/automation.json

# Load moves from a file and tag the run for dashboards
python -m tictactoe.ui.cli.main --script-file scripts/demo.moves --label nightly-seed

# Serialize a theme preset to disk for editing
python - <<"PY"
from pathlib import Path
from tictactoe.config.gui import serialize_game_view_config, get_theme
Path("themes/dark.json").write_text(
   __import__("json").dumps(serialize_game_view_config(get_theme("dark")), indent=2),
   encoding="utf-8",
)
PY
```

Want to flip JSON experiments back into typed dataclasses? The sample payloads live in `src/tictactoe/assets/themes/`, and you can promote any of them with:

```bash
python -m tictactoe.tools.theme_codegen src/tictactoe/assets/themes/light.json --variable-prefix marketing
```

The script prints an import block plus a `marketing_light_theme` variable so you can commit polished presets once you're happy with the JSON prototype.

When you don't want to pass CLI flags, switch to the service frontend (`--ui service`) 
and configure the environment variables above. This is handy for installer smoke
tests or GitHub Actions jobs that already manage state through env vars.

### Adopt This Template in Order

| Step | Files to touch | What to change |
| --- | --- | --- |
| 1. Rename the package | `pyproject.toml`, `src/tictactoe/`, `README.md` | Update `[project]` metadata, rename the package directory, adjust imports/entry points, and rewrite the hero copy for your product. |
| 2. Refresh configs & assets | `tictactoe.config.gui`, `src/tictactoe/assets/` | Replace fonts/colors/texts via `GameViewConfig`, swap `favicon.ico`, and add any extra assets you plan to copy into the installer bundle. |
| 3. Align UIs & controllers | `tictactoe.ui.gui.*`, `tictactoe.ui.cli.main`, `tictactoe.domain.logic` | Rework copy, widgets, or domain actions to match your app while keeping `HeadlessGameView` + CLI automation helpers intact. |
| 4. Update installers | `wheel-builder.bat`, generated `installation.bat`, `tic-tac-toe-starter.vbs` | Change shortcut names, manifest metadata, and smoke-test scripts; rerun `wheel-builder.bat --ci --no-pause` to verify. |
| 5. Lock quality gates | `scripts/run-ci.ps1`, `scripts/run-ci.sh`, `tests/` | Keep the formatter/linter/type checker suites, expand pytest coverage for your modules, and ensure GUI markers still pass headless. |

Each step links back into the deeper docs in `docs/TEMPLATE-USAGE-GUIDE.md` and
`docs/TEMPLATE-CHECKLIST.md`, so contributors can follow the same adoption path.

#### Swap the View Adapter

The GUI layer now ships with adapter-friendly contracts so you can choose how the
widgets are rendered without touching the controller:

```python
from tictactoe.ui.gui import HeadlessGameView
from tictactoe.ui.gui.main import TicTacToeGUI

# Exercise the controller and domain logic without CustomTkinter widgets
app = TicTacToeGUI(view_factory=HeadlessGameView)
app.run()
```

`HeadlessGameView` implements the shared `GameViewPort` protocol alongside the
default `GameView` (CustomTkinter) so template users can bundle their own adapters
without rewriting `TicTacToeGUI`. The same telemetry helpers (`cell_text`,
`status_text`, etc.) are available for tests regardless of the adapter in use.

#### Build Distribution

```bash
# Build the interactive bundle (prompts if anything fails)
.\wheel-builder.bat

# Build + smoke-test into %%TEMP%% (useful for CI)
.\wheel-builder.bat --ci --no-pause
```

The script stamps the current version, copies `src/tictactoe/assets/`, and
emits a complete installer payload in `dist/`:

- `tictactoe-<version>-py3-none-any.whl`
- `installation.bat` (pre-configured install root + smoke tests)
- `tic-tac-toe-starter.vbs` launcher with relative paths
- `how-to-install-me.txt` and `license.txt`
- `assets/` directory (icons, future resources)

---

## 📦 Distribution & Installation

### Building for Distribution

This project includes an automated build system:

1. **Run** `wheel-builder.bat` (or `wheel-builder.bat --ci --no-pause` inside pipelines)
2. **Outputs** the wheel, installer script, launcher, and docs/asset bundle under `dist/`

### Installation System

The installer (`installation.bat`) now mirrors production-ready workflows:

1. ✅ Version-stamped install directory (`%LOCALAPPDATA%\Programs\yourapp-starter-<version>%` by default, `%TEMP%` when built with `--ci`)
2. ✅ Full bundle copy including `assets/` so icons/config ship with the app
3. ✅ Private virtual environment creation + wheel installation
4. ✅ Post-install smoke test (`python -m tictactoe --ui service --script 0,4,8 --quiet`)
5. ✅ Desktop shortcut + VBScript launcher with custom icon name (`YourApp Starter.lnk`)
6. ✅ `install-info.json` manifest for inventory/telemetry scripts
7. ✅ `how-to-install-me.txt` aid packaged beside the installer for hand-off documentation

To uninstall, delete the stamped install directory and remove the shortcut.

For technical details, see [INSTALLATION-TECHNICAL-DETAILS.md](docs/INSTALLATION-TECHNICAL-DETAILS.md).

---

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Programming language
- **CustomTkinter**: Modern UI framework (enhanced Tkinter)
- **setuptools**: Python packaging
- **wheel**: Binary distribution format

### Dependencies
- `customtkinter>=5.2.2` - Modern UI components
- `pillow>=12.0.0` - Image handling
- `darkdetect>=0.8.0` - OS theme detection
- `packaging>=25.0` - Version management

### Development Tools
- `pytest` - Unit testing
- `black` - Code formatting
- `ruff` - Linting
- `mypy` - Type checking

---

## 🎨 Using This Template

### Adapting for Your Project

1. **Clone/Download** this repository
2. **Rename** the project folder and package
3. **Update** `pyproject.toml`:
   - Change `name`, `version`, `description`
   - Update author information
   - Modify dependencies as needed
4. **Replace** game logic in `domain/` with your business logic
5. **Redesign** UI in `ui/gui/` for your application
6. **Update** `favicon.ico` with your application icon
7. **Modify** `wheel-builder.bat` to match your project name/version
8. **Rebuild** and test installation

### Key Concepts to Reuse

- **Virtual Environment Installation**: Keeps user's Python clean
- **Wheel Distribution**: Professional packaging method
- **Desktop Integration**: Icons and shortcuts
- **VBScript Launcher**: Silent execution without console
- **AppUserModelID**: Proper Windows taskbar integration
- **Automated Installer**: One-click installation experience

### Configuration Knobs You Can Toggle

All fonts, strings, dimensions, and color hooks for the CustomTkinter frontend live in `tictactoe.config.gui`. Inject a `GameViewConfig` (and optionally a `WindowConfig`) into `TicTacToeGUI` to reskin or resize the app without touching the widget code:

```python
from tictactoe.config import (
   ColorConfig,
   FontConfig,
   FontSpec,
   GameViewConfig,
   LayoutConfig,
   TextConfig,
   WindowConfig,
)
from tictactoe.ui.gui.main import TicTacToeGUI

view_config = GameViewConfig(
   fonts=FontConfig(
      title=FontSpec(size=40, weight="bold"),
      cell=FontSpec(size=48, weight="bold"),
   ),
   layout=LayoutConfig(
      board_padding=(30, 30),
      cell_size=(120, 120),
      cell_spacing=8,
   ),
   text=TextConfig(
      title="Ultimate YourApp",
      reset_button="Play Again",
      win_message_template="Congrats {winner}!",
   ),
   colors=ColorConfig(
      board_background="#101828",
      cell_fg="#1D2939",
      cell_hover="#344054",
      status_text="#F2F4F7",
   ),
)

window_config = WindowConfig(title="Ultimate YourApp", geometry="500x720")

app = TicTacToeGUI(view_config=view_config, window_config=window_config)
app.run()
```

Every field is optional; omit keys you do not want to override. Because the config layer uses frozen dataclasses, you can share presets throughout your project or load them from JSON/YAML before instantiating the GUI.

---

## 📚 Documentation

- **[INSTALLATION-GUIDE.md](docs/INSTALLATION-GUIDE.md)**: User-friendly installation instructions
- **[INSTALLATION-TECHNICAL-DETAILS.md](docs/INSTALLATION-TECHNICAL-DETAILS.md)**: Technical deep-dive for developers
- **[TEMPLATE-USAGE-GUIDE.md](docs/TEMPLATE-USAGE-GUIDE.md)**: Step-by-step instructions plus rationale for customizing the template

---

## 🧪 Required Tests & Quality Gates

- Keep coverage-focused pytest suites (headless + GUI markers) so domain and UI regressions are caught before shipping.
- Always run the formatter (`black`), linter (`ruff`), and type checker (`mypy`) before pushing.
- Mirror the local CI scripts (`scripts/run-ci.ps1` / `.sh`) inside your automation so installer smoke tests stay representative.

```pwsh
# Run the default non-GUI suite with coverage
python -m pytest -m "not gui"

# Run only the GUI smoke tests (requires Tk runtime unless headless)
python -m pytest -m gui

# Formatting and linting
python -m black --check src tests
python -m ruff check src tests

# Static type checking
python -m mypy src

# Full tox automation (lint + type + tests)
python -m tox -e lint,type,py313

# One-command local CI rehearsal (PowerShell)
#   -> runs black/ruff/mypy, pytest markers, wheel-builder, installation.bat
pwsh scripts/run-ci.ps1

# Bash/zsh equivalent (uses a temporary virtualenv sandbox for installer verification)
bash scripts/run-ci.sh
```

### Local automation helpers

- `scripts/run-ci.ps1` / `scripts/run-ci.sh` mirror the CI pipeline (dev requirements + editable install + tox lint/type/py313). Run them before every push to catch formatting, typing, or packaging issues locally. Pass `-SkipRequirementsInstall` (PowerShell) or `SKIP_REQUIREMENTS_INSTALL=1` (bash/zsh) if you have already synced dependencies in the current shell.
- `.pre-commit-config.yaml` wires up Black, Ruff, mypy, file-format checks, **and now runs `python -m pytest -m "not gui"` both before each commit and push**. Install once and forget:

```pwsh
python -m pip install pre-commit
pre-commit install           # run on every commit
pre-commit install --hook-type pre-push
```

The pre-push hook replays the fast pytest suite and `tox -e lint,type`, matching the workflow GitHub Actions enforces.

---

## 🤝 Contributing

This is a template project, but improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Submit a pull request

---

## 📝 License

This project is licensed under the Zero-Clause BSD License (0BSD) - see the [LICENSE](LICENSE) file for details.

---

## 🎓 Learning Resources

### If You're New To:

**Python Packaging:**
- [Python Packaging User Guide](https://packaging.python.org/)
- [setuptools documentation](https://setuptools.pypa.io/)

**CustomTkinter:**
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [Tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)

**Virtual Environments:**
- [venv documentation](https://docs.python.org/3/library/venv.html)
- [Real Python: Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)

**Windows Scripting:**
- [VBScript Reference](https://docs.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/)
- [Batch Scripting Guide](https://ss64.com/nt/)

---

## 🚧 Roadmap / Future Enhancements

Potential improvements for this template:

- [ ] AI opponent (single-player mode)
- [ ] Settings/preferences system
- [ ] Multiple themes (dark/light mode)
- [ ] Sound effects
- [ ] Statistics tracking
- [ ] Linux/Mac installer support
- [ ] PyInstaller build for standalone .exe
- [ ] Automated testing in CI/CD
- [ ] Internationalization (i18n)

---

## 💡 Design Decisions

### Why CustomTkinter?
- Modern, professional look
- Easy to use (similar to Tkinter)
- Built-in theming support
- Active development and community

### Why Virtual Environment Installation?
- **Isolation**: No conflicts with user's Python packages
- **Clean**: Easy uninstall (just delete folder)
- **Professional**: Industry standard for Python applications
- **Versioning**: Each version can have different dependencies

### Why Wheel Distribution?
- **Standard**: Python-recommended distribution format
- **Fast**: Binary format, no compilation needed
- **Compatible**: Works with pip and all package managers
- **Professional**: Used by major Python projects

### Why VBScript Launcher?
- **Silent**: Runs without console window (pythonw.exe)
- **Integration**: Allows custom icon in taskbar
- **Simple**: No additional dependencies needed
- **Windows-native**: Uses built-in Windows Script Host

---

## ❓ FAQ

**Q: Can I use this for commercial projects?**
A: Yes. The 0BSD License places almost no restrictions on redistribution or commercial use.

**Q: Does this work on Linux/Mac?**
A: The installer is Windows-specific, but the code runs on any platform. You'd need to create platform-specific installers.

**Q: Can I package this as a standalone .exe?**
A: Yes! Use PyInstaller or similar tools. This template focuses on wheel distribution, but .exe packaging is compatible.

**Q: Why not use Qt/wxPython instead of Tkinter?**
A: CustomTkinter provides a modern look with Tkinter's simplicity. Qt/wxPython are great alternatives but have larger dependencies.

**Q: How do I update users to a new version?**
A: Users just run the new installer - it automatically removes the old version first.

---

## 🙏 Acknowledgments

- **CustomTkinter** by Tom Schimansky - Modern Tkinter components
- **Python Packaging Authority** - Packaging tools and guidance
- **Microsoft** - Windows integration APIs

---

## 📧 Contact

For questions about using this template:
- Open an issue on GitHub
- Check existing documentation
- Review the technical details document

---

**Built with ❤️ as a learning resource and project template**

*Last Updated: November 15, 2025*
