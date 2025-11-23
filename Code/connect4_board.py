import numpy as np

# Constants
ROW_COUNT = 6
COL_COUNT = 7
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2
EMPTY = 0


class position:
    def __init__(self):
        """Create a 6x7 Connect 4 board initialized with zeros."""
        self.board = np.zeros((ROW_COUNT, COL_COUNT), dtype=int)
        self.move_num = 0

    def __init__(self, board):
        """Create a 6x7 Connect 4 board initialized with zeros."""
        self.board = board
        self.move_num = 0

    def get_board(self):
        return self.board
    
    def get_move(self):
        return self.move_num
    
    def copy(self):
        copy_board = np.copy(self.board)
        return position(copy_board)

    def drop_piece(self, col, piece):
        """Place the player's piece in the board at (row, col)."""
        row = self.get_next_open_row(col)
        self.board[row][col] = piece
        self.move_num += 1

    def is_valid_location(self, col):
        """Return True if the top cell in a column is empty."""
        return self.board[0][col] == EMPTY


    def get_next_open_row(self, col):
        """Find the lowest empty row in a column."""
        for r in range(ROW_COUNT - 1, -1, -1):
            if self.board[r][col] == EMPTY:
                return r
        return None


    def print_board(self):
        print("\nCurrent Board:")
        for r in range(ROW_COUNT):  # top (0) → bottom (5)
            print(" ".join(str(int(x)) for x in self.board[r]))
        

    def tie_board(self):
        return self.move_num == ROW_COUNT*COL_COUNT


    # Win Checking Logic
    def winning_move(self, piece):
        """Check all directions for a 4-in-a-row."""
        # Check horizontal locations
        for c in range(COL_COUNT - 3):
            for r in range(ROW_COUNT):
                if (
                    self.board[r][c] == piece
                    and self.board[r][c + 1] == piece
                    and self.board[r][c + 2] == piece
                    and self.board[r][c + 3] == piece
                ):
                    return True

        # Check vertical locations
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c] == piece
                    and self.board[r + 2][c] == piece
                    and self.board[r + 3][c] == piece
                ):
                    return True

        # Check positively sloped diagonals
        for c in range(COL_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if (
                    self.board[r][c] == piece
                    and self.board[r + 1][c + 1] == piece
                    and self.board[r + 2][c + 2] == piece
                    and self.board[r + 3][c + 3] == piece
                ):
                    return True

        # Check negatively sloped diagonals
        for c in range(COL_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if (
                    self.board[r][c] == piece
                    and self.board[r - 1][c + 1] == piece
                    and self.board[r - 2][c + 2] == piece
                    and self.board[r - 3][c + 3] == piece
                ):
                    return True

        return False



if __name__ == "__main__":
    board = position()
    board.print_board()

    turn = 0

    while not(board.tie_board()):
        try:
            # Ask player for input
            col = input(f"Player {turn + 1} make your move (0–6): ")

            # Validate input is numeric
            if not col.isdigit():
                print("Invalid input — please enter a number between 0 and 6.")
                continue

            col = int(col)

            # Validate input range
            if col < 0 or col >= COL_COUNT:
                print("Invalid column — choose a number between 0 and 6.")
                continue

            # Validate column availability
            if not board.is_valid_location(col):
                print("That column is full. Try another one.")
                continue

            # Drop the piece
            piece = PLAYER1_PIECE if turn == 0 else PLAYER2_PIECE
            board.drop_piece(col, piece)
            board.print_board()

            if board.winning_move(piece):
                print(f"Player {turn + 1} wins!")
                break

            # Alternate turns
            turn = (turn + 1) % 2

        except Exception as e:
            print(f"Error: {e}. Please try again.")