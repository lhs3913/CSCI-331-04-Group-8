import numpy as np

# Constants
ROW_COUNT = 6
COL_COUNT = 7

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0


# Board Setup
def create_board():
    """Create a 6x7 Connect 4 board initialized with zeros."""
    board = np.zeros((ROW_COUNT, COL_COUNT), dtype=int)
    return board


def drop_piece(board, row, col, piece):
    """Place the player's piece in the board at (row, col)."""
    board[row][col] = piece


def is_valid_location(board, col):
    """Return True if the top cell in a column is empty."""
    return board[0][col] == EMPTY


def get_next_open_row(board, col):
    """Find the lowest empty row in a column."""
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None


def print_board(board):
    """Print board in a readable grid format (bottom row printed last)."""
    print(np.flip(board, 0))



# Win Checking Logic
def winning_move(board, piece):
    """Check all directions for a 4-in-a-row."""
    # Check horizontal locations
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical locations
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positively sloped diagonals
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negatively sloped diagonals
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True

    return False



if __name__ == "__main__":
    board = create_board()
    print_board(board)

    game_over = False
    turn = 0

    while not game_over:
        # Player 1 Input
        if turn == 0:
            col = int(input("Player 1 make your move (0-6): "))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)

                if winning_move(board, PLAYER_PIECE):
                    print_board(board)
                    print("PLAYER 1 WINS!!")
                    game_over = True

        # Player 2 Input
        else:
            col = int(input("Player 2 make your move (0-6): "))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    print_board(board)
                    print("PLAYER 2 WINS!!")
                    game_over = True

        print_board(board)
        turn += 1
        turn %= 2