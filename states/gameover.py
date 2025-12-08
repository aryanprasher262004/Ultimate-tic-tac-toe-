
import pygame
import math
import config
from config import *
from ui.ui_button import UIButton
from ui.tween import tweener
from PIL import Image, ImageFilter

class GameOverState:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.font = pygame.font.Font(FONTS["bold"], 64)
        self.subtitle_font = pygame.font.Font(FONTS["regular"], 28)
        self.blurred_bg = None
        self.overlay_surf = None
        
        # Animation properties
        self.popup_alpha = 0
        self.shake_offset = 0
        self.shake_timer = 0
        self.icon_rotation = 0
        self.icon_flash_alpha = 255

    def enter(self):
        # Reset animations
        self.popup_alpha = 0
        self.shake_offset = 0
        self.shake_timer = 0
        self.icon_rotation = 0
        self.icon_flash_alpha = 255
        
        # Fade in animation
        tweener.add(self, "popup_alpha", 0, 255, 300, "ease_out")
        
        # Shake animation if timeout loss
        if self.game.timeout_win:
            self.shake_timer = 1000  # Shake for 1 second
        
        # 1. Capture Logic
        try:
            # Capture screen
            screen_str = pygame.image.tostring(self.game.screen, 'RGB')
            pil_image = Image.frombytes('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), screen_str)
            
            # Blur
            blurred_image = pil_image.filter(ImageFilter.GaussianBlur(radius=8))
            
            # Convert back to Pygame surface
            self.blurred_bg = pygame.image.fromstring(blurred_image.tobytes(), blurred_image.size, 'RGB')
        except Exception as e:
            print(f"Error creating blurred background: {e}")
            self.blurred_bg = None # Fallback

        # Create overlay surface for darkening
        self.overlay_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay_surf.set_alpha(150) # Semi-transparent
        self.overlay_surf.fill((0, 0, 0)) # Black

        # Setup Buttons
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        start_y = center_y + 80
        gap = 80

        def restart(): self.game.change_state("game", "new_game")
        def go_home(): self.game.change_state("home")

        self.buttons = [
            UIButton(center_x - 100, start_y, 200, 60, "Play Again", restart),
            UIButton(center_x - 100, start_y + gap, 200, 60, "Main Menu", go_home)
        ]

    def exit(self):
        self.blurred_bg = None # Clean up memory

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def update(self):
        for btn in self.buttons:
            btn.update()
        
        # Update shake animation
        if self.shake_timer > 0:
            dt = self.game.clock.get_time()
            self.shake_timer -= dt
            # Shake decreases over time
            shake_intensity = (self.shake_timer / 1000.0) * 5
            self.shake_offset = math.sin(pygame.time.get_ticks() * 0.05) * shake_intensity
        else:
            self.shake_offset = 0
        
        # Update icon rotation
        self.icon_rotation = (self.icon_rotation + 2) % 360
        
        # Flash animation for timeout
        if self.game.timeout_win:
            self.icon_flash_alpha = 128 + 127 * abs(math.sin(pygame.time.get_ticks() * 0.005))

    def get_timeout_message(self):
        """Generate message based on timeout reason"""
        reason = self.game.timeout_reason
        winner = self.game.winner
        
        if reason == "p1_timeout":
            return "⏳ Player 2 Wins", "Player 1 ran out of time!"
        elif reason == "p2_timeout":
            return "⏳ Player 1 Wins", "Player 2 ran out of time!"
        elif reason == "both_boards":
            player_name = "Player 1" if winner == "X" else "Player 2"
            return f"⏰ {player_name} Wins", "Time expired — Won by captured boards!"
        elif reason == "both_draw":
            return "⏳ Draw", "Times expired and board captures are equal"
        else:
            return None, None

    def draw_clock_icon(self, surface, x, y, size, color, alpha=255):
        """Draw an animated clock/hourglass icon"""
        # Create surface for alpha
        icon_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        
        # Draw hourglass shape
        points = [
            (size, size*0.3),  # Top
            (size*1.6, size*0.3),
            (size*1.3, size),  # Middle
            (size*1.6, size*1.7),
            (size, size*1.7),  # Bottom
            (size*0.7, size),  # Middle
        ]
        
        pygame.draw.polygon(icon_surf, (*color[:3], alpha), points, 3)
        
        # Draw sand (rotating)
        sand_y = size + math.sin(self.icon_rotation * 0.05) * size * 0.3
        pygame.draw.circle(icon_surf, (*color[:3], alpha), (int(size), int(sand_y)), int(size*0.2))
        
        # Blit to main surface
        surface.blit(icon_surf, (x - size, y - size))

    def draw(self, surface):
        # 1. Draw Blurred Background
        if self.blurred_bg:
            surface.blit(self.blurred_bg, (0, 0))
        else:
            surface.fill(COLORS["bg_dark"])
            
        # 2. Draw Dark Overlay
        surface.blit(self.overlay_surf, (0, 0))
        
        # 3. Draw Popup Box with fade-in
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        popup_width = 600
        popup_height = 400
        
        popup_rect = pygame.Rect(0, 0, popup_width, popup_height)
        popup_rect.center = (center_x, center_y)
        
        # Apply alpha to popup
        popup_surf = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        pygame.draw.rect(popup_surf, (40, 40, 40, int(self.popup_alpha)), popup_surf.get_rect(), border_radius=16)
        pygame.draw.rect(popup_surf, (*COLORS["white"][:3], int(self.popup_alpha)), popup_surf.get_rect(), 4, border_radius=16)
        surface.blit(popup_surf, popup_rect.topleft)
        
        # 4. Draw Result Text with shake if timeout
        if self.game.timeout_win:
            # Timeout-specific message
            title, subtitle = self.get_timeout_message()
            
            # Draw timeout icon
            icon_x = center_x
            icon_y = center_y - 120
            icon_color = COLORS["glow_red"] if self.game.timeout_reason in ["p1_timeout", "p2_timeout"] else COLORS["glow_yellow"]
            self.draw_clock_icon(surface, icon_x, icon_y, 30, icon_color, int(self.icon_flash_alpha))
            
            # Title with shake
            title_surf = self.font.render(title, True, COLORS["glow_red"])
            title_surf.set_alpha(int(self.popup_alpha))
            title_rect = title_surf.get_rect(center=(center_x + self.shake_offset, center_y - 50))
            surface.blit(title_surf, title_rect)
            
            # Subtitle
            subtitle_surf = self.subtitle_font.render(subtitle, True, COLORS["white"])
            subtitle_surf.set_alpha(int(self.popup_alpha))
            subtitle_rect = subtitle_surf.get_rect(center=(center_x, center_y + 10))
            surface.blit(subtitle_surf, subtitle_rect)
        else:
            # Normal win message
            if self.game.winner:
                text = f"{self.game.winner} Wins!" if self.game.winner != "D" else "It's a Draw!"
                color = COLORS["glow_yellow"] if self.game.winner != "D" else COLORS["white"]
                if self.game.winner == "X": color = COLORS["x_color"]
                if self.game.winner == "O": color = COLORS["o_color"]
            else:
                text = "Game Over"
                color = COLORS["white"]
            
            text_surf = self.font.render(text, True, color)
            text_surf.set_alpha(int(self.popup_alpha))
            text_rect = text_surf.get_rect(center=(center_x, center_y - 60))
            surface.blit(text_surf, text_rect)

        # 5. Buttons (with alpha)
        for btn in self.buttons:
            btn.draw(surface)
