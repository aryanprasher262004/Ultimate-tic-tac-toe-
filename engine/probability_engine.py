"""
Monte Carlo Win Probability Evaluator for Ultimate Tic-Tac-Toe
Uses random simulations with heuristic weighting to estimate win probabilities.
"""

import random
import copy


class ProbabilityEngine:
    """
    Monte Carlo simulation engine for evaluating win probabilities
    in Ultimate Tic-Tac-Toe.
    """
    
    def __init__(self):
        # Weights for heuristic move selection
        self.CAPTURED_BOARD_WEIGHT = 3.0
        self.THREAT_WEIGHT = 2.5
        self.CENTER_WEIGHT = 1.5
        self.CORNER_WEIGHT = 1.2
        
    def evaluate_win_probabilities(self, game_state, simulations=200):
        """
        Returns (win_prob, lose_prob, draw_prob)
        Each value is float between 0 and 1.
        
        Args:
            game_state: UltimateTicTacToeLogic instance
            simulations: Number of Monte Carlo simulations to run
            
        Returns:
            tuple: (win_prob, lose_prob, draw_prob) for current player
        """
        if game_state.game_over:
            # Game already over, return definitive probabilities
            if game_state.winner == game_state.current_turn:
                return (1.0, 0.0, 0.0)
            elif game_state.winner == "D":
                return (0.0, 0.0, 1.0)
            else:
                return (0.0, 1.0, 0.0)
        
        wins = 0
        losses = 0
        draws = 0
        
        current_player = game_state.current_turn
        
        for _ in range(simulations):
            result = self._simulate_game(game_state, current_player)
            
            if result == current_player:
                wins += 1
            elif result == "D":
                draws += 1
            else:
                losses += 1
        
        total = simulations
        win_prob = wins / total
        lose_prob = losses / total
        draw_prob = draws / total
        
        return (win_prob, lose_prob, draw_prob)
    
    def _simulate_game(self, original_state, original_player):
        """
        Simulate a single game from the current state to completion.
        Uses heuristic-weighted random moves.
        
        Returns:
            str: Winner ("X", "O", or "D" for draw)
        """
        # Deep copy the game state
        state = self._copy_game_state(original_state)
        
        # Play until game ends
        max_moves = 81  # Safety limit
        moves_made = 0
        
        while not state.game_over and moves_made < max_moves:
            move = self._get_weighted_random_move(state)
            
            if move is None:
                # No valid moves (shouldn't happen, but safety check)
                break
            
            board_idx, row, col = move
            state.make_move(board_idx, row, col)
            moves_made += 1
        
        return state.winner if state.winner else "D"
    
    def _get_weighted_random_move(self, state):
        """
        Get a random move weighted by heuristics.
        Better moves have higher probability of being selected.
        
        Returns:
            tuple: (board_idx, row, col) or None if no valid moves
        """
        valid_moves = self._get_valid_moves(state)
        
        if not valid_moves:
            return None
        
        # Calculate weights for each move
        move_weights = []
        for move in valid_moves:
            weight = self._evaluate_move_quality(state, move)
            move_weights.append(weight)
        
        # Select move based on weights
        total_weight = sum(move_weights)
        if total_weight == 0:
            # All weights are 0, choose uniformly
            return random.choice(valid_moves)
        
        # Weighted random selection
        rand_val = random.uniform(0, total_weight)
        cumulative = 0
        
        for move, weight in zip(valid_moves, move_weights):
            cumulative += weight
            if rand_val <= cumulative:
                return move
        
        # Fallback (shouldn't reach here)
        return valid_moves[-1]
    
    def _evaluate_move_quality(self, state, move):
        """
        Evaluate the quality of a move using heuristics.
        Higher score = better move.
        
        Args:
            state: Current game state
            move: (board_idx, row, col)
            
        Returns:
            float: Quality score for the move
        """
        board_idx, row, col = move
        score = 1.0  # Base score
        
        # Heuristic 1: Prioritize moves that can capture a small board
        if self._can_capture_board(state, board_idx, row, col):
            score *= self.CAPTURED_BOARD_WEIGHT
        
        # Heuristic 2: Prioritize moves that create threats in big board
        if self._creates_big_board_threat(state, board_idx):
            score *= self.THREAT_WEIGHT
        
        # Heuristic 3: Prefer center positions
        if self._is_center_position(row, col):
            score *= self.CENTER_WEIGHT
        
        # Heuristic 4: Prefer corner positions (secondary to center)
        elif self._is_corner_position(row, col):
            score *= self.CORNER_WEIGHT
        
        # Heuristic 5: Avoid sending opponent to already captured boards
        next_board_idx = row * 3 + col
        if state.board_states[next_board_idx] != "":
            score *= 1.3  # Slight bonus for giving opponent free choice
        
        return score
    
    def _can_capture_board(self, state, board_idx, row, col):
        """
        Check if this move would capture the small board.
        """
        # Create temporary state to test
        temp_state = self._copy_game_state(state)
        temp_state.small_boards[board_idx][row][col] = temp_state.current_turn
        
        # Check if this wins the small board
        winner = temp_state.check_small_board_win(board_idx)
        return winner == temp_state.current_turn
    
    def _creates_big_board_threat(self, state, board_idx):
        """
        Check if capturing this board would create a threat (2 in a row) on big board.
        """
        # First check if this move can capture the board
        current_player = state.current_turn
        
        # Simulate capturing this board
        temp_board_states = state.board_states.copy()
        temp_board_states[board_idx] = current_player
        
        # Check for two-in-a-row patterns
        win_patterns = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        
        for pattern in win_patterns:
            player_count = sum(1 for idx in pattern if temp_board_states[idx] == current_player)
            empty_count = sum(1 for idx in pattern if temp_board_states[idx] == "")
            
            # Two of ours and one empty = threat
            if player_count == 2 and empty_count == 1:
                return True
        
        return False
    
    def _is_center_position(self, row, col):
        """Check if position is center of a 3x3 board."""
        return row == 1 and col == 1
    
    def _is_corner_position(self, row, col):
        """Check if position is a corner of a 3x3 board."""
        return (row, col) in [(0, 0), (0, 2), (2, 0), (2, 2)]
    
    def _get_valid_moves(self, state):
        """
        Get all valid moves for the current state.
        
        Returns:
            list: List of (board_idx, row, col) tuples
        """
        valid_moves = []
        
        # Determine which boards we can play in
        if state.next_board_index != -1:
            # Must play in specific board
            boards_to_check = [state.next_board_index]
        else:
            # Can play in any uncaptured board
            boards_to_check = [i for i in range(9) if state.board_states[i] == ""]
        
        # Find all valid cells in allowed boards
        for board_idx in boards_to_check:
            for row in range(3):
                for col in range(3):
                    if state.small_boards[board_idx][row][col] == "":
                        valid_moves.append((board_idx, row, col))
        
        return valid_moves
    
    def _copy_game_state(self, state):
        """
        Create a deep copy of the game state.
        
        Args:
            state: UltimateTicTacToeLogic instance
            
        Returns:
            UltimateTicTacToeLogic: Deep copy of the state
        """
        # Import here to avoid circular dependency
        from states.game import UltimateTicTacToeLogic
        
        new_state = UltimateTicTacToeLogic()
        
        # Deep copy small boards
        new_state.small_boards = [
            [row.copy() for row in board]
            for board in state.small_boards
        ]
        
        # Copy board states
        new_state.board_states = state.board_states.copy()
        
        # Copy game state variables
        new_state.current_turn = state.current_turn
        new_state.next_board_index = state.next_board_index
        new_state.winner = state.winner
        new_state.game_over = state.game_over
        
        return new_state


# Global instance for easy access
probability_engine = ProbabilityEngine()


def evaluate_win_probabilities(game_state, simulations=200):
    """
    Convenience function to evaluate win probabilities.
    
    Args:
        game_state: UltimateTicTacToeLogic instance
        simulations: Number of Monte Carlo simulations (default: 200)
    
    Returns:
        tuple: (win_prob, lose_prob, draw_prob)
               Each value is float between 0 and 1.
    
    Example:
        >>> from engine.probability_engine import evaluate_win_probabilities
        >>> win_prob, lose_prob, draw_prob = evaluate_win_probabilities(game.logic)
        >>> print(f"Win: {win_prob:.1%}, Lose: {lose_prob:.1%}, Draw: {draw_prob:.1%}")
    """
    return probability_engine.evaluate_win_probabilities(game_state, simulations)
