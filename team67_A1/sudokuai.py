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

import copy
import math
import random

import competitive_sudoku.sudokuai
from competitive_sudoku.sudoku import GameState, Move, SudokuBoard

from .moves import apply_move, candidate_moves
from .evaluation import evaluate


def _board_full(game_state: GameState) -> bool:
    """True if no empty square is left on the board (the game is over)."""
    return SudokuBoard.empty not in game_state.board.squares


def _pass_turn(game_state: GameState) -> GameState:
    """
    Return a copy of game_state in which the current player has passed.

    The framework skips a player who has no square to play on and gives the
    turn to the opponent, so the search must model that too. A shallow copy is
    enough: only current_player changes, and apply_move() deep-copies the state
    before it modifies anything else.
    """
    new_state = copy.copy(game_state)
    new_state.current_player = 3 - game_state.current_player
    return new_state

class SudokuAI(competitive_sudoku.sudokuai.SudokuAI):
    """Sudoku AI that computes a move for a given sudoku configuration."""

    def __init__(self):
        super().__init__()

    def compute_best_move(self, game_state: GameState) -> None:
        moves = candidate_moves(game_state)
        if not moves:
            return  # no legal move exists (anything proposed loses)

        # Anytime requirement: propose something immediately, in case the
        # time limit is very short.
        self.propose_move(random.choice(moves))

        # We are the player to move at the root. evaluate() scores every leaf
        # from this player's point of view.
        our_player = game_state.current_player

        # Searching deeper than the number of empty squares is pointless:
        # the game ends when the board is full.
        max_useful_depth = game_state.board.squares.count(SudokuBoard.empty)

        # Iterative deepening: search depth 1, 2, 3, ... until killed.
        for depth in range(1, max_useful_depth + 1):
            best_move = self._search_root(game_state, moves, depth, our_player)
            self.propose_move(best_move)

            # Move ordering: try the best move of this depth first at the next
            # depth. Good moves found early give tighter alpha/beta bounds,
            # which lets alpha-beta prune much more.
            moves.remove(best_move)
            moves.insert(0, best_move)
    
    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------
    def _search_root(self, game_state: GameState, moves: list[Move],
                        depth: int, our_player: int) -> Move:
        """
        Run alpha-beta to the given depth and return the best move for us.

        The root is always a MAX node (it is our turn). The alpha bound is
        raised after each root move, so later root moves are pruned using the
        value of the best move found so far.
        """
        alpha, beta = -math.inf, math.inf
        best_value = -math.inf
        best_move = moves[0]

        for move in moves:
            child = apply_move(game_state, move)
            value = self._alphabeta(child, depth - 1, alpha, beta,
                                    our_player, previous_passed=False)
            if value > best_value:
                best_value, best_move = value, move
            alpha = max(alpha, best_value)

        return best_move

    def _alphabeta(self, state: GameState, depth: int, alpha: float, beta: float,
                    our_player: int, previous_passed: bool) -> float:
        """
        Return the minimax value of `state` (from our_player's point of view),
        searching `depth` more moves, with alpha-beta pruning.

        alpha = best value MAX (us) is already guaranteed higher up the tree.
        beta  = best value MIN (opponent) is already guaranteed higher up.
        If alpha >= beta, the remaining children cannot affect the root
        decision and are skipped.

        previous_passed is True if the player before this one had to pass;
        two passes in a row mean nobody can move, so the game is over.
        """
        # Leaf: depth limit reached, or game over because the board is full.
        if depth == 0 or _board_full(state):
            return evaluate(state, our_player)

        moves = candidate_moves(state)

        # The player to move has no move: they pass (as the framework does).
        # If the opponent also just passed, nobody can move: the game is over.
        # Passing does not consume depth, as no move was actually played.
        if not moves:
            if previous_passed:
                return evaluate(state, our_player)
            return self._alphabeta(_pass_turn(state), depth, alpha, beta,
                                    our_player, previous_passed=True)

        if state.current_player == our_player:
            # MAX node: we pick the child with the highest value.
            value = -math.inf
            for move in moves:
                child = apply_move(state, move)
                value = max(value, self._alphabeta(child, depth - 1, alpha, beta,
                                                    our_player, previous_passed=False))
                if value >= beta:
                    break  # beta cut-off: the opponent will avoid this node
                alpha = max(alpha, value)
            return value
        else:
            # MIN node: the opponent picks the child with the lowest value.
            value = math.inf
            for move in moves:
                child = apply_move(state, move)
                value = min(value, self._alphabeta(child, depth - 1, alpha, beta,
                                                    our_player, previous_passed=False))
                if value <= alpha:
                    break  # alpha cut-off: we will avoid this node
                beta = min(beta, value)
            return value
    