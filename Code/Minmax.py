import connect4_board as c4
import numpy as np
import sys
import heuristic as h

def negmax(depth, position=c4.position):
    currentPiece = c4.PLAYER1_PIECE if position.get_move() % 2 == 0 else c4.PLAYER2_PIECE
    if position.winning_move(c4.PLAYER1_PIECE) or position.winning_move(c4.PLAYER2_PIECE):
        score = (c4.COL_COUNT * c4.ROW_COUNT + 1 - position.get_move()) / 2 
        return [1000000000, position]
        
    if position.tie_board():
        return [0, position]
    if depth == 0:
        return [h.score_position.score_position(position, currentPiece), position]
        
    best_score = -float('inf')
    best_position = position.copy()

    for col in range(c4.COL_COUNT):
        if position.is_valid_location(col):
            next_position = position.copy()
            next_position.drop_piece(col, currentPiece)
            score = -negmax(next_position, depth - 1)[0]
            if score > best_score: 
                best_score = score
                best_position = next_position
    return [best_score, best_position]

if __name__ == "__main__":
    try:
        player = int(sys.argv[1])
        if not (player == 0 or player == 1):
            print("Invalid Argument: Player must be '0' or '1'. ")
            sys.exit()
        turn = 0
    except IndexError:
        print("Index Error: Please provide a 0 or 1 as a command line argument")
        sys.exit()
    except Exception:
        print("Invalid Argument: Please try again")
        sys.exit()
    
    board = c4.position 
    board.print_board
    while not board.tie_board():
        currentPiece = c4.PLAYER1_PIECE if turn == 0 else c4.PLAYER2_PIECE 

        if turn == player:
            try:
                col = input(f"Player {turn + 1} (Human) make your move (0–6): ")
                    
                if not col.isdigit():
                    print("Invalid input — please enter a number between 0 and 6.")
                    continue

                col = int(col)

                if col < 0 or col >= c4.COL_COUNT:
                    print("Invalid column — choose a number between 0 and 6.")
                    continue

                if not board.is_valid_location(col):
                    print("That column is full. Try another one.")
                    continue

                board.drop_piece(col, currentPiece)
                board.print_board()

                if board.winning_move(currentPiece):
                    print(f"Player {turn + 1} wins!")
                    break

                turn = (turn + 1) % 2

            except Exception as e:
                    print(f"Error: {e}. Please try again.")
        else:
            # Set a depth of 5 for default running
            best_move_result = negmax(board, 5)
            board = best_move_result[1]
            board.print_board()
            if board.winning_move(currentPiece):
                print(f"Player {turn + 1} (AI) wins!")
                break

            turn = (turn + 1) % 2

        if board.tie_board():
            print("Game is a tie!")