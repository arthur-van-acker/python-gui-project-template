"""Main entry point for the Tic Tac Toe application."""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Mapping, MutableMapping, Optional, Sequence, cast

FrontendRunner = Callable[[], Optional[int]]

_FRONTEND_ENV_VAR = "TICTACTOE_UI"
_DEFAULT_FRONTEND = "gui"
_THEME_ENV_VAR = "TICTACTOE_THEME"
_THEME_FILE_ENV_VAR = "TICTACTOE_THEME_FILE"
_THEME_PAYLOAD_ENV_VAR = "TICTACTOE_THEME_PAYLOAD"


@dataclass(frozen=True)
class FrontendSpec:
    """Definition for a UI frontend that can be launched from the CLI."""

    target: str
    description: str
    env_overrides: Mapping[str, str] = field(default_factory=dict)

    def load(self) -> FrontendRunner:
        """Import and return the callable referenced by *target*."""

        module_name, _, attr_name = self.target.partition(":")
        attr_name = attr_name or "main"
        module = importlib.import_module(module_name)
        runner = getattr(module, attr_name)
        if not callable(runner):  # pragma: no cover - defensive
            message = f"Frontend target {self.target!r} is not callable"
            raise TypeError(message)
        return cast(FrontendRunner, runner)


FRONTENDS: MutableMapping[str, FrontendSpec] = {
    "gui": FrontendSpec(
        target="tictactoe.ui.gui.main:main",
        description="CustomTkinter desktop GUI",
    ),
    "headless": FrontendSpec(
        target="tictactoe.ui.gui.main:main",
        description="GUI rendered via the headless CustomTkinter shim",
        env_overrides={"TICTACTOE_HEADLESS": "1"},
    ),
    "cli": FrontendSpec(
        target="tictactoe.ui.cli.main:main",
        description="Placeholder CLI with automation-friendly script mode",
    ),
    "service": FrontendSpec(
        target="tictactoe.ui.service.main:main",
        description="Headless automation/service runner (env driven)",
    ),
}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Launch the Tic Tac Toe template using the desired user interface "
            "(GUI, headless GUI, or CLI)."
        )
    )
    parser.add_argument(
        "--ui",
        "--frontend",
        dest="ui",
        choices=sorted(FRONTENDS.keys()),
        help=(
            "Frontend to launch. Overrides the "
            f"{_FRONTEND_ENV_VAR} environment variable."
        ),
    )
    parser.add_argument(
        "--list-frontends",
        action="store_true",
        help="List the available frontends without launching the app.",
    )
    parser.add_argument(
        "--theme",
        help=(
            "Theme name registered in tictactoe.config.gui.NAMED_THEMES. "
            "Overrides the TICTACTOE_THEME environment variable."
        ),
    )
    parser.add_argument(
        "--theme-file",
        type=Path,
        help="Path to a JSON file that stores a serialized GameViewConfig.",
    )
    return parser


def _print_available_frontends() -> None:
    for name in sorted(FRONTENDS.keys()):
        spec = FRONTENDS[name]
        print(f"{name:<9} - {spec.description}")


def _normalize_choice(raw_choice: str) -> str:
    return raw_choice.strip().lower()


def _determine_frontend(cli_choice: Optional[str]) -> FrontendSpec:
    choice = cli_choice or os.environ.get(_FRONTEND_ENV_VAR) or _DEFAULT_FRONTEND
    normalized = _normalize_choice(choice)
    try:
        return FRONTENDS[normalized]
    except KeyError as exc:
        available = ", ".join(sorted(FRONTENDS.keys()))
        message = f"Unknown frontend '{choice}'. Choose one of: {available}."
        raise SystemExit(message) from exc


def _apply_env_overrides(overrides: Mapping[str, str]) -> None:
    for key, value in overrides.items():
        os.environ[key] = value


def _load_theme_from_json(path: Path) -> Optional[Mapping[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _resolve_theme_payload(args) -> Optional[Mapping[str, Any]]:
    from tictactoe.config.gui import get_theme, serialize_game_view_config

    theme_file = args.theme_file or os.environ.get(_THEME_FILE_ENV_VAR)
    if theme_file:
        return _load_theme_from_json(Path(theme_file))

    theme_name = args.theme or os.environ.get(_THEME_ENV_VAR)
    if theme_name:
        config = get_theme(theme_name)
        return serialize_game_view_config(config)

    payload = os.environ.get(_THEME_PAYLOAD_ENV_VAR)
    if payload:
        return json.loads(payload)

    return None


def _set_theme_payload_env(payload: Optional[Mapping[str, Any]]) -> None:
    if payload is None:
        os.environ.pop(_THEME_PAYLOAD_ENV_VAR, None)
        return
    os.environ[_THEME_PAYLOAD_ENV_VAR] = json.dumps(payload)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point for launching the requested frontend."""

    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.list_frontends:
        _print_available_frontends()
        return 0

    frontend = _determine_frontend(args.ui)
    _apply_env_overrides(frontend.env_overrides)
    runner = frontend.load()
    if frontend.target.startswith("tictactoe.ui.gui"):
        _set_theme_payload_env(_resolve_theme_payload(args))
    else:
        _set_theme_payload_env(None)
    result = runner()
    return int(result) if isinstance(result, int) else 0


if __name__ == "__main__":
    sys.exit(main())
