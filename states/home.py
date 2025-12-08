
import pygame
import os
import random
from config import *
from ui.ui_button import UIButton
from ui.tween import tweener

class HomeState:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.background_image = None
        
        # Neon Title Animation Properties
        self.glow_intensity = 1.0
        self.title_opacity = 255
        self.flicker_timer = 0
        self.big_flicker_timer = 0
        self.is_big_flickering = False
        
        # Load background if exists
        if os.path.exists(BACKGROUND_IMAGE_PATH):
            try:
                self.background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
                self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error:
                print(f"Failed to load background: {BACKGROUND_IMAGE_PATH}")

    def start_glow_loop(self):
        """Start the continuous glow intensity animation"""
        def loop_glow():
            tweener.add(self, "glow_intensity", self.glow_intensity, 0.8, 800, "ease_in_out", callback=lambda: self.reverse_glow())
        loop_glow()
    
    def reverse_glow(self):
        """Reverse glow animation"""
        tweener.add(self, "glow_intensity", self.glow_intensity, 1.2, 800, "ease_in_out", callback=lambda: self.start_glow_loop())
    
    def start_flicker_loop(self):
        """Start the continuous opacity flicker animation"""
        def loop_flicker():
            tweener.add(self, "title_opacity", self.title_opacity, 180, 300, "ease_in_out", callback=lambda: self.reverse_flicker())
        loop_flicker()
    
    def reverse_flicker(self):
        """Reverse flicker animation"""
        tweener.add(self, "title_opacity", self.title_opacity, 255, 300, "ease_in_out", callback=lambda: self.start_flicker_loop())

    def enter(self):
        """Called when entering this state"""
        center_x = self.game.screen.get_width() // 2
        start_y = 180
        gap = 70
        
        # Start animations
        self.start_glow_loop()
        self.start_flicker_loop()
        self.big_flicker_timer = random.randint(2000, 5000)
        
        # Callbacks
        def go_resume(): self.game.change_state("game")
        def go_new_game(): self.game.change_state("game", "new_game")
        def go_modes(): self.game.change_state("modes")
        def go_settings(): self.game.change_state("settings")
        def go_quit(): self.game.running = False

        self.buttons = []
        
        # Check if game is in progress
        game_state = self.game.states["game"]
        
        is_game_active = False
        if game_state.logic:
             # Check if any move made
             for b in game_state.logic.board_states:
                 if b != "":
                     is_game_active = True
                     break
             # Also check small boards if big boards empty
             if not is_game_active:
                  for b in range(9):
                      for r in range(3):
                          for c in range(3):
                              if game_state.logic.small_boards[b][r][c] != "":
                                  is_game_active = True
                                  break
        
        if game_state.logic.game_over:
            is_game_active = False

        if is_game_active:
            self.buttons.append(UIButton(center_x - 100, start_y, 200, 60, "Resume", go_resume))
            self.buttons.append(UIButton(center_x - 100, start_y + gap, 200, 60, "New Game", go_new_game))
            self.buttons.append(UIButton(center_x - 100, start_y + gap * 2, 200, 60, "Modes", go_modes))
            self.buttons.append(UIButton(center_x - 100, start_y + gap * 3, 200, 60, "Settings", go_settings))
            self.buttons.append(UIButton(center_x - 100, start_y + gap * 4, 200, 60, "Quit", go_quit))
        else:
            self.buttons.append(UIButton(center_x - 100, start_y, 200, 60, "Play", go_new_game))
            self.buttons.append(UIButton(center_x - 100, start_y + gap, 200, 60, "Modes", go_modes))
            self.buttons.append(UIButton(center_x - 100, start_y + gap * 2, 200, 60, "Settings", go_settings))
            self.buttons.append(UIButton(center_x - 100, start_y + gap * 3, 200, 60, "Quit", go_quit))

    def exit(self):
        pass

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def update(self):
        for btn in self.buttons:
            btn.update()
        
        # Big flicker logic
        dt = self.game.clock.get_time()
        self.big_flicker_timer -= dt
        
        if self.big_flicker_timer <= 0 and not self.is_big_flickering:
            # Trigger big flicker
            self.is_big_flickering = True
            self.flicker_timer = 50  # 50ms flicker
            self.big_flicker_timer = random.randint(3000, 7000)  # Next flicker in 3-7 seconds
        
        if self.is_big_flickering:
            self.flicker_timer -= dt
            if self.flicker_timer <= 0:
                self.is_big_flickering = False

    def draw(self, surface):
        w = surface.get_width()
        
        # Draw Background
        if self.background_image:
             surface.blit(pygame.transform.scale(self.background_image, surface.get_size()), (0, 0))
        else:
             surface.fill(COLORS["bg_dark"])

        # Neon Flickering Title
        if not self.is_big_flickering:
            title_font = pygame.font.Font(FONTS["bold"], FONT_SIZE_TITLE)
            
            # Calculate colors with animation
            base_cyan = COLORS["neon_blue"]
            glow_color = COLORS["glow_cyan"]
            
            # Apply opacity
            opacity = int(self.title_opacity)
            
            # Outer glow layers (multiple for stronger effect)
            glow_sizes = [8, 6, 4]
            glow_alphas = [30, 50, 80]
            
            for i, (size_offset, alpha_base) in enumerate(zip(glow_sizes, glow_alphas)):
                glow_alpha = int(alpha_base * self.glow_intensity)
                glow_font = pygame.font.Font(FONTS["bold"], FONT_SIZE_TITLE + size_offset)
                glow_surf = glow_font.render(SCREEN_TITLE, True, glow_color)
                glow_surf.set_alpha(glow_alpha)
                glow_rect = glow_surf.get_rect(center=(w // 2, 80))
                surface.blit(glow_surf, glow_rect)
            
            # Main title with opacity
            title_surf = title_font.render(SCREEN_TITLE, True, base_cyan)
            title_surf.set_alpha(opacity)
            title_rect = title_surf.get_rect(center=(w // 2, 80))
            surface.blit(title_surf, title_rect)
            
            # Inner bright core
            core_surf = title_font.render(SCREEN_TITLE, True, (255, 255, 255))
            core_surf.set_alpha(int(120 * self.glow_intensity))
            surface.blit(core_surf, title_rect)

        for btn in self.buttons:
            btn.draw(surface)
