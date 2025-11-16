"""Tests for theming utilities and serialization."""

from __future__ import annotations

import json

import pytest

from tictactoe.config.gui import (
    GameViewConfig,
    deserialize_game_view_config,
    get_theme,
    list_themes,
    serialize_game_view_config,
)


def test_named_themes_list_contains_presets():
    names = list_themes()
    assert {"default", "light", "dark", "enterprise"}.issubset(set(names))


def test_get_theme_returns_clone():
    theme = get_theme("light")
    other = get_theme("light")
    assert isinstance(theme, GameViewConfig)
    assert theme is not other
    assert theme.colors is not other.colors


def test_serialize_deserialize_round_trip():
    original = get_theme("dark")
    payload = serialize_game_view_config(original)
    rebuilt = deserialize_game_view_config(payload)
    assert rebuilt.text.title == original.text.title
    assert rebuilt.colors.board_background == original.colors.board_background


def test_deserialize_handles_partial_payload():
    payload = {"text": {"title": "Custom"}}
    rebuilt = deserialize_game_view_config(payload)
    assert rebuilt.text.title == "Custom"
    assert rebuilt.layout.cell_size == (100, 100)


def test_gui_main_env_loader(monkeypatch):
    from importlib import import_module

    payload = json.dumps({"text": {"title": "Env Theme"}})
    monkeypatch.setenv("TICTACTOE_THEME_PAYLOAD", payload)

    gui_module = import_module("tictactoe.ui.gui.main")
    theme = gui_module._theme_from_env()  # type: ignore[attr-defined]
    assert theme is not None
    assert theme.text.title == "Env Theme"

    monkeypatch.delenv("TICTACTOE_THEME_PAYLOAD", raising=False)
    assert gui_module._theme_from_env() is None  # type: ignore[attr-defined]
