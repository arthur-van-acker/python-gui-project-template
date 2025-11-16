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
YourApp Starter is a CustomTkinter-based template that shows how to ship a Windows-friendly desktop app with multiple launchers, automated installers, and docs-first guidance. It still looks like Tic Tac Toe out of the box, but the real goal is giving you a neutral codebase where you can plug in your own business rules without guessing how things hang together. Think of CustomTkinter as "Tkinter with a modern skin"—you still write standard Python widgets, but the toolkit adds dark mode, theming, and rounder controls. For quick context, skim the project overview in `README.md` (see [README – Project Goals](../README.md#-project-goals)).

Screenshot TODO: capture a single image that shows the GUI, CLI, and desktop shortcut after you finish Section 9 so learners know what a successful setup looks like.

> _Screenshot placeholder: hero shot of the CustomTkinter window + CLI side by side so viewers can see both frontends._

[Back to TOC](#table-of-contents)

## 2. How to Use This Guide {#guide-map}
- **Beginners first:** Every section explains why something exists before diving into file paths.
- **Doc cross-links everywhere:** If you need a deeper dive, follow the inline links to `docs/*.md`. Advanced contributors can still stick with the original documentation set.
- **Screenshot placeholders:** Drop visuals wherever you see "Screenshot placeholder" callouts when you're ready to capture your own screenshots.
- **Return path:** Every section ends with a "Back to TOC" link so you can bounce around without losing your spot.

When you reach a screenshot placeholder, jot down the scenario it should capture (e.g., "Section 4 install log") and grab the image the first time you successfully finish that step. Keeping a running list now prevents a last-minute scramble before release day.

**Quick glossary for recurring terms**
- *headless mode:* Runs the GUI logic with fake widgets so CI can exercise it without a display.
- *service mode:* An automation-first launcher that reads environment variables instead of prompting you.
- *telemetry hooks:* Convenience functions in `src/tictactoe/controller/__init__.py` that log structured events when you flip logging env vars.
- *CustomTkinter:* A themed fork of Tkinter that exposes the same widget concepts with a modern appearance.

### Quick prerequisites
- **OS & tooling:** Windows 10/11 for installer work, macOS/Linux acceptable for CLI/GUI dev, PowerShell 7+ or a modern bash shell, and Git if you plan to contribute back.
- **Python basics:** Comfortable creating/activating virtual environments, running `python -m <module>`, and installing wheels.
- **GUI requirements:** Tk runtime (bundled with official Windows Python installers) or willingness to run in headless mode during CI.
- **Optional niceties:** VS Code or another IDE with Python linting, plus a screenshot tool for the placeholders later in the guide.

### Choose your learning path
- **Quick trial:** Follow Sections 4–6 and 10 to clone, run the GUI/CLI, and explore automation without touching installers.
- **Reskin & rename:** Pair Sections 4, 8, and 9 with [Template Usage Guide – Bootstrap Your Copy](./TEMPLATE-USAGE-GUIDE.md#2-bootstrap-your-copy) and [Template Checklist – Rename the Template Safely](./TEMPLATE-CHECKLIST.md#3-rename-the-template-safely) for the exact search/replace order.
- **Ship installers & CI:** Combine Sections 4–5, 10–13, plus [Installation Guide – Installation Steps](./INSTALLATION-GUIDE.md#installation-steps) and [CI/CD Overview – Local & Cloud Pipelines](./CI-CD.md#cicd-overview) to rehearse packaging, smoke tests, and GitHub Actions.

[Back to TOC](#table-of-contents)

## 3. Template Highlights at a Glance {#template-highlights}
Why teams adopt this starter (see [README – Template Highlights](../README.md#-template-highlights)):
- **One entry point, many frontends:** `python -m tictactoe` dispatches GUI, CLI, headless, or service modes from `src/tictactoe/__main__.py`. You never touch multiple scripts—flags or env vars pick the experience for you.
- **Typed configuration:** `src/tictactoe/config/gui.py` keeps fonts, colors, layout, and copy as immutable dataclasses, so changing `GameViewConfig` feels like editing normal Python objects instead of ad-hoc dicts.
- **Installer + launcher duo:** `wheel-builder.bat` generates `installation.bat`, `tic-tac-toe-starter.vbs`, helper docs, and the signed wheel bundle under `dist/`. That bundle is exactly what you zip and ship to testers.
- **Headless-friendly testing:** `tictactoe.ui.gui.headless_view` mirrors the CustomTkinter widgets so GUI tests run inside CI (documented in `docs/TESTING.md`). Flip `TICTACTOE_HEADLESS=1` and the app behaves like the GUI even though no window opens.
- **Docs-first approach:** `docs/TEMPLATE-USAGE-GUIDE.md` and `docs/TEMPLATE-CHECKLIST.md` walk you through adopting the template in a specific order, preventing "where do I start?" moments.

> _Screenshot placeholder: collage of `dist/` folder, installer console, and desktop shortcut._

[Back to TOC](#table-of-contents)

## 4. Set Up Your Local Environment {#setup}
Everything below is distilled from [README – Quick Start](../README.md#-quick-start), which explains why the template standardizes on CustomTkinter + isolated installs, and [Template Usage Guide – Bootstrap Your Copy](./TEMPLATE-USAGE-GUIDE.md#2-bootstrap-your-copy), which walks step-by-step through cloning, creating a venv, and installing the editable package.

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

macOS/Linux quick ref:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m tictactoe --ui cli --script 0,4,8
```

If Windows blocks the activation script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once inside an elevated PowerShell window. Need Python first? Install from python.org, check "Add to PATH," then reopen your terminal so `python` resolves correctly.

> **Troubleshooting tip:** If `python -m venv` fails or `pip install` cannot reach the internet, follow [Troubleshooting – Virtual Environment Creation Fails](./TROUBLESHOOTING.md#virtual-environment-creation-fails) and [Troubleshooting – `pip install` Cannot Reach the Internet](./TROUBLESHOOTING.md#pip-install-cannot-reach-the-internet) for cleanup commands, proxy flags, and offline wheel instructions before retrying the steps above.

> _Screenshot placeholder: terminal session showing the activation + pip install + first run output._

[Back to TOC](#table-of-contents)

## 5. Install the Packaged Build {#installer}
Want to preview the real installer experience? Follow [Installation Guide – Installation Steps](./INSTALLATION-GUIDE.md#installation-steps) for the screenshot-by-screenshot flow covering SmartScreen prompts, expected console logs, and how to relaunch from the shortcut without reopening a terminal.

> Windows-only heads up: the installer and `.bat/.vbs` scripts rely on PowerShell and the Windows desktop shell. If SmartScreen pauses the run, choose **More info > Run anyway** after verifying the script came from your build.

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

Expected log excerpt so you know things are on track:
```
Creating venv under %LOCALAPPDATA%\Programs\yourapp-starter-<version>
Installing wheel ... done
Seed data: python -m tictactoe --ui service --script 0,4,8 --quiet
Shortcut created on Desktop
```

For an under-the-hood blow-by-blow, read [Installation Technical Details – Installation Process](./INSTALLATION-TECHNICAL-DETAILS.md#installation-process---step-by-step); it explains each batch/VBScript command, registry lookup, and AppUserModelID tweak so you can customize the installer confidently.

> **Troubleshooting tip:** If `wheel-builder.bat` cannot locate `python` or the desktop shortcut keeps the old name/icon after a rename, jump to [Troubleshooting – Wheel Builder Cannot Find `python`](./TROUBLESHOOTING.md#wheel-builder-cannot-find-python) and [Troubleshooting – Desktop Shortcut Uses Old Name/Icon](./TROUBLESHOOTING.md#desktop-shortcut-uses-old-nameicon) for the exact script edits and cleanup commands before rerunning the installer.

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

Launch options (mirrors the quick table in [README – Choose a Frontend](../README.md#choose-a-frontend)):
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

Setter quick ref:
```pwsh
$env:TICTACTOE_HEADLESS = "1"
python -m tictactoe
Remove-Item Env:TICTACTOE_HEADLESS
```
```bash
export TICTACTOE_HEADLESS=1
python -m tictactoe
unset TICTACTOE_HEADLESS
```

Think of **headless mode** as a fake GUI—it renders the same layout through `HeadlessGameView`, so screenshot tests and CI runs stay deterministic. **Service mode** skips prompts entirely and only reads environment variables, which is what the installer and smoke tests rely on. Capture a screenshot of `python -m tictactoe --list-frontends` and the shortcut properties to replace the placeholder once everything is renamed.

> _Screenshot placeholder: `python -m tictactoe --list-frontends` output next to the desktop shortcut properties dialog._

[Back to TOC](#table-of-contents)

## 7. Architecture Walkthrough {#architecture}
Use this section as your quick-reference script when explaining the template to teammates; [Architecture Deep Dive – Layer Diagram](./ARCHITECTURE.md#architecture-deep-dive) includes the full diagram and class-level notes if you want the play-by-play.

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

Whenever you replace the domain logic, keep returning `ExampleState`-shaped objects so the GUI bindings stay alive. Later you can rename the class once tests and UI references are updated. Telemetry hooks are just helper functions (`emit_event`, `log_action`, etc.)—calling them is optional during prototyping but useful once you need trace logs.

> _Screenshot placeholder: architecture block diagram showing entry point → frontends → domain/config → installer._

[Back to TOC](#table-of-contents)

## 8. Configuration & Theming {#configuration}
Everything visual lives in `src/tictactoe/config/gui.py` (see [Configuration Guide – GUI Config Reference](./CONFIGURATION.md#configuration--theming-reference) for field-by-field defaults and layout diagrams). The important bits:
- **`WindowConfig`** controls title, geometry, and resizability.
- **`GameViewConfig`** bundles fonts, layout, strings, and colors via nested dataclasses.
- **`NAMED_THEMES`** exposes `default`, `light`, `dark`, and `enterprise` presets plus helpers (`get_theme`, `list_themes`).
- **JSON round-tripping:** `serialize_game_view_config()` + `deserialize_game_view_config()` let you edit JSON themes under `src/tictactoe/assets/themes/` and load them at runtime.
- **CLI hooks:** `python -m tictactoe --theme dark` or `--theme-file path/to/theme.json` injects payloads through `TICTACTOE_THEME_PAYLOAD`.
- **Dataclass generation:** convert JSON to Python with `python -m tictactoe.tools.theme_codegen src/tictactoe/assets/themes/dark.json --variable-prefix brand`.

Mini walkthrough:
```bash
cp src/tictactoe/assets/themes/dark.json tmp-theme.json
# Edit tmp-theme.json colors/fonts...
python -m tictactoe.tools.theme_codegen tmp-theme.json --variable-prefix demo
python -m tictactoe --theme-file tmp-theme.json
```
If the app loads without complaining, your JSON validated; if not, the stack trace points to the exact field that needs fixing.

> _Screenshot placeholder: side-by-side view of light vs dark theme plus a snippet of the JSON payload._

[Back to TOC](#table-of-contents)

## 9. Customize the Template Step by Step {#customizing}
Follow [Template Adoption Checklist – Rename → Docs Flow](./TEMPLATE-CHECKLIST.md#template-adoption-checklist); it spells out the exact order (rename → config → UI → installer → docs) so you never break imports or ship stale shortcuts.

1. **Rename everything**
   - Update `[project]` metadata inside `pyproject.toml`.
   - Rename `src/tictactoe` to your package name and fix imports.
   - Refresh README hero copy and badges.

   Quick helper commands (PowerShell shown, adapt paths as needed—double-check matches before replacing so you do not rename unrelated strings inside JSON/assets):
   ```pwsh
   Rename-Item src/tictactoe src/<your_package>
   Get-ChildItem -Recurse -Filter *.py | ForEach-Object { (Get-Content $_.FullName) -replace "tictactoe","<your_package>" | Set-Content $_.FullName }
   python -m pytest -m "not gui"
   ```
   When the test run passes, commit immediately—you just validated the rename.
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

   Watching the script finish once gives you confidence that GitHub Actions will accept your PR later.
6. **Regenerate installers + docs**
   - Rebuild via `wheel-builder.bat`.
   - Update [Installation Guide – Installation Steps](./INSTALLATION-GUIDE.md#installation-steps) with your new product names/log excerpts, [Installer Customization – Common Customizations](./INSTALLER-CUSTOMIZATION.md#common-customizations) so template variables stay in sync, and [Release Playbook – Publish GitHub Release](./RELEASE.md#6-publish-github-release) so downstream instructions match the updated artifacts.

> **Troubleshooting tip:** If the desktop shortcut or installer assets keep referencing the old name after step 6, revisit [Troubleshooting – Desktop Shortcut Uses Old Name/Icon](./TROUBLESHOOTING.md#desktop-shortcut-uses-old-nameicon) to clear cached VBScript files and rebuild before distributing artifacts.

> _Screenshot placeholder: checklist with checkmarks showing rename → config → UI → installer → docs._

Replace the placeholder with a screenshot of your own tracking document, VS Code checklist, or whiteboard so future readers can see what progress looks like.

[Back to TOC](#table-of-contents)

## 10. Automation & Headless Workflows {#automation}
Need scripted runs or CI demos without a GUI? Lean on the CLI + service pair from [README – Choose a Frontend](../README.md#choose-a-frontend), which lists every flag/env fallback combo, and [Template Usage Guide – Leverage the Multi-Frontend Entry Point](./TEMPLATE-USAGE-GUIDE.md#5-leverage-the-multi-frontend-entry-point), which shows how to register new launchers or override defaults.

- **CLI mode (`tictactoe.ui.cli.main`)**
  ```pwsh
  python -m tictactoe.ui.cli.main --script 0,4,8 --output-json artifacts\automation.json --label nightly-demo
  ```
  Produces a human-readable summary plus optional JSON file and emits controller telemetry if `TICTACTOE_CLI_LOGGING=1`.
   Example JSON payload:
   ```json
   {
      "label": "nightly-demo",
      "moves": [0,4,8],
      "result": "player_x"
   }
   ```
- **Service mode (`tictactoe.ui.service.main`)** consumes env vars:
  ```pwsh
  $env:TICTACTOE_SCRIPT = "0,4,8"
  $env:TICTACTOE_AUTOMATION_OUTPUT = "$PWD\artifacts\service.json"
  python -m tictactoe --ui service --quiet
  ```
   Remember to clean up afterward with `Remove-Item Env:TICTACTOE_SCRIPT, Env:TICTACTOE_AUTOMATION_OUTPUT` (PowerShell) or `unset` (bash) so later runs do not inherit old values.
- **Headless GUI** just works by launching `python -m tictactoe --ui headless` or setting `TICTACTOE_HEADLESS=1`; the shim lives in `tictactoe/ui/gui/headless_view.py`.
- **Telemetry hooks** (see `tictactoe/controller/__init__.py`) let every frontend log events once you flip `TICTACTOE_LOGGING=1`—great for installers or automated smoke tests.

> **Troubleshooting tip:** If headless runs complain that `HeadlessGameView has not been built yet`, follow [Troubleshooting – Headless Tests Crash](./TROUBLESHOOTING.md#headless-tests-crash-with-headlessgameview-has-not-been-built-yet) to ensure `build()` is called before `render()` and that your custom views respect the `GameViewPort` contract.

> _Screenshot placeholder: log output from CLI automation plus a JSON summary snippet._ ← Capture the CLI summary text next to the JSON file in your editor once you have the automation folder in place.

[Back to TOC](#table-of-contents)

## 11. Build, Package, and Distribute {#build-release}
See [Release Playbook – Build & Release](./RELEASE.md#build--release-playbook) for the full checklist and [Installer Customization – Where to Edit](./INSTALLER-CUSTOMIZATION.md#where-to-edit) for the knobs that regenerate installer/launcher scripts. The short version:

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
5. **Zip and publish** `dist/` as the release payload (see [Release Playbook – Publish GitHub Release](./RELEASE.md#6-publish-github-release)).

> **Troubleshooting tip:** If `wheel-builder.bat` fails mid-run or leaves stale installs behind, check [Troubleshooting – Wheel Builder Cannot Find `python`](./TROUBLESHOOTING.md#wheel-builder-cannot-find-python) and [Troubleshooting – Installer Leaves Behind Old Versions](./TROUBLESHOOTING.md#installer-leaves-behind-old-versions) before rerunning the build; both sections include the cleanup commands and script flags needed to recover.

`--ci` skips pauses and writes to `%TEMP%` so GitHub Actions can run unattended; the plain invocation prompts you and installs under `%LOCALAPPDATA%`. Both commands require Windows, PowerShell, and access to the Windows desktop shell (no Server Core). Capture a screenshot of the final `dist/` explorer window before zipping so teammates know exactly which files to ship.

> _Screenshot placeholder: PowerShell transcript from `wheel-builder.bat` plus the resulting `dist/` explorer window._

[Back to TOC](#table-of-contents)

## 12. Testing & Quality Gates {#testing}
Everything you need lives in [Testing Guide – Toolchain & Markers](./TESTING.md#testing-guide), but here are the highlights:

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

If Tk libraries are missing on Windows, install the official Python build (it bundles Tk) or set `TICTACTOE_HEADLESS=1` before running GUI tests. macOS/Linux users should install the system `tk` package (`brew install python-tk` or distro equivalent). Typical pytest success output:
```
==================== 12 passed, 2 skipped in 5.23s ====================
```
Seeing green like that means you can move on to packaging with confidence.

> _Screenshot placeholder: VS Code test explorer or pytest output highlighting GUI vs non-GUI markers._

[Back to TOC](#table-of-contents)

## 13. CI/CD & Release Automation {#cicd}
[CI/CD Overview – Local Automation Stack](./CI-CD.md#cicd-overview) pairs with `scripts/run-ci.ps1` / `scripts/run-ci.sh` and the existing GitHub Actions workflow so you can rehearse every job locally before pushing.

- **Local rehearsal:**
  ```pwsh
  pwsh scripts\run-ci.ps1 -SkipRequirementsInstall
  ```
- **What the script runs:** editable install, Black, Ruff, Mypy, `pytest -m "not gui"`, GUI-only pytest, then installer smoke tests (Windows) or sandboxed wheel installs (POSIX).
- **GitHub Actions:** `.github/workflows/ci.yml` mirrors the same steps (lint, type, pytest, build wheel). The sample matrix in [CI/CD Overview – Sample GitHub Actions Workflow](./CI-CD.md#sample-github-actions-workflow) shows how to wire tox if you prefer environment matrices.
- **Release workflow:** [Release Playbook – Publish GitHub Release](./RELEASE.md#6-publish-github-release) covers tagging, uploading `dist/`, and notifying users. When you need extra installer tweaks, log them in [Installer Customization – Common Customizations](./INSTALLER-CUSTOMIZATION.md#common-customizations) so future maintainers know why scripts changed.

Open `.github/workflows/ci.yml` to see the exact job order; the file sits at the repo root so you can tweak it without hunting around. To re-run a workflow manually, head to GitHub → Actions tab → pick the `CI` workflow → **Run workflow**. Grab a screenshot of the green workflow summary for this section once your branch passes.

> _Screenshot placeholder: CI pipeline diagram or GitHub Actions run summary._

[Back to TOC](#table-of-contents)

## 14. Troubleshooting & FAQ {#troubleshooting}
Common issues and quick fixes (the complete matrix lives in [Troubleshooting & FAQ](./TROUBLESHOOTING.md#troubleshooting--faq)):
- **Virtual environment fails:** Install Python 3.8+ with "Add to PATH" and delete partially created `.venv/` directories before retrying.
- **`pip install` blocked:** Pre-download wheels and add `--no-index --find-links`, covered in `docs/INSTALLER-CUSTOMIZATION.md`.
- **CustomTkinter / Tcl errors:** Force headless mode with `TICTACTOE_HEADLESS=1` or install the Tk runtime.
- **OneDrive desktop confusion:** The installer reads the registry path automatically; as a fallback, manually create a shortcut to `%LOCALAPPDATA%\Programs\yourapp-starter-<version>\tic-tac-toe-starter.vbs`.
- **Shortcut still says Tic Tac Toe:** Regenerate installers after editing `wheel-builder.bat` so the VBScript + `.lnk` pick up the new names.

> _Screenshot placeholder: snippet of `docs/TROUBLESHOOTING.md` or an error dialog with a fix overlay._

Quick matcher table (copy into your notes as you debug):

| Symptom | Likely cause | Fast fix |
| --- | --- | --- |
| `Activate.ps1 cannot be loaded because running scripts is disabled on this system.` | Execution policy blocking venv activation | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` then retry |
| `ModuleNotFoundError: No module named 'tictactoe'` after rename | Imports still reference old package name | Run a project-wide search/replace for `tictactoe` and rerun tests |
| SmartScreen warns "unrecognized app" when running installer | Unsigned local build | Click **More info > Run anyway** after verifying hash/source |
| GUI launch fails with `No module named '_tkinter'` | Tk runtime missing | Install official Python or system `tk` package, or force headless mode |

[Back to TOC](#table-of-contents)

## 15. Next Steps & Additional Resources {#next-steps}
Here’s where to go once you finish this guide:
- **Deep dives:**
   - Architecture: [Architecture Deep Dive – Layer Diagram](./ARCHITECTURE.md#architecture-deep-dive) explains how entry points, controllers, config, and installers connect.
   - Configuration & theming: [Configuration Guide – GUI Config Reference](./CONFIGURATION.md#configuration--theming-reference) lists every dataclass field, default, and layout diagram.
   - Installer internals: [Installation Technical Details – Installation Process](./INSTALLATION-TECHNICAL-DETAILS.md#installation-process---step-by-step) walks through each batch/VBScript command so you can customize safely.
   - Template adoption story: [Template Usage Guide – Bootstrap → Docs](./TEMPLATE-USAGE-GUIDE.md#template-usage-guide--design-rationale) plus [Template Adoption Checklist – Rename → Docs Flow](./TEMPLATE-CHECKLIST.md#template-adoption-checklist) narrate the recommended end-to-end workflow.
- **Stretch goals:** [Improvements Plan – Upcoming Enhancements](./IMPROVEMENTS.md#template-improvement-plan) tracks telemetry ideas, new themes, and release automation experiments.
- **Release playbook:** [Release Playbook – Build & Release](./RELEASE.md#build--release-playbook) covers tagging, smoke testing, signing, and publishing zipped installers.
- **Community help:** Capture FAQs or gotchas inside [Troubleshooting & FAQ](./TROUBLESHOOTING.md#troubleshooting--faq) so the next teammate has zero surprises.

> _Screenshot placeholder: summary graphic highlighting the key links + "Happy Building!" message._

Suggested next-study order once this guide clicks: [Architecture Deep Dive – Layer Diagram](./ARCHITECTURE.md#architecture-deep-dive) → [Configuration Guide – GUI Config Reference](./CONFIGURATION.md#configuration--theming-reference) → [Template Usage Guide – Bootstrap → Docs](./TEMPLATE-USAGE-GUIDE.md#template-usage-guide--design-rationale) → [Release Playbook – Build & Release](./RELEASE.md#build--release-playbook). Pair that with two hands-on tasks—(1) create a brand-new theme JSON, and (2) rerun `scripts/run-ci.ps1`—so the knowledge sticks.

[Back to TOC](#table-of-contents)
