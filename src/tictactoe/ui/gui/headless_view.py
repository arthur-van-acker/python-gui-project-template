"""Headless GameView adapter for CI and automated tests."""

from __future__ import annotations

from typing import Callable, List, Sequence

from tictactoe.config import GameViewConfig
from tictactoe.domain.logic import GameSnapshot, GameState
from tictactoe.ui.gui.contracts import GameViewPort


class HeadlessGameView(GameViewPort):
    """Pure-Python implementation that mirrors the CustomTk view behavior."""

    def __init__(
        self,
        *,
        ctk_module,
        root,
        on_cell_click: Callable[[int], None],
        on_reset: Callable[[], None],
        view_config: GameViewConfig | None = None,
    ) -> None:
        del ctk_module, root  # unused but kept for signature compatibility
        self._on_cell_click = on_cell_click
        self._on_reset = on_reset
        self.config = view_config or GameViewConfig()

        self._built = False
        self._cells: List[dict[str, str]] = [self._make_empty_cell() for _ in range(9)]
        self._status_text = ""
        self._reset_label = self.config.text.reset_button

    def build(self) -> None:
        self._built = True

    def is_ready(self) -> bool:
        return self._built

    def render(self, snapshot: GameSnapshot) -> None:
        if not self.is_ready():
            return

        self._render_board(snapshot.board)
        self._status_text = self._status_message(snapshot)

    def cell_count(self) -> int:
        self._ensure_built()
        return len(self._cells)

    def cell_text(self, position: int) -> str:
        cell = self._cell_at(position)
        return cell["text"]

    def cell_state(self, position: int) -> str:
        cell = self._cell_at(position)
        return cell["state"]

    def status_text(self) -> str:
        return self._status_text

    def reset_button_label(self) -> str:
        return self._reset_label

    def button_count(self) -> int:
        return self.cell_count()

    def button_text(self, position: int) -> str:
        return self.cell_text(position)

    def button_state(self, position: int) -> str:
        return self.cell_state(position)

    # ------------------------------------------------------------------
    # Helpers mirrored from the CustomTk view
    # ------------------------------------------------------------------
    def _render_board(self, board: Sequence) -> None:
        for position in range(len(self._cells)):
            cell_value = board[position]
            target = self._cells[position]
            if cell_value is None:
                target.update(text="", state="normal")
            else:
                target.update(text=cell_value.value, state="disabled")

    def _status_message(self, snapshot: GameSnapshot) -> str:
        if snapshot.state == GameState.PLAYING:
            player = snapshot.current_player.value if snapshot.current_player else "?"
            return self.config.text.turn_message_template.format(player=player)
        if snapshot.state == GameState.DRAW:
            return self.config.text.draw_message
        winner = snapshot.winner.value if snapshot.winner else "Unknown"
        return self.config.text.win_message_template.format(winner=winner)

    def _cell_at(self, position: int) -> dict[str, str]:
        self._ensure_built()
        if position < 0 or position >= len(self._cells):
            raise IndexError(position)
        return self._cells[position]

    def _make_empty_cell(self) -> dict[str, str]:
        return {"text": "", "state": "normal"}

    def _ensure_built(self) -> None:
        if not self._built:
            raise RuntimeError("HeadlessGameView has not been built yet")
