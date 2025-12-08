
import pygame
import os
from config import *
from ui.button import Button

class HomeState:
    def __init__(self, game):
        self.game = game
        self.play_button = None
        self.modes_button = None
        self.settings_button = None
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_NORMAL)
        self.background_image = None
        
        # Load background if exists, otherwise None (will fill color)
        if os.path.exists(BACKGROUND_IMAGE_PATH):
            try:
                self.background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
                self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error:
                print(f"Failed to load background: {BACKGROUND_IMAGE_PATH}")

    def enter(self):
        """Called when entering this state"""
        center_x = SCREEN_WIDTH // 2
        start_y = 250
        gap = 80
        
        self.play_button = Button(center_x - 100, start_y, 200, 60, "Play", self.font, bg_color=GREEN, sound_path=CLICK_SOUND_PATH)
        self.modes_button = Button(center_x - 100, start_y + gap, 200, 60, "Modes", self.font, bg_color=BLUE, sound_path=CLICK_SOUND_PATH)
        self.settings_button = Button(center_x - 100, start_y + gap * 2, 200, 60, "Settings", self.font, bg_color=CYAN, sound_path=CLICK_SOUND_PATH)
        # Note: Quit button removed as per PROMPT 2 requirements, can be added back if requested

    def exit(self):
        """Called when exiting this state"""
        pass

    def handle_event(self, event):
        if self.play_button.handle_event(event):
            self.game.change_state("game")
        elif self.modes_button.handle_event(event):
            self.game.change_state("modes")
        elif self.settings_button.handle_event(event):
            self.game.change_state("settings")

    def update(self):
        pass

    def draw(self, surface):
        # Draw Background
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill(DARK_GRAY)
        
        # Title
        title_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_TITLE, bold=True)
        title_surf = title_font.render(SCREEN_TITLE, True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(title_surf, title_rect)

        # Buttons
        self.play_button.draw(surface)
        self.modes_button.draw(surface)
        self.settings_button.draw(surface)
