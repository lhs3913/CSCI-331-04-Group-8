import numpy as np

# Constants
ROW_COUNT = 6
COL_COUNT = 7
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2
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
    print("\nCurrent Board:")
    for r in range(ROW_COUNT):  # top (0) → bottom (5)
        print(" ".join(str(int(x)) for x in board[r]))
        

def valid_board(board):
    for c in range(COL_COUNT):
        if(is_valid_location(board, c)):
            return True
    return False


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

    while valid_board(board):
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
            if not is_valid_location(board, col):
                print("That column is full. Try another one.")
                continue

            # Drop the piece
            row = get_next_open_row(board, col)
            piece = PLAYER1_PIECE if turn == 0 else PLAYER2_PIECE
            drop_piece(board, row, col, piece)

            print_board(board)

            if winning_move(board, piece):
                print(f"Player {turn + 1} wins!")
                game_over = True
                break

            # Alternate turns
            turn = (turn + 1) % 2

        except Exception as e:
            print(f"Error: {e}. Please try again.")