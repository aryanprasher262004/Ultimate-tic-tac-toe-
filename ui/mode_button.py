import pygame
from ui.tween import tweener
import config
from config import COLORS
from engine.sound_manager import sound

class ModeButton:
    """
    Custom button for mode selection with:
    - Highlight glow for selected mode
    - Dimming for non-selected modes
    - Press bounce animation
    - Optional clock icon for timed modes
    """
    def __init__(self, x, y, w, h, text, mode_value, on_click, show_clock=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.mode_value = mode_value
        self.on_click = on_click
        self.show_clock = show_clock
        
        # Animation properties
        self.scale = 1.0
        self.glow_intensity = 0.0
        self.hover = False
        
        # Font
        try:
            self.font = pygame.font.Font(config.FONTS["semi"], 28)
        except:
            self.font = pygame.font.SysFont("arial", 28, bold=True)
    
    def is_selected(self):
        """Check if this mode is currently selected"""
        return config.GAME_TIME_MODE == self.mode_value
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                sound.play("click")
                # Bounce animation
                tweener.add(self, "scale", 1.0, 0.9, 80, "ease_out", callback=lambda: self.bounce_back())
                self.on_click()
                return True
        return False
    
    def bounce_back(self):
        """Bounce back animation after press"""
        tweener.add(self, "scale", 0.9, 1.0, 150, "elastic_out")
    
    def update(self, dt):
        """Update glow animation for selected mode"""
        if self.is_selected():
            # Pulse glow for selected mode
            self.glow_intensity = 0.5 + 0.5 * abs(pygame.time.get_ticks() % 2000 - 1000) / 1000
    
    def draw(self, surface):
        # Calculate scaled rect
        w = self.rect.width * self.scale
        h = self.rect.height * self.scale
        cx, cy = self.rect.center
        draw_rect = pygame.Rect(cx - w/2, cy - h/2, w, h)
        
        is_selected = self.is_selected()
        
        # Draw glow for selected mode
        if is_selected:
            glow_size = 15
            glow_surf = pygame.Surface((int(w + glow_size*2), int(h + glow_size*2)), pygame.SRCALPHA)
            alpha = int(100 * self.glow_intensity)
            pygame.draw.rect(glow_surf, (*COLORS["glow_cyan"], alpha), glow_surf.get_rect(), border_radius=15)
            surface.blit(glow_surf, (draw_rect.x - glow_size, draw_rect.y - glow_size))
        
        # Background color
        if is_selected:
            bg_color = COLORS["btn_hover"]
            border_color = COLORS["glow_cyan"]
            border_width = 3
        elif self.hover:
            bg_color = (60, 60, 70)
            border_color = (150, 150, 150)
            border_width = 2
        else:
            bg_color = (40, 40, 50)  # Dimmed
            border_color = (80, 80, 80)
            border_width = 1
        
        # Draw button background
        pygame.draw.rect(surface, bg_color, draw_rect, border_radius=12)
        pygame.draw.rect(surface, border_color, draw_rect, border_width, border_radius=12)
        
        # Draw clock icon for timed modes (centered above text)
        if self.show_clock:
            icon_x = draw_rect.centerx
            icon_y = draw_rect.centery - 8  # Slightly above center
            self.draw_clock_icon(surface, icon_x, icon_y, 12, COLORS["glow_yellow"])
        
        # Draw text
        text_color = COLORS["white"] if is_selected or self.hover else (150, 150, 150)
        text_surf = self.font.render(self.text, True, text_color)
        
        # Position text centered (or slightly below if clock is shown)
        text_y_offset = 12 if self.show_clock else 0
        text_rect = text_surf.get_rect(center=(draw_rect.centerx, draw_rect.centery + text_y_offset))
        surface.blit(text_surf, text_rect)
    
    def draw_clock_icon(self, surface, x, y, radius, color):
        """Draw a simple clock icon"""
        # Circle
        pygame.draw.circle(surface, color, (int(x), int(y)), radius, 2)
        # Hour hand
        pygame.draw.line(surface, color, (x, y), (x, y - radius * 0.6), 2)
        # Minute hand
        pygame.draw.line(surface, color, (x, y), (x + radius * 0.5, y - radius * 0.3), 2)
