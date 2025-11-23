import connect4_board as c4

def evaluate_window(window, piece):
    score = 0
    opp_piece = 1 if piece == 2 else 2
    
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2
        
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4  # Block opponent

    return score

def score_position(board_obj, piece):
    score = 0
    board = board_obj.get_board()
    
    # Score Center Column
    center_array = [int(i) for i in list(board[:, c4.COL_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal
    for r in range(c4.ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(c4.COL_COUNT - 3):
            score += evaluate_window(row_array[c:c+4], piece)

    # Vertical
    for c in range(c4.COL_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(c4.ROW_COUNT - 3):
            score += evaluate_window(col_array[r:r+4], piece)

    # Positive Diagonal
    for r in range(c4.ROW_COUNT - 3):
        for c in range(c4.COL_COUNT - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)
            
    # Negative Diagonal
    for r in range(c4.ROW_COUNT - 3):
        for c in range(c4.COL_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score