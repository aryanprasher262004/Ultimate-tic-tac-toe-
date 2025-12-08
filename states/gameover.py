
import pygame
import config
from config import *
from ui.button import Button
from PIL import Image, ImageFilter

class GameOverState:
    def __init__(self, game):
        self.game = game
        self.menu_button = None
        self.restart_button = None
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_NORMAL)
        self.blurred_bg = None
        self.overlay_surf = None

    def enter(self):
        # 1. Capture Logic
        # It's difficult to capture the previous screen directly from here because `game.screen` has already been flipped/cleared potentially.
        # However, usually the last frame of "Game" state is still on the screen surface when we enter "GameOver".
        # Let's try capturing the current display surface.
        
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

        # Setup Buttons (Centered Popup style)
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        popup_width = 400
        popup_height = 300
        start_y = center_y + 20 
        gap = 80

        self.restart_button = Button(center_x - 100, start_y, 200, 60, "Play Again", self.font, bg_color=GREEN, sound_path=CLICK_SOUND_PATH)
        self.menu_button = Button(center_x - 100, start_y + gap, 200, 60, "Main Menu", self.font, bg_color=BLUE, sound_path=CLICK_SOUND_PATH)

    def exit(self):
        self.blurred_bg = None # Clean up memory

    def handle_event(self, event):
        if self.restart_button.handle_event(event):
            self.game.change_state("game")
        elif self.menu_button.handle_event(event):
            self.game.change_state("home")

    def update(self):
        pass

    def draw(self, surface):
        # 1. Draw Blurred Background
        if self.blurred_bg:
            surface.blit(self.blurred_bg, (0, 0))
        else:
            surface.fill(DARK_GRAY)
            
        # 2. Draw Dark Overlay
        surface.blit(self.overlay_surf, (0, 0))
        
        # 3. Draw Popup Box
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        popup_width = 500
        popup_height = 350
        
        popup_rect = pygame.Rect(0, 0, popup_width, popup_height)
        popup_rect.center = (center_x, center_y)
        
        pygame.draw.rect(surface, (40, 40, 40), popup_rect) # Bg
        pygame.draw.rect(surface, WHITE, popup_rect, 4) # Border
        
        # 4. Draw Result Text
        title_font = pygame.font.SysFont(FONT_NAME, 64, bold=True)
        
        if self.game.winner:
            text = f"{self.game.winner} Wins!" if self.game.winner != "D" else "It's a Draw!"
            color = YELLOW if self.game.winner != "D" else WHITE
            if self.game.winner == "X": color = COLOR_X
            if self.game.winner == "O": color = COLOR_O
        else:
             text = "Game Over"
             color = WHITE
        
        text_surf = title_font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(center_x, center_y - 80))
        surface.blit(text_surf, text_rect)

        # 5. Buttons
        self.restart_button.draw(surface)
        self.menu_button.draw(surface)
