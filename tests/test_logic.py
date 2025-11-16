"""Executable documentation for the template domain placeholders."""

from __future__ import annotations

import pytest

from tictactoe.domain.logic import ExampleAction, ExampleState, GameState, TicTacToe


def test_placeholder_snapshot_documents_override_points() -> None:
    """The starter kit ships with a neutral snapshot that carries TODO notes."""

    game = TicTacToe()
    snapshot = game.snapshot

    assert isinstance(snapshot, ExampleState)
    assert snapshot.state == GameState.PLAYING
    assert snapshot.current_player is None
    assert snapshot.winner is None
    assert snapshot.board == tuple([None] * 9)
    assert snapshot.notes, "Snapshot should include guidance for template adopters."
    assert any("TODO" in note for note in snapshot.notes)


def test_dispatch_action_is_not_implemented_yet() -> None:
    """Dispatch raises until adopters plug in their actual business rules."""

    game = TicTacToe()
    action = ExampleAction(name="demo")

    with pytest.raises(NotImplementedError):
        game.dispatch_action(action)
