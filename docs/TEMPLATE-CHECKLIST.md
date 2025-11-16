# Template Adoption Checklist

Use this checklist when cloning the Tic Tac Toe template for a new product. Each section focuses on a single file (or tightly coupled file pair) so you can mark off the updates you complete. Keep the template9s architecture intact unless you intentionally change it and document the rationale in your own repo.

---

## LICENSE
- [ ] Replace the copyright line with your organization and year.
- [ ] Confirm the chosen license matches your distribution requirements.
- [ ] If you change the license, update any license badges in `README.md` accordingly.

## README.md
- [ ] Rename the project and refresh the hero description/screenshots.
- [ ] Update badges (Python version, license, platform) to match your targets.
- [ ] Rewrite the “Project Goals” and “Features” sections for your app.
- [ ] Adjust quick-start instructions so they reference your distribution artifact names.
- [ ] Verify architecture diagrams and directory listings reflect your layout after renaming packages.

## pyproject.toml
- [ ] Update `[project]` metadata (`name`, `version`, `description`, `authors`, `urls`).
- [ ] Confirm `requires-python` and dependency lists match your runtime needs.
- [ ] Change the console entry point (under `[project.scripts]` or `[project.gui-scripts]`) to the new package/module name.
- [ ] Review classifiers to ensure they describe your audience and license.

## src/tictactoe/__init__.py & __main__.py
- [ ] Rename the package folder (`tictactoe`) to your module name and fix imports.
- [ ] Update `__all__`, version strings, and docstrings.
- [ ] In `__main__.py`, rename CLI flags or environment variables if you change the UI selector names.
- [ ] Register or remove frontends in the `FRONTENDS` dispatch map based on what you ship.

## src/tictactoe/domain/logic.py
- [ ] Replace the Tic Tac Toe rules with your own domain logic while keeping public APIs stable or updating every caller (`ui` packages and tests).
- [ ] Ensure docstrings and type hints explain the new rules/state machine.
- [ ] Add new unit tests in `tests/test_logic.py` for your rules.

## src/tictactoe/config/gui.py
- [ ] Update dataclass defaults (colors, fonts, copy) for your brand.
- [ ] Remove unused config fields or add new ones; document them in `README.md`.
- [ ] Propagate config changes into `ui/gui` so widgets consume the new options.

## src/tictactoe/assets/
- [ ] Replace `favicon.ico` and any other bundled media with your branding.
- [ ] Verify `wheel-builder.bat` copies any new assets into `dist/`.
- [ ] If you add fonts/images, update `pyproject.toml` and `MANIFEST.in` (if applicable) to include them in the wheel.

## src/tictactoe/ui/gui/main.py & view.py
- [ ] Update window titles, status text, and callbacks to speak your domain language.
- [ ] Confirm `HeadlessGameView` still mirrors the live widgets for CI use.
- [ ] Wire in any new controllers or services but keep the view adapter pattern intact.

## src/tictactoe/ui/cli/main.py
- [ ] Rewrite prompts and output strings for your game/app.
- [ ] Maintain CLI arguments (`--ui`, `--script`, etc.) or document breaking changes.
- [ ] Update tests in `tests/test_cli.py` as needed.

## docs/INSTALLATION-GUIDE.md
- [ ] Replace screenshots, file names, and installer copy with your branding.
- [ ] Ensure OS requirements, shortcut names, and uninstall steps match your installer behavior.
- [ ] Link to your public support resources.

## docs/INSTALLATION-TECHNICAL-DETAILS.md
- [ ] Document any modifications to `installation.bat`, VBS scripts, or environment layout.
- [ ] Call out additional dependencies (e.g., system packages, GPU drivers).
- [ ] Note any security considerations (code signing, antivirus exceptions, etc.).

## docs/TESTING.md
- [ ] Align the documented test matrix with the suites you run (pytest markers, tox environments, GUI smoke tests).
- [ ] Update instructions for running tests locally and in CI.

## wheel-builder.bat
- [ ] Search-and-replace `ttt.v0.1.0` and other paths with your package/version.
- [ ] Update shortcut names, icon references, and any hard-coded wheel filenames.
- [ ] Review the generated `license.txt` and `how-to-install-me.txt` sections for accuracy.
- [ ] If you add new artifacts, append copy steps or creation blocks.

## docs/TEMPLATE-USAGE-GUIDE.md
- [ ] Decide whether to keep this file for contributors; if so, rewrite it with guidance specific to your template.
- [ ] If you remove it, reference the replacement in the README so future template users know where to start.

## scripts/run-ci.ps1 & run-ci.sh
- [ ] Adapt environment bootstrap commands (Python version, poetry/uv/pip usage).
- [ ] Keep parity between PowerShell and Bash versions for cross-platform CI.

## tests/
- [ ] Update fixtures and expected strings after renaming packages or changing domain logic.
- [ ] Add coverage for any new modules you introduce.
- [ ] Ensure GUI tests still run headless (markers/types in `pytest.ini`).

## installers (installation.bat, tic-tac-toe-starter.vbs)
- [ ] Rename shortcut labels, window titles, and target paths.
- [ ] Confirm the VBS launcher points to your package module.
- [ ] If you add post-install tasks (config files, telemetry opt-in), script them here and document the behavior.

---

**Tip:** When the checklist is complete, run `wheel-builder.bat`, execute the generated installer on a clean Windows profile, and perform a smoke test using the new desktop shortcut. Finally, update `TEMPLATE-CHECKLIST.md` with any project-specific steps you discovered so the next contributor benefits from your learnings.
