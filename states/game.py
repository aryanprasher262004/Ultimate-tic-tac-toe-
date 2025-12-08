
import pygame
import config
from config import *
from ui.button import Button

class GameState:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_NORMAL)
        self.small_font = pygame.font.SysFont(FONT_NAME, 20)
        self.back_button = None
        
        # Board Dimensions
        self.board_size = 450
        self.cell_size = self.board_size // 9
        self.big_cell_size = self.board_size // 3
        # Center the board
        self.start_x = (SCREEN_WIDTH - self.board_size) // 2
        self.start_y = (SCREEN_HEIGHT - self.board_size) // 2 + 20 

        # Dummy scores for UI demo
        self.x_wins = 0
        self.o_wins = 0
        self.current_turn = "X" 

    def enter(self):
        self.back_button = Button(10, 10, 100, 40, "Menu", self.small_font, bg_color=GRAY, sound_path=CLICK_SOUND_PATH)

    def exit(self):
        pass

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            self.game.change_state("home")
            
        # Placeholder for click logic
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(COLOR_BG)
        
        self.draw_board(surface)
        self.draw_ui(surface)
        
        self.back_button.draw(surface)

    def draw_board(self, surface):
        # 1. Draw Small Grid (Internal lines)
        for row in range(9):
            for col in range(9):
                rect = pygame.Rect(
                    self.start_x + col * self.cell_size,
                    self.start_y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                # Using width=1 for thin lines
                pygame.draw.rect(surface, COLOR_SMALL_BORDER, rect, 1)

        # 2. Draw Big Grid (Thick lines) - divides the 9x9 into 3x3 big cells
        for i in range(4):
            # Vertical lines
            start_pos_v = (self.start_x + i * self.big_cell_size, self.start_y)
            end_pos_v = (self.start_x + i * self.big_cell_size, self.start_y + self.board_size)
            pygame.draw.line(surface, COLOR_BIG_BORDER, start_pos_v, end_pos_v, 5)
            
            # Horizontal lines
            start_pos_h = (self.start_x, self.start_y + i * self.big_cell_size)
            end_pos_h = (self.start_x + self.board_size, self.start_y + i * self.big_cell_size)
            pygame.draw.line(surface, COLOR_BIG_BORDER, start_pos_h, end_pos_h, 5)

    def draw_ui(self, surface):
        # Turn Indicator (Center Top)
        turn_text = f"{self.current_turn}'s Turn"
        turn_color = COLOR_X if self.current_turn == "X" else COLOR_O
        turn_surf = self.font.render(turn_text, True, turn_color)
        turn_rect = turn_surf.get_rect(center=(SCREEN_WIDTH // 2, 40))
        surface.blit(turn_surf, turn_rect)

        # Player 1 (Left Side)
        p1_text = "Player 1"
        p1_symbol = "(X)"
        # Highlight if it's X's turn
        p1_color = COLOR_X if self.current_turn == "X" else WHITE
        
        p1_surf = self.font.render(p1_text, True, p1_color)
        p1_sym_surf = self.font.render(p1_symbol, True, COLOR_X)
        
        surface.blit(p1_surf, (20, 150))
        surface.blit(p1_sym_surf, (20, 190))
        
        score_x_surf = self.small_font.render(f"Wins: {self.x_wins}", True, WHITE)
        surface.blit(score_x_surf, (20, 230))

        # Player 2 / Computer (Right Side)
        p2_name = "Computer" if config.GAME_MODE == "computer" else "Player 2"
        p2_symbol = "(O)"
        # Highlight if it's O's turn
        p2_color = COLOR_O if self.current_turn == "O" else WHITE
        
        p2_surf = self.font.render(p2_name, True, p2_color)
        p2_sym_surf = self.font.render(p2_symbol, True, COLOR_O)
        
        p2_rect = p2_surf.get_rect(topright=(SCREEN_WIDTH - 20, 150))
        p2_sym_rect = p2_sym_surf.get_rect(topright=(SCREEN_WIDTH - 20, 190))
        
        surface.blit(p2_surf, p2_rect)
        surface.blit(p2_sym_surf, p2_sym_rect)

        score_o_surf = self.small_font.render(f"Wins: {self.o_wins}", True, WHITE)
        score_o_rect = score_o_surf.get_rect(topright=(SCREEN_WIDTH - 20, 230))
        surface.blit(score_o_surf, score_o_rect)
