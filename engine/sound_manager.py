
import pygame
import os
import config

class SoundManager:
    def __init__(self):
        # We need to ensure pygame mixer is init
        if not pygame.mixer.get_init():
             try:
                 pygame.mixer.init()
             except:
                 pass

        self.sounds = {}
        
        # Define paths
        self.paths = {
            "click": "assets/sounds/click.wav", 
            "move": "assets/sounds/place.wav",
            "win": "assets/sounds/win.wav",
            "lose": "assets/sounds/lose.wav"
        }
        
        for key, path in self.paths.items():
            if os.path.exists(path):
                try:
                    s = pygame.mixer.Sound(path)
                    s.set_volume(config.SFX_VOLUME)
                    self.sounds[key] = s
                except:
                    print(f"Failed to load sound: {path}")
            else:
                pass

    def play(self, key):
        if not config.SFX_ENABLED:
            return
            
        if key in self.sounds:
            self.sounds[key].play()
        else:
             pass

    def set_sfx_volume(self, volume):
        """Update volume for all loaded sounds"""
        for s in self.sounds.values():
            s.set_volume(volume)

# Create global instance
sound = SoundManager()
