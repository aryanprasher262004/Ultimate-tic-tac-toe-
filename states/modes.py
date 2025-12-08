
import pygame
import os
import config
from config import *
from ui.ui_button import UIButton
from ui.mode_button import ModeButton
from engine.save_manager import save_settings

class ModesState:
    def __init__(self, game):
        self.game = game
        self.mode_buttons = []
        self.back_button = None
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
        
        if self.bg_original:
            self.bg_scaled = pygame.transform.scale(self.bg_original, (w, h))
        else:
            self.bg_scaled = None

        # Layout for mode buttons
        start_y = 180
        button_width = 280
        button_height = 70
        gap = 30  # Increased padding between buttons
        
        # Left column: Player modes
        left_x = center_x - button_width - gap // 2
        
        # Right column: Time modes
        right_x = center_x + gap // 2
        
        # Callbacks for player modes
        def set_mode_self():
            config.GAME_MODE = "self"
            print(f"Mode set to: {config.GAME_MODE}") 
            save_settings()

        def set_mode_ai():
            config.GAME_MODE = "computer"
            print(f"Mode set to: {config.GAME_MODE}")
            save_settings()
        
        # Callbacks for time modes
        def set_time_classic():
            config.GAME_TIME_MODE = "classic"
            save_settings()
        
        def set_time_3m():
            config.GAME_TIME_MODE = "3m"
            save_settings()
        
        def set_time_5m():
            config.GAME_TIME_MODE = "5m"
            save_settings()
        
        def set_time_10m():
            config.GAME_TIME_MODE = "10m"
            save_settings()
        
        def go_back():
            self.game.change_state("home")

        # Create mode buttons
        self.mode_buttons = [
            # Time mode buttons (right column)
            ModeButton(right_x, start_y, button_width, button_height, 
                      "Classic Mode", "classic", set_time_classic, show_clock=False),
            ModeButton(right_x, start_y + (button_height + gap), button_width, button_height,
                      "3-Minute Blitz", "3m", set_time_3m, show_clock=True),
            ModeButton(right_x, start_y + (button_height + gap) * 2, button_width, button_height,
                      "5-Minute Rapid", "5m", set_time_5m, show_clock=True),
            ModeButton(right_x, start_y + (button_height + gap) * 3, button_width, button_height,
                      "10-Minute Classic", "10m", set_time_10m, show_clock=True),
        ]
        
        # Player mode buttons (left column) - using regular UIButton
        self.player_buttons = [
            UIButton(left_x, start_y, button_width, button_height, "Play vs Self", set_mode_self),
            UIButton(left_x, start_y + (button_height + gap), button_width, button_height, 
                    "Play vs Computer", set_mode_ai),
        ]
        
        # Back button at bottom
        self.back_button = UIButton(center_x - 100, h - 100, 200, 60, "Back", go_back)

    def exit(self):
        pass

    def handle_event(self, event):
        self.back_button.handle_event(event)
        for btn in self.player_buttons:
            btn.handle_event(event)
        for btn in self.mode_buttons:
            btn.handle_event(event)

    def update(self):
        self.back_button.update()
        for btn in self.player_buttons:
            btn.update()
        
        dt = self.game.clock.get_time() / 1000.0
        for btn in self.mode_buttons:
            btn.update(dt)

    def draw(self, surface):
        if self.bg_scaled:
            surface.blit(self.bg_scaled, (0, 0))
        else:
            surface.fill(COLORS["bg_dark"])
        
        w = surface.get_width()
        
        # Title
        title_font = pygame.font.Font(FONTS["bold"], 56)
        title_surf = title_font.render("Game Modes", True, COLORS["white"])
        title_rect = title_surf.get_rect(center=(w // 2, 80))
        surface.blit(title_surf, title_rect)

        # Section labels
        label_font = pygame.font.Font(FONTS["semi"], 32)
        
        # Player mode label
        player_label = label_font.render("Player Mode", True, COLORS["glow_cyan"])
        surface.blit(player_label, (w // 2 - 280 - 20 // 2, 140))
        
        # Time mode label
        time_label = label_font.render("Time Control", True, COLORS["glow_yellow"])
        surface.blit(time_label, (w // 2 + 20 // 2, 140))

        # Current selections display
        info_font = pygame.font.Font(FONTS["regular"], 24)
        player_mode_text = "Vs Self" if config.GAME_MODE == "self" else "Vs Computer"
        time_mode_map = {
            "classic": "No Timer",
            "3m": "3 Minutes",
            "5m": "5 Minutes",
            "10m": "10 Minutes"
        }
        time_mode_text = time_mode_map.get(config.GAME_TIME_MODE, "No Timer")
        
        info_text = f"Selected: {player_mode_text} • {time_mode_text}"
        info_surf = info_font.render(info_text, True, COLORS["glow_purple"])  # Changed to vibrant purple
        info_rect = info_surf.get_rect(center=(w // 2, surface.get_height() - 130))
        surface.blit(info_surf, info_rect)

        # Draw buttons
        for btn in self.player_buttons:
            btn.draw(surface)
        for btn in self.mode_buttons:
            btn.draw(surface)
        self.back_button.draw(surface)
