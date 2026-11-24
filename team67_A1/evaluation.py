"""
Evaluation function for team 67's competitive sudoku AI.

The search in sudokuai.py calls evaluate() on the game states at the bottom
of its search tree, so this file can be developed and tested on its own.
"""


from competitive_sudoku.sudoku import GameState

def evaluate(game_state: GameState, our_player: int) -> float:
    """
    Return a number that says how good game_state is for our player
    (higher = better for us).

    Useful fields: game_state.scores (list [player1, player2]),
    game_state.current_player (1 or 2), game_state.board.

    """
    player1_score, player2_score = game_state.scores
    
    # Positive = player 1 ahead, negative = player 2 ahead.
    score_difference = player1_score - player2_score

    # Flip the sign when we are player 2, so that positive always means "good for us".
    return score_difference if our_player == 1 else -score_difference
