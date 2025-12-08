
import pygame
import os
import config
from config import *
from ui.ui_button import UIButton
from engine.save_manager import save_settings

class ModesState:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.font = pygame.font.Font(FONTS["regular"], FONT_SIZE_NORMAL)
        
        self.bg_original = None
        self.bg_scaled = None
        if os.path.exists(MODES_BACKGROUND_IMAGE_PATH):
            try:
                self.bg_original = pygame.image.load(MODES_BACKGROUND_IMAGE_PATH)
            except:
                pass

    def enter(self):
        w, h = self.game.screen.get_size()
        center_x = w // 2
        start_y = 200
        
        if self.bg_original:
            self.bg_scaled = pygame.transform.scale(self.bg_original, (w, h))
        else:
            self.bg_scaled = None
        gap = 80

        def set_mode_self():
            config.GAME_MODE = "self"
            print(f"Mode set to: {config.GAME_MODE}") 
            save_settings()

        def set_mode_ai():
            config.GAME_MODE = "computer"
            print(f"Mode set to: {config.GAME_MODE}")
            save_settings()

        def go_back():
            self.game.change_state("home")

        # Note: UIButton currently standardizes color. If we want coloring (Blue/Magenta) we'd need to extend UIButton or stick to the theme.
        # Strict PROMPT guidelines suggest using the provided component as is. I'll stick to the modern theme colors.
        
        self.buttons = [
            UIButton(center_x - 120, start_y, 240, 60, "Play vs Self", set_mode_self),
            UIButton(center_x - 120, start_y + gap, 240, 60, "Play vs Computer", set_mode_ai),
            UIButton(center_x - 120, start_y + gap * 2.5, 240, 60, "Back", go_back)
        ]

    def exit(self):
        pass

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def update(self):
        for btn in self.buttons:
            btn.update()

    def draw(self, surface):
        if self.bg_scaled:
            surface.blit(self.bg_scaled, (0, 0))
        else:
            surface.fill(COLORS["bg_dark"])
        
        w = surface.get_width()
        
        # Title
        title_font = pygame.font.Font(FONTS["bold"], FONT_SIZE_TITLE)
        title_surf = title_font.render("Select Mode", True, COLORS["white"])
        title_rect = title_surf.get_rect(center=(w // 2, 100))
        surface.blit(title_surf, title_rect)

        # Current Mode Display
        mode_text = f"Current Mode: {'Vs Self' if config.GAME_MODE == 'self' else 'Vs Computer'}"
        mode_surf = self.font.render(mode_text, True, COLORS["glow_yellow"])
        mode_rect = mode_surf.get_rect(center=(w // 2, 160))
        surface.blit(mode_surf, mode_rect)

        # Buttons
        for btn in self.buttons:
            btn.draw(surface)
