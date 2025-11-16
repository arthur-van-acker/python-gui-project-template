# Template Adoption Checklist

Use this linear checklist when cloning the YourApp Starter template. Each task links to the exact file (or documentation section) that needs an edit. Work in order—rename → config → UI → installer → docs—so renames propagate cleanly and your installers/tests stay in sync.

---

## 1. Rename & Update Metadata
- [ ] Update [`pyproject.toml`](../pyproject.toml) per the guidance in [README – Adopt This Template in Order](../README.md#adopt-this-template-in-order) (project name, description, version, authors, classifiers, entry points).
- [ ] Rename the package folder (`src/tictactoe`) and adjust imports as described in [docs/TEMPLATE-USAGE-GUIDE – Rename the Template Safely](./TEMPLATE-USAGE-GUIDE.md#3-rename-the-template-safely).
- [ ] Refresh the hero section and badges in [README – Project Goals](../README.md#-project-goals) to describe your product instead of the sample game.

## 2. Configure Look, Feel, and Assets
- [ ] Customize colors/fonts/copy in [`tictactoe.config.gui`](../src/tictactoe/config/gui.py) using the knobs highlighted in [README – Configuration Knobs You Can Toggle](../README.md#configuration-knobs-you-can-toggle).
- [ ] Replace media inside [`src/tictactoe/assets/`](../src/tictactoe/assets/) (favicon, themes, extra files) and confirm `wheel-builder.bat` copies any new folders.
- [ ] Document the available presets/env vars in [README – Choose a Frontend](../README.md#choose-a-frontend) after you rename them.

## 3. Align Domain Logic & Frontends
- [ ] Swap the sample rules inside [`tictactoe/domain/logic.py`](../src/tictactoe/domain/logic.py) and update usage in GUI/CLI modules as noted in [docs/TEMPLATE-USAGE-GUIDE – Keep the Architecture Contracts](./TEMPLATE-USAGE-GUIDE.md#4-keep-the-architecture-contracts).
- [ ] Rewrite copy and behaviors in [`tictactoe/ui/gui/main.py`](../src/tictactoe/ui/gui/main.py) and [`tictactoe/ui/cli/main.py`](../src/tictactoe/ui/cli/main.py) while keeping `HeadlessGameView` + automation hooks.
- [ ] Extend or prune the frontend dispatcher inside [`tictactoe/__main__.py`](../src/tictactoe/__main__.py) following [docs/TEMPLATE-USAGE-GUIDE – Leverage the Multi-Frontend Entry Point](./TEMPLATE-USAGE-GUIDE.md#5-leverage-the-multi-frontend-entry-point).

## 4. Tests, Tooling, and CI
- [ ] Update pytest fixtures/expected strings in [`tests/`](../tests/) so both `-m "not gui"` and `-m gui` suites pass with your domain (see [README – Required Tests & Quality Gates](../README.md#-required-tests--quality-gates)).
- [ ] Keep formatter/linter/type-checker invocations in [`scripts/run-ci.ps1`](../scripts/run-ci.ps1) and [`scripts/run-ci.sh`](../scripts/run-ci.sh) aligned with your Python version/tooling.
- [ ] Re-run `pwsh scripts/run-ci.ps1` (or the Bash equivalent) before every release to catch installer regressions.

## 5. Installers & Distribution
- [ ] Update [`wheel-builder.bat`](../wheel-builder.bat) to set the proper product metadata, shortcut names, smoke-test scripts, and helper docs for your brand.
- [ ] Verify the generated `installation.bat` + `tic-tac-toe-starter.vbs` pair reflect your renamed package (see [docs/INSTALLATION-TECHNICAL-DETAILS.md](./INSTALLATION-TECHNICAL-DETAILS.md) for the flow you must keep in sync).
- [ ] Double-check `dist/assets/`, `license.txt`, and `how-to-install-me.txt` for wording that mentions the sample app.

## 6. Documentation & Support Material
- [ ] Rewrite [README – Distribution & Installation](../README.md#-distribution--installation) with your installer paths, shortcuts, and troubleshooting tips.
- [ ] Update [docs/INSTALLATION-GUIDE.md](./INSTALLATION-GUIDE.md) and [docs/INSTALLATION-TECHNICAL-DETAILS.md](./INSTALLATION-TECHNICAL-DETAILS.md) to match the installer changes you made in step 5.
- [ ] Decide whether to keep or rewrite [docs/TEMPLATE-USAGE-GUIDE.md](./TEMPLATE-USAGE-GUIDE.md#9-update-docs-for-your-audience) for future internal contributors; link to the replacement if you move it.

---

**Finish Line:** When every box is checked, run `wheel-builder.bat --ci --no-pause`, execute `installation.bat` on a clean profile, launch the desktop shortcut, and archive the updated `TEMPLATE-CHECKLIST.md` so the next adopter benefits from your edits.
