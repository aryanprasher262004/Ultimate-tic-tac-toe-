"""
Test script for the game timer module
"""
import sys
sys.path.insert(0, 'd:/ALL PROJECTS/Ultimate tic tak toe')

from engine.timer import game_timer

# Test 1: Initialize 3-minute timer
print("=== Test 1: Initialize 3-minute timer ===")
game_timer.start("3m")
print(f"Player 1 time: {game_timer.get_time_string(1)}")
print(f"Player 2 time: {game_timer.get_time_string(2)}")
print(f"Active player: {game_timer.active_player}")
print(f"Is running: {game_timer.is_running}")

# Test 2: Update timer (simulate 1 second)
print("\n=== Test 2: Update timer (1 second) ===")
game_timer.update(1.0)
print(f"Player 1 time: {game_timer.get_time_string(1)}")
print(f"Player 2 time: {game_timer.get_time_string(2)}")

# Test 3: Switch turn
print("\n=== Test 3: Switch turn ===")
game_timer.switch_turn()
print(f"Active player: {game_timer.active_player}")
game_timer.update(1.0)
print(f"Player 1 time: {game_timer.get_time_string(1)}")
print(f"Player 2 time: {game_timer.get_time_string(2)}")

# Test 4: Pause and resume
print("\n=== Test 4: Pause and resume ===")
game_timer.pause()
print(f"Is running: {game_timer.is_running}")
game_timer.update(5.0)  # Should not update
print(f"Player 2 time (should be same): {game_timer.get_time_string(2)}")
game_timer.resume()
game_timer.update(1.0)
print(f"Player 2 time (should decrease): {game_timer.get_time_string(2)}")

# Test 5: Time out scenario
print("\n=== Test 5: Time out scenario ===")
game_timer.player2_time_ms = 500  # 0.5 seconds left
game_timer.update(1.0)  # Update by 1 second
print(f"Player 2 time: {game_timer.get_time_string(2)}")
print(f"Out of time: Player {game_timer.is_out_of_time()}")

# Test 6: Different modes
print("\n=== Test 6: Different time modes ===")
for mode in ["3m", "5m", "10m"]:
    game_timer.start(mode)
    print(f"{mode} mode - P1: {game_timer.get_time_string(1)}, P2: {game_timer.get_time_string(2)}")

print("\n✅ All tests completed!")
