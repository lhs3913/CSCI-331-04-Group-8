# Filename: connect4_gui.py
# Requires: ./Resources/art/*.png
# Works with: connect4_board.py

import pygame
import sys
import connect4_board as c4
import math

# CONFIG
TILE_SIZE = 100
SCREEN_WIDTH = c4.COL_COUNT * TILE_SIZE
SCREEN_HEIGHT = (c4.ROW_COUNT + 1) * TILE_SIZE  # extra row for preview area

# COLORS
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Art file paths
ART_PATH = "./Resources/art/"
IMG_EMPTY = ART_PATH + "empty connect 4-export.png"
IMG_RED_PIECE = ART_PATH + "red piece-export.png"
IMG_YELLOW_PIECE = ART_PATH + "yellow piece-export.png"

# INITIALIZE PYGAME
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect 4")
font = pygame.font.SysFont("arial", 60, bold=True)

# Load and scale images
def load_image(path):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    except:
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surf.fill(GRAY)
        pygame.draw.circle(surf, WHITE, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2-5)
        return surf

img_empty = load_image(IMG_EMPTY)
img_red_piece = load_image(IMG_RED_PIECE)
img_yellow_piece = load_image(IMG_YELLOW_PIECE)

# DRAW BOARD
def draw_board(board):
    """Draws the current board state with images."""
    # Draw Board Background
    pygame.draw.rect(screen, BLUE, (0, TILE_SIZE, SCREEN_WIDTH, c4.ROW_COUNT * TILE_SIZE))

    for c in range(c4.COL_COUNT):
        for r in range(c4.ROW_COUNT):
            x = c * TILE_SIZE
            y = (r + 1) * TILE_SIZE  # offset by one tile for top row

            # Draw empty slot image
            screen.blit(img_empty, (x, y))

            # Draw pieces
            if board[r][c] == c4.PLAYER1_PIECE:
                screen.blit(img_red_piece, (x, y))
            elif board[r][c] == c4.PLAYER2_PIECE:
                screen.blit(img_yellow_piece, (x, y))

    pygame.display.update()

def display_message(message, color):
    """Display a win message across the top of the screen."""
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, TILE_SIZE))
    label = font.render(message, True, color)
    text_rect = label.get_rect(center=(SCREEN_WIDTH // 2, TILE_SIZE // 2))
    screen.blit(label, text_rect)
    pygame.display.update()

# MAIN GAME LOOP
def main():
    board = c4.position()
    
    # Determine turn based on board state (from text file)
    turn = board.get_starting_turn()
    
    game_over = False

    draw_board(board.get_board())

    while True:
        is_p1_turn = (turn == 0)
        current_piece = c4.PLAYER1_PIECE if is_p1_turn else c4.PLAYER2_PIECE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse movement preview
            if event.type == pygame.MOUSEMOTION and not game_over:
                pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, TILE_SIZE))
                posx = event.pos[0]
                img = img_red_piece if is_p1_turn else img_yellow_piece
                screen.blit(img, (posx - TILE_SIZE // 2, 0))
                pygame.display.update()

            # Handle click
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, TILE_SIZE))
                posx = event.pos[0]
                
                # Integer division to get column
                col = int(posx // TILE_SIZE)

                if board.is_valid_location(col):
                    board.drop_piece(col, current_piece)
                    draw_board(board.get_board())

                    # WIN CHECK
                    if board.winning_move(current_piece):
                        color = RED if is_p1_turn else YELLOW
                        msg = "Player 1 Wins!" if is_p1_turn else "Player 2 Wins!"
                        display_message(msg, color)
                        game_over = True
                        # Optional: wait and exit
                        pygame.time.wait(3000)
                        pygame.quit()
                        sys.exit()

                    # Switch turns
                    turn = (turn + 1) % 2

        pygame.display.update()


if __name__ == "__main__":
    main()