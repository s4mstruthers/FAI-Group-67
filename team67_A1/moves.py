"""
Move generation for team 67's competitive sudoku AI.

Anything about *which moves exist* in a game state lives here, so that the
search (sudokuai.py) and the evaluation (evaluation.py) can be worked on
independently without merge conflicts.
"""

from competitive_sudoku.sudoku import GameState, Move, SudokuBoard, TabooMove


def candidate_moves(game_state: GameState) -> list[Move]:
    """
    Return every move the framework will not reject outright: the square is
    empty, the square is one the current player may play on, and the move
    has not been declared taboo.

    NOTE: this is naive_player's logic. It does NOT yet check the sudoku rules
    (no duplicate value in the same row, column or region), which is why
    naive_player regularly loses by playing an illegal move.
    TODO(A1): filter out moves that break the sudoku rules.
    """
    board = game_state.board
    N = board.N
    allowed_squares = game_state.player_squares()

    def possible(i: int, j: int, value: int) -> bool:
        return (board.get((i, j)) == SudokuBoard.empty
                and TabooMove((i, j), value) not in game_state.taboo_moves
                and (i, j) in allowed_squares)

    return [Move((i, j), value)
            for i in range(N) for j in range(N)
            for value in range(1, N + 1)
            if possible(i, j, value)]
