import sys
import copy

# Constants
ROW_COUNT = 6
COL_COUNT = 7
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2
EMPTY = 0
BOARD_FILE = "./Resources/boards/valid_boards/blank board.txt"

class position:
    def __init__(self):
        """Initialize the board by reading from a text file and validating state."""
        self.board = []
        self.move_num = 0
        self.current_turn = 0 # 0 = P1, 1 = P2
        
        p1_count = 0
        p2_count = 0
        
        try:
            with open(BOARD_FILE, "r") as f:
                lines = f.readlines()
                
                # --- STEP 1: READ & CHECK INVALID CHARACTERS ---
                raw_rows = []
                for line in lines:
                    stripped = line.strip()
                    if not stripped: continue 
                    
                    parts = stripped.split(' ')
                    row_data = []
                    
                    for char in parts:
                        if char not in ['x', 'o', '.']:
                            print(f"Invalid character in file: {BOARD_FILE}")
                            print('Must use "x", "o", or "."')
                            sys.exit()
                        row_data.append(char)
                    raw_rows.append(row_data)

                # --- STEP 2: CONVERT TO GAME BOARD & COUNT PIECES ---
                for r_idx, row_chars in enumerate(raw_rows):
                    int_row = []
                    for c_idx, char in enumerate(row_chars):
                        if char == 'x':
                            int_row.append(PLAYER1_PIECE)
                            p1_count += 1
                        elif char == 'o':
                            int_row.append(PLAYER2_PIECE)
                            p2_count += 1
                        else:
                            int_row.append(EMPTY)
                    self.board.append(int_row)

            # Handle empty file case safely
            if not self.board:
                 self.board = [[EMPTY for _ in range(COL_COUNT)] for _ in range(ROW_COUNT)]

            # --- STEP 3: CHECK PIECE COUNTS (TURN ORDER VALIDATION) ---
            # P2 cannot have more than P1. P1 cannot have >1 more than P2.
            if p2_count > p1_count or (p1_count - p2_count) > 1:
                print(f"Invalid number of starting peices for players in file: {BOARD_FILE}")
                print('Can only have 1 more "x" than "o"')
                print('Can never have more "o"\'s than "x"\'s')
                print('Can never have a puck amount difference greater than 1')
                sys.exit()

            # --- STEP 4: CHECK GRAVITY (FLOATING PIECES) ---
            for c in range(COL_COUNT):
                gap_found = False
                # Scan column from bottom (5) to top (0)
                for r in range(ROW_COUNT - 1, -1, -1):
                    cell = self.board[r][c]
                    if cell == EMPTY:
                        gap_found = True
                    elif gap_found:
                        # If we found a piece AFTER finding a gap below it, it's floating
                        print(f"Floating token in file: {BOARD_FILE}")
                        print("All pucks must be on the bottom row or on top of another puck")
                        sys.exit()

            # --- STEP 5: SET GAME STATE ---
            self.move_num = p1_count + p2_count
            
            # Determine turn: If equal pieces, P1 goes. If P1 has 1 more, P2 goes.
            if p1_count == p2_count:
                self.current_turn = 0
            else:
                self.current_turn = 1

        except FileNotFoundError:
            print("Error: Board file not found. Creating empty board.")
            self.board = [[EMPTY for _ in range(COL_COUNT)] for _ in range(ROW_COUNT)]
            self.current_turn = 0

    def get_board(self):
        return self.board
    
    def get_move(self):
        return self.move_num
        
    def get_starting_turn(self):
        return self.current_turn

    def drop_piece(self, col, piece):
        """Place the player's piece in the board at (row, col)."""
        row = self.get_next_open_row(col)
        if row is not None:
            self.board[row][col] = piece
            self.move_num += 1

    def is_valid_location(self, col):
        """Return True if the top cell in a column is empty."""
        if col < 0 or col >= COL_COUNT: return False
        return self.board[0][col] == EMPTY

    def get_next_open_row(self, col):
        """Find the lowest empty row in a column."""
        for r in range(ROW_COUNT - 1, -1, -1):
            if self.board[r][col] == EMPTY:
                return r
        return None

    def print_board(self):
        print("\nCurrent Board:")
        for r in range(ROW_COUNT):
            print(" ".join(str(int(x)) for x in self.board[r]))
        print("-" * 13)
        print("0 1 2 3 4 5 6")
        
    def tie_board(self):
        return self.move_num >= ROW_COUNT*COL_COUNT

    def copy(self):
        new_pos = position().__new__(position)
        new_pos.board = copy.deepcopy(self.board)
        new_pos.move_num = self.move_num
        new_pos.current_turn = self.current_turn
        return new_pos

    # Win Checking Logic
    def winning_move(self, piece):
        """Check all directions for a 4-in-a-row."""
        # Check horizontal
        for c in range(COL_COUNT - 3):
            for r in range(ROW_COUNT):
                if (self.board[r][c] == piece and self.board[r][c+1] == piece and 
                    self.board[r][c+2] == piece and self.board[r][c+3] == piece):
                    return True

        # Check vertical
        for c in range(COL_COUNT):
            for r in range(ROW_COUNT - 3):
                if (self.board[r][c] == piece and self.board[r+1][c] == piece and 
                    self.board[r+2][c] == piece and self.board[r+3][c] == piece):
                    return True

        # Check positively sloped diagonals
        for c in range(COL_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if (self.board[r][c] == piece and self.board[r+1][c+1] == piece and 
                    self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece):
                    return True

        # Check negatively sloped diagonals
        for c in range(COL_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if (self.board[r][c] == piece and self.board[r-1][c+1] == piece and 
                    self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece):
                    return True

        return False

if __name__ == "__main__":
    board = position()
    board.print_board()
    
    # Initialize turn based on the loaded file
    turn = board.current_turn

    while not(board.tie_board()):
        try:
            # Ask player for input
            col_input = input(f"Player {turn + 1} make your move (0–6): ")

            # Validate input is numeric
            if not col_input.isdigit():
                print("Invalid input — please enter a number between 0 and 6.")
                continue

            col = int(col_input)

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