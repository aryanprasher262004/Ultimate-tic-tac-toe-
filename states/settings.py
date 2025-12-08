
import pygame
import config
from config import *
from ui.button import Button

class SettingsState:
    def __init__(self, game):
        self.game = game
        self.back_button = None
        self.sfx_button = None
        self.vol_up_button = None
        self.vol_down_button = None
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_NORMAL)

    def enter(self):
        center_x = SCREEN_WIDTH // 2
        start_y = 250
        gap = 80

        # SFX Toggle Button
        sfx_text = "SFX: ON" if config.SFX_ENABLED else "SFX: OFF"
        color = GREEN if config.SFX_ENABLED else RED
        self.sfx_button = Button(center_x - 120, start_y, 240, 60, sfx_text, self.font, bg_color=color, sound_path=CLICK_SOUND_PATH)

        # Volume Controls
        self.vol_down_button = Button(center_x - 150, start_y + gap, 60, 60, "-", self.font, bg_color=GRAY, sound_path=CLICK_SOUND_PATH)
        self.vol_up_button = Button(center_x + 90, start_y + gap, 60, 60, "+", self.font, bg_color=GRAY, sound_path=CLICK_SOUND_PATH)

        self.back_button = Button(center_x - 100, 500, 200, 60, "Back", self.font, bg_color=GRAY, sound_path=CLICK_SOUND_PATH)

    def exit(self):
        pass

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            self.game.change_state("home")
            
        elif self.sfx_button.handle_event(event):
            config.SFX_ENABLED = not config.SFX_ENABLED
            # Update button appearance immediately
            self.sfx_button.text = "SFX: ON" if config.SFX_ENABLED else "SFX: OFF"
            self.sfx_button.bg_color = GREEN if config.SFX_ENABLED else RED
            
        elif self.vol_up_button.handle_event(event):
            if config.MUSIC_VOLUME < 1.0:
                config.MUSIC_VOLUME = min(1.0, config.MUSIC_VOLUME + 0.1)
                pygame.mixer.music.set_volume(config.MUSIC_VOLUME)
                
        elif self.vol_down_button.handle_event(event):
            if config.MUSIC_VOLUME > 0.0:
                config.MUSIC_VOLUME = max(0.0, config.MUSIC_VOLUME - 0.1)
                pygame.mixer.music.set_volume(config.MUSIC_VOLUME)

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(DARK_GRAY)
        
        # Title
        title_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_TITLE)
        title_surf = title_font.render("Settings", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(title_surf, title_rect)

        # Volume Display
        vol_text = f"Music Volume: {int(config.MUSIC_VOLUME * 100)}%"
        vol_surf = self.font.render(vol_text, True, WHITE)
        vol_rect = vol_surf.get_rect(center=(SCREEN_WIDTH // 2, 330 + 30)) # Aligned with buttons row
        surface.blit(vol_surf, vol_rect)

        self.sfx_button.draw(surface)
        self.vol_down_button.draw(surface)
        self.vol_up_button.draw(surface)
        self.back_button.draw(surface)
