
import pygame
import config
from config import *
from ui.button import Button
from engine.ai_minimax import MinimaxAI
import threading

class UltimateTicTacToeLogic:
    def __init__(self):
        # 9 small boards, each 3x3
        # 0 1 2
        # 3 4 5
        # 6 7 8
        self.small_boards = [[["" for _ in range(3)] for _ in range(3)] for _ in range(9)]
        # State of small boards: "" (playing), "X", "O", "D" (Draw)
        self.board_states = ["" for _ in range(9)]
        
        self.current_turn = "X"
        self.next_board_index = -1 # -1 means any board is valid (free move)
        self.winner = None
        self.game_over = False

    def check_small_board_win(self, board_index):
        b = self.small_boards[board_index]
        
        # Check rows
        for row in range(3):
            if b[row][0] == b[row][1] == b[row][2] and b[row][0] != "":
                return b[row][0]
                
        # Check cols
        for col in range(3):
            if b[0][col] == b[1][col] == b[2][col] and b[0][col] != "":
                return b[0][col]
        
        # Check diagonals
        if b[0][0] == b[1][1] == b[2][2] and b[0][0] != "":
            return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] and b[0][2] != "":
            return b[0][2]
            
        # Check Draw (Full board)
        is_full = True
        for r in range(3):
            for c in range(3):
                if b[r][c] == "":
                    is_full = False
                    break
        if is_full:
            return "D"
            
        return ""

    def check_big_board_win(self):
        b = self.board_states
        # Win patterns (rows, cols, diags) - indices 0-8
        wins = [
            (0,1,2), (3,4,5), (6,7,8), # rows
            (0,3,6), (1,4,7), (2,5,8), # cols
            (0,4,8), (2,4,6) # diags
        ]
        
        for p in wins:
            if b[p[0]] == b[p[1]] == b[p[2]] and b[p[0]] in ["X", "O"]:
                return b[p[0]]
                
        # Check Draw
        if "" not in b:
            return "D"
        
        return None

    def make_move(self, board_idx, row, col):
        if self.game_over:
            return False
            
        # Validate Move
        # 1. Must be in the correct board (unless free move)
        if self.next_board_index != -1 and board_idx != self.next_board_index:
            return False
            
        # 2. Target board must be active (not won/full)
        if self.board_states[board_idx] != "":
            return False
            
        # 3. Target cell must be empty
        if self.small_boards[board_idx][row][col] != "":
            return False
            
        # EXECUTE MOVE
        self.small_boards[board_idx][row][col] = self.current_turn
        
        # Check for small board win
        sb_win = self.check_small_board_win(board_idx)
        if sb_win:
            self.board_states[board_idx] = sb_win
            
        # Check for big board win
        bb_win = self.check_big_board_win()
        if bb_win:
            self.winner = bb_win
            self.game_over = True
            return True
            
        # Update Turn
        self.current_turn = "O" if self.current_turn == "X" else "X"
        
        # Determine Next Board
        # The next board is determined by the relative position (row, col) in the small board
        next_idx = row * 3 + col
        
        if self.board_states[next_idx] != "":
            self.next_board_index = -1 # Free Move
        else:
            self.next_board_index = next_idx
            
        return True

class GameState:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_NORMAL)
        self.small_font = pygame.font.SysFont(FONT_NAME, 20)
        self.back_button = None
        
        self.logic = UltimateTicTacToeLogic()
        self.ai = MinimaxAI(depth=3) # Set depth to 3 for performance
        self.ai_thinking = False
        
        # Board Dimensions
        self.board_size = 450
        self.cell_size = self.board_size // 9
        self.big_cell_size = self.board_size // 3
        # Center the board
        self.start_x = (SCREEN_WIDTH - self.board_size) // 2
        self.start_y = (SCREEN_HEIGHT - self.board_size) // 2 + 20 

        self.x_wins = 0
        self.o_wins = 0

    def enter(self):
        self.back_button = Button(10, 10, 100, 40, "Menu", self.small_font, bg_color=GRAY, sound_path=CLICK_SOUND_PATH)
        self.logic = UltimateTicTacToeLogic() # Reset game on enter
        self.ai_thinking = False

    def exit(self):
        pass

    def run_ai_turn(self):
        """Run AI in a separate thread/process if blocking, but here simple blocking call since simple logic"""
        move = self.ai.get_best_move(self.logic)
        if move:
            board_idx, r, c = move
            self.logic.make_move(board_idx, r, c)
            self.check_game_over()
        self.ai_thinking = False

    def check_game_over(self):
        if self.logic.game_over:
            self.game.winner = self.logic.winner
            if self.logic.winner == "X":
                self.x_wins += 1
            elif self.logic.winner == "O":
                self.o_wins += 1
            self.game.change_state("gameover")

    def handle_event(self, event):
        if self.back_button.handle_event(event):
            self.game.change_state("home")
            return

        # Disable input if AI is thinking
        if self.ai_thinking:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and not self.logic.game_over:
            if event.button == 1: # Left click
                mx, my = event.pos
                
                # Check if click is inside board area
                if self.start_x <= mx < self.start_x + self.board_size and \
                   self.start_y <= my < self.start_y + self.board_size:
                       
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
                             self.check_game_over()
                            
    def update(self):
        # Trigger AI Turn
        if config.GAME_MODE == "computer" and \
           not self.logic.game_over and \
           self.logic.current_turn == "O" and \
           not self.ai_thinking:
            
            self.ai_thinking = True
            # For now, running on main thread directly is slightly safer for Pygame compatibility without complex threading
            # If it lags, we can optimize or use threading with caution
            self.run_ai_turn()

    def draw(self, surface):
        surface.fill(COLOR_BG)
        
        self.draw_board(surface)
        self.draw_ui(surface)
        
        self.back_button.draw(surface)

    def draw_board(self, surface):
        # 1. Highlight Valid Boards
        if not self.logic.game_over:
            if self.logic.next_board_index != -1:
                # Highlight specific board
                bx = self.logic.next_board_index % 3
                by = self.logic.next_board_index // 3
                rect = pygame.Rect(
                    self.start_x + bx * self.big_cell_size,
                    self.start_y + by * self.big_cell_size,
                    self.big_cell_size,
                    self.big_cell_size
                )
                pygame.draw.rect(surface, (50, 60, 50), rect) # Subtle highlight
            else:
                # Highlight all active boards
                for i, state in enumerate(self.logic.board_states):
                    if state == "":
                        bx = i % 3
                        by = i // 3
                        rect = pygame.Rect(
                            self.start_x + bx * self.big_cell_size,
                            self.start_y + by * self.big_cell_size,
                            self.big_cell_size,
                            self.big_cell_size
                        )
                        pygame.draw.rect(surface, (50, 60, 50), rect)

        # 2. Draw Grid Lines
        # Small Grid (Internal lines)
        for row in range(9):
            for col in range(9):
                rect = pygame.Rect(
                    self.start_x + col * self.cell_size,
                    self.start_y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(surface, COLOR_SMALL_BORDER, rect, 1)

        # Big Grid (Thick lines)
        for i in range(4):
            # Vertical
            start_pos_v = (self.start_x + i * self.big_cell_size, self.start_y)
            end_pos_v = (self.start_x + i * self.big_cell_size, self.start_y + self.board_size)
            pygame.draw.line(surface, COLOR_BIG_BORDER, start_pos_v, end_pos_v, 5)
            
            # Horizontal
            start_pos_h = (self.start_x, self.start_y + i * self.big_cell_size)
            end_pos_h = (self.start_x + self.board_size, self.start_y + i * self.big_cell_size)
            pygame.draw.line(surface, COLOR_BIG_BORDER, start_pos_h, end_pos_h, 5)

        # 3. Draw Moves (X and O)
        for b_idx in range(9):
            # If board is won, draw big symbol
            if self.logic.board_states[b_idx] != "":
                symbol = self.logic.board_states[b_idx]
                bx = b_idx % 3
                by = b_idx // 3
                
                center_x = self.start_x + bx * self.big_cell_size + self.big_cell_size // 2
                center_y = self.start_y + by * self.big_cell_size + self.big_cell_size // 2
                
                if symbol != "D":
                    color = (COLOR_X if symbol == "X" else COLOR_O) + (100,)
                    font_big = pygame.font.SysFont(FONT_NAME, 100, bold=True)
                    text = font_big.render(symbol, True, color if symbol == "X" else COLOR_O)
                    rect = text.get_rect(center=(center_x, center_y))
                    surface.blit(text, rect)
            
            # Always draw small moves
            for r in range(3):
                for c in range(3):
                    val = self.logic.small_boards[b_idx][r][c]
                    if val != "":
                        bx = b_idx % 3
                        by = b_idx // 3
                        
                        abs_col = bx * 3 + c
                        abs_row = by * 3 + r
                        
                        center_x = self.start_x + abs_col * self.cell_size + self.cell_size // 2
                        center_y = self.start_y + abs_row * self.cell_size + self.cell_size // 2
                        
                        color = COLOR_X if val == "X" else COLOR_O
                        text = self.small_font.render(val, True, color)
                        rect = text.get_rect(center=(center_x, center_y))
                        surface.blit(text, rect)

    def draw_ui(self, surface):
        # Turn Indicator
        turn_text = f"{self.logic.current_turn}'s Turn"
        if self.ai_thinking:
            turn_text = "Computer Thinking..."
        
        turn_color = COLOR_X if self.logic.current_turn == "X" else COLOR_O
        turn_surf = self.font.render(turn_text, True, turn_color)
        turn_rect = turn_surf.get_rect(center=(SCREEN_WIDTH // 2, 40))
        surface.blit(turn_surf, turn_rect)

        # Player 1
        p1_text = "Player 1"
        p1_symbol = "(X)"
        p1_color = COLOR_X if self.logic.current_turn == "X" else WHITE
        
        p1_surf = self.font.render(p1_text, True, p1_color)
        p1_sym_surf = self.font.render(p1_symbol, True, COLOR_X)
        
        surface.blit(p1_surf, (20, 150))
        surface.blit(p1_sym_surf, (20, 190))
        
        score_x_surf = self.small_font.render(f"Wins: {self.x_wins}", True, WHITE)
        surface.blit(score_x_surf, (20, 230))

        # Player 2
        p2_name = "Computer" if config.GAME_MODE == "computer" else "Player 2"
        p2_symbol = "(O)"
        p2_color = COLOR_O if self.logic.current_turn == "O" else WHITE
        
        p2_surf = self.font.render(p2_name, True, p2_color)
        p2_sym_surf = self.font.render(p2_symbol, True, COLOR_O)
        
        p2_rect = p2_surf.get_rect(topright=(SCREEN_WIDTH - 20, 150))
        p2_sym_rect = p2_sym_surf.get_rect(topright=(SCREEN_WIDTH - 20, 190))
        
        surface.blit(p2_surf, p2_rect)
        surface.blit(p2_sym_surf, p2_sym_rect)

        score_o_surf = self.small_font.render(f"Wins: {self.o_wins}", True, WHITE)
        score_o_rect = score_o_surf.get_rect(topright=(SCREEN_WIDTH - 20, 230))
        surface.blit(score_o_surf, score_o_rect)
