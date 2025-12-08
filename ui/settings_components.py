import pygame
import config
from config import COLORS
from engine.sound_manager import sound
from engine.themes import theme_manager

class ThemeCard:
    def __init__(self, x, y, w, h, theme_name, on_select):
        self.rect = pygame.Rect(x, y, w, h)
        self.theme_name = theme_name
        self.on_select = on_select
        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                sound.play("click")
                self.on_select(self.theme_name)
                return True
        return False

    def draw(self, surface):
        # Draw Card BG
        is_selected = (theme_manager.current_theme_name == self.theme_name)
        
        # Determine local colors from the theme without switching global theme
        thm = theme_manager.themes[self.theme_name]
        bg_col = thm.get_color("bg_color")
        grid_col = thm.get_color("small_grid_color")
        
        # Card Border
        border_col = (100, 100, 100)
        border_width = 2
        
        if is_selected:
            border_col = COLORS["glow_blue"]
            border_width = 4
            # Glow effect
            glow_surf = pygame.Surface((self.rect.width+20, self.rect.height+20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*COLORS["glow_blue"], 80), glow_surf.get_rect(), border_radius=12)
            surface.blit(glow_surf, (self.rect.x-10, self.rect.y-10))
        elif self.hover:
            border_col = (200, 200, 200)

        # Draw content
        pygame.draw.rect(surface, bg_col, self.rect, border_radius=8)
        pygame.draw.rect(surface, border_col, self.rect, border_width, border_radius=8)
        
        # Draw Mini Grid (Hash symbol style)
        margin = 15
        area_size = self.rect.width - margin*2
        cell_size = area_size // 3
        start_x = self.rect.x + margin
        start_y = self.rect.y + margin # Offset
        
        # Draw lines
        if self.theme_name == "RGB_GAMER":
             grid_col = (255, 0, 0) # Fallback / Static
             
        for i in range(4):
            # Vertical
            pygame.draw.line(surface, grid_col, (start_x + i*cell_size, start_y), (start_x + i*cell_size, start_y + area_size), 2)
            # Horizontal
            pygame.draw.line(surface, grid_col, (start_x, start_y + i*cell_size), (start_x + area_size, start_y + i*cell_size), 2)

        # Draw Title
        font = pygame.font.SysFont("arial", 16, bold=True)
        text = font.render(self.theme_name, True, (255, 255, 255))
        surface.blit(text, (self.rect.centerx - text.get_width()//2, self.rect.bottom - 25))


class SymbolButton:
    def __init__(self, x, y, size, symbol, on_select):
        self.rect = pygame.Rect(x, y, size, size)
        self.symbol = symbol # "X", "O", "✓"
        self.on_select = on_select
        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                sound.play("click")
                self.on_select(self.symbol)
                return True
        return False
        
    def draw(self, surface):
        is_selected = (config.PLAYER_SYMBOL == self.symbol)
        
        center = self.rect.center
        radius = self.rect.width // 2
        
        # Color Logic
        bg_col = (30, 30, 40)
        border_col = (100, 100, 100)
        width = 2
        
        if is_selected:
            border_col = COLORS["glow_green"] if self.symbol == "✓" else COLORS["glow_blue"]
            width = 4
            # Glow
            glow_surf = pygame.Surface((self.rect.width+20, self.rect.height+20), pygame.SRCALPHA)
            c = border_col
            pygame.draw.circle(glow_surf, (*c, 80), (glow_surf.get_width()//2, glow_surf.get_height()//2), radius+5)
            surface.blit(glow_surf, (self.rect.x-10, self.rect.y-10))

        elif self.hover:
             border_col = (200, 200, 200)

        pygame.draw.circle(surface, bg_col, center, radius)
        pygame.draw.circle(surface, border_col, center, radius, width)
        
        # Draw Symbol
        font = pygame.font.SysFont("arial", 28, bold=True)
        txt = self.symbol
        tsurf = font.render(txt, True, (255, 255, 255))
        surface.blit(tsurf, tsurf.get_rect(center=center))
