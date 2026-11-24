"""
Move generation for team 67's competitive sudoku AI.

Anything about *which moves exist* in a game state lives here, so that the
search (sudokuai.py) and the evaluation (evaluation.py) can be worked on
independently without merge conflicts.
"""
import copy
from shutil import move

from competitive_sudoku.sudoku import GameState, Move, SudokuBoard, TabooMove

def _region_complete(board: SudokuBoard, squares) -> bool:
    """True if none of the given squares is empty."""
    return all(board.get(sq) != SudokuBoard.empty for sq in squares)

def apply_move(game_state: GameState, move: Move) -> GameState:
    """
    Simulates moves
    """
    # 1. Independent copy, so the real game state stays untouched.
    new_state = copy.deepcopy(game_state)
    board = new_state.board
    N = board.N

    i, j = move.square
    mover = new_state.current_player          # 1 or 2: who is playing this move

    # 2. Write the value on the board.
    board.put((i, j), move.value)

    # 3. The cell now belongs to the mover. occupied_squares() returns the
    #    CURRENT player's list, so this must happen BEFORE we switch players.
    #    (In classic mode there are no occupied lists, so skip it there.)
    if not new_state.is_classic_game():
        new_state.occupied_squares().append((i, j))

    # 4. Score: count the regions this move completed and convert to points.
    row = [(i, c) for c in range(N)]                       # all cells in row i
    col = [(r, j) for r in range(N)]                       # all cells in column j
    top = (i // board.region_height()) * board.region_height()   # block's top row
    left = (j // board.region_width()) * board.region_width()    # block's left column
    block = [(r, c)
             for r in range(top, top + board.region_height())
             for c in range(left, left + board.region_width())]

    completed = sum(_region_complete(board, region) for region in (row, col, block))
    points = [0, 1, 3, 7][completed]          # rules: 0/1/2/3 regions -> 0/1/3/7 points
    new_state.scores[mover - 1] += points     # scores is [player 1, player 2]
    new_state.moves.append(move) #this just records the move in the history bc that's an option we have, maybe we'll use it later
    # 5. Hand the turn to the other player (1 -> 2, 2 -> 1).
    new_state.current_player = 3 - mover

    return new_state

def candidate_moves(game_state: GameState) -> list[Move]:
    """
    Return every move the framework will not reject outright: the square is
    empty, the square is one the current player may play on, the move has
    not been declared taboo, and the value does not already appear in the
    same row, column or block (rule C0).
    """
    board = game_state.board
    N = board.N
    allowed_squares = game_state.player_squares()

    # None means classic mode: every cell on the board is allowed.
    if allowed_squares is None:
        allowed_squares = [(i, j) for i in range(N) for j in range(N)]

    def possible(i: int, j: int, value: int) -> bool:
        return (board.get((i, j)) == SudokuBoard.empty
                and TabooMove((i, j), value) not in game_state.taboo_moves
                and (i, j) in allowed_squares)

    # Check whether a an empty cell can have a value such that:
    # the value is not already in the region, in the row, in the column
    def legal_move(i, j, value):
    
        # Row check

        row_ok = True
        for k in range(game_state.board.board_width()):
            if k != j and game_state.board.get((i, k)) == value:
                row_ok = False

        # Column check
        col_ok = True
        for k in range(game_state.board.board_height()):
            if k != i and game_state.board.get((k, j)) == value:
                col_ok = False

        # Check boxes
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

        return row_ok and col_ok and region_constraint

    
    return [Move((i, j), value)
            for i in range(N) for j in range(N)
            for value in range(1, N + 1)
            if possible(i, j, value) and legal_move(i, j, value)]
