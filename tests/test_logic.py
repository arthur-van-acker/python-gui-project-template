"""Unit tests for tictactoe.domain.logic."""

from tictactoe.domain.logic import GameState, Player, TicTacToe


def test_initial_state():
    game = TicTacToe()
    assert game.state == GameState.PLAYING
    assert game.current_player == Player.X
    assert all(cell is None for cell in game.board)


def test_x_wins_top_row():
    game = TicTacToe()
    moves = [0, 3, 1, 4, 2]
    for move in moves:
        assert game.make_move(move)
    assert game.state == GameState.X_WON
    assert game.get_winner() == Player.X


def test_o_wins_right_column():
    game = TicTacToe()
    moves = [0, 2, 3, 5, 4, 8]
    for move in moves:
        assert game.make_move(move)
    assert game.state == GameState.O_WON
    assert game.get_winner() == Player.O


def test_draw_game():
    game = TicTacToe()
    moves = [0, 1, 2, 4, 3, 5, 7, 6, 8]
    for move in moves:
        assert game.make_move(move)
    assert game.state == GameState.DRAW
    assert game.get_winner() is None


def test_illegal_move_same_position():
    game = TicTacToe()
    assert game.make_move(0)
    assert not game.make_move(0)
    assert game.current_player == Player.O


def test_illegal_move_out_of_bounds():
    game = TicTacToe()
    assert not game.make_move(-1)
    assert not game.make_move(9)
    assert all(cell is None for cell in game.board)


def test_no_moves_after_win():
    game = TicTacToe()
    moves = [0, 3, 1, 4, 2]
    for move in moves:
        assert game.make_move(move)
    assert not game.make_move(5)
    assert game.board[5] is None


def test_reset_restores_initial_state():
    game = TicTacToe()
    game.make_move(0)
    game.make_move(4)
    game.reset()
    assert game.state == GameState.PLAYING
    assert game.current_player == Player.X
    assert all(cell is None for cell in game.board)
