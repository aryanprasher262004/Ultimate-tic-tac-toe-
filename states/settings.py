import pygame
import os
import config
from config import *
from ui.ui_button import UIButton
from ui.ui_toggle import UIToggle
from ui.settings_components import ThemeCard, SymbolButton
from engine.sound_manager import sound
from engine.save_manager import save_settings
from engine.themes import theme_manager

class SettingsState:
    def __init__(self, game):
        self.game = game
        self.ui_elements = [] # Generic list for update/handle/draw if common interface
        self.toggles = []
        self.theme_cards = []
        self.symbol_buttons = []
        self.back_button = None
        
        self.font = pygame.font.Font(FONTS["regular"], FONT_SIZE_NORMAL)

        self.bg_original = None
        self.bg_scaled = None
        if os.path.exists(SETTINGS_BACKGROUND_IMAGE_PATH):
            try:
                self.bg_original = pygame.image.load(SETTINGS_BACKGROUND_IMAGE_PATH)
            except: pass

    def on_music_toggle(self, val):
        config.MUSIC_ENABLED = val
        if config.MUSIC_ENABLED:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
            else:
                 pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        save_settings()

    def on_sfx_toggle(self, val):
        config.SFX_ENABLED = val
        save_settings()

    def on_fs_toggle(self, val):
        config.FULLSCREEN = val
        if config.FULLSCREEN:
             self.game.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
             self.game.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        save_settings()
        # Re-enter to rescale BG
        self.enter()

    def on_theme_select(self, theme_name):
        theme_manager.set_theme(theme_name)
        config.CURRENT_THEME = theme_name.lower() # map specific?
        save_settings()
        
    def on_symbol_select(self, symbol):
        config.PLAYER_SYMBOL = symbol
        save_settings()

    def enter(self, params=None):
        w, h = self.game.screen.get_size()
        
        # Scale background
        if self.bg_original:
            self.bg_scaled = pygame.transform.scale(self.bg_original, (w, h))

        # Clear lists
        self.toggles = []
        self.theme_cards = []
        self.symbol_buttons = []
        
        # Layout Config
        col1_x = 100
        start_y = 150
        gap_y = 70
        
        # 1. Toggles (Left)
        # Music
        self.toggles.append(UIToggle(col1_x + 150, start_y, 80, 40, config.MUSIC_ENABLED, self.on_music_toggle, "neon"))
        # SFX
        self.toggles.append(UIToggle(col1_x + 150, start_y + gap_y, 80, 40, config.SFX_ENABLED, self.on_sfx_toggle, "minimal"))
        # Fullscreen
        self.toggles.append(UIToggle(col1_x + 150, start_y + gap_y*2, 80, 40, config.FULLSCREEN, self.on_fs_toggle, "rgb"))

        # 2. Theme Grid (Right)
        grid_start_x = w // 2 + 50
        grid_start_y = 150
        cw, ch = 140, 140
        cgap = 20
        
        themes = ["NEON", "BLACK_WHITE", "RGB_GAMER", "PASTEL_SOFT"]
        for i, name in enumerate(themes):
            r = i // 2
            c = i % 2
            cx = grid_start_x + c * (cw + cgap)
            cy = grid_start_y + r * (ch + cgap)
            card = ThemeCard(cx, cy, cw, ch, name, self.on_theme_select)
            self.theme_cards.append(card)
            
        # 3. Symbol Picker (Bottom)
        sym_y = 550
        sym_size = 60
        sym_gap = 40
        # Symbols: X, O, Check
        syms = ["X", "O", "✓"]
        total_w = len(syms) * sym_size + (len(syms)-1) * sym_gap
        start_sym_x = (w - total_w) // 2
        
        for i, s in enumerate(syms):
            sx = start_sym_x + i * (sym_size + sym_gap)
            sb = SymbolButton(sx, sym_y, sym_size, s, self.on_symbol_select)
            self.symbol_buttons.append(sb)

        # Back Button (Top Left)
        def go_back(): self.game.change_state("home")
        self.back_button = UIButton(20, 20, 100, 40, "Back", go_back)

    def exit(self):
        pass

    def handle_event(self, event):
        self.back_button.handle_event(event)
        for t in self.toggles: t.handle_event(event)
        for c in self.theme_cards: c.handle_event(event)
        for s in self.symbol_buttons: s.handle_event(event)

    def update(self):
        self.back_button.update()
        dt = self.game.clock.get_time() / 1000.0
        for t in self.toggles: t.update(dt)
        # Theme cards might need update? No, just draw.
        # Symbols need update? No.
        
    def draw(self, surface):
        if self.bg_scaled:
            surface.blit(self.bg_scaled, (0, 0))
        else:
            surface.fill(COLORS["bg_dark"])
        
        w, h = surface.get_size()
        
        # Title "Settings"
        # title_font = pygame.font.Font(FONTS["bold"], FONT_SIZE_TITLE) # Keep original title?
        # Maybe smaller or centered
        title_font = pygame.font.Font(FONTS["bold"], 64)
        t_surf = title_font.render("Settings", True, (255, 255, 255))
        surface.blit(t_surf, t_surf.get_rect(center=(w//2, 70)))
        
        # Labels for Toggles
        col1_x = 100
        start_y = 150
        gap_y = 70
        
        labels = ["Music", "SFX", "Fullscreen"]
        lbl_font = pygame.font.Font(FONTS["semi"], 32)
        
        for i, lbl in enumerate(labels):
            l_surf = lbl_font.render(lbl, True, (255, 255, 255))
            ly = start_y + i * gap_y + 20 - l_surf.get_height()//2
            surface.blit(l_surf, (col1_x, ly))

        # Draw Elements
        for t in self.toggles: t.draw(surface)
        
        # Grid Label
        # grid_lbl = lbl_font.render("Themes", True, (255, 255, 255))
        # surface.blit(grid_lbl, (w//2 + 50, 100))
        
        for c in self.theme_cards: c.draw(surface)
        
        # Symbol Label
        sym_lbl = lbl_font.render("Your Symbol", True, (255, 255, 255))
        surface.blit(sym_lbl, sym_lbl.get_rect(center=(w//2, 510)))
        
        for s in self.symbol_buttons: s.draw(surface)
            
        self.back_button.draw(surface)
