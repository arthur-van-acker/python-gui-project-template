"""Neutral domain placeholders for the CustomTkinter starter kit."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Mapping, Optional, Tuple


class ExampleActor(Enum):
    """Placeholder actors shown in the sample UI until replaced."""

    PRIMARY = "Actor A"
    SECONDARY = "Actor B"


# Backwards compatibility for older imports that still expect `Player`.
Player = ExampleActor


class GameState(Enum):
    """High-level lifecycle markers rendered by the default UI."""

    PLAYING = "playing"
    X_WON = "x_won"
    O_WON = "o_won"
    DRAW = "draw"


BoardTuple = Tuple[Optional[Player], ...]


@dataclass(frozen=True)
class ExampleAction:
    """Describes a unit of work the adopter can route into the domain layer."""

    name: str
    payload: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class ExampleState:
    """Immutable snapshot passed to views, tests, and automation hooks."""

    board: BoardTuple
    current_player: Optional[Player]
    state: GameState
    winner: Optional[Player]
    notes: tuple[str, ...] = ()


# Alias retained so the existing view/controller contracts remain unchanged.
GameSnapshot = ExampleState


PLACEHOLDER_NOTES: tuple[str, ...] = (
    "TODO: Replace ExampleState with your domain-specific data.",
    "TODO: Implement TicTacToe.dispatch_action to mutate that state.",
)


class TicTacToe:
    """Template-friendly shell that adopters replace with real business rules."""

    def __init__(self, board_size: int = 9):
        self._listeners: list[Callable[[ExampleState], None]] = []
        self._board_size = board_size
        self._board: list[Optional[Player]] = [None for _ in range(board_size)]
        self.current_player: Optional[Player] = None
        self.state: GameState = GameState.PLAYING
        self._winner: Optional[Player] = None
        self._notes: tuple[str, ...] = PLACEHOLDER_NOTES
        self.reset()

    def add_listener(self, listener: Callable[[ExampleState], None]) -> None:
        """Register a callback triggered whenever `ExampleState` changes."""

        self._listeners.append(listener)

    def remove_listener(self, listener: Callable[[ExampleState], None]) -> None:
        """Remove a previously registered listener."""

        if listener in self._listeners:
            self._listeners.remove(listener)

    @property
    def board(self) -> BoardTuple:
        """Expose an immutable view of the board placeholders."""

        return tuple(self._board)

    @property
    def snapshot(self) -> ExampleState:
        """Summarize the state that will eventually drive the UI."""

        return ExampleState(
            board=self.board,
            current_player=self.current_player,
            state=self.state,
            winner=self._winner,
            notes=self._notes,
        )

    def dispatch_action(self, action: ExampleAction) -> ExampleState:
        """Entry point adopters override with their business rules.

        Replace this method with real state transitions, then update the
        placeholder tests to assert your expected behavior.
        """

        raise NotImplementedError(
            "TODO: Wire dispatch_action to your application's domain logic."
        )

    def make_move(self, position: int) -> bool:
        """Legacy controller hook kept for backwards compatibility."""

        action = ExampleAction(
            name="grid.select",
            payload={
                "position": position,
                "actor": self.current_player.value if self.current_player else None,
            },
        )
        self.dispatch_action(action)
        return False

    def reset(self) -> None:
        """Return to the neutral placeholder state and notify observers."""

        self._board = [None for _ in range(self._board_size)]
        self.current_player = None
        self.state = GameState.PLAYING
        self._winner = None
        self._notify_listeners()

    def get_winner(self) -> Optional[Player]:
        """Expose the winning token once custom rules set it."""

        return self._winner

    def _notify_listeners(self) -> None:
        """Notify all registered listeners of the latest snapshot."""

        if not self._listeners:
            return

        snapshot = self.snapshot
        for listener in list(self._listeners):
            listener(snapshot)
