
import pygame
import sys
import config
from config import *

# Import States
from states.home import HomeState
from states.modes import ModesState
from states.settings import SettingsState
from states.game import GameState
from states.gameover import GameOverState

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

    def change_state(self, state_name):
        if self.current_state:
            self.current_state.exit()
        
        self.current_state = self.states[state_name]
        self.current_state.enter()

    def run(self):
        while self.running:
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.current_state:
                    self.current_state.handle_event(event)
            
            # Update
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
