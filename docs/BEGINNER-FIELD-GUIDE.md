# YourApp Starter Beginner Field Guide

Welcome! This all-in-one tutorial is for beginning programmers who know a bit of Python and want to ship a polished desktop app without wading through advanced docs. Work through it front to back or hop around using the Table of Contents—each section is self-contained and links to the deeper references when you're ready.

## Table of Contents {#table-of-contents}
1. [Welcome to YourApp Starter](#welcome)
2. [How to Use This Guide](#guide-map)
3. [Template Highlights at a Glance](#template-highlights)
4. [Set Up Your Local Environment](#setup)
5. [Install the Packaged Build](#installer)
6. [Launchers, Frontends, and Shortcuts](#frontends)
7. [Architecture Walkthrough](#architecture)
8. [Configuration & Theming](#configuration)
9. [Customize the Template Step by Step](#customizing)
10. [Automation & Headless Workflows](#automation)
11. [Build, Package, and Distribute](#build-release)
12. [Testing & Quality Gates](#testing)
13. [CI/CD & Release Automation](#cicd)
14. [Troubleshooting & FAQ](#troubleshooting)
15. [Next Steps & Additional Resources](#next-steps)

---

## 1. Welcome to YourApp Starter {#welcome}
YourApp Starter is a CustomTkinter-based template that shows how to ship a Windows-friendly desktop app with multiple launchers, automated installers, and docs-first guidance. It still looks like Tic Tac Toe out of the box, but the real goal is giving you a neutral codebase where you can plug in your own business rules without guessing how things hang together. For quick context, skim the project overview in `README.md` (see [README – Project Goals](../README.md#-project-goals)).

> _Screenshot placeholder: hero shot of the CustomTkinter window + CLI side by side so viewers can see both frontends._

[Back to TOC](#table-of-contents)

## 2. How to Use This Guide {#guide-map}
- **Beginners first:** Every section explains why something exists before diving into file paths.
- **Doc cross-links everywhere:** If you need a deeper dive, follow the inline links to `docs/*.md`. Advanced contributors can still stick with the original documentation set.
- **Screenshot placeholders:** Drop visuals wherever you see "Screenshot placeholder" callouts when you're ready to capture your own screenshots.
- **Return path:** Every section ends with a "Back to TOC" link so you can bounce around without losing your spot.

[Back to TOC](#table-of-contents)

## 3. Template Highlights at a Glance {#template-highlights}
Why teams adopt this starter (see [README – Template Highlights](../README.md#-template-highlights)):
- **One entry point, many frontends:** `python -m tictactoe` dispatches GUI, CLI, headless, or service modes from `src/tictactoe/__main__.py`.
- **Typed configuration:** `src/tictactoe/config/gui.py` keeps fonts, colors, layout, and copy as immutable dataclasses.
- **Installer + launcher duo:** `wheel-builder.bat` generates `installation.bat`, `tic-tac-toe-starter.vbs`, helper docs, and the signed wheel bundle under `dist/`.
- **Headless-friendly testing:** `tictactoe.ui.gui.headless_view` mirrors the CustomTkinter widgets so GUI tests run inside CI (documented in `docs/TESTING.md`).
- **Docs-first approach:** `docs/TEMPLATE-USAGE-GUIDE.md` and `docs/TEMPLATE-CHECKLIST.md` walk you through adopting the template in a specific order.

> _Screenshot placeholder: collage of `dist/` folder, installer console, and desktop shortcut._

[Back to TOC](#table-of-contents)

## 4. Set Up Your Local Environment {#setup}
Everything below is straight from `README.md` plus `docs/TEMPLATE-USAGE-GUIDE.md` Section 2.

1. **Clone and open the repo**
   ```pwsh
   git clone <your-fork-url>
   cd python-gui-project-template
   ```
2. **Create a virtual environment** (mirrors what the installer does):
   ```pwsh
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. **Install the editable package + dev tools** (requirements already end with `-e .`):
   ```pwsh
   pip install -r requirements.txt
   ```
4. **Launch the sample app**:
   ```pwsh
   python -m tictactoe
   ```
5. **List frontends** if you want to test the CLI or headless adapter:
   ```pwsh
   python -m tictactoe --list-frontends
   ```

Tip: keep `pwsh` terminals handy so PowerShell-specific scripts such as `wheel-builder.bat` and `scripts/run-ci.ps1` run without quoting gymnastics.

> _Screenshot placeholder: terminal session showing the activation + pip install + first run output._

[Back to TOC](#table-of-contents)

## 5. Install the Packaged Build {#installer}
Want to preview the real installer experience? Follow `docs/INSTALLATION-GUIDE.md`:

1. **Build artifacts** (or download a release ZIP):
   ```pwsh
   .\wheel-builder.bat
   ```
2. **Extract `dist/`** somewhere safe and double-click `installation.bat`.
3. The script will:
   - Delete previous installs (`%LOCALAPPDATA%\Programs\yourapp-starter-<version>`),
   - Create a private `.venv`,
   - Install the wheel,
   - Run `python -m tictactoe --ui service --script 0,4,8 --quiet`,
   - Drop `YourApp Starter.lnk` on the desktop via the VBScript launcher.
4. Launch from the shortcut (uses `pythonw.exe` so no console window pops up).

For an under-the-hood blow-by-blow, read `docs/INSTALLATION-TECHNICAL-DETAILS.md`—it covers everything from registry lookups for OneDrive desktops to how AppUserModelIDs keep icons tidy.

> _Screenshot placeholder: SmartScreen prompt and installer console log._

[Back to TOC](#table-of-contents)

## 6. Launchers, Frontends, and Shortcuts {#frontends}
`src/tictactoe/__main__.py` registers four `FrontendSpec` entries:

| Name | Target | When to use |
| --- | --- | --- |
| `gui` | `tictactoe.ui.gui.main:main` | CustomTkinter desktop app (default).
| `headless` | same target, but forces `TICTACTOE_HEADLESS=1` | GUI widgets rendered by the shim, perfect for CI.
| `cli` | `tictactoe.ui.cli.main:main` | Automation-friendly terminal client with `--script`/`--script-file`.
| `service` | `tictactoe.ui.service.main:main` | Headless/batch runner driven entirely by env vars.

Launch options (defaults shown in `README.md#choose-a-frontend`):
```pwsh
python -m tictactoe --ui gui --theme dark          # Named theme
python -m tictactoe --ui headless                  # Same GUI, shim widgets
python -m tictactoe --ui cli --script 0,4,8        # Scripted CLI run
python -m tictactoe --ui service --quiet           # Installer/CI style
```
Environment fallbacks keep installers and CI simple:
- `TICTACTOE_UI`, `TICTACTOE_HEADLESS`, `TICTACTOE_THEME*`
- `TICTACTOE_SCRIPT`, `TICTACTOE_SCRIPT_FILE`, `TICTACTOE_AUTOMATION_*`
- `TICTACTOE_LOGGING` (plus legacy `*_LOGGING`) enabling telemetry hooks defined in `src/tictactoe/controller/__init__.py`.

> _Screenshot placeholder: `python -m tictactoe --list-frontends` output next to the desktop shortcut properties dialog._

[Back to TOC](#table-of-contents)

## 7. Architecture Walkthrough {#architecture}
Use this section as your quick-reference script when explaining the template to teammates (full details live in `docs/ARCHITECTURE.md`).

1. **Entry Points (`python -m tictactoe`)** select a frontend via CLI flags or env vars.
2. **Frontends:**
   - GUI (`src/tictactoe/ui/gui/main.py`) instantiates `TicTacToeGUI`, loads CustomTkinter via `ui/gui/bootstrap.py`, and can swap to `HeadlessGameView` for tests.
   - CLI (`src/tictactoe/ui/cli/main.py`) renders placeholder automation summaries and supports JSON exports.
   - Service (`src/tictactoe/ui/service/main.py`) reuses the CLI automation helpers but reads env vars for scripts and labels.
3. **Controller hooks** (`src/tictactoe/controller/__init__.py`) centralize telemetry/logging so every frontend can emit consistent events.
4. **Domain layer** (`src/tictactoe/domain/logic.py`) ships as a stub with `ExampleState` snapshots and a `dispatch_action` method that you replace with real business logic.
5. **Config layer** (`src/tictactoe/config/gui.py`) contains immutable dataclasses plus `NAMED_THEMES`, serialization helpers, and JSON loaders.
6. **Assets & tools:** `src/tictactoe/assets/` for icons/themes and `src/tictactoe/tools/theme_codegen.py` for converting JSON themes into typed configs.
7. **Installer pipeline:** `wheel-builder.bat` → `dist/installation.bat` + VBScript launcher + helper docs.

> _Screenshot placeholder: architecture block diagram showing entry point → frontends → domain/config → installer._

[Back to TOC](#table-of-contents)

## 8. Configuration & Theming {#configuration}
Everything visual lives in `src/tictactoe/config/gui.py` (see `docs/CONFIGURATION.md`). The important bits:
- **`WindowConfig`** controls title, geometry, and resizability.
- **`GameViewConfig`** bundles fonts, layout, strings, and colors via nested dataclasses.
- **`NAMED_THEMES`** exposes `default`, `light`, `dark`, and `enterprise` presets plus helpers (`get_theme`, `list_themes`).
- **JSON round-tripping:** `serialize_game_view_config()` + `deserialize_game_view_config()` let you edit JSON themes under `src/tictactoe/assets/themes/` and load them at runtime.
- **CLI hooks:** `python -m tictactoe --theme dark` or `--theme-file path/to/theme.json` injects payloads through `TICTACTOE_THEME_PAYLOAD`.
- **Dataclass generation:** convert JSON to Python with `python -m tictactoe.tools.theme_codegen src/tictactoe/assets/themes/dark.json --variable-prefix brand`.

> _Screenshot placeholder: side-by-side view of light vs dark theme plus a snippet of the JSON payload._

[Back to TOC](#table-of-contents)

## 9. Customize the Template Step by Step {#customizing}
Follow `docs/TEMPLATE-CHECKLIST.md` for a linear adoption flow:

1. **Rename everything**
   - Update `[project]` metadata inside `pyproject.toml`.
   - Rename `src/tictactoe` to your package name and fix imports.
   - Refresh README hero copy and badges.
2. **Adjust config + assets**
   - Edit `tictactoe.config.gui` or drop new JSON themes.
   - Swap icons or additional files in `src/tictactoe/assets/` (wheel-builder copies the entire folder).
3. **Replace the domain placeholder**
   - Implement `TicTacToe.dispatch_action` (or rename the class) so the GUI/CLI keep receiving `ExampleState`-like snapshots.
   - Update tests in `tests/test_logic.py` to describe your real rules.
4. **Retheme the frontends**
   - Update copy/layout in `tictactoe/ui/gui/view.py` and `tictactoe/ui/gui/main.py` while leaving `HeadlessGameView` intact.
   - Rewrite CLI prompts or automation metadata in `tictactoe/ui/cli/main.py`.
5. **Keep quality gates green**
   - Re-run `pwsh scripts/run-ci.ps1` after every big change to mirror the CI workflow.
6. **Regenerate installers + docs**
   - Rebuild via `wheel-builder.bat`.
   - Update `docs/INSTALLATION-GUIDE.md`, `docs/INSTALLER-CUSTOMIZATION.md`, and `docs/RELEASE.md` with your new product name and flows.

> _Screenshot placeholder: checklist with checkmarks showing rename → config → UI → installer → docs._

[Back to TOC](#table-of-contents)

## 10. Automation & Headless Workflows {#automation}
Need scripted runs or CI demos without a GUI? Lean on the CLI + service pair from `README.md#choose-a-frontend` and `docs/TEMPLATE-USAGE-GUIDE.md#5-leverage-the-multi-frontend-entry-point`.

- **CLI mode (`tictactoe.ui.cli.main`)**
  ```pwsh
  python -m tictactoe.ui.cli.main --script 0,4,8 --output-json artifacts\automation.json --label nightly-demo
  ```
  Produces a human-readable summary plus optional JSON file and emits controller telemetry if `TICTACTOE_CLI_LOGGING=1`.
- **Service mode (`tictactoe.ui.service.main`)** consumes env vars:
  ```pwsh
  $env:TICTACTOE_SCRIPT = "0,4,8"
  $env:TICTACTOE_AUTOMATION_OUTPUT = "$PWD\artifacts\service.json"
  python -m tictactoe --ui service --quiet
  ```
- **Headless GUI** just works by launching `python -m tictactoe --ui headless` or setting `TICTACTOE_HEADLESS=1`; the shim lives in `tictactoe/ui/gui/headless_view.py`.
- **Telemetry hooks** (see `tictactoe/controller/__init__.py`) let every frontend log events once you flip `TICTACTOE_LOGGING=1`—great for installers or automated smoke tests.

> _Screenshot placeholder: log output from CLI automation plus a JSON summary snippet._

[Back to TOC](#table-of-contents)

## 11. Build, Package, and Distribute {#build-release}
`docs/RELEASE.md` and `docs/INSTALLER-CUSTOMIZATION.md` cover the production-ready workflow. The short version:

1. **Run local CI** first:
   ```pwsh
   pwsh scripts\run-ci.ps1
   ```
2. **Build artifacts**:
   ```pwsh
   .\wheel-builder.bat --ci --no-pause   # CI-style: installs into %TEMP%
   .\wheel-builder.bat                   # Interactive local build
   ```
   Outputs `dist/` with:
   - `tictactoe-<version>-py3-none-any.whl`
   - `installation.bat`
   - `tic-tac-toe-starter.vbs`
   - `assets/`, `how-to-install-me.txt`, `license.txt`, `install-info.json`
3. **Customize installers** by editing `wheel-builder.bat` (shortcut names, icons, install root, offline mode). Regenerate scripts after every change.
4. **Smoke test** the generated installer on a clean Windows profile.
5. **Zip and publish** `dist/` as the release payload (see `docs/RELEASE.md#6-publish-github-release`).

> _Screenshot placeholder: PowerShell transcript from `wheel-builder.bat` plus the resulting `dist/` explorer window._

[Back to TOC](#table-of-contents)

## 12. Testing & Quality Gates {#testing}
Everything you need lives in `docs/TESTING.md`, but here are the highlights:

- **pytest markers** split GUI vs non-GUI tests (`tests/test_gui.py` is headless-ready):
  ```pwsh
  python -m pytest -m "not gui"
  python -m pytest -m gui
  ```
- **Quality stack** (Black, Ruff, Mypy) matches what `scripts/run-ci.ps1` runs.
- **Sample suites:**
  - `tests/test_logic.py` documents the placeholder domain behavior.
  - `tests/test_cli.py` covers the multi-frontend dispatcher + CLI helpers.
  - `tests/test_config.py` guards exported symbols.
  - `tests/test_theme_codegen.py` keeps the JSON↔dataclass tooling solid.
- **Headless GUI testing** uses `tictactoe.ui.gui.headless_view.HeadlessGameView` so CustomTkinter widgets can be "rendered" without Tk.
- **Coverage** is optional but easy: `python -m pytest --cov=tictactoe --cov-report=term-missing`.
- **Helper commands** (from `docs/TESTING.md#16-quick-reference-commands`) keep newcomers productive.

> _Screenshot placeholder: VS Code test explorer or pytest output highlighting GUI vs non-GUI markers._

[Back to TOC](#table-of-contents)

## 13. CI/CD & Release Automation {#cicd}
`docs/CI-CD.md` pairs with `scripts/run-ci.ps1` / `scripts/run-ci.sh` and the existing GitHub Actions workflow.

- **Local rehearsal:**
  ```pwsh
  pwsh scripts\run-ci.ps1 -SkipRequirementsInstall
  ```
- **What the script runs:** editable install, Black, Ruff, Mypy, `pytest -m "not gui"`, GUI-only pytest, then installer smoke tests (Windows) or sandboxed wheel installs (POSIX).
- **GitHub Actions:** `.github/workflows/ci.yml` mirrors the same steps (lint, type, pytest, build wheel). Use the sample matrix in `docs/CI-CD.md` if you want tox-driven jobs.
- **Release workflow:** `docs/RELEASE.md` describes tagging, uploading `dist/`, and notifying users. When you need extra installer tweaks, capture them in `docs/INSTALLER-CUSTOMIZATION.md` for future maintainers.

> _Screenshot placeholder: CI pipeline diagram or GitHub Actions run summary._

[Back to TOC](#table-of-contents)

## 14. Troubleshooting & FAQ {#troubleshooting}
Common issues and quick fixes (see `docs/TROUBLESHOOTING.md` for the full FAQ):
- **Virtual environment fails:** Install Python 3.8+ with "Add to PATH" and delete partially created `.venv/` directories before retrying.
- **`pip install` blocked:** Pre-download wheels and add `--no-index --find-links`, covered in `docs/INSTALLER-CUSTOMIZATION.md`.
- **CustomTkinter / Tcl errors:** Force headless mode with `TICTACTOE_HEADLESS=1` or install the Tk runtime.
- **OneDrive desktop confusion:** The installer reads the registry path automatically; as a fallback, manually create a shortcut to `%LOCALAPPDATA%\Programs\yourapp-starter-<version>\tic-tac-toe-starter.vbs`.
- **Shortcut still says Tic Tac Toe:** Regenerate installers after editing `wheel-builder.bat` so the VBScript + `.lnk` pick up the new names.

> _Screenshot placeholder: snippet of `docs/TROUBLESHOOTING.md` or an error dialog with a fix overlay._

[Back to TOC](#table-of-contents)

## 15. Next Steps & Additional Resources {#next-steps}
Here’s where to go once you finish this guide:
- **Deep dives:**
  - Architecture: `docs/ARCHITECTURE.md`
  - Configuration & theming: `docs/CONFIGURATION.md`
  - Installer internals: `docs/INSTALLATION-TECHNICAL-DETAILS.md`
  - Template adoption story: `docs/TEMPLATE-USAGE-GUIDE.md` + `docs/TEMPLATE-CHECKLIST.md`
- **Stretch goals:** `docs/IMPROVEMENTS.md` tracks future-ready enhancements (e.g., telemetry, new themes, release automation).
- **Release playbook:** `docs/RELEASE.md` for tagging, smoke testing, and publishing zipped installers.
- **Community help:** capture your own FAQs or gotchas inside `docs/TROUBLESHOOTING.md` so the next teammate has zero surprises.

> _Screenshot placeholder: summary graphic highlighting the key links + "Happy Building!" message._

[Back to TOC](#table-of-contents)
