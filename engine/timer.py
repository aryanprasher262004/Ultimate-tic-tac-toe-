"""
Chess-clock style timer system for Ultimate Tic Tac Toe
Supports 3m, 5m, and 10m game modes with per-player time tracking
"""

class GameTimer:
    def __init__(self):
        self.player1_time_ms = 0
        self.player2_time_ms = 0
        self.active_player = 1  # 1 or 2
        self.is_running = False
        self.mode = None
        
    def start(self, mode="10m"):
        """
        Initialize timers based on mode
        Args:
            mode: "3m", "5m", or "10m"
        """
        self.mode = mode
        
        # Convert mode to milliseconds
        time_map = {
            "3m": 3 * 60 * 1000,   # 3 minutes
            "5m": 5 * 60 * 1000,   # 5 minutes
            "10m": 10 * 60 * 1000  # 10 minutes
        }
        
        initial_time = time_map.get(mode, 10 * 60 * 1000)
        self.player1_time_ms = initial_time
        self.player2_time_ms = initial_time
        self.active_player = 1
        self.is_running = True
        
    def update(self, dt):
        """
        Update the active player's timer
        Args:
            dt: Delta time in seconds
        """
        if not self.is_running:
            return
            
        dt_ms = dt * 1000  # Convert to milliseconds
        
        if self.active_player == 1:
            self.player1_time_ms = max(0, self.player1_time_ms - dt_ms)
        elif self.active_player == 2:
            self.player2_time_ms = max(0, self.player2_time_ms - dt_ms)
    
    def switch_turn(self):
        """Switch the active player (called when turn changes)"""
        if self.active_player == 1:
            self.active_player = 2
        else:
            self.active_player = 1
    
    def pause(self):
        """Pause the timer"""
        self.is_running = False
    
    def resume(self):
        """Resume the timer"""
        self.is_running = True
    
    def stop(self):
        """Stop the timer completely"""
        self.is_running = False
    
    def is_out_of_time(self):
        """
        Check if any player has run out of time
        Returns:
            1 if player 1 is out of time
            2 if player 2 is out of time
            None if both players have time remaining
        """
        if self.player1_time_ms <= 0:
            return 1
        if self.player2_time_ms <= 0:
            return 2
        return None
    
    def get_time_string(self, player):
        """
        Get formatted time string for a player
        Args:
            player: 1 or 2
        Returns:
            String in MM:SS format
        """
        if player == 1:
            time_ms = self.player1_time_ms
        elif player == 2:
            time_ms = self.player2_time_ms
        else:
            return "00:00"
        
        # Convert to seconds
        total_seconds = int(time_ms / 1000)
        
        # Calculate minutes and seconds
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_time_ms(self, player):
        """Get raw time in milliseconds for a player"""
        if player == 1:
            return self.player1_time_ms
        elif player == 2:
            return self.player2_time_ms
        return 0
    
    def reset(self):
        """Reset the timer to initial state"""
        self.player1_time_ms = 0
        self.player2_time_ms = 0
        self.active_player = 1
        self.is_running = False
        self.mode = None


# Global timer instance
game_timer = GameTimer()
