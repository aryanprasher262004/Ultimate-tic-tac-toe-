
import pygame
from config import *

class Button:
    def __init__(self, x, y, width, height, text, font, text_color=BLACK, bg_color=GRAY, hover_color=WHITE, sound_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False
        self.sound = None
        if sound_path:
            try:
                self.sound = pygame.mixer.Sound(sound_path)
            except (pygame.error, FileNotFoundError):
                print(f"Warning: Could not load sound file {sound_path}")

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:
                if self.sound:
                    self.sound.play()
                return True
        return False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2) # Border

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
