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
import time
import competitive_sudoku.sudokuai
from competitive_sudoku.sudoku import GameState, Move, TabooMove, SudokuBoard

from .moves import candidate_moves
# from .evaluation import evaluate   # TODO(A1): use once evaluate() exists


class SudokuAI(competitive_sudoku.sudokuai.SudokuAI):
    """Sudoku AI that computes a move for a given sudoku configuration."""

    def __init__(self):
        super().__init__()

    def compute_best_move(self, game_state: GameState) -> None:
        N = game_state.board.N

        # Check whether a cell is empty, a value in that cell is not taboo, and that cell is allowed
        def possible(i, j, value):
            return game_state.board.get((i, j)) == SudokuBoard.empty \
                   and not TabooMove((i, j), value) in game_state.taboo_moves \
                       and (i, j) in game_state.player_squares()

        # Check whether a an empty cell can have a value such that:
        #   the value is not already in the region, in the row, in the column
        def C0(i, j, value):
            column_constraint = True
            for k in range(game_state.board.board_width()):
                if k != j and game_state.board.get((i, k)) == value:
                    column_constraint = False

            print("Evaluating state...")
            print(game_state.scores)
            row_constraint = True
            for k in range(game_state.board.board_height()):
                if k != i and game_state.board.get((k, j)) == value:
                    row_constraint = False

            region_constraint = True
            region_width = game_state.board.region_width()
            region_height = game_state.board.region_height()
            region_i = i // region_height
            region_j = j // region_width
            for k in range(region_height):
                for l in range(region_width):
                    if (region_i * region_height + k != i and region_j * region_width + l != j) and game_state.board.get((region_i * region_height + k, region_j * region_width + l)) == value:
                        region_constraint = False
                        break
                if region_constraint == False:
                    break

            return column_constraint and row_constraint and region_constraint

        def state_eval(game_state: GameState):
            print("Evaluating state...")
            print(game_state.scores)
            return None

        all_legal_moves = [Move((i, j), value) for i in range(N) for j in range(N)
                     for value in range(1, N+1) if possible(i, j, value) and C0(i, j, value)]
        
        move = random.choice(all_legal_moves)
        self.propose_move(move)
        while True:
            time.sleep(0.2)
            self.propose_move(random.choice(all_legal_moves))
