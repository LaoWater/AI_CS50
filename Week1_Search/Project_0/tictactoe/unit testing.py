from tictactoe import player, actions, result, winner, terminal, utility
import math


def test_utility():
    # Test Case 1: X has won
    board_u = [[X, X, X],
               [O, O, EMPTY],
               [EMPTY, EMPTY, EMPTY]]
    assert utility(board_u) == 1, "Test Case 1 Failed"

    # Test Case 2: O has won
    board_u = [[X, O, X],
               [X, O, EMPTY],
               [EMPTY, O, EMPTY]]
    assert utility(board_u) == -1, "Test Case 2 Failed"

    # Test Case 3: Tie game
    board_u = [[X, O, X],
               [X, O, O],
               [O, X, X]]
    assert utility(board_u) == 0, "Test Case 3 Failed"

    print("All test cases passed!")


def test_terminal():
    # Test Case 1: Game is not over, still in progress
    board_terminal_check = [[X, O, EMPTY],
                            [O, X, EMPTY],
                            [EMPTY, O, EMPTY]]
    assert terminal(board_terminal_check) == False, "Test Case 1 Failed"

    # Test Case 2: X has won, game is over
    board_terminal_check = [[X, X, X],
                            [O, O, EMPTY],
                            [EMPTY, EMPTY, EMPTY]]
    assert terminal(board_terminal_check) == True, "Test Case 2 Failed"

    # Test Case 3: O has won, game is over
    board_terminal_check = [[X, O, X],
                            [X, O, EMPTY],
                            [EMPTY, O, EMPTY]]
    assert terminal(board_terminal_check) == True, "Test Case 3 Failed"

    # Test Case 4: Tie game, board is full
    board_terminal_check = [[X, O, X],
                            [X, O, O],
                            [O, X, X]]
    assert terminal(board_terminal_check) == True, "Test Case 4 Failed"

    # Test Case 5: Game is not over, still in progress
    board_terminal_check = [[X, O, X],
                            [X, EMPTY, O],
                            [O, EMPTY, X]]
    assert terminal(board_terminal_check) == False, "Test Case 5 Failed"

    print("All test cases passed!")


def test_winner():
    # Test Case 1: X wins in a row
    board = [[X, X, X],
             [O, O, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    assert winner(board) == X, "Test Case 1 Failed"

    # Test Case 2: O wins in a column
    board = [[X, O, X],
             [X, O, EMPTY],
             [EMPTY, O, EMPTY]]
    assert winner(board) == O, "Test Case 2 Failed"

    # Test Case 3: X wins in a diagonal
    board = [[X, O, EMPTY],
             [O, X, EMPTY],
             [EMPTY, O, X]]
    assert winner(board) == X, "Test Case 3 Failed"

    # Test Case 4: No winner yet
    board = [[X, O, EMPTY],
             [O, X, EMPTY],
             [EMPTY, O, EMPTY]]
    assert winner(board) == None, "Test Case 4 Failed"

    # Test Case 5: O wins in a diagonal (other direction)
    board = [[X, X, O],
             [X, O, EMPTY],
             [O, EMPTY, EMPTY]]
    assert winner(board) == O, "Test Case 5 Failed"

    print("All test cases passed!")


def test_player():
    # Test Case 1: Initial empty board, X should go first
    board = [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    assert player(board) == X, "Test Case 1 Failed"

    # Test Case 2: X has one move, O's turn
    board = [[X, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    assert player(board) == O, "Test Case 2 Failed"

    # Test Case 3: X has one move, O has one move, X's turn
    board = [[X, O, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    assert player(board) == X, "Test Case 3 Failed"

    # Test Case 4: X has two moves, O has one move, O's turn
    board = [[X, O, X],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    assert player(board) == O, "Test Case 4 Failed"

    # Test Case 5: X has two moves, O has two moves, X's turn
    board = [[X, O, X],
             [O, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    assert player(board) == X, "Test Case 5 Failed"

    # Test Case 6: More O's than X's, should raise an error
    board = [[X, O, O],
             [O, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    try:
        player(board)
        assert False, "Test Case 6 Failed: Should raise ValueError"
    except ValueError:
        pass

    print("All test cases passed!")


def test_result_function():
    ''' # Test Case 1: Valid move by X on an empty board
    board_input = [[EMPTY, EMPTY, EMPTY],
                   [EMPTY, EMPTY, EMPTY],
                   [EMPTY, EMPTY, EMPTY]]
    action = (1, 1)  # X's turn, center move
    new_board = result(board_input, action)
    expected_board = [[EMPTY, EMPTY, EMPTY],
                      [EMPTY, X, EMPTY],
                      [EMPTY, EMPTY, EMPTY]]
    assert new_board == expected_board, "Test Case 1 Failed"

    # Test Case 4: Ensure original board is not modified
    board_input = [[X, O, EMPTY],
                   [EMPTY, EMPTY, EMPTY],
                   [EMPTY, EMPTY, EMPTY]]
    action = (1, 1)
    _ = result(board_input, action)  # Run result function but don't use the output
    unchanged_board = [[X, EMPTY, EMPTY],
                       [EMPTY, EMPTY, EMPTY],
                       [EMPTY, EMPTY, EMPTY]]
    assert board_input == unchanged_board, "Test Case 4 Failed: Original board modified"

    print("All test cases passed! \nMoving onto user input game state and action test:")
    '''

    # Test Case 2: Valid move by O after X
    board_input = [[X, X, EMPTY],
                   [EMPTY, EMPTY, EMPTY],
                   [O, EMPTY, EMPTY]]
    action = (2, 2)  # O's turn
    new_board = result(board_input, action)
    action = (1, 2)  # 1's turn
    new_board = result(new_board, action)
    for i in new_board:
        print(i)


X = "X"
O = "O"
EMPTY = None

#################
## Test Player ##
#################
print("\nTesting Player Function:")
test_player()

#################
## Test Action ##
#################
print("\nTesting Action Function:")
board = [[X, EMPTY, O],
         [EMPTY, O, X],
         [X, EMPTY, EMPTY]]

print(actions(board))  # Expected output: {(0, 1), (1, 0), (2, 1), (2, 2)}

#################
## Test Result ##
#################
print("\nTesting Result Function:")
test_result_function()

#################
## Test Winner ##
#################
print("\nTesting Winner Function:")
test_winner()

#################
## Test Terminal ##
#################
print("\nTesting Terminal Function:")
test_terminal()

#################
## Test Utility ##
#################
print("\nTesting Utility Function:")
test_utility()


#################
## Test Terminal ##
#################
print("\nTesting Terminal Function:")
test_terminal()
