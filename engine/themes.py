import pygame
import math

class Theme:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.cache = {}
        
    def get(self, key):
        return self.data.get(key, (255, 255, 255))
        
    def get_color(self, key):
        # Handle string hex codes
        val = self.data.get(key, (255, 255, 255))
        if isinstance(val, str) and val.startswith("#"):
            return pygame.Color(val)
        return val

THEMES_DATA = {
    "NEON": {
        "bg_color": "#0A0014",
        "small_grid_color": "#302040", # Darker for small
        "big_grid_color": "#00FFFF",  # Bright cyan
        "x_color": "#FF0080",
        "o_color": "#00FFFF",
        "glow_color": (255, 0, 255),
        "text_color": "#FFFFFF",
        "highlight_color": (50, 0, 50)
    },
    "BLACK_WHITE": {
        "bg_color": "#000000",
        "small_grid_color": "#333333",
        "big_grid_color": "#FFFFFF",
        "x_color": "#FFFFFF",
        "o_color": "#CCCCCC",
        "glow_color": (200, 200, 200),
        "text_color": "#FFFFFF",
        "highlight_color": (50, 50, 50)
    },
    "RGB_GAMER": {
        "bg_color": "#050505",
        "small_grid_color": "#202020",
        "big_grid_color": "RGB", # Special flag
        "x_color": "#FF3333",
        "o_color": "#3333FF",
        "glow_color": (0, 255, 0), # Dynamic usually
        "text_color": "#FFFFFF",
        "highlight_color": (20, 20, 40)
    },
    "PASTEL_SOFT": {
        "bg_color": "#F6F2FF",
        "small_grid_color": "#E0D0FF",
        "big_grid_color": "#B4E4FF",
        "x_color": "#FFB5B5",
        "o_color": "#B9F3E4",
        "glow_color": (255, 255, 200),
        "text_color": "#606080",
        "highlight_color": (240, 240, 250)
    }
}

class ThemeManager:
    def __init__(self):
        self.themes = {name: Theme(name, data) for name, data in THEMES_DATA.items()}
        self.current_theme_name = "NEON"
        self.current_theme = self.themes[self.current_theme_name]
        self.rgb_hue = 0.0

    def set_theme(self, name):
        if name in self.themes:
            self.current_theme_name = name
            self.current_theme = self.themes[name]
    
    def next_theme(self):
        names = list(self.themes.keys())
        idx = names.index(self.current_theme_name)
        new_idx = (idx + 1) % len(names)
        self.set_theme(names[new_idx])

    def update(self, dt):
        self.rgb_hue += dt * 50 # Speed
        if self.rgb_hue > 360:
             self.rgb_hue -= 360

    def get_color(self, key):
        # Special logic for RGB theme
        if self.current_theme_name == "RGB_GAMER" and key == "big_grid_color":
             c = pygame.Color(0,0,0)
             c.hsva = (self.rgb_hue, 100, 100, 100)
             return c
        return self.current_theme.get_color(key)

    def get_bg_color(self):
        return self.get_color("bg_color")

theme_manager = ThemeManager()
