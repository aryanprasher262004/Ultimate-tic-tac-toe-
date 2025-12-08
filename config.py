
import pygame

# -----------------------------
#  MODERN UI STYLE CONFIG PACK
# -----------------------------

# Color Palette (Modern Neon + Dark Mode)
COLORS = {
    "bg_dark": (20, 20, 20),
    "panel_dark": (30, 30, 30),
    "white": (255, 255, 255),
    "grey": (180, 180, 180),
    "black": (0, 0, 0),

    # Grid
    "big_border": (255, 255, 255),
    "small_border": (150, 150, 150),

    # X / O Colors
    "x_color": (255, 75, 75),
    "o_color": (75, 163, 255),

    # Button colors
    "btn_idle": (40, 40, 40),
    "btn_hover": (60, 60, 60),
    "btn_active": (80, 80, 80),

    # Glow & highlights
    "glow_blue": (0, 140, 255),
    "glow_red": (255, 60, 60),
    "glow_yellow": (255, 230, 90),
}

# Fonts
FONTS = {
    "regular": "assets/fonts/Inter-Regular.ttf",
    "bold": "assets/fonts/Inter-Bold.ttf",
    "semi": "assets/fonts/Inter-SemiBold.ttf",
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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Ultimate Tic Tac Toe"
FPS = 60

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
BACKGROUND_IMAGE_PATH = "assets/backgrounds/home_bg.jpg"
CLICK_SOUND_PATH = "assets/sounds/click.wav"

# Game State
GAME_MODE = "self" # "self" or "computer"

# Audio Settings
MUSIC_VOLUME = 0.6
SFX_ENABLED = True
SFX_VOLUME = 0.8
