
import json
import os
import config

SAVE_FILE = "user_settings.json"

def save_settings():
    data = {
        "MUSIC_VOLUME": config.MUSIC_VOLUME,
        "MUSIC_ENABLED": config.MUSIC_ENABLED,
        "SFX_VOLUME": config.SFX_VOLUME,
        "SFX_ENABLED": config.SFX_ENABLED,
        "GAME_MODE": config.GAME_MODE,
        "SCREEN_WIDTH": config.SCREEN_WIDTH,
        "SCREEN_HEIGHT": config.SCREEN_HEIGHT,
        "FULLSCREEN": config.FULLSCREEN,
        "CURRENT_THEME": config.CURRENT_THEME,
        "PLAYER_SYMBOL": config.PLAYER_SYMBOL

    }
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f)
        print("Settings saved.")
    except Exception as e:
        print(f"Error saving settings: {e}")

def load_settings():
    if not os.path.exists(SAVE_FILE):
        return

    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            
        if "MUSIC_VOLUME" in data: config.MUSIC_VOLUME = data["MUSIC_VOLUME"]
        if "MUSIC_ENABLED" in data: config.MUSIC_ENABLED = data["MUSIC_ENABLED"]
        if "SFX_VOLUME" in data: config.SFX_VOLUME = data["SFX_VOLUME"]
        if "SFX_ENABLED" in data: config.SFX_ENABLED = data["SFX_ENABLED"]
        if "GAME_MODE" in data: config.GAME_MODE = data["GAME_MODE"]
        if "SCREEN_WIDTH" in data: config.SCREEN_WIDTH = data["SCREEN_WIDTH"]
        if "SCREEN_HEIGHT" in data: config.SCREEN_HEIGHT = data["SCREEN_HEIGHT"]
        if "FULLSCREEN" in data: config.FULLSCREEN = data["FULLSCREEN"]
        if "CURRENT_THEME" in data: config.CURRENT_THEME = data["CURRENT_THEME"]
        if "PLAYER_SYMBOL" in data: config.PLAYER_SYMBOL = data["PLAYER_SYMBOL"]

        
        print("Settings loaded.")
    except Exception as e:
        print(f"Error loading settings: {e}")
