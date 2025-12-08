import pygame
import config
from config import * 
from engine.sound_manager import sound
from ui.tween import tweener

class UIButton:
    def __init__(self, x, y, w, h, text, onclick, sound_path=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.onclick = onclick
        
        # State
        self.is_hovered = False
        self.is_pressed = False
        
        # Animation Properties
        self.scale = 1.0
        self.glow_opacity = 0.0
        
        # Font
        try:
            self.font = pygame.font.Font(FONTS["semi"], 32)
        except:
             self.font = pygame.font.SysFont("arial", 32, bold=True)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            is_inside = self.rect.collidepoint(event.pos)
            if is_inside and not self.is_hovered:
                self.on_enter()
            elif not is_inside and self.is_hovered:
                self.on_leave()
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_press()
                return True # Captured

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed:
                self.on_release()
                # Check if still inside to trigger click
                if self.rect.collidepoint(event.pos):
                    sound.play("click")
                    if self.onclick:
                         self.onclick()
                return True
        return False

    def update(self):
        # Tweener updates globally, so no local update logic needed
        # Unless we want to poll mouse if events aren't passed (safety)
        # But handle_event should suffice.
        pass

    def on_enter(self):
        self.is_hovered = True
        tweener.add(self, "glow_opacity", self.glow_opacity, 180, 200, "ease_out")
        tweener.add(self, "scale", self.scale, 1.05, 200, "ease_out")

    def on_leave(self):
        self.is_hovered = False
        self.is_pressed = False # Safety reset
        tweener.add(self, "glow_opacity", self.glow_opacity, 0, 200, "ease_out")
        tweener.add(self, "scale", self.scale, 1.0, 200, "ease_out")

    def on_press(self):
        self.is_pressed = True
        tweener.add(self, "scale", self.scale, 0.95, 80, "ease_out")

    def on_release(self):
        self.is_pressed = False
        tweener.add(self, "scale", self.scale, 1.0, 300, "elastic_out")

    def draw(self, surface):
        # Center scaling around self.rect.center
        w = self.rect.width * self.scale
        h = self.rect.height * self.scale
        cx, cy = self.rect.center
        
        # 1. Draw Glow/Shadow Bloom
        if self.glow_opacity > 1:
            glow_surf = pygame.Surface((int(w + 10), int(h + 10)), pygame.SRCALPHA)
            alpha = int(self.glow_opacity)
            # Make a soft colored glow
            # Using glow_blue from config or a cyan
            c = COLORS.get("glow_blue", (0, 255, 255))
            pygame.draw.rect(glow_surf, (*c, alpha), glow_surf.get_rect(), border_radius=16)
            
            # Blit centered
            surface.blit(glow_surf, (cx - glow_surf.get_width()//2, cy - glow_surf.get_height()//2), special_flags=pygame.BLEND_RGBA_ADD)

        # 2. Draw Button Body
        # Create temp surface for button to allow scale without artifacts or re-generation?
        # Drawing primitives dynamicly is better for quality
        
        btn_rect = pygame.Rect(0, 0, int(w), int(h))
        # Center rect calculation for direct draw
        draw_x = cx - w/2
        draw_y = cy - h/2
        draw_rect = pygame.Rect(draw_x, draw_y, w, h)
        
        # Color transition based on hover/press?
        # Basic Modern Style: Dark bg, Bright Border
        # Or standard config colors.
        bg_color = COLORS["btn_hover"] if self.is_hovered else COLORS["btn_idle"]
        if self.is_pressed: bg_color = (max(0, bg_color[0]-30), max(0, bg_color[1]-30), max(0, bg_color[2]-30))
        
        pygame.draw.rect(surface, bg_color, draw_rect, border_radius=12)
        
        # 3. Border Highlight
        border_color = (255, 255, 255) if self.is_hovered else (100, 100, 100)
        pygame.draw.rect(surface, border_color, draw_rect, 2, border_radius=12)

        # 4. Text
        # Scale text? typically yes
        # Re-render font? Expensive if every frame?
        # Optimization: Render once and scale image.
        # But simple way first.
        txt = self.font.render(self.text, True, COLORS["white"])
        # Scale text image to match scale factor?
        if self.scale != 1.0:
            ts_w = int(txt.get_width() * self.scale)
            ts_h = int(txt.get_height() * self.scale)
            if ts_w > 0 and ts_h > 0:
                 txt = pygame.transform.smoothscale(txt, (ts_w, ts_h))
        
        txt_rect = txt.get_rect(center=(cx, cy))
        surface.blit(txt, txt_rect)
