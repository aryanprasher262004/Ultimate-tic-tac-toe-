import pygame
import sys
import os
import config
from config import *
from engine.save_manager import load_settings, save_settings
from engine.sound_manager import sound

from ui.tween import tweener
from engine.themes import theme_manager

# Import States
from states.home import HomeState
from states.modes import ModesState
from states.settings import SettingsState
from states.game import GameState
from states.gameover import GameOverState

class Game:
    def __init__(self):
        load_settings() # Load user preferences
        
        # Apply saved theme
        if hasattr(config, 'CURRENT_THEME') and config.CURRENT_THEME:
            # Map theme name to proper format
            theme_map = {
                "neon": "NEON",
                "black_white": "BLACK_WHITE", 
                "rgb_gamer": "RGB_GAMER",
                "pastel_soft": "PASTEL_SOFT"
            }
            theme_name = theme_map.get(config.CURRENT_THEME.lower(), "NEON")
            theme_manager.set_theme(theme_name)
        
        # Apply volume settings immediately
        pygame.init()
        pygame.mixer.music.set_volume(config.MUSIC_VOLUME)
        sound.set_sfx_volume(config.SFX_VOLUME)
        
        # Load and play background music
        bg_music_path = "assets/sounds/homescreenplayback.mp3"
        if os.path.exists(bg_music_path):
            try:
                pygame.mixer.music.load(bg_music_path)
                pygame.mixer.music.set_volume(config.MUSIC_VOLUME)
                if config.MUSIC_ENABLED:
                    pygame.mixer.music.play(-1) # Loop forever
            except pygame.error as e:
                print(f"Failed to load music: {e}")

        if config.FULLSCREEN:
             self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
             self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
             
        pygame.display.set_caption(SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Game State Data
        self.game_mode = "pvp" # pvp or ai
        self.winner = None

        # State Management
        self.states = {
            "home": HomeState(self),
            "modes": ModesState(self),
            "settings": SettingsState(self),
            "game": GameState(self),
            "gameover": GameOverState(self)
        }
        self.current_state = None
        self.change_state("home")

    def change_state(self, state_name, params=None):
        # Prevent input buffering from triggering transitions
        pygame.event.clear()
        
        # 1. Fade Out (if there is a current state)
        # Skip fade out for "gameover" so it can capture the previous screen
        if self.current_state and state_name != "gameover":
            # Capture current screen
            old_surface = self.screen.copy()
            fade_overlay = pygame.Surface(self.screen.get_size())
            fade_overlay.fill(COLORS["bg_dark"]) # Fade to background color
            
            # Fade Loop
            for alpha in range(0, 255, 40): # Speed increased to 40
                self.screen.blit(old_surface, (0,0))
                fade_overlay.set_alpha(alpha)
                self.screen.blit(fade_overlay, (0,0))
                pygame.display.update()
                pygame.time.delay(5)
            
            self.current_state.exit()
        
        # 2. Switch State
        self.current_state = self.states[state_name]
        
        # Check if enter accepts params (using introspection or try/except, but known interface is simpler)
        # We'll update the base state interface or just use try/except
        try:
             self.current_state.enter(params)
        except TypeError:
             self.current_state.enter()
        
        # 3. Fade In
        # We need to draw the NEW state once to fade from black to it
        self.current_state.draw(self.screen) # Draw new state to screen (it's hidden by next loop initially)
        new_state_surface = self.screen.copy()
        
        fade_overlay = pygame.Surface(self.screen.get_size())
        fade_overlay.fill(COLORS["bg_dark"])
        
        for alpha in range(255, 0, -40):
             self.screen.blit(new_state_surface, (0,0))
             fade_overlay.set_alpha(alpha)
             self.screen.blit(fade_overlay, (0,0))
             pygame.display.update()
             pygame.time.delay(5)
             
        pygame.event.clear() # Clear any inputs accumulated during transition

    def run(self):
        while self.running:
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.current_state:
                    self.current_state.handle_event(event)
            
            # Update
            dt = self.clock.get_time() / 1000.0
            tweener.update(dt)
            theme_manager.update(dt)
            
            if self.current_state:
                self.current_state.update()

            # Draw
            if self.current_state:
                self.current_state.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
