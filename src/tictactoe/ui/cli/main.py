"""Console placeholder utilities for the CustomTkinter starter template."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, MutableMapping, Sequence

from tictactoe.controller import (
    ControllerHooks,
    logging_hooks,
    telemetry_logging_requested,
)
from tictactoe.domain.logic import ExampleAction, TicTacToe


@dataclass(frozen=True)
class AutomationSummary:
    """Structured output emitted by script/automation runs."""

    label: str
    actions: tuple[ExampleAction, ...]
    metadata: Mapping[str, str]
    notes: tuple[str, ...]


_CLI_TELEMETRY_ENV_VAR = "TICTACTOE_CLI_LOGGING"


def _env_controller_hooks(flag: str = _CLI_TELEMETRY_ENV_VAR) -> ControllerHooks | None:
    return logging_hooks() if telemetry_logging_requested(flag) else None


def _emit_view_event(hooks: ControllerHooks | None, action: str, **payload: Any) -> None:
    if not hooks:
        return
    hooks.emit("view", action, **payload)


def _emit_domain_event(hooks: ControllerHooks | None, action: str, **payload: Any) -> None:
    if not hooks:
        return
    hooks.emit("domain", action, **payload)


def _report_controller_error(
    hooks: ControllerHooks | None, exc: Exception, *, action: str, **payload: Any
) -> None:
    if not hooks:
        return
    hooks.emit_error(exc, action=action, **payload)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Preview how scripted runs can feed your domain layer. Supply a "
            "comma-separated move list or point to a file that describes the "
            "actions to record."
        )
    )
    parser.add_argument(
        "--script",
        help=(
            "Comma separated list of zero-based board positions (e.g. 0,4,8). "
            "Acts as a lightweight batch driver for CI."
        ),
    )
    parser.add_argument(
        "--script-file",
        type=Path,
        help="Path to a text file containing the same comma-separated format.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Optional path that will receive the automation summary as JSON.",
    )
    parser.add_argument(
        "--label",
        default="cli-script",
        help="Tag stored in the automation summary to describe the scenario.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress stdout output (handy for CI once JSON is captured).",
    )
    return parser


def parse_script(script: str) -> list[int]:
    """Convert comma separated positions into integers with validation."""

    tokens = [token.strip() for token in script.split(",") if token.strip()]
    if not tokens:
        raise ValueError("Script must contain at least one move.")
    moves: list[int] = []
    for token in tokens:
        value = int(token)
        if value < 0 or value > 8:
            raise ValueError("Moves must be between 0 and 8.")
        moves.append(value)
    return moves


def _load_script_from_file(path: Path) -> str:
    if not path.exists():  # pragma: no cover - defensive
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def _resolve_moves(script: str | None, script_file: Path | None) -> list[int] | None:
    if script:
        return parse_script(script)
    if script_file:
        return parse_script(_load_script_from_file(script_file))
    return None


def build_automation_summary(
    moves: Iterable[int],
    *,
    label: str,
    metadata: Mapping[str, str] | None = None,
) -> AutomationSummary:
    """Wrap the provided moves inside ExampleAction placeholders."""

    actions = tuple(
        ExampleAction(
            name="grid.select",
            payload={
                "position": position,
                "actor": "Actor A" if index % 2 == 0 else "Actor B",
            },
        )
        for index, position in enumerate(moves)
    )
    base_metadata: MutableMapping[str, str] = {
        "action_count": str(len(actions)),
        "board_size": "3x3",
    }
    if metadata:
        base_metadata.update(metadata)

    notes = (
        "TODO: Replace ExampleAction with calls into your domain layer.",
        "TODO: Extend AutomationSummary to capture the outputs your CI needs.",
    )
    return AutomationSummary(
        label=label,
        actions=actions,
        metadata=dict(base_metadata),
        notes=notes,
    )


def render_summary(summary: AutomationSummary) -> str:
    """Return a human-friendly version of an automation summary."""

    lines = [f"Automation label: {summary.label}"]
    lines.append(f"Recorded actions: {len(summary.actions)}")
    if summary.metadata:
        lines.append("Metadata:")
        for key, value in summary.metadata.items():
            lines.append(f"  - {key}: {value}")
    lines.append("Actions:")
    if summary.actions:
        for action in summary.actions:
            payload = action.payload or {}
            lines.append(f"  - {action.name} {payload}")
    else:
        lines.append("  (none)")
    lines.append("Notes:")
    for note in summary.notes:
        lines.append(f"  * {note}")
    return "\n".join(lines)


def write_summary_json(summary: AutomationSummary, destination: Path) -> None:
    """Persist the summary to disk as JSON for downstream tooling."""

    payload: dict[str, Any] = {
        "label": summary.label,
        "metadata": dict(summary.metadata),
        "notes": list(summary.notes),
        "actions": [
            {
                "name": action.name,
                "payload": dict(action.payload or {}),
            }
            for action in summary.actions
        ],
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _print_placeholder_help() -> None:
    game = TicTacToe()
    snapshot = game.snapshot
    print("Template CLI placeholder – pass --script or --script-file to see how")
    print("automation data can be captured for CI or batch tooling.")
    print(f"ExampleState snapshot: board={len(snapshot.board)} cells, state={snapshot.state.value}")
    if snapshot.notes:
        print("Snapshot notes:")
        for note in snapshot.notes:
            print(f"  * {note}")


def run_script(
    moves: Iterable[int],
    *,
    label: str,
    quiet: bool = False,
    output_json: Path | None = None,
    controller_hooks: ControllerHooks | None = None,
) -> AutomationSummary:
    moves_tuple = tuple(moves)
    _emit_view_event(
        controller_hooks,
        "script_started",
        label=label,
        action_count=len(moves_tuple),
    )
    summary = build_automation_summary(moves_tuple, label=label)
    _emit_domain_event(
        controller_hooks,
        "automation_summary_ready",
        label=label,
        action_count=len(summary.actions),
    )

    if not quiet:
        rendered = render_summary(summary)
        print(rendered)
        _emit_view_event(
            controller_hooks,
            "summary_rendered",
            label=label,
            line_count=rendered.count("\n") + 1,
        )

    if output_json:
        write_summary_json(summary, output_json)
        _emit_view_event(
            controller_hooks,
            "summary_written",
            label=label,
            path=str(output_json),
        )

    return summary


def main(
    argv: Sequence[str] | None = None,
    *,
    controller_hooks: ControllerHooks | None = None,
) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    hooks = controller_hooks or _env_controller_hooks()

    try:
        moves = _resolve_moves(args.script, args.script_file)
    except ValueError as exc:
        _report_controller_error(hooks, exc, action="parse_script")
        raise SystemExit(str(exc)) from exc
    if moves is None:
        _emit_view_event(hooks, "placeholder_rendered")
        _print_placeholder_help()
        return 0

    run_script(
        moves,
        label=args.label,
        quiet=args.quiet,
        output_json=args.output_json,
        controller_hooks=hooks,
    )
    return 0


__all__ = [
    "AutomationSummary",
    "build_automation_summary",
    "main",
    "parse_script",
    "render_summary",
    "run_script",
    "write_summary_json",
]
