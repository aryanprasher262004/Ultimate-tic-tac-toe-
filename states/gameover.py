
import pygame
from config import *
from ui.button import Button

class GameOverState:
    def __init__(self, game):
        self.game = game
        self.menu_button = None
        self.restart_button = None
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_NORMAL)

    def enter(self):
        center_x = SCREEN_WIDTH // 2
        start_y = 350
        gap = 80

        self.restart_button = Button(center_x - 100, start_y, 200, 60, "Rematch", self.font, bg_color=GREEN)
        self.menu_button = Button(center_x - 100, start_y + gap, 200, 60, "Main Menu", self.font, bg_color=BLUE)

    def exit(self):
        pass

    def handle_event(self, event):
        if self.restart_button.handle_event(event):
            self.game.change_state("game")
        elif self.menu_button.handle_event(event):
            self.game.change_state("home")

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(DARK_GRAY) # Overlay effect?
        
        title_font = pygame.font.SysFont(FONT_NAME, 80, bold=True)
        text = f"{self.game.winner} Wins!" if self.game.winner else "It's a Draw!"
        color = YELLOW if self.game.winner else WHITE
        
        text_surf = title_font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))
        surface.blit(text_surf, text_rect)

        self.restart_button.draw(surface)
        self.menu_button.draw(surface)
