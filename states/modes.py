
import pygame
import config
from config import * # Import constants directly
from ui.button import Button

class ModesState:
    def __init__(self, game):
        self.game = game
        self.pvp_button = None
        self.ai_button = None
        self.back_button = None
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_NORMAL)

    def enter(self):
        center_x = SCREEN_WIDTH // 2
        start_y = 200
        gap = 80

        self.pvp_button = Button(center_x - 120, start_y, 240, 60, "Play vs Self", self.font, bg_color=BLUE, sound_path=CLICK_SOUND_PATH)
        self.ai_button = Button(center_x - 120, start_y + gap, 240, 60, "Play vs Computer", self.font, bg_color=MAGENTA, sound_path=CLICK_SOUND_PATH)
        self.back_button = Button(center_x - 120, start_y + gap * 2.5, 240, 60, "Back", self.font, bg_color=GRAY, sound_path=CLICK_SOUND_PATH)

    def exit(self):
        pass

    def handle_event(self, event):
        if self.pvp_button.handle_event(event):
            config.GAME_MODE = "self"
            # Optional: Add visual feedback or logic here
            print(f"Mode set to: {config.GAME_MODE}") 
        elif self.ai_button.handle_event(event):
            config.GAME_MODE = "computer"
            print(f"Mode set to: {config.GAME_MODE}")
        elif self.back_button.handle_event(event):
            self.game.change_state("home")

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(DARK_GRAY)
        
        # Title
        title_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_TITLE)
        title_surf = title_font.render("Select Mode", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(title_surf, title_rect)

        # Current Mode Display
        mode_text = f"Current Mode: {'Vs Self' if config.GAME_MODE == 'self' else 'Vs Computer'}"
        mode_surf = self.font.render(mode_text, True, YELLOW)
        mode_rect = mode_surf.get_rect(center=(SCREEN_WIDTH // 2, 160))
        surface.blit(mode_surf, mode_rect)

        # Buttons
        self.pvp_button.draw(surface)
        self.ai_button.draw(surface)
        self.back_button.draw(surface)
