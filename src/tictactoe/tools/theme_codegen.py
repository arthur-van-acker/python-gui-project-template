"""CLI helper to convert JSON themes into `GameViewConfig` snippets.

The GUI already supports loading JSON payloads via `--theme-file`, but template
adopters often want to graduate those serialized dictionaries into first-class
Python objects. This tool parses one or more JSON files and prints fully-typed
`GameViewConfig` assignments that can be pasted back into `tictactoe.config.gui`
or any other module.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List, Sequence

from tictactoe.config.gui import (
    ColorConfig,
    FontConfig,
    FontSpec,
    GameViewConfig,
    LayoutConfig,
    TextConfig,
    deserialize_game_view_config,
)

INDENT = " " * 4
IMPORT_BLOCK = """from tictactoe.config.gui import (
    ColorConfig,
    FontConfig,
    FontSpec,
    GameViewConfig,
    LayoutConfig,
    TextConfig,
)
"""

__all__ = [
    "generate_dataclass_snippet",
    "load_theme_config",
    "main",
    "sanitize_variable_name",
]


def _indent(level: int) -> str:
    return INDENT * level


def sanitize_variable_name(value: str) -> str:
    """Return a Python-safe identifier for generated variables."""

    if not value:
        return "generated_theme"
    sanitized = [ch if (ch.isalnum() or ch == "_") else "_" for ch in value]
    # Collapse consecutive underscores to keep the output tidy.
    collapsed: List[str] = []
    for ch in sanitized:
        if ch == "_" and collapsed and collapsed[-1] == "_":
            continue
        collapsed.append(ch)
    identifier = "".join(collapsed).strip("_") or "generated_theme"
    if identifier[0].isdigit():
        identifier = f"theme_{identifier}"
    return identifier


def _tuple_repr(values: Sequence[int]) -> str:
    return f"({values[0]}, {values[1]})"


def _format_font_spec(label: str, spec: FontSpec, level: int) -> str:
    return (
        f"{_indent(level)}{label}=FontSpec(size={spec.size}, "
        f"weight={repr(spec.weight)}),"
    )


def _format_fonts(fonts: FontConfig, level: int) -> List[str]:
    lines = [f"{_indent(level)}fonts=FontConfig("]
    inner = level + 1
    lines.append(_format_font_spec("title", fonts.title, inner))
    lines.append(_format_font_spec("status", fonts.status, inner))
    lines.append(_format_font_spec("cell", fonts.cell, inner))
    lines.append(_format_font_spec("reset", fonts.reset, inner))
    lines.append(f"{_indent(level)}),")
    return lines


def _format_layout(layout: LayoutConfig, level: int) -> List[str]:
    lines = [f"{_indent(level)}layout=LayoutConfig("]
    inner = _indent(level + 1)
    lines.append(f"{inner}title_padding={layout.title_padding},")
    lines.append(f"{inner}status_padding={layout.status_padding},")
    lines.append(f"{inner}board_padding={_tuple_repr(layout.board_padding)},")
    lines.append(f"{inner}cell_size={_tuple_repr(layout.cell_size)},")
    lines.append(f"{inner}cell_spacing={layout.cell_spacing},")
    lines.append(f"{inner}reset_padding={layout.reset_padding},")
    lines.append(f"{_indent(level)}),")
    return lines


def _format_text(text: TextConfig, level: int) -> List[str]:
    lines = [f"{_indent(level)}text=TextConfig("]
    inner = _indent(level + 1)
    lines.append(f"{inner}title={repr(text.title)},")
    lines.append(f"{inner}reset_button={repr(text.reset_button)},")
    lines.append(f"{inner}draw_message={repr(text.draw_message)},")
    lines.append(f"{inner}win_message_template={repr(text.win_message_template)},")
    lines.append(f"{inner}turn_message_template={repr(text.turn_message_template)},")
    lines.append(f"{_indent(level)}),")
    return lines


def _format_colors(colors: ColorConfig, level: int) -> List[str]:
    lines = [f"{_indent(level)}colors=ColorConfig("]
    inner = _indent(level + 1)
    lines.append(f"{inner}title_text={repr(colors.title_text)},")
    lines.append(f"{inner}status_text={repr(colors.status_text)},")
    lines.append(f"{inner}board_background={repr(colors.board_background)},")
    lines.append(f"{inner}cell_text={repr(colors.cell_text)},")
    lines.append(f"{inner}cell_fg={repr(colors.cell_fg)},")
    lines.append(f"{inner}cell_hover={repr(colors.cell_hover)},")
    lines.append(f"{inner}reset_fg={repr(colors.reset_fg)},")
    lines.append(f"{_indent(level)}),")
    return lines


def generate_dataclass_snippet(
    config: GameViewConfig, variable_name: str, source: Path | None = None
) -> str:
    """Return python code that recreates a `GameViewConfig` instance."""

    lines: List[str] = []
    if source is not None:
        lines.append(f"# Generated from {source}")
    lines.append(f"{variable_name} = GameViewConfig(")
    lines.extend(_format_fonts(config.fonts, 1))
    lines.extend(_format_layout(config.layout, 1))
    lines.extend(_format_text(config.text, 1))
    lines.extend(_format_colors(config.colors, 1))
    lines.append(")")
    return "\n".join(lines)


def load_theme_config(path: Path) -> GameViewConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    return deserialize_game_view_config(data)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Convert serialized GameViewConfig JSON payloads into typed "
            "dataclass assignments."
        )
    )
    parser.add_argument(
        "theme_files",
        nargs="+",
        help="Path(s) to JSON files previously produced by serialize_game_view_config",
    )
    parser.add_argument(
        "--variable-prefix",
        default="",
        help=(
            "Optional prefix prepended to each generated variable name. "
            "Underscores are handled automatically."
        ),
    )
    parser.add_argument(
        "--variable-suffix",
        default="_theme",
        help="Suffix appended to each generated variable name (default: '_theme').",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the snippets to the given file instead of stdout.",
    )
    return parser


def _derive_variable_name(
    path: Path, prefix: str, suffix: str
) -> str:
    effective_prefix = prefix
    if effective_prefix and not effective_prefix.endswith("_"):
        effective_prefix = f"{effective_prefix}_"
    raw_name = f"{effective_prefix}{path.stem}{suffix}"
    return sanitize_variable_name(raw_name)


def _join_snippets(snippets: Iterable[str]) -> str:
    body = "\n\n".join(snippets)
    return f"{IMPORT_BLOCK}{body}\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    snippets: List[str] = []
    for raw in args.theme_files:
        path = Path(raw)
        if not path.exists():
            raise FileNotFoundError(path)
        config = load_theme_config(path)
        variable_name = _derive_variable_name(
            path,
            args.variable_prefix,
            args.variable_suffix,
        )
        snippets.append(generate_dataclass_snippet(config, variable_name, source=path))

    output = _join_snippets(snippets)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
