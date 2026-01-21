"""
Test script for the Monte Carlo Probability Engine
Demonstrates the probability evaluator with various game states.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from states.game import UltimateTicTacToeLogic
from engine.probability_engine import evaluate_win_probabilities


def print_board_state(logic):
    """Print a visual representation of the big board state."""
    print("\n=== Big Board State ===")
    for i in range(3):
        row = []
        for j in range(3):
            idx = i * 3 + j
            state = logic.board_states[idx]
            if state == "":
                row.append("·")
            else:
                row.append(state)
        print(" | ".join(row))
        if i < 2:
            print("---------")
    print()


def test_empty_board():
    """Test probability on an empty board (should be roughly equal)."""
    print("\n" + "="*60)
    print("TEST 1: Empty Board")
    print("="*60)
    
    logic = UltimateTicTacToeLogic()
    print_board_state(logic)
    print(f"Current turn: {logic.current_turn}")
    
    win_prob, lose_prob, draw_prob = evaluate_win_probabilities(logic, simulations=500)
    
    print(f"\nProbabilities for {logic.current_turn}:")
    print(f"  Win:  {win_prob:.1%}")
    print(f"  Lose: {lose_prob:.1%}")
    print(f"  Draw: {draw_prob:.1%}")


def test_mid_game():
    """Test probability in a mid-game scenario."""
    print("\n" + "="*60)
    print("TEST 2: Mid-Game Scenario")
    print("="*60)
    
    logic = UltimateTicTacToeLogic()
    
    # Simulate some moves
    # X captures board 0
    logic.make_move(0, 0, 0)  # X in board 0
    logic.make_move(0, 1, 1)  # O in board 0
    logic.make_move(1, 0, 1)  # X in board 1
    logic.make_move(1, 1, 0)  # O in board 1
    logic.make_move(0, 0, 2)  # X in board 0
    logic.make_move(2, 1, 1)  # O in board 2
    logic.make_move(1, 0, 0)  # X in board 1 (captures it)
    
    print_board_state(logic)
    print(f"Current turn: {logic.current_turn}")
    print(f"Next board: {logic.next_board_index if logic.next_board_index != -1 else 'Any'}")
    
    win_prob, lose_prob, draw_prob = evaluate_win_probabilities(logic, simulations=500)
    
    print(f"\nProbabilities for {logic.current_turn}:")
    print(f"  Win:  {win_prob:.1%}")
    print(f"  Lose: {lose_prob:.1%}")
    print(f"  Draw: {draw_prob:.1%}")


def test_winning_position():
    """Test probability when one player has a strong advantage."""
    print("\n" + "="*60)
    print("TEST 3: Strong Position for X")
    print("="*60)
    
    logic = UltimateTicTacToeLogic()
    
    # X captures boards 0, 1, 4 (has a threat)
    # Board 0
    logic.small_boards[0][0][0] = "X"
    logic.small_boards[0][0][1] = "X"
    logic.small_boards[0][0][2] = "X"
    logic.board_states[0] = "X"
    
    # Board 1
    logic.small_boards[1][1][0] = "X"
    logic.small_boards[1][1][1] = "X"
    logic.small_boards[1][1][2] = "X"
    logic.board_states[1] = "X"
    
    # Board 4
    logic.small_boards[4][2][0] = "X"
    logic.small_boards[4][2][1] = "X"
    logic.small_boards[4][2][2] = "X"
    logic.board_states[4] = "X"
    
    # O has board 3
    logic.small_boards[3][0][0] = "O"
    logic.small_boards[3][1][1] = "O"
    logic.small_boards[3][2][2] = "O"
    logic.board_states[3] = "O"
    
    logic.current_turn = "X"
    logic.next_board_index = -1
    
    print_board_state(logic)
    print(f"Current turn: {logic.current_turn}")
    print(f"X has boards: 0, 1, 4 (threat on row 0 and diagonal!)")
    
    win_prob, lose_prob, draw_prob = evaluate_win_probabilities(logic, simulations=500)
    
    print(f"\nProbabilities for {logic.current_turn}:")
    print(f"  Win:  {win_prob:.1%}")
    print(f"  Lose: {lose_prob:.1%}")
    print(f"  Draw: {draw_prob:.1%}")


def test_game_over():
    """Test probability when game is already over."""
    print("\n" + "="*60)
    print("TEST 4: Game Already Won")
    print("="*60)
    
    logic = UltimateTicTacToeLogic()
    
    # X wins with boards 0, 1, 2
    logic.board_states[0] = "X"
    logic.board_states[1] = "X"
    logic.board_states[2] = "X"
    logic.winner = "X"
    logic.game_over = True
    logic.current_turn = "X"
    
    print_board_state(logic)
    print(f"Game Over! Winner: {logic.winner}")
    
    win_prob, lose_prob, draw_prob = evaluate_win_probabilities(logic, simulations=100)
    
    print(f"\nProbabilities for {logic.current_turn}:")
    print(f"  Win:  {win_prob:.1%}")
    print(f"  Lose: {lose_prob:.1%}")
    print(f"  Draw: {draw_prob:.1%}")


def test_performance():
    """Test performance with different simulation counts."""
    print("\n" + "="*60)
    print("TEST 5: Performance Comparison")
    print("="*60)
    
    import time
    
    logic = UltimateTicTacToeLogic()
    
    # Make a few moves
    logic.make_move(4, 1, 1)  # X center
    logic.make_move(4, 0, 0)  # O corner
    logic.make_move(0, 1, 1)  # X
    
    simulation_counts = [50, 100, 200, 500, 1000]
    
    print(f"Current turn: {logic.current_turn}")
    print("\nSimulation Count | Time (ms) | Win% | Lose% | Draw%")
    print("-" * 60)
    
    for sim_count in simulation_counts:
        start_time = time.time()
        win_prob, lose_prob, draw_prob = evaluate_win_probabilities(logic, simulations=sim_count)
        elapsed_ms = (time.time() - start_time) * 1000
        
        print(f"{sim_count:15d} | {elapsed_ms:8.1f} | {win_prob:4.1%} | {lose_prob:5.1%} | {draw_prob:5.1%}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("MONTE CARLO PROBABILITY ENGINE - TEST SUITE")
    print("="*60)
    
    test_empty_board()
    test_mid_game()
    test_winning_position()
    test_game_over()
    test_performance()
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60 + "\n")
