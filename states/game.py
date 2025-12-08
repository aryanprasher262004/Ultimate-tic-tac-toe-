import pygame
import os
import config
from config import *
from ui.ui_button import UIButton
from engine.ai_minimax import MinimaxAI
from engine.sound_manager import sound
from engine.themes import theme_manager
import threading
from ui.tween import tweener

class UltimateTicTacToeLogic:
    def __init__(self):
        # 9 small boards, each 3x3
        self.small_boards = [[["" for _ in range(3)] for _ in range(3)] for _ in range(9)]
        # State of small boards: "" (playing), "X", "O", "D" (Draw)
        self.board_states = ["" for _ in range(9)]
        
        self.current_turn = "X"
        self.next_board_index = -1 
        self.winner = None
        self.game_over = False

    def check_small_board_win(self, board_index):
        b = self.small_boards[board_index]
        # Check rows
        for row in range(3):
            if b[row][0] == b[row][1] == b[row][2] and b[row][0] != "": return b[row][0]
        # Check cols
        for col in range(3):
            if b[0][col] == b[1][col] == b[2][col] and b[0][col] != "": return b[0][col]
        # Check diagonals
        if b[0][0] == b[1][1] == b[2][2] and b[0][0] != "": return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] and b[0][2] != "": return b[0][2]
        # Check Draw
        is_full = True
        for r in range(3):
            for c in range(3):
                if b[r][c] == "":
                    is_full = False
                    break
        if is_full: return "D"
        return ""

    def check_big_board_win(self):
        b = self.board_states
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for p in wins:
            if b[p[0]] == b[p[1]] == b[p[2]] and b[p[0]] in ["X", "O"]: return b[p[0]]
        if "" not in b: return "D"
        return None

    def make_move(self, board_idx, row, col):
        if self.game_over: return False
        if self.next_board_index != -1 and board_idx != self.next_board_index: return False
        if self.board_states[board_idx] != "": return False
        if self.small_boards[board_idx][row][col] != "": return False
        
        self.small_boards[board_idx][row][col] = self.current_turn
        sb_win = self.check_small_board_win(board_idx)
        if sb_win: self.board_states[board_idx] = sb_win
        
        bb_win = self.check_big_board_win()
        if bb_win:
            self.winner = bb_win
            self.game_over = True
            return True
            
        self.current_turn = "O" if self.current_turn == "X" else "X"
        next_idx = row * 3 + col
        if self.board_states[next_idx] != "": self.next_board_index = -1
        else: self.next_board_index = next_idx
        return True

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.rect = pygame.Rect(0,0,0,0)
        self.scale = 1.0
        self.border_opacity = 0.0
        self.hover = False
        
        # Symbol Animation
        self.symbol_scale = 1.0
        self.symbol_y_offset = 0

    def on_enter(self):
        self.hover = True
        tweener.add(self, "border_opacity", self.border_opacity, 255, 150, "ease_out")
        tweener.add(self, "scale", self.scale, 1.05, 120, "ease_out")

    def on_leave(self):
        self.hover = False
        tweener.add(self, "border_opacity", self.border_opacity, 0, 150, "ease_out")
        tweener.add(self, "scale", self.scale, 1.0, 120, "ease_out")

    def play_symbol_animation(self):
        # Start state
        self.symbol_scale = 0.0
        self.symbol_y_offset = -20
        # Scale up elastic
        tweener.add(self, "symbol_scale", 0.0, 1.0, 350, "elastic_out")
        # Drop with bounce (optional match) or just linear drop to 0
        tweener.add(self, "symbol_y_offset", -20, 0, 300, "ease_out")

    def draw(self, surface):
        if self.border_opacity > 1:
            w = self.rect.width * self.scale
            h = self.rect.height * self.scale
            cx, cy = self.rect.center
            
            s_surf = pygame.Surface((int(w), int(h)), pygame.SRCALPHA)
            
            c = theme_manager.get_color("glow_color")
            if hasattr(c, "r"): c = (c.r, c.g, c.b)
            color = (*c[:3], int(self.border_opacity))
            
            draw_rect = s_surf.get_rect()
            pygame.draw.rect(s_surf, color, draw_rect, 2, border_radius=4)
            
            draw_pos = (cx - w/2, cy - h/2)
            surface.blit(s_surf, draw_pos)


class MiniBoard:
    def __init__(self, idx):
        self.idx = idx
        self.rect = pygame.Rect(0,0,0,0)
        
        # Animation Properties
        self.claim_opacity = 255.0
        self.winner_symbol_scale = 0.0
        self.claim_glow_opacity = 0.0
        
        self.is_animated = False

    def trigger_win_animation(self):
        self.is_animated = True
        tweener.add(self, "claim_opacity", 255.0, 120.0, 300, "ease_out")
        
        def bounce_back():
            tweener.add(self, "winner_symbol_scale", 1.25, 1.0, 150, "ease_out")
            
        tweener.add(self, "winner_symbol_scale", 0.0, 1.25, 200, "ease_out", callback=bounce_back)
        
        def fade_glow():
            tweener.add(self, "claim_glow_opacity", 255.0, 0.0, 400, "ease_out")
            
        tweener.add(self, "claim_glow_opacity", 0.0, 255.0, 400, "ease_out", callback=fade_glow)

    def draw(self, surface, state):
        logic = state.logic
        
        bx = self.idx % 3
        by = self.idx // 3
        
        start_x = state.start_x
        start_y = state.start_y
        cell_size = state.cell_size
        
        # 1. Draw Small Moves
        for r in range(3):
            for c in range(3):
                val = logic.small_boards[self.idx][r][c]
                if val != "":
                    abs_col = bx * 3 + c
                    abs_row = by * 3 + r
                    
                    center_x = start_x + abs_col * cell_size + cell_size // 2
                    center_y = start_y + abs_row * cell_size + cell_size // 2
                    
                    cell = state.cells[abs_row][abs_col]
                    
                    # Theme Colors
                    base_color = theme_manager.get_color("x_color") if val == "X" else theme_manager.get_color("o_color")
                    
                    text = state.small_font.render(val, True, base_color)
                    
                    if cell.symbol_scale != 1.0:
                         w, h = text.get_size()
                         new_w = int(w * cell.symbol_scale)
                         new_h = int(h * cell.symbol_scale)
                         if new_w > 0 and new_h > 0:
                              text = pygame.transform.scale(text, (new_w, new_h))
                    
                    if self.claim_opacity < 255:
                         text.set_alpha(int(self.claim_opacity))
                    
                    rect = text.get_rect(center=(center_x, center_y + cell.symbol_y_offset))
                    surface.blit(text, rect)

        # 2. Draw Winner Symbol
        symbol = logic.board_states[self.idx]
        if symbol != "" and symbol != "D":
            center_x = self.rect.centerx
            center_y = self.rect.centery
            
            c = theme_manager.get_color("x_color") if symbol == "X" else theme_manager.get_color("o_color")
            
            size = int(100 * self.winner_symbol_scale)
            if size > 0:
                font_big = pygame.font.Font(FONTS["bold"], size)
                text = font_big.render(symbol, True, c)
                rect = text.get_rect(center=(center_x, center_y))
                surface.blit(text, rect)

        # 3. Draw Glow Border
        if self.claim_glow_opacity > 1:
            glow_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            alpha = int(self.claim_glow_opacity)
            c = theme_manager.get_color("glow_color")
            if hasattr(c, "r"): c = (c.r, c.g, c.b)
            pygame.draw.rect(glow_surf, (*c, alpha), glow_surf.get_rect(), 4)
            surface.blit(glow_surf, self.rect.topleft, special_flags=pygame.BLEND_RGBA_ADD)


class GameState:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(FONTS["regular"], FONT_SIZE_NORMAL)
        self.small_font = pygame.font.SysFont("arial", 36, bold=True) 
        self.back_button = None
        
        self.logic = UltimateTicTacToeLogic()
        self.ai = MinimaxAI(depth=3) 
        self.ai_thinking = False
        self.ai_timer = 0
        self.ai_delay_duration = 0
        self.ai_message = ""
        self.pending_move = None
        
        # Cells for hover effects
        self.cells = [[Cell(r, c) for c in range(9)] for r in range(9)]
        self.last_hovered_cell = None
        
        # MiniBoards for win animation
        self.mini_boards = [MiniBoard(i) for i in range(9)]
        
        self.update_dimensions()
        self.x_wins = 0
        self.o_wins = 0
        self.pulse_value = 0
        self.pulse_dir = 1
        self.background_image = None
        
        # Check initial state (e.g. load)
        for i in range(9):
             if self.logic.board_states[i] != "":
                  self.mini_boards[i].winner_symbol_scale = 1.0
                  self.mini_boards[i].claim_opacity = 120.0
                  self.mini_boards[i].is_animated = True

    def update_dimensions(self):
        w, h = self.game.screen.get_size()
        self.board_size = int(h * 0.8)
        self.cell_size = self.board_size // 9
        self.big_cell_size = self.board_size // 3
        self.start_x = (w - self.board_size) // 2
        self.start_y = (h - self.board_size) // 2 + 30
        
        # Update Cell Rects
        for r in range(9):
            for c in range(9):
                rect = pygame.Rect(
                    self.start_x + c * self.cell_size,
                    self.start_y + r * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                self.cells[r][c].rect = rect
                
        # Update MiniBoard Rects
        for i in range(9):
            bx = i % 3
            by = i // 3
            rect = pygame.Rect(
                self.start_x + bx * self.big_cell_size,
                self.start_y + by * self.big_cell_size,
                self.big_cell_size,
                self.big_cell_size
            )
            self.mini_boards[i].rect = rect

        if os.path.exists(GAME_BACKGROUND_IMAGE_PATH):
            try:
                self.background_image = pygame.image.load(GAME_BACKGROUND_IMAGE_PATH)
                self.background_image = pygame.transform.scale(self.background_image, (w, h))
            except: pass

    def enter(self, params=None):
        self.update_dimensions()
        def go_home(): self.game.change_state("home")
        self.back_button = UIButton(10, 10, 100, 40, "Menu", go_home)
        if params == "new_game" or self.logic.game_over:
             self.logic = UltimateTicTacToeLogic() 
             self.ai_thinking = False
             self.pending_move = None
             self.x_wins = 0
             self.o_wins = 0 
             # Reset visual states
             self.mini_boards = [MiniBoard(i) for i in range(9)]
             self.update_dimensions()

    def exit(self): pass

    def run_ai_turn(self):
        move = self.ai.get_best_move(self.logic)
        if move:
            board_idx, r, c = move
            self.logic.make_move(board_idx, r, c)
            self.check_game_over()
        self.ai_thinking = False

    def check_game_over(self):
        if self.logic.game_over:
            sound.play("win")
            self.game.winner = self.logic.winner
            if self.logic.winner == "X": self.x_wins += 1
            elif self.logic.winner == "O": self.o_wins += 1
            self.game.change_state("gameover")

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            self.game.change_state("home")
            return
        if self.ai_thinking: return
        
        # Hover Logic
        if event.type == pygame.MOUSEMOTION and not self.logic.game_over:
             mx, my = event.pos
             found_cell = None
             if self.start_x <= mx < self.start_x + self.board_size and self.start_y <= my < self.start_y + self.board_size:
                  rel_x = mx - self.start_x
                  rel_y = my - self.start_y
                  c = rel_x // self.cell_size
                  r = rel_y // self.cell_size
                  if 0 <= r < 9 and 0 <= c < 9:
                       found_cell = self.cells[r][c]
            
             if found_cell != self.last_hovered_cell:
                  if self.last_hovered_cell:
                       self.last_hovered_cell.on_leave()
                  if found_cell:
                       found_cell.on_enter()
                  self.last_hovered_cell = found_cell

        if event.type == pygame.MOUSEBUTTONDOWN and not self.logic.game_over:
            if event.button == 1:
                mx, my = event.pos
                if self.start_x <= mx < self.start_x + self.board_size and self.start_y <= my < self.start_y + self.board_size:
                    rel_x = mx - self.start_x
                    rel_y = my - self.start_y
                    col_idx = rel_x // self.cell_size
                    row_idx = rel_y // self.cell_size
                    big_row = row_idx // 3
                    big_col = col_idx // 3
                    board_idx = big_row * 3 + big_col
                    local_row = row_idx % 3
                    local_col = col_idx % 3
                    if config.GAME_MODE == "self" or self.logic.current_turn == "X":
                         if self.logic.make_move(board_idx, local_row, local_col):
                             sound.play("move")
                             # Trigger Animation
                             global_r = big_row * 3 + local_row
                             global_c = big_col * 3 + local_col
                             self.cells[global_r][global_c].play_symbol_animation()
                             
                             self.check_game_over()

    def update(self):
        self.back_button.update()
        
        # Check for MiniBoard Animations
        for i in range(9):
             if self.logic.board_states[i] != "" and not self.mini_boards[i].is_animated:
                  self.mini_boards[i].trigger_win_animation()

        if config.GAME_MODE == "computer" and not self.logic.game_over and self.logic.current_turn == "O":
            current_time = pygame.time.get_ticks()
            if not self.ai_thinking:
                self.ai_thinking = True
                self.ai_timer = current_time
                import random
                msgs = ["Thinking...", "Hmm...", "Analyzing...", "Planning...", "Observing...", "Wait...", "Calculating...", "Interesting...", "Nice move...", "Let me see...", "Tricky...", "Winning...", "You sure?", "I see it..."]
                self.ai_message = random.choice(msgs)
                self.ai_delay_duration = random.randint(1500, 3000)
                self.pending_move = self.ai.get_best_move(self.logic)
            else:
                if current_time - self.ai_timer > self.ai_delay_duration:
                    if self.pending_move:
                        board_idx, r, c = self.pending_move
                        sound.play("move")
                        
                        # Trigger Animation
                        big_row = board_idx // 3
                        big_col = board_idx % 3
                        global_r = big_row * 3 + r
                        global_c = big_col * 3 + c
                        self.cells[global_r][global_c].play_symbol_animation()

                        self.logic.make_move(board_idx, r, c)
                        self.check_game_over()
                    self.ai_thinking = False
                    self.pending_move = None

    def draw_pulse_glow(self, surface, rect, color):
        self.pulse_value += self.pulse_dir * 0.05
        if self.pulse_value > 1: self.pulse_dir = -1
        if self.pulse_value < 0: self.pulse_dir = 1
        glow = pygame.Surface((rect.width+20, rect.height+20), pygame.SRCALPHA)
        alpha = int(80 + self.pulse_value * 80)
        
        if hasattr(color, "r"): c = (color.r, color.g, color.b)
        else: c = color[:3]
        
        pygame.draw.rect(glow, (*c, alpha), glow.get_rect(), border_radius=18)
        surface.blit(glow, (rect.x-10, rect.y-10))

    def draw(self, surface):
        if self.background_image:
             surface.blit(self.background_image, (0, 0))
             overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
             overlay.set_alpha(50) 
             overlay.fill((0, 0, 0))
             surface.blit(overlay, (0,0))
        else:
             surface.fill(theme_manager.get_bg_color())
        self.draw_board(surface)
        self.draw_ui(surface)
        self.back_button.draw(surface)

    def draw_ui(self, surface):
        w, h = surface.get_size()
        theme_text_color = theme_manager.get_color("text_color")
        theme_o = theme_manager.get_color("o_color")
        theme_x = theme_manager.get_color("x_color")
        
        if self.ai_thinking:
            ai_font = pygame.font.SysFont("arial", 24, italic=True)
            turn_surf = ai_font.render(f'"{self.ai_message}"', True, theme_o)
        else:
            turn_text = f"{self.logic.current_turn}'s Turn"
            turn_color = theme_x if self.logic.current_turn == "X" else theme_o
            turn_surf = self.font.render(turn_text, True, turn_color)
        turn_rect = turn_surf.get_rect(center=(w // 2, 40))
        surface.blit(turn_surf, turn_rect)

        p1_text = "Player 1"
        p1_symbol = "(X)"
        p1_color = theme_x if self.logic.current_turn == "X" else theme_text_color
        p1_surf = self.font.render(p1_text, True, p1_color)
        p1_rect = p1_surf.get_rect(topleft=(20, 150))
        
        p2_name = "Computer" if config.GAME_MODE == "computer" else "Player 2"
        p2_symbol = "(O)"
        p2_color = theme_o if self.logic.current_turn == "O" else theme_text_color
        p2_surf = self.font.render(p2_name, True, p2_color)
        p2_rect = p2_surf.get_rect(topright=(w - 20, 150))

        if self.logic.current_turn == "X": self.draw_pulse_glow(surface, p1_rect, theme_x)
        else: self.draw_pulse_glow(surface, p2_rect, theme_o)

        p1_sym_surf = self.font.render(p1_symbol, True, theme_x)
        surface.blit(p1_surf, p1_rect)
        surface.blit(p1_sym_surf, (20, 190))
        
        score_x_surf = self.small_font.render(f"Wins: {self.x_wins}", True, theme_text_color)
        surface.blit(score_x_surf, (20, 230))
        
        p2_sym_surf = self.font.render(p2_symbol, True, theme_o)
        p2_sym_rect = p2_sym_surf.get_rect(topright=(w - 20, 190))
        surface.blit(p2_surf, p2_rect)
        surface.blit(p2_sym_surf, p2_sym_rect)

        score_o_surf = self.small_font.render(f"Wins: {self.o_wins}", True, theme_text_color)
        score_o_rect = score_o_surf.get_rect(topright=(w - 20, 230))
        surface.blit(score_o_surf, score_o_rect)

    def draw_board(self, surface):
        if not self.logic.game_over:
            if self.logic.next_board_index != -1:
                bx = self.logic.next_board_index % 3
                by = self.logic.next_board_index // 3
                rect = pygame.Rect(self.start_x + bx * self.big_cell_size, self.start_y + by * self.big_cell_size, self.big_cell_size, self.big_cell_size)
                hl = theme_manager.get_color("highlight_color")
                if hasattr(hl, "r"): hl = (hl.r, hl.g, hl.b)
                pygame.draw.rect(surface, (*hl, 100), rect) 
            else:
                for i, state in enumerate(self.logic.board_states):
                    if state == "":
                        bx = i % 3
                        by = i // 3
                        rect = pygame.Rect(self.start_x + bx * self.big_cell_size, self.start_y + by * self.big_cell_size, self.big_cell_size, self.big_cell_size)
                        hl = theme_manager.get_color("highlight_color")
                        if hasattr(hl, "r"): hl = (hl.r, hl.g, hl.b)
                        pygame.draw.rect(surface, (*hl, 100), rect)

        small_color = theme_manager.get_color("small_grid_color")
        big_color = theme_manager.get_color("big_grid_color")

        for row in range(9):
            for col in range(9):
                rect = pygame.Rect(self.start_x + col * self.cell_size, self.start_y + row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(surface, small_color, rect, 1)

        for i in range(4):
            start_pos_v = (self.start_x + i * self.big_cell_size, self.start_y)
            end_pos_v = (self.start_x + i * self.big_cell_size, self.start_y + self.board_size)
            pygame.draw.line(surface, big_color, start_pos_v, end_pos_v, 5)
            start_pos_h = (self.start_x, self.start_y + i * self.big_cell_size)
            end_pos_h = (self.start_x + self.board_size, self.start_y + i * self.big_cell_size)
            pygame.draw.line(surface, big_color, start_pos_h, end_pos_h, 5)

        for i in range(9):
             self.mini_boards[i].draw(surface, self)
        
        for row in range(9):
            for col in range(9):
                self.cells[row][col].draw(surface)
