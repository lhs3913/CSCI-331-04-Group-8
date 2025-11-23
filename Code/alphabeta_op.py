import connect4_board as c4
import numpy as np
import sys
import copy

COL_ORDER = [3,4,2,5,1,6,0]

def alphabeta(alpha, beta, position=c4.position):
    piece = c4.PLAYER1_PIECE if position.get_move()%2 == 0 else c4.PLAYER2_PIECE
    best_position = position.copy
    if(position.tie_board()):
        return [0, best_position]; 
    maximum = (c4.COL_COUNT*c4.ROW_COUNT-1 - position.get_move())/2;	
    if(beta > maximum):
        beta = maximum                     
        if(alpha >= beta):
            return [beta, best_position]
        
    best_score = -c4.COL_COUNT*c4.ROW_COUNT
    for col in range(c4.COL_COUNT):
        if(position.is_valid_location(COL_ORDER[col])):
            next_posistion = position.copy()
            next_posistion.drop_piece(COL_ORDER[col], piece)
            if(next_posistion.winning_move(piece)):
                return [(c4.COL_COUNT*c4.ROW_COUNT+1 - next_posistion.get_move())/2,next_posistion]
            score = -alphabeta(-beta, -alpha, next_posistion)[0]
            if(score>best_score): 
                best_score = score
                best_position = next_posistion
                if(score >= beta): return [score,best_position]  
                if(score > alpha): alpha = score
    return [alpha,best_position]         

if __name__ == "__main__":
    try:
        player = int(sys.argv[1])
        if(not(player == 0 or player == 1)):
            print("invalid argument")
            sys.exit()
        turn = 0
    except Exception as e:
        print("invalid argument")
        sys.exit()
    board = c4.position()
    board.print_board()
    while not(board.tie_board()):
        if(turn == player):
            try:
                # Ask player for input
                col = input(f"Player {turn + 1} make your move (0–6): ")

                # Validate input is numeric
                if not col.isdigit():
                    print("Invalid input — please enter a number between 0 and 6.")
                    continue

                col = int(col)

                # Validate input range
                if col < 0 or col >= c4.COL_COUNT:
                    print("Invalid column — choose a number between 0 and 6.")
                    continue

                # Validate column availability
                if not board.is_valid_location(col):
                    print("That column is full. Try another one.")
                    continue

                # Drop the piece
                piece = c4.PLAYER1_PIECE if turn == 0 else c4.PLAYER2_PIECE
                board.drop_piece(col, piece)
                board.print_board()

                if board.winning_move(piece):
                    print(f"Player {turn + 1} wins!")
                    break

                # Alternate turns
                turn = (turn + 1) % 2

            except Exception as e:
                print(f"Error: {e}. Please try again.")
        else:
            board = alphabeta(-float("inf"), float("inf"), board)[1]
            board.print_board()
            turn = (turn + 1) % 2