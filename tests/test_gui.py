"""Lightweight GUI smoke tests for TicTacToeGUI."""

from __future__ import annotations

import os
import platform
from tkinter import TclError

os.environ.setdefault("TICTACTOE_HEADLESS", "1")

import pytest

from tictactoe.config import WindowConfig
from tictactoe.domain.logic import GameState, TicTacToe
from tictactoe.ui.gui.headless_view import HeadlessGameView
from tictactoe.ui.gui.main import TicTacToeGUI

NEEDS_DISPLAY = platform.system() != "Windows" and not os.environ.get("DISPLAY")


def _skip_if_no_display() -> None:
    if NEEDS_DISPLAY:
        pytest.skip("GUI tests require a display")


TK_MISSING_PATTERNS = (
    "tcl_findlibrary",
    "can't find a usable tk.tcl",
    "tk wasn't installed properly",
)


def _create_app_or_skip(**kwargs) -> TicTacToeGUI:
    _skip_if_no_display()
    kwargs.setdefault("view_factory", HeadlessGameView)
    try:
        return TicTacToeGUI(**kwargs)
    except TclError as exc:
        message = str(exc).lower()
        if any(pattern in message for pattern in TK_MISSING_PATTERNS):
            pytest.skip("Tk runtime is unavailable in this environment")
        raise


@pytest.mark.gui
def test_gui_initializes_widgets():
    app = _create_app_or_skip()
    try:
        assert app.view.cell_count() == 9
        assert "Player X" in app.view.status_text()
        assert app.view.reset_button_label() == "New Game"
    finally:
        app.root.destroy()


@pytest.mark.gui
def test_gui_click_updates_button_and_status():
    app = _create_app_or_skip()
    try:
        app._on_cell_click(0)
        assert app.view.cell_text(0) == "X"
        assert app.view.cell_state(0) == "disabled"
        assert "Player O" in app.view.status_text()
    finally:
        app.root.destroy()


@pytest.mark.gui
def test_gui_reset_game_restores_state():
    app = _create_app_or_skip()
    try:
        app._on_cell_click(0)
        app._on_cell_click(3)
        app._reset_game()

        for index in range(app.view.cell_count()):
            assert app.view.cell_text(index) == ""
            assert app.view.cell_state(index) == "normal"
        assert app.game.state == GameState.PLAYING
        assert "Player X" in app.view.status_text()
    finally:
        app.root.destroy()


@pytest.mark.gui
def test_gui_win_updates_status_message():
    app = _create_app_or_skip()
    try:
        for move in (0, 3, 1, 4, 2):
            app._on_cell_click(move)

        assert app.game.state == GameState.X_WON
        assert "wins" in app.view.status_text()
    finally:
        app.root.destroy()


@pytest.mark.gui
def test_gui_accepts_custom_factories_and_window_config():
    class DummyWidget:
        def __init__(self):
            self._text = ""
            self._state = "normal"

        def cget(self, key: str):
            if key == "text":
                return self._text
            if key == "state":
                return self._state
            raise KeyError(key)

    class DummyView:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.title_label = DummyWidget()
            self.status_label = DummyWidget()
            self.board_frame = object()
            self.reset_button = DummyWidget()
            self.buttons = [DummyWidget() for _ in range(9)]
            self.render_calls = []
            self._built = False

        def build(self):
            self._built = True

        def render(self, snapshot):
            self.render_calls.append(snapshot)

        # Minimal telemetry helpers to align with the GameViewPort surface
        def is_ready(self):
            return self._built

        def cell_count(self):
            return len(self.buttons)

        def cell_text(self, position):
            return self.buttons[position].cget("text")

        def cell_state(self, position):
            return self.buttons[position].cget("state")

        def status_text(self):
            return self.status_label.cget("text")

        def reset_button_label(self):
            return self.reset_button.cget("text")

    factory_calls = []

    def game_factory():
        factory_calls.append("called")
        return TicTacToe()

    custom_config = WindowConfig(
        title="Custom Title",
        geometry="420x640",
        resizable=(True, False),
    )

    app = _create_app_or_skip(
        game_factory=game_factory,
        view_factory=lambda **kwargs: DummyView(**kwargs),
        window_config=custom_config,
    )
    try:
        assert factory_calls == ["called"]
        assert isinstance(app.view, DummyView)
        assert app.view.render_calls  # render invoked with snapshot
        assert app.window_config == custom_config
    finally:
        app.root.destroy()
