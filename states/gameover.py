
import pygame
import config
from config import *
from ui.ui_button import UIButton
from PIL import Image, ImageFilter

class GameOverState:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.font = pygame.font.Font(FONTS["bold"], 64)
        self.blurred_bg = None
        self.overlay_surf = None

    def enter(self):
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
        start_y = center_y + 20 
        gap = 80

        def restart(): self.game.change_state("game")
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

    def draw(self, surface):
        # 1. Draw Blurred Background
        if self.blurred_bg:
            surface.blit(self.blurred_bg, (0, 0))
        else:
            surface.fill(COLORS["bg_dark"])
            
        # 2. Draw Dark Overlay
        surface.blit(self.overlay_surf, (0, 0))
        
        # 3. Draw Popup Box
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        popup_width = 500
        popup_height = 350
        
        popup_rect = pygame.Rect(0, 0, popup_width, popup_height)
        popup_rect.center = (center_x, center_y)
        
        pygame.draw.rect(surface, (40, 40, 40), popup_rect, border_radius=16) # Bg with rounded corners
        pygame.draw.rect(surface, COLORS["white"], popup_rect, 4, border_radius=16) # Border
        
        # 4. Draw Result Text
        if self.game.winner:
            text = f"{self.game.winner} Wins!" if self.game.winner != "D" else "It's a Draw!"
            color = COLORS["glow_yellow"] if self.game.winner != "D" else COLORS["white"]
            if self.game.winner == "X": color = COLORS["x_color"]
            if self.game.winner == "O": color = COLORS["o_color"]
        else:
             text = "Game Over"
             color = COLORS["white"]
        
        text_surf = self.font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(center_x, center_y - 80))
        surface.blit(text_surf, text_rect)

        # 5. Buttons
        for btn in self.buttons:
            btn.draw(surface)
