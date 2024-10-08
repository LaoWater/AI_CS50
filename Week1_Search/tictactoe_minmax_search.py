import tkinter as tk
import math


# Function to evaluate the board and return a score based on the current state
def evaluate(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            if row[0] == 'X':
                return 10
            elif row[0] == 'O':
                return -10

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            if board[0][col] == 'X':
                return 10
            elif board[0][col] == 'O':
                return -10

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        if board[0][0] == 'X':
            return 10
        elif board[0][0] == 'O':
            return -10

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        if board[0][2] == 'X':
            return 10
        elif board[0][2] == 'O':
            return -10

    return 0


def is_moves_left(board):
    for row in board:
        if ' ' in row:
            return True
    return False


def minimax(board, depth, is_max):
    score = evaluate(board)

    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if not is_moves_left(board):
        return 0

    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    best = max(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = ' '
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    best = min(best, minimax(board, depth + 1, not is_max))
                    board[i][j] = ' '
        return best


def find_best_move(board):
    best_val = math.inf  # AI is 'O' and wants to minimize the score
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_val = minimax(board, 0, True)
                board[i][j] = ' '
                if move_val < best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move


def check_game_over(board):
    score = evaluate(board)
    if score == 10:
        return "X wins!"
    elif score == -10:
        return "O wins!"
    elif not is_moves_left(board):
        return "It's a tie!"
    return None


def on_click(row, col):
    if buttons[row][col]["text"] == " " and not game_over:
        buttons[row][col]["text"] = "X"
        board[row][col] = "X"
        result = check_game_over(board)
        if result:
            label.config(text=result)
            global game_over
            game_over = True
        else:
            ai_move()


def ai_move():
    move = find_best_move(board)
    buttons[move[0]][move[1]]["text"] = "O"
    board[move[0]][move[1]] = "O"
    result = check_game_over(board)
    if result:
        label.config(text=result)
        global game_over
        game_over = True


# Initialize the game
root = tk.Tk()
root.title("Tic-Tac-Toe")

board = [[" " for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
game_over = False

label = tk.Label(root, text="Your turn (X)", font=("Helvetica", 16))
label.grid(row=0, column=0, columnspan=3)

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text=" ", font=("Helvetica", 20), height=3, width=6,
                                  command=lambda i=i, j=j: on_click(i, j))
        buttons[i][j].grid(row=i + 1, column=j)

root.mainloop()
