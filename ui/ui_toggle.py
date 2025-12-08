import pygame
from ui.tween import tweener
import config
from config import COLORS
from engine.sound_manager import sound

class UIToggle:
    def __init__(self, x, y, w, h, initial_value, on_toggle, style="neon"):
        self.rect = pygame.Rect(x, y, w, h)
        self.value = initial_value
        self.on_toggle = on_toggle
        self.style = style
        
        # Knob Animation
        self.knob_x_off = 1.0 if self.value else 0.0
        
        # RGB Animation
        self.hue = 0.0

    def update(self, dt):
        self.hue = (self.hue + dt * 100) % 360

    def toggle(self):
        self.value = not self.value
        target = 1.0 if self.value else 0.0
        tweener.add(self, "knob_x_off", self.knob_x_off, target, 200, "ease_out")
        if self.on_toggle:
            self.on_toggle(self.value)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                sound.play("click")
                self.toggle()
                return True
        return False

    def draw(self, surface):
        # Draw background pill
        bg_col = (50, 50, 50)
        
        alpha = 255
        
        if self.style == "neon":
            if self.value: 
                bg_col = COLORS["glow_purple"]
            else:
                bg_col = (40, 40, 40)
        elif self.style == "minimal":
            if self.value: bg_col = (220, 220, 220)
            else: bg_col = (80, 80, 80)
        elif self.style == "rgb":
            if self.value:
                c = pygame.Color(0,0,0)
                c.hsva = (self.hue, 100, 100, 100)
                bg_col = (c.r, c.g, c.b)
            else:
                 bg_col = (40, 40, 40)

        pygame.draw.rect(surface, bg_col, self.rect, border_radius=self.rect.height//2)
        
        # Draw Knob
        pad = 4
        knob_size = self.rect.height - pad * 2
        start_x = self.rect.x + pad
        end_x = self.rect.right - pad - knob_size
        
        curr_x = start_x + (end_x - start_x) * self.knob_x_off
        knob_rect = pygame.Rect(curr_x, self.rect.y + pad, knob_size, knob_size)
        
        knob_col = (255, 255, 255)
        if self.style == "minimal" and not self.value: knob_col = (180, 180, 180)
        
        pygame.draw.ellipse(surface, knob_col, knob_rect)
