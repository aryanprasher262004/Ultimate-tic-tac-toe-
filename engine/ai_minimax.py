
import copy
import random

WIN_SCORE = 10000
SMALL_WIN_SCORE = 100
BLOCK_SCORE = 50
CENTER_SCORE = 10

class MinimaxAI:
    def __init__(self, depth=4):
        self.max_depth = depth
        self.node_count = 0

    def get_best_move(self, logic_state):
        self.node_count = 0
        # Clone state to avoid mutating actual game
        # Note: logic_state needs to be pickle-able or explicitly copyable. 
        # Deepcopy is safest but slow. For UTTT it might be okay for depth 4.
        root_state = copy.deepcopy(logic_state)
        
        best_score = -float('inf')
        best_move = None
        
        # Get all legal moves
        moves = self.get_legal_moves(root_state)
        
        # If no moves, return None
        if not moves:
            return None
            
        # Shuffle moves to add variety if scores are equal
        random.shuffle(moves)

        alpha = -float('inf')
        beta = float('inf')

        for move in moves:
            board_idx, r, c = move
            
            # Simulate move
            next_state = copy.deepcopy(root_state)
            next_state.make_move(board_idx, r, c)
            
            score = self.minimax(next_state, self.max_depth - 1, alpha, beta, False)
            
            if score > best_score:
                best_score = score
                best_move = move
                
            alpha = max(alpha, best_score)
            
        print(f"AI Selected Move: {best_move} Score: {best_score} Nodes: {self.node_count}")
        return best_move

    def minimax(self, state, depth, alpha, beta, is_maximizing):
        self.node_count += 1
        
        # Terminal conditions or max depth
        if state.game_over:
            if state.winner == "O": # AI is 'O'
                return WIN_SCORE + depth
            elif state.winner == "X":
                return -WIN_SCORE - depth
            else:
                return 0 # Draw
                
        if depth == 0:
            return self.evaluate(state)
            
        moves = self.get_legal_moves(state)
        
        if is_maximizing:
            max_eval = -float('inf')
            for move in moves:
                board_idx, r, c = move
                next_state = copy.deepcopy(state)
                next_state.make_move(board_idx, r, c)
                
                eval = self.minimax(next_state, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                board_idx, r, c = move
                next_state = copy.deepcopy(state)
                next_state.make_move(board_idx, r, c)
                
                eval = self.minimax(next_state, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_legal_moves(self, state):
        moves = []
        
        # If free move (-1), check all active boards
        target_boards = []
        if state.next_board_index == -1:
            for i in range(9):
                if state.board_states[i] == "":
                    target_boards.append(i)
        else:
            # Must play in specific board if active
            if state.board_states[state.next_board_index] == "":
                target_boards.append(state.next_board_index)
            else:
                # Fallback (should be covered by -1 logic, but just in case)
                 for i in range(9):
                    if state.board_states[i] == "":
                        target_boards.append(i)

        for b_idx in target_boards:
            for r in range(3):
                for c in range(3):
                    if state.small_boards[b_idx][r][c] == "":
                        moves.append((b_idx, r, c))
        return moves

    def evaluate(self, state):
        score = 0
        
        # Evaluate Big Board
        score += self.evaluate_board(state.board_states) * 10
        
        # Evaluate Small Boards
        for i in range(9):
            # Only eval active boards, adds nuance
            if state.board_states[i] == "":
                 # Convert 3x3 array to list for common eval
                 flat_board = []
                 for r in range(3):
                     for c in range(3):
                         flat_board.append(state.small_boards[i][r][c])
                 score += self.evaluate_board(flat_board)
        
        return score

    def evaluate_board(self, board_list):
        # Heuristic for a single board (big or small)
        # board_list is size 9
        score = 0
        lines = [
            (0,1,2), (3,4,5), (6,7,8), # rows
            (0,3,6), (1,4,7), (2,5,8), # cols
            (0,4,8), (2,4,6) # diags
        ]
        
        for p in lines:
            line = [board_list[p[0]], board_list[p[1]], board_list[p[2]]]
            score += self.evaluate_line(line)
            
        return score

    def evaluate_line(self, line):
        o_count = line.count("O")
        x_count = line.count("X")
        empty_count = line.count("")
        
        score = 0
        if o_count == 3:
            score += 100
        elif o_count == 2 and empty_count == 1:
            score += 10
        elif o_count == 1 and empty_count == 2:
            score += 1
            
        if x_count == 3:
            score -= 100
        elif x_count == 2 and empty_count == 1:
            score -= 10
        elif x_count == 1 and empty_count == 2:
            score -= 1
            
        return score
