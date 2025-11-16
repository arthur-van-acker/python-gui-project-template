"""Headless/service entry point that reuses the CLI automation helpers."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Sequence

from tictactoe.controller import (
    ControllerHooks,
    logging_hooks,
    telemetry_logging_requested,
)
from tictactoe.ui.cli import main as cli_main

_ENV_SCRIPT = "TICTACTOE_SCRIPT"
_ENV_SCRIPT_FILE = "TICTACTOE_SCRIPT_FILE"
_ENV_OUTPUT = "TICTACTOE_AUTOMATION_OUTPUT"
_ENV_LABEL = "TICTACTOE_AUTOMATION_LABEL"
_ENV_QUIET = "TICTACTOE_AUTOMATION_QUIET"
_SERVICE_TELEMETRY_ENV_VAR = "TICTACTOE_SERVICE_LOGGING"


def _service_controller_hooks(flag: str = _SERVICE_TELEMETRY_ENV_VAR) -> ControllerHooks | None:
    return logging_hooks() if telemetry_logging_requested(flag) else None


def _emit_view_event(hooks: ControllerHooks | None, action: str, **payload) -> None:
    if not hooks:
        return
    hooks.emit("view", action, **payload)


def _report_controller_error(
    hooks: ControllerHooks | None, exc: Exception, *, action: str, **payload
) -> None:
    if not hooks:
        return
    hooks.emit_error(exc, action=action, **payload)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Headless automation helper. Reads scripts from environment "
            "variables or CLI flags and emits the same AutomationSummary JSON "
            "as the CLI frontend."
        )
    )
    parser.add_argument("--script", help="Override the script provided via environment variables.")
    parser.add_argument(
        "--script-file",
        type=Path,
        help="Path to a script file if not using the env var version.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Write the automation summary to this path (falls back to env).",
    )
    parser.add_argument(
        "--label",
        help="Label stored in the AutomationSummary. Defaults to the env var or 'service-run'.",
    )
    parser.add_argument(
        "--quiet",
        dest="quiet",
        action="store_true",
        help="Suppress stdout. Overrides any env configuration.",
    )
    parser.add_argument(
        "--verbose",
        dest="quiet",
        action="store_false",
        help="Force stdout rendering even if the env requests quiet mode.",
    )
    parser.set_defaults(quiet=None)
    return parser


def _env_path(value: str | None) -> Path | None:
    if not value:
        return None
    return Path(value)


def _env_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() not in {"0", "false", "no"}


def _resolve_script_text(script: str | None, script_file: Path | None) -> str | None:
    if script:
        return script
    if script_file and script_file.exists():
        return script_file.read_text(encoding="utf-8")
    return None


def main(
    argv: Sequence[str] | None = None,
    *,
    controller_hooks: ControllerHooks | None = None,
) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    hooks = controller_hooks or _service_controller_hooks()

    script_value = args.script or os.environ.get(_ENV_SCRIPT)
    script_file = args.script_file or _env_path(os.environ.get(_ENV_SCRIPT_FILE))
    output_path = args.output_json or _env_path(os.environ.get(_ENV_OUTPUT))
    label = args.label or os.environ.get(_ENV_LABEL) or "service-run"

    if args.quiet is None:
        quiet = _env_bool(os.environ.get(_ENV_QUIET), default=True)
    else:
        quiet = args.quiet

    script_text = _resolve_script_text(script_value, script_file)
    if not script_text:
        _emit_view_event(hooks, "no_script_provided")
        print(
            "No script provided. Set TICTACTOE_SCRIPT or TICTACTOE_SCRIPT_FILE "
            "(or pass --script/--script-file) to describe the automation run."
        )
        return 0

    origin = "script" if script_value else "script_file"
    _emit_view_event(
        hooks,
        "script_resolved",
        origin=origin,
        label=label,
    )

    try:
        moves = cli_main.parse_script(script_text)
    except ValueError as exc:  # pragma: no cover - validated in CLI tests
        _report_controller_error(hooks, exc, action="parse_script")
        raise SystemExit(str(exc)) from exc

    output = output_path if output_path else None
    cli_main.run_script(
        moves,
        label=label,
        quiet=quiet,
        output_json=output,
        controller_hooks=hooks,
    )
    return 0


__all__ = ["main"]
