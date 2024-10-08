"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count the number of X's and O's
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # Check for invalid board (O can't be more than X)
    if o_count > x_count:
        raise ValueError("Invalid board: More O's than X's.")
    elif x_count > o_count + 1:
        raise ValueError("Invalid board: Too many X's!")
    # If X has played more than O, it's O's turn
    if x_count > o_count:
        return O
    # If X and O have the same number of moves, it's X's turn
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):  # Loop through rows
        for j in range(len(board[i])):  # Loop through columns in each row
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions



def result(board, action):
    """
    Returns the board that results from making the given move (i, j) on the board.
    """
    i, j = action

    try:
        # Check if action is valid
        if board[i][j] is not EMPTY:
            raise ValueError(f"Invalid action: Cell ({i}, {j}) is already filled.")
    except IndexError:
        # Raise a more descriptive error if action is out of bounds
        raise ValueError(f"Invalid action: Position ({i}, {j}) is out of bounds.")

    # Make a deep copy of the board
    new_board = copy.deepcopy(board)

    # Determine which player's turn it is
    current_player = player(board)

    # Apply the move to the new board
    new_board[i][j] = current_player

    return new_board



def winner(board):
    """
    Returns the winner of the game if there is one, else returns None.
    """
    # Check rows for a winner
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    # Check columns for a winner
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not EMPTY:
            return board[0][col]

    # Check diagonals for a winner
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    # No winner found
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there is a winner
    if winner(board) is not None:
        return True

    # Check if the board is full (no more empty cells)
    for row in board:
        if EMPTY in row:
            return False

    # If the board is full and no winner, it's a tie
    return True


def utility(board):
    """
    Returns 1 if X has won, -1 if O has won, 0 otherwise (tie).
    """
    game_winner = winner(board)

    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
