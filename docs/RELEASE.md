# Build & Release Playbook

Follow this checklist whenever you cut a new template release so downstream users receive a reproducible installer.

## 1. Prep the Repository
1. Verify the working tree is clean: `git status -sb`.
2. Update `pyproject.toml`:
   - Bump `version`.
   - Refresh `[project.urls]` and metadata if necessary.
3. Update `README.md` badges (version tag) and any docs referencing the version number (`wheel-builder.bat` embeds `ttt.v0.1.0`).
4. Regenerate `CHANGELOG.md` (if applicable) and mention new features/fixes.

## 2. Run Quality Gates
Use the provided scripts to match CI:

```powershell
pwsh scripts/run-ci.ps1
```
```bash
./scripts/run-ci.sh
```

These commands:
- Install dependencies (unless `-SkipRequirementsInstall`/`SKIP_REQUIREMENTS_INSTALL=1`).
- Execute `tox -e lint,type,py313`, which runs Ruff, Black, Mypy, and pytest (GUI + non-GUI markers).
- Mirror the pre-commit configuration, ensuring commits will pass hooks.

## 3. Build Distribution Artifacts
1. Activate the project virtual environment (`.venv\Scripts\activate`).
2. Run `wheel-builder.bat` from the repo root. The script will:
   - Clean `dist/` and previous build outputs.
   - Invoke `python -m build --wheel` producing `tictactoe-<version>-py3-none-any.whl`.
   - Copy `favicon.ico` and auto-generate helper docs (`license.txt`, `how-to-install-me.txt`).
   - Emit `installation.bat` and `tic-tac-toe-starter.vbs` tailored to `%LOCALAPPDATA%\Programs\ttt.vX.Y.Z`.
3. Inspect `dist/`:
   - Wheel file.
   - `installation.bat`.
   - `tic-tac-toe-starter.vbs`.
   - `favicon.ico` + documentation.

## 4. Smoke Test the Installer
1. Copy the `dist/` folder to a Windows test machine or clean user profile.
2. Double-click `installation.bat` and wait for "Installation complete".
3. Launch the app via the desktop shortcut and ensure:
   - Icons render correctly.
   - GUI + CLI entry points function.
   - Uninstall (delete `%LOCALAPPDATA%\Programs\ttt.vX.Y.Z` and shortcut) works without leftover files.

## 5. Optional Code Signing
If your organization signs scripts/executables:
- Sign the wheel using `signtool` or your package registry’s signing workflow.
- Sign `installation.bat` and `tic-tac-toe-starter.vbs` if your IT policy requires it. Document the process in `docs/INSTALLER-CUSTOMIZATION.md`.

## 6. Publish GitHub Release
1. Create a tag (`git tag vX.Y.Z && git push origin vX.Y.Z`).
2. On GitHub, draft a release:
   - Title: `vX.Y.Z`.
   - Copy changelog highlights.
   - Upload zipped `dist/` (or individual wheel + installer bundle).
3. Attach release notes linking to `INSTALLATION-GUIDE.md` for end users and `RELEASE.md` for maintainers.

## 7. Notify Consumers
- Update README badges or documentation portals.
- Communicate the release internally (Teams/Slack) with links to the download and changelog.

## 8. Post-Release Maintenance
- Increment the version (e.g., set to `<next>.dev0`) so ongoing commits are clearly ahead of the release.
- Capture any follow-up issues discovered during smoke tests in GitHub issues.

Following this playbook keeps releases predictable, reproducible, and documented so anyone on the team can ship a new version without guesswork.
