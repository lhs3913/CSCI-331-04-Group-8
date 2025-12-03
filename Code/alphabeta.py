import connect4_board as c4
import sys
import heuristic as h
import time # Metric: Import time library

# Metric: Global counter for nodes
NODES_VISITED = 0
SEARCH_DEPTH = 42

def alphabeta(position, depth, alpha, beta):
    # Metric: Increment counter
    global NODES_VISITED
    NODES_VISITED += 1

    if position.winning_move(c4.PLAYER1_PIECE) or position.winning_move(c4.PLAYER2_PIECE):
        return [1000000000 + depth, position]
    
    # NOTE: 'piece' was undefined in your original code here; assuming standard check logic or relying on global turn. 
    # For safety in score_position, we usually need to know whose turn it is. 
    # Added logic to determine piece based on move number for the heuristic call.
    piece = c4.PLAYER1_PIECE if position.get_move() % 2 == 0 else c4.PLAYER2_PIECE
    
    if position.tie_board() or depth == 0:
        return [h.score_position(position, piece), position]
        
    best_position = position.copy()
    best_score = -float('inf')
    for col in range(c4.COL_COUNT):
        if position.is_valid_location(col):
            next_posistion = position.copy()
            next_posistion.drop_piece(col, piece)
            
            score = -alphabeta(next_posistion, depth - 1, -beta, -alpha)[0]
            
            if score > best_score: 
                best_score = score
                best_position = next_posistion
            alpha = max(alpha, best_score)
            if alpha >= beta: 
                break 
                 
    return [best_score, best_position]

if __name__ == "__main__":
    try:
        player = int(sys.argv[1])
        if not (player == 0 or player == 1):
            print("Invalid argument")
            sys.exit()
        turn = 0

    except Exception:
        print("Error: Please provide a starting player (0 or 1) as a command line argument.")
        sys.exit()
    board = c4.position()
    board.print_board()

    while not board.tie_board():
        current_piece = c4.PLAYER1_PIECE if turn == 0 else c4.PLAYER2_PIECE

        if turn == player:
            try:
                col_input = input(f"Player {turn + 1} make your move (0–6): ")
                if not col_input.isdigit():
                    print("Invalid input — please enter a number between 0 and 6.")
                    continue

                col = int(col_input)

                if col < 0 or col >= c4.COL_COUNT:
                    print("Invalid column — choose a number between 0 and 6.")
                    continue

                if not board.is_valid_location(col):
                    print("Column is full try again")
                    continue

                piece = c4.PLAYER1_PIECE if turn == 0 else c4.PLAYER2_PIECE
                board.drop_piece(col, piece)
                board.print_board()

                if board.winning_move(piece):
                    print(f"Player {turn + 1} wins!")
                    break

                turn = (turn + 1) % 2

            except Exception as e:
                print(f"Error: {e}. Please try again.")
        else:
            print("AI is thinking...")
            
            # --- METRICS START ---
            NODES_VISITED = 0           # Reset counter
            start_time = time.time()    # Start timer
            
            DEPTH = SEARCH_DEPTH
            best_move_result = alphabeta(board, DEPTH, -float('inf'), float('inf'))
            
            end_time = time.time()      # End timer
            print(f"Stats -> Depth: {DEPTH} | Time: {end_time - start_time:.4f}s | Nodes: {NODES_VISITED}")
            # --- METRICS END ---

            board = best_move_result[1]
            board.print_board()

            if board.winning_move(current_piece):
                print(f"Player {turn + 1} wins!")
                break

            turn = (turn + 1) % 2
            
    if board.tie_board():
        print("Game is a tie!")