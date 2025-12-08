
import pygame

# -----------------------------
#   VIBRANT GAMING UI THEME
# -----------------------------
COLORS = {
    # Backgrounds
    "bg_primary": (15, 15, 15),
    "bg_surface": (26, 26, 26),
    "bg_elevated": (36, 36, 36),
    "bg_dark": (15, 15, 15), # Mapped for compatibility

    # Text
    "text_main": (255, 255, 255),
    "text_subtle": (180, 180, 180),
    "white": (255, 255, 255), # Mapped
    "grey": (180, 180, 180), # Mapped
    "black": (0, 0, 0),

    # Accents (Modern)
    "accent_blue": (59,130,246),      # Electric Blue
    "accent_purple": (168,85,247),   # Neon Purple
    "accent_cyan": (34,211,238),     # Aqua Cyan
    "accent_green": (16,185,129),    # Neon Green
    "accent_red": (239,68,68),       # Neon Red
    "accent_gold": (250,204,21),     # Gold Highlight
    
    # Mappings for legacy/existing code usage
    "neon_blue": (34,211,238),       # Mapped to Cyan
    "panel_dark": (26, 26, 26),      # Mapped to Surface

    # Glow Colors
    "glow_blue": (96,165,250),
    "glow_purple": (192,132,252),
    "glow_cyan": (103,232,249),
    "glow_red": (248,113,113),
    "glow_yellow": (250,204,21),     # Mapped to Gold
    "glow_green": (16,185,129),

    # Board Grid
    "big_border": (255, 255, 255),
    "small_border": (150, 150, 150),

    # X/O colors
    "x_color": (239,68,68),    # neon red
    "o_color": (34,211,238),   # neon cyan

    # Buttons
    "btn_idle": (36, 36, 36),
    "btn_hover": (59,130,246),
    "btn_active": (168,85,247),
}

# Fonts
FONTS = {
    "regular": None,
    "bold": None,
    "semi": None,
}

# Animation speeds
ANIM = {
    "button_hover_speed": 0.15,
    "fade_speed": 0.08,
    "glow_pulse_speed": 0.05,
}

# -----------------------------
#  GAME CONSTANTS (Mapped to Style Pack)
# -----------------------------

# Screen Dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Ultimate Tic Tac Toe"
FPS = 60
FULLSCREEN = False # Store fullscreen state

# Legacy Colors (Mapped to new Palette for backward compatibility)
WHITE = COLORS["white"]
BLACK = COLORS["black"]
GRAY = COLORS["grey"]
DARK_GRAY = COLORS["panel_dark"]
RED = COLORS["x_color"]     # Theming red to X color
BLUE = COLORS["o_color"]    # Theming blue to O color
GREEN = (50, 255, 50)       # Keep standard green for now or map to success
YELLOW = COLORS["glow_yellow"]
CYAN = COLORS["glow_blue"]
MAGENTA = (255, 0, 255)

# Game UI Colors (Directly using new Palette)
COLOR_BG = COLORS["bg_dark"]
COLOR_BIG_BORDER = COLORS["big_border"]
COLOR_SMALL_BORDER = COLORS["small_border"]
COLOR_X = COLORS["x_color"]
COLOR_O = COLORS["o_color"]

# Fonts
FONT_NAME = "arial" # Fallback if Inter not found
FONT_SIZE_TITLE = 64
FONT_SIZE_NORMAL = 32

# Asset Paths
BACKGROUND_IMAGE_PATH = "assets/backgrounds/bghome.jpeg"
GAME_BACKGROUND_IMAGE_PATH = "assets/backgrounds/bggame.jpeg"
SETTINGS_BACKGROUND_IMAGE_PATH = "assets/backgrounds/bgsettings.jpeg"
MODES_BACKGROUND_IMAGE_PATH = "assets/backgrounds/bgmodes.jpeg"
CLICK_SOUND_PATH = "assets/sounds/click.wav"

# Game State
GAME_MODE = "self" # "self" or "computer"

# Audio Settings
MUSIC_VOLUME = 0.6
MUSIC_ENABLED = True
SFX_ENABLED = True
SFX_VOLUME = 0.8

# Visual Settings
CURRENT_THEME = "neon"
PLAYER_SYMBOL = "X"
