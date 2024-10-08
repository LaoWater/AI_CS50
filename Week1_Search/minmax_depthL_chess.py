class Piece:
    def __init__(self, color, x, y, value, is_developed=False):
        self.color = color
        self.x = x
        self.y = y
        self.value = value
        self.is_developed = is_developed

    def __repr__(self):
        return f"{self.color} {self.__class__.__name__} at ({self.x}, {self.y})"


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y, value=1000)

    def is_under_attack(self, board):
        # Simplified check for demonstration purposes
        for piece in board.pieces:
            if piece.color != self.color and piece.__class__.__name__ == "Queen":
                if abs(piece.x - self.x) <= 1 and abs(piece.y - self.y) <= 1:
                    return True
        return False


class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y, value=9)


class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y, value=5)


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y, value=3)


class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y, value=3)


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y, value=1)


class Board:
    def __init__(self):
        self.pieces = []
        self.current_player = "white"
        self.is_game_over = False

        # Initialize pieces to a specific state
        self.pieces.append(King("white", 4, 0))
        self.pieces.append(Queen("white", 3, 0))
        self.pieces.append(Rook("white", 0, 0))
        self.pieces.append(Rook("white", 7, 0))
        self.pieces.append(Bishop("white", 2, 0))
        self.pieces.append(Bishop("white", 5, 0))
        self.pieces.append(Knight("white", 1, 0))
        self.pieces.append(Knight("white", 6, 0))
        self.pieces.append(Pawn("white", 0, 1))
        self.pieces.append(Pawn("white", 1, 1))
        self.pieces.append(Pawn("white", 2, 1))
        self.pieces.append(Pawn("white", 3, 1))
        self.pieces.append(Pawn("white", 4, 1))
        self.pieces.append(Pawn("white", 5, 1))
        self.pieces.append(Pawn("white", 6, 1))
        self.pieces.append(Pawn("white", 7, 1))

        self.pieces.append(King("black", 4, 7))
        self.pieces.append(Queen("black", 3, 7))
        self.pieces.append(Rook("black", 0, 7))
        self.pieces.append(Rook("black", 7, 7))
        self.pieces.append(Bishop("black", 2, 7))
        self.pieces.append(Bishop("black", 5, 7))
        self.pieces.append(Knight("black", 1, 7))
        self.pieces.append(Knight("black", 6, 7))
        self.pieces.append(Pawn("black", 0, 6))
        self.pieces.append(Pawn("black", 1, 6))
        self.pieces.append(Pawn("black", 2, 6))
        self.pieces.append(Pawn("black", 3, 6))
        self.pieces.append(Pawn("black", 4, 6))
        self.pieces.append(Pawn("black", 5, 6))
        self.pieces.append(Pawn("black", 6, 6))
        self.pieces.append(Pawn("black", 7, 6))

        # Move some pieces to create a more challenging state
        self.pieces.append(Pawn("white", 4, 3))
        self.pieces.append(Pawn("black", 4, 4))
        self.pieces.append(Knight("white", 3, 3))
        self.pieces.append(Bishop("black", 5, 5))

    def get_king(self, color):
        for piece in self.pieces:
            if piece.__class__.__name__ == "King" and piece.color == color:
                return piece

    def get_possible_moves(self):
        # Simplified move generation for demonstration purposes
        moves = []
        for piece in self.pieces:
            if piece.color == self.current_player:
                if piece.__class__.__name__ == "Pawn":
                    moves.append((piece.x, piece.y + 1))
                elif piece.__class__.__name__ == "Knight":
                    moves.append((piece.x + 2, piece.y + 1))
                    moves.append((piece.x + 2, piece.y - 1))
                    moves.append((piece.x - 2, piece.y + 1))
                    moves.append((piece.x - 2, piece.y - 1))
        return moves

    def make_move(self, move):
        new_board = Board()
        new_board.pieces = self.pieces[:]
        new_board.current_player = self.current_player
        new_board.is_game_over = self.is_game_over

        # Find the piece to move
        piece_to_move = None
        for piece in new_board.pieces:
            if piece.x == move[0] and piece.y == move[1] - 1:
                piece_to_move = piece
                break

        # Move the piece
        if piece_to_move:
            piece_to_move.x = move[0]
            piece_to_move.y = move[1]

        # Switch current player
        if new_board.current_player == "white":
            new_board.current_player = "black"
        else:
            new_board.current_player = "white"

        return new_board

    def print_board(self):
        print("  a b c d e f g h")
        for y in range(8):
            print(y + 1, end=" ")
            for x in range(8):
                piece = None
                for p in self.pieces:
                    if p.x == x and p.y == y:
                        piece = p
                        break
                if piece:
                    if piece.color == "white":
                        if piece.__class__.__name__ == "King":
                            print("K", end=" ")
                        elif piece.__class__.__name__ == "Queen":
                            print("Q", end=" ")
                        elif piece.__class__.__name__ == "Rook":
                            print("R", end=" ")
                        elif piece.__class__.__name__ == "Bishop":
                            print("B", end=" ")
                        elif piece.__class__.__name__ == "Knight":
                            print("N", end=" ")
                        elif piece.__class__.__name__ == "Pawn":
                            print("P", end=" ")
                    else:
                        if piece.__class__.__name__ == "King":
                            print("k", end=" ")
                        elif piece.__class__.__name__ == "Queen":
                            print("q", end=" ")
                        elif piece.__class__.__name__ == "Rook":
                            print("r", end=" ")
                        elif piece.__class__.__name__ == "Bishop":
                            print("b", end=" ")
                        elif piece.__class__.__name__ == "Knight":
                            print("n", end=" ")
                        elif piece.__class__.__name__ == "Pawn":
                            print("p", end=" ")
                else:
                    print(".", end=" ")
            print()


def evaluate_board(board):
    material_balance = 0
    piece_development = 0
    king_safety = 0

    # Material balance
    for piece in board.pieces:
        if piece.color == board.current_player:
            material_balance += piece.value
        else:
            material_balance -= piece.value

    # Piece development
    for piece in board.pieces:
        if piece.color == board.current_player and piece.is_developed:
            piece_development += 1

    # King safety
    king = board.get_king(board.current_player)
    if king.is_under_attack(board):
        king_safety -= 50
    else:
        king_safety += 50

    return material_balance * 100 + piece_development * 20 + king_safety * 50


def min_max(board, depth, is_maximizing_player):
    if depth == 0 or board.is_game_over:
        return evaluate_board(board)

    if is_maximizing_player:
        best_score = -float('inf')
        for move in board.get_possible_moves():
            new_board = board.make_move(move)
            score = min_max(new_board, depth - 1, False)
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for move in board.get_possible_moves():
            new_board = board.make_move(move)
            score = min_max(new_board, depth - 1, True)
            best_score = min(best_score, score)
        return best_score


def get_best_move(board, depth):
    best_score = -float('inf')
    best_move = None
    for move in board.get_possible_moves():
        new_board = board.make_move(move)
        score = min_max(new_board, depth - 1, False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def interpret_move(move):
    x = move[0]
    y = move[1]
    files = ["a", "b", "c", "d", "e", "f", "g", "h"]
    ranks = ["1", "2", "3", "4", "5", "6", "7", "8"]
    return files[x] + ranks[y]


# Example usage
board = Board()
board.print_board()
depth = 3
best_move = get_best_move(board, depth)
print("Best move:", interpret_move(best_move))
