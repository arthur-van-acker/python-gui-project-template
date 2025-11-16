"""Simple console frontend for Tic Tac Toe."""

from __future__ import annotations

import argparse
from typing import Iterable, Sequence

from tictactoe.domain.logic import GameSnapshot, GameState, TicTacToe

_QUIT_COMMANDS = {"q", "quit", "exit"}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Play Tic Tac Toe in the terminal, or replay a scripted sequence "
            "of moves."
        )
    )
    parser.add_argument(
        "--script",
        help=(
            "Comma separated list of zero-based board positions to run without "
            "prompts (e.g. 0,4,8)."
        ),
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress board rendering for scripted runs.",
    )
    return parser


def _format_board(snapshot: GameSnapshot) -> str:
    board = snapshot.board
    rows = []
    for base in range(0, 9, 3):
        cells = []
        for offset in range(3):
            idx = base + offset
            cell = board[idx]
            value = cell.value if cell is not None else str(idx)
            cells.append(value)
        rows.append(" | ".join(cells))
    return "\n---------\n".join(rows)


def _format_state_line(snapshot: GameSnapshot) -> str:
    if snapshot.state == GameState.DRAW:
        return "Result: draw."
    if snapshot.state == GameState.PLAYING:
        return f"Next player: {snapshot.current_player.value}"
    winner = snapshot.winner.value if snapshot.winner else "?"
    return f"Winner: {winner}"


def _print_snapshot(snapshot: GameSnapshot) -> None:
    print(_format_board(snapshot))
    print(_format_state_line(snapshot))


def _parse_script(script: str) -> list[int]:
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


def _run_script(game: TicTacToe, moves: Iterable[int], quiet: bool) -> None:
    for move in moves:
        if not game.make_move(move):
            raise SystemExit(f"Move {move} is invalid for the current board state.")
    if not quiet:
        _print_snapshot(game.snapshot)


def _interactive_session(game: TicTacToe) -> int:
    print("Press Q to quit at any time.")
    while game.state == GameState.PLAYING:
        _print_snapshot(game.snapshot)
        user_input = input(
            f"Player {game.current_player.value}, choose a cell (0-8): "
        ).strip()
        if user_input.lower() in _QUIT_COMMANDS:
            print("Exiting CLI – goodbye!")
            return 0
        try:
            position = int(user_input)
        except ValueError:
            print("Please enter a number between 0 and 8, or Q to quit.")
            continue
        if not game.make_move(position):
            print("Move rejected – cell occupied or out of range. Try again.")
    _print_snapshot(game.snapshot)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    game = TicTacToe()
    if args.script:
        try:
            moves = _parse_script(args.script)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        _run_script(game, moves, args.quiet)
        return 0

    return _interactive_session(game)


__all__ = ["main"]
