"""
Team 67 – competitive sudoku AI for Assignment A1.

Entry point used by simulate_game.py. The framework runs compute_best_move()
in a separate process and kills it when the time per move runs out; the last
move passed to propose_move() is the one that gets played. So: propose a
reasonable move early, then keep proposing better ones as the search deepens.

Structure of this module:
  moves.py       - which moves are possible in a game state
  evaluation.py  - how good a game state is for us
  sudokuai.py    - the search that ties the two together (this file)

Imports between these files are *relative* (from .moves import ...), so the
folder can be copied to team67_A2 later without editing any imports.
"""

import random

import competitive_sudoku.sudokuai
from competitive_sudoku.sudoku import GameState

from .moves import candidate_moves
# from .evaluation import evaluate   # TODO(A1): use once evaluate() exists


class SudokuAI(competitive_sudoku.sudokuai.SudokuAI):
    """Sudoku AI that computes a move for a given sudoku configuration."""

    def __init__(self):
        super().__init__()

    def compute_best_move(self, game_state: GameState) -> None:
        # Placeholder behaviour (same as naive_player): propose a random
        # candidate move so the module always plays *something*.
        # TODO(A1): replace with a search (e.g. minimax with alpha-beta,
        # deepening step by step and calling propose_move after each depth).
        moves = candidate_moves(game_state)
        self.propose_move(random.choice(moves))
