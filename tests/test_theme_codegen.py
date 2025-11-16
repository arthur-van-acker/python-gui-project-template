from __future__ import annotations

import json
from pathlib import Path

from tictactoe.config.gui import deserialize_game_view_config
from tictactoe.tools import theme_codegen as tg


def test_sanitize_variable_name_cleans_prefixes() -> None:
    assert tg.sanitize_variable_name("123-my theme") == "theme_123_my_theme"
    assert tg.sanitize_variable_name("__already_clean__") == "already_clean"


def test_generate_dataclass_snippet_contains_sections(tmp_path: Path) -> None:
    payload = {"text": {"title": "Doc Test"}}
    config = deserialize_game_view_config(payload)

    snippet = tg.generate_dataclass_snippet(config, "doc_theme", source=tmp_path / "doc.json")

    assert "doc_theme = GameViewConfig(" in snippet
    assert "TextConfig(" in snippet
    assert "Doc Test" in snippet
    assert "# Generated from" in snippet


def test_main_emits_cli_snippet(tmp_path: Path, capsys) -> None:
    payload = {"text": {"title": "CLI Theme"}}
    theme_path = tmp_path / "cli-theme.json"
    theme_path.write_text(json.dumps(payload), encoding="utf-8")

    tg.main([str(theme_path)])

    output = capsys.readouterr().out
    assert "from tictactoe.config.gui import" in output
    assert "cli_theme_theme = GameViewConfig(" in output
    assert "CLI Theme" in output
