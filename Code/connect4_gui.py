# Filename: connect4_gui.py
# Requires: ./Resources/art/*.png
# Works with: connect4_board.py

import pygame
import sys
import numpy as np
import connect4_board as c4

# CONFIG
TILE_SIZE = 100
SCREEN_WIDTH = c4.COL_COUNT * TILE_SIZE
SCREEN_HEIGHT = (c4.ROW_COUNT + 1) * TILE_SIZE  # extra row for preview area

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
    img = pygame.image.load(path)
    return pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

img_empty = load_image(IMG_EMPTY)
img_red_piece = load_image(IMG_RED_PIECE)
img_yellow_piece = load_image(IMG_YELLOW_PIECE)

# DRAW BOARD
def draw_board(board):
    """Draws the current board state with images."""
    for c in range(c4.COL_COUNT):
        for r in range(c4.ROW_COUNT):
            x = c * TILE_SIZE
            y = (r + 1) * TILE_SIZE  # offset by one tile for top row

            # Draw empty slot
            screen.blit(img_empty, (x, y))

            # Draw pieces
            if board[r][c] == c4.PLAYER1_PIECE:
                screen.blit(img_red_piece, (x, y))
            elif board[r][c] == c4.PLAYER2_PIECE:
                screen.blit(img_yellow_piece, (x, y))

    pygame.display.update()


def display_message(message, color=(255, 255, 255)):
    """Display a win message across the top of the screen."""
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, TILE_SIZE))
    label = font.render(message, True, color)
    text_rect = label.get_rect(center=(SCREEN_WIDTH // 2, TILE_SIZE // 2))
    screen.blit(label, text_rect)
    pygame.display.update()


# MAIN GAME LOOP
def main():
    board = c4.position()
    turn = 0  # 0 = Player 1 (Red), 1 = Player 2 (Yellow)

    draw_board(board.get_board())
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse movement preview
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, TILE_SIZE))
                posx = event.pos[0]
                if turn == 0:
                    screen.blit(img_red_piece, (posx - TILE_SIZE // 2, 0))
                else:
                    screen.blit(img_yellow_piece, (posx - TILE_SIZE // 2, 0))
                pygame.display.update()

            # Handle click
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, TILE_SIZE))
                posx = event.pos[0]
                col = int(np.floor(posx / TILE_SIZE))

                if board.is_valid_location(col):
                    piece = c4.PLAYER1_PIECE if turn == 0 else c4.PLAYER2_PIECE
                    board.drop_piece(col, piece)

                    draw_board(board.get_board())

                    # WIN CHECK
                    if board.winning_move(piece):
                        color = (255, 0, 0) if piece == c4.PLAYER1_PIECE else (255, 255, 0)
                        message = "Player 1 (Red) Wins!" if piece == c4.PLAYER1_PIECE else "Player 2 (Yellow) Wins!"
                        display_message(message, color)
                        pygame.display.update()
                        pygame.time.wait(3000)
                        pygame.quit()
                        sys.exit()
                        break

                    # Switch turns
                    turn = (turn + 1) % 2

        pygame.display.update()


if __name__ == "__main__":
    main()