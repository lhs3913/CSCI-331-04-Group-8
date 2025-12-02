# Filename: connect4_gui.py
# Requires: ./Resources/art/*.png
# Works with: connect4_board.py, alphabeta.py, heuristic.py

import pygame
import sys
import os
import connect4_board as c4
import alphabeta as ab
import heuristic as h
import time

# --- CONFIGURATION ---
TILE_SIZE = 100
SIDEBAR_WIDTH = 250
BOTTOM_BAR_HEIGHT = 100
BOARD_DIR = "./Resources/boards/valid_boards/"

# Board dimensions
BOARD_COLS = c4.COL_COUNT
BOARD_ROWS = c4.ROW_COUNT

# Window dimensions
GAME_WIDTH = BOARD_COLS * TILE_SIZE
GAME_HEIGHT = (BOARD_ROWS + 1) * TILE_SIZE 
SCREEN_WIDTH = SIDEBAR_WIDTH + GAME_WIDTH
SCREEN_HEIGHT = GAME_HEIGHT + BOTTOM_BAR_HEIGHT

# COLORS
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
RED = (200, 0, 0)
YELLOW = (200, 200, 0)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (100, 149, 237)

# Art file paths
ART_PATH = "./Resources/art/"
IMG_EMPTY = ART_PATH + "empty connect 4-export.png"
IMG_RED_PIECE = ART_PATH + "red piece-export.png"
IMG_YELLOW_PIECE = ART_PATH + "yellow piece-export.png"

# INITIALIZE PYGAME
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect 4 - AI Project")
font_large = pygame.font.SysFont("arial", 35, bold=True)
font_medium = pygame.font.SysFont("arial", 28, bold=True)
font_small = pygame.font.SysFont("arial", 20, bold=True)
font_score = pygame.font.SysFont("arial", 50, bold=True)

# LOAD IMAGES
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

# --- DROPDOWN CLASS ---
class Dropdown:
    def __init__(self, x, y, w, h, main_color, text_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.main_color = main_color
        self.text_color = text_color
        self.options = self.get_files()
        self.is_open = False
        self.item_height = 40
        
        # Set default selection to 'blank board.txt' if it exists
        try:
            self.selected_index = self.options.index("blank board.txt")
        except ValueError:
            self.selected_index = 0
        
    def get_files(self):
        """Fetch .txt files from the board directory."""
        files = []
        if os.path.exists(BOARD_DIR):
            try:
                files = [f for f in os.listdir(BOARD_DIR) if f.endswith(".txt")]
            except OSError:
                pass
        
        if not files:
            return ["No Files"]
        return files

    def draw(self, surface):
        # Draw Main Box
        pygame.draw.rect(surface, self.main_color, self.rect, border_radius=5)
        
        # Text
        current_text = self.options[self.selected_index] if self.options else "No Files"
        if len(current_text) > 15: current_text = current_text[:12] + "..."
            
        txt_surf = font_small.render(current_text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)
        
        # Draw Arrow
        arrow = "v" if not self.is_open else "^"
        arrow_surf = font_small.render(arrow, True, self.text_color)
        surface.blit(arrow_surf, (self.rect.right - 20, self.rect.y + 10))

        # Draw Options if open
        if self.is_open:
            for i, option in enumerate(self.options):
                opt_rect = pygame.Rect(self.rect.x, self.rect.bottom + (i * self.item_height), self.rect.width, self.item_height)
                
                # Hover effect
                mouse_pos = pygame.mouse.get_pos()
                color = DARK_GRAY
                if opt_rect.collidepoint(mouse_pos):
                    color = GRAY
                
                pygame.draw.rect(surface, color, opt_rect)
                pygame.draw.rect(surface, WHITE, opt_rect, 1) # Border
                
                # Text
                opt_txt = option
                if len(opt_txt) > 15: opt_txt = opt_txt[:12] + "..."
                opt_surf = font_small.render(opt_txt, True, WHITE)
                surface.blit(opt_surf, (opt_rect.x + 10, opt_rect.y + 10))

    def handle_event(self, event):
        """
        Returns status code:
        0: No interaction
        1: Toggled Open/Close (Needs redraw)
        2: New Selection Made (Needs reset)
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If open, check clicks on options
            if self.is_open:
                for i, option in enumerate(self.options):
                    opt_rect = pygame.Rect(self.rect.x, self.rect.bottom + (i * self.item_height), self.rect.width, self.item_height)
                    if opt_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.is_open = False
                        return 2 # Selection made
            
            # Toggle Open/Close on main box click
            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open
                return 1 # Toggled (needs redraw)
            
            elif self.is_open:
                # Close if clicked outside
                self.is_open = False
                return 1 # Toggled Closed (needs redraw)
                
        return 0
    
    def get_selected_path(self):
        if not self.options or self.options[0] == "No Files":
            return "./Resources/boards/blank board.txt" # Hard fallback
            
        selected = self.options[self.selected_index]
        return os.path.join(BOARD_DIR, selected)

# --- GLOBAL STATE ---
p1_auto = False
p2_auto = False
game_paused = False
reset_trigger = False
DEPTH = 4 

# Create Dropdown Instance
board_selector = Dropdown(25, 450, 200, 40, LIGHT_BLUE, BLACK)

def map_score_to_simple_range(raw_score):
    if raw_score >= 90: return 2
    if raw_score >= 4: return 1   
    if raw_score > -4: return 0
    if raw_score > -90: return -1 
    return -2

def draw_sidebar(turn):
    """Draws the control panel on the left."""
    pygame.draw.rect(screen, GRAY, (0, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
    
    # Title
    title = font_medium.render("Controls", True, WHITE)
    screen.blit(title, (50, 20))

    # --- PLAYER 1 TOGGLE ---
    p1_color = RED if not p1_auto else (150, 0, 0)
    pygame.draw.rect(screen, p1_color, (25, 60, 200, 60), border_radius=10)
    
    status_text = "BOT" if p1_auto else "MANUAL"
    label_p1 = font_small.render(f"Player 1 (Red)", True, WHITE)
    state_p1 = font_medium.render(status_text, True, WHITE)
    screen.blit(label_p1, (40, 65))
    screen.blit(state_p1, (40, 90))

    # --- PLAYER 2 TOGGLE ---
    p2_color = YELLOW if not p2_auto else (200, 200, 100)
    text_color = BLACK if not p2_auto else WHITE
    pygame.draw.rect(screen, p2_color, (25, 130, 200, 60), border_radius=10)
    
    status_text_2 = "BOT" if p2_auto else "MANUAL"
    label_p2 = font_small.render(f"Player 2 (Yel)", True, text_color)
    state_p2 = font_medium.render(status_text_2, True, text_color)
    screen.blit(label_p2, (40, 135))
    screen.blit(state_p2, (40, 160))

    # --- PAUSE BUTTON ---
    pause_color = ORANGE if game_paused else (0, 150, 0)
    pause_text = "RESUME" if game_paused else "PAUSE"
    pygame.draw.rect(screen, pause_color, (25, 230, 200, 60), border_radius=10)
    lbl_pause = font_medium.render(pause_text, True, WHITE)
    text_rect = lbl_pause.get_rect(center=(125, 260))
    screen.blit(lbl_pause, text_rect)

    # --- RESTART BUTTON ---
    pygame.draw.rect(screen, (50, 50, 150), (25, 300, 200, 60), border_radius=10)
    lbl_restart = font_medium.render("RESTART", True, WHITE)
    text_rect_rst = lbl_restart.get_rect(center=(125, 330))
    screen.blit(lbl_restart, text_rect_rst)

    # --- FILE SELECTOR LABEL ---
    lbl_file = font_small.render("Load Board State:", True, WHITE)
    screen.blit(lbl_file, (25, 420))
    
    # --- INFO TEXT ---
    if game_paused:
        info_txt = "PAUSED"
    else:
        info_txt = "P1 Turn" if turn == 0 else "P2 Turn"
    
    info = font_large.render(info_txt, True, WHITE)
    screen.blit(info, (50, SCREEN_HEIGHT - 80))

def draw_heuristic_bar(board, current_piece):
    """Calculates and draws the simplified (-2 to +2) heuristic score."""
    pygame.draw.rect(screen, BLACK, (SIDEBAR_WIDTH, GAME_HEIGHT, GAME_WIDTH, BOTTOM_BAR_HEIGHT))
    
    for c in range(BOARD_COLS):
        x = SIDEBAR_WIDTH + (c * TILE_SIZE)
        y = GAME_HEIGHT + 10
        w = TILE_SIZE
        h_rect = BOTTOM_BAR_HEIGHT - 20

        score_text = ""
        color = GRAY
        
        if board.is_valid_location(c):
            temp_board = board.copy()
            temp_board.drop_piece(c, current_piece)
            raw_score = h.score_position(temp_board, current_piece)
            simple_score = map_score_to_simple_range(raw_score)
            score_text = f"{simple_score:+d}"

            if simple_score >= 1: color = GREEN
            elif simple_score <= -1: color = RED
            else: color = WHITE
        
            text_surf = font_score.render(score_text, True, color)
            text_rect = text_surf.get_rect(center=(x + w//2, y + h_rect//2))
            
            pygame.draw.rect(screen, (20, 20, 20), (x + 5, y, w - 10, h_rect), border_radius=5)
            screen.blit(text_surf, text_rect)
        else:
            pygame.draw.rect(screen, (20, 20, 20), (x + 5, y, w - 10, h_rect), border_radius=5)

def draw_board(board, turn):
    """Draws the main game board."""
    start_x = SIDEBAR_WIDTH
    pygame.draw.rect(screen, BLUE, (start_x, TILE_SIZE, GAME_WIDTH, BOARD_ROWS * TILE_SIZE))

    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS):
            x = start_x + (c * TILE_SIZE)
            y = (r + 1) * TILE_SIZE

            screen.blit(img_empty, (x, y))
            if board.get_board()[r][c] == c4.PLAYER1_PIECE:
                screen.blit(img_red_piece, (x, y))
            elif board.get_board()[r][c] == c4.PLAYER2_PIECE:
                screen.blit(img_yellow_piece, (x, y))
    
    current_piece = c4.PLAYER1_PIECE if turn == 0 else c4.PLAYER2_PIECE
    draw_heuristic_bar(board, current_piece)
    draw_sidebar(turn)
    
    # Draw Dropdown LAST so it appears on top
    board_selector.draw(screen)
    
    pygame.display.update()

def display_message(message, color):
    pygame.draw.rect(screen, BLACK, (SIDEBAR_WIDTH, 0, GAME_WIDTH, TILE_SIZE))
    label = font_large.render(message, True, color)
    text_rect = label.get_rect(center=(SIDEBAR_WIDTH + GAME_WIDTH // 2, TILE_SIZE // 2))
    screen.blit(label, text_rect)
    pygame.display.update()

def toggle_click(event):
    """Handle clicks on the sidebar."""
    global p1_auto, p2_auto, game_paused, reset_trigger
    
    # 1. Check Dropdown
    status = board_selector.handle_event(event)
    if status == 2: # Selection Made -> Reset
        c4.BOARD_FILE = board_selector.get_selected_path()
        reset_trigger = True
        return True
    elif status == 1: # Toggled -> Redraw Only
        return True

    # 2. Check Other Buttons
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        if x < SIDEBAR_WIDTH:
            # P1 (25, 60, 200, 60)
            if 25 <= x <= 225 and 60 <= y <= 120:
                p1_auto = not p1_auto
                return True
            # P2 (25, 130, 200, 60)
            if 25 <= x <= 225 and 130 <= y <= 190:
                p2_auto = not p2_auto
                return True
            # Pause (25, 230, 200, 60)
            if 25 <= x <= 225 and 230 <= y <= 290:
                game_paused = not game_paused
                return True
            # Restart (25, 300, 200, 60)
            if 25 <= x <= 225 and 300 <= y <= 360:
                reset_trigger = True
                return True
            
    return False

def main():
    global reset_trigger, game_paused
    
    # --- SET DEFAULT BOARD FILE ON STARTUP ---
    # We explicitly set the board file in c4 module to the one selected in the dropdown
    # The dropdown logic automatically selects "blank board.txt" if present.
    c4.BOARD_FILE = board_selector.get_selected_path()
    
    board = c4.position()
    turn = board.get_starting_turn()
    game_over = False

    draw_board(board, turn)

    while True:
        if reset_trigger:
            board = c4.position()
            turn = board.get_starting_turn()
            game_over = False
            reset_trigger = False
            game_paused = False 
            draw_board(board, turn)
            continue 

        is_p1 = (turn == 0)
        is_bot = ((is_p1 and p1_auto) or (not is_p1 and p2_auto)) and not game_paused
        current_piece = c4.PLAYER1_PIECE if is_p1 else c4.PLAYER2_PIECE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse Motion: Draw piece if on board, ERASE piece if on sidebar
            if event.type == pygame.MOUSEMOTION and not game_over and not is_bot and not game_paused:
                posx = event.pos[0]
                if posx > SIDEBAR_WIDTH: 
                    pygame.draw.rect(screen, BLACK, (SIDEBAR_WIDTH, 0, GAME_WIDTH, TILE_SIZE))
                    
                    img = img_red_piece if is_p1 else img_yellow_piece
                    draw_x = posx - TILE_SIZE // 2
                    screen.blit(img, (draw_x, 0))
                    pygame.display.update()
                else:
                    # Clear preview bar if mouse moves to sidebar
                    pygame.draw.rect(screen, BLACK, (SIDEBAR_WIDTH, 0, GAME_WIDTH, TILE_SIZE))
                    pygame.display.update()

            # Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if toggle_click(event):
                    draw_board(board, turn) 
                
                # Manual Move Logic
                elif not game_over and not is_bot and not game_paused and not board_selector.is_open:
                    posx = event.pos[0]
                    if posx > SIDEBAR_WIDTH:
                        col = int((posx - SIDEBAR_WIDTH) // TILE_SIZE)

                        if board.is_valid_location(col):
                            board.drop_piece(col, current_piece)
                            draw_board(board, turn)

                            if board.winning_move(current_piece):
                                msg = "Player 1 Wins!" if is_p1 else "Player 2 Wins!"
                                colr = RED if is_p1 else YELLOW
                                display_message(msg, colr)
                                game_over = True
                            elif board.tie_board():
                                display_message("Tie Game!", WHITE)
                                game_over = True
                            else:
                                turn = (turn + 1) % 2
                                draw_board(board, turn)

        if is_bot and not game_over and not game_paused and not board_selector.is_open:
            pygame.time.wait(500)
            
            # Show Thinking
            pygame.draw.rect(screen, BLACK, (SIDEBAR_WIDTH, 0, GAME_WIDTH, TILE_SIZE))
            lbl = font_large.render("AI Thinking...", True, WHITE)
            screen.blit(lbl, (SIDEBAR_WIDTH + 200, 20))
            pygame.display.update()

            result = ab.alphabeta(board, DEPTH, -float('inf'), float('inf'))
            board = result[1]
            draw_board(board, turn)

            if board.winning_move(current_piece):
                msg = "Player 1 (AI) Wins!" if is_p1 else "Player 2 (AI) Wins!"
                colr = RED if is_p1 else YELLOW
                display_message(msg, colr)
                game_over = True
            elif board.tie_board():
                display_message("Game Tie!", WHITE)
                game_over = True
            else:
                turn = (turn + 1) % 2
                draw_board(board, turn)

if __name__ == "__main__":
    main()