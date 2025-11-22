import connect4_board as c4
import numpy as np

def negmax(position=c4.position):
    piece = c4.PLAYER1_PIECE if position.get_move()%2 == 0 else c4.PLAYER2_PIECE
    if(position.tie_board()):
        return 0; 

    for col in range(c4.COL_COUNT):
        if(position.is_valid_location(i=col) and position.winning_move(piece)):
            return (c4.COL_COUNT*c4.ROW_COUNT+1 - position.get_move())/2
        
    best_score = -c4.COL_COUNT*c4.ROW_COUNT
    best_position = position
    for col in range(c4.COL_COUNT*c4.ROW_COUNT):
        if(position.is_valid_location(col)):
            next_posistion = c4.position(position)
            next_posistion.drop_piece(col, piece)
            score = negmax(next_posistion)
            if(score>best_score): 
                best_score = score
                best_position = next_posistion
                 
    return best_position