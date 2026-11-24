"""
Evaluation function for team 67's competitive sudoku AI.

The search in sudokuai.py calls evaluate() on the game states at the bottom
of its search tree, so this file can be developed and tested on its own.
"""

from competitive_sudoku.sudoku import GameState


def evaluate(game_state: GameState) -> float:
    """
    Return a number that says how good game_state is for our player
    (higher = better for us).

    Useful fields: game_state.scores (list [player1, player2]),
    game_state.current_player (1 or 2), game_state.board.

    TODO(A1): implement. Not called yet, so the module still runs as-is.
    """
    raise NotImplementedError
