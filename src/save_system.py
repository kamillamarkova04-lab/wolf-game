"""
Save System - Handles game state persistence
"""

import json
import os
from datetime import datetime
from config import SAVE_DIR

class SaveSystem:
    """Manages saving and loading game state"""
    
    def __init__(self):
        self.save_dir = SAVE_DIR
        self._ensure_save_dir()
    
    def _ensure_save_dir(self):
        """Create save directory if it doesn't exist"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def save_game(self, game_data, auto=False):
        """Save game to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if auto:
            filename = f"autosave_{timestamp}.json"
        else:
            filename = f"save_{timestamp}.json"
        
        filepath = os.path.join(self.save_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(game_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, filepath):
        """Load game from file"""
        try:
            with open(filepath, 'r') as f:
                game_data = json.load(f)
            return game_data
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    def list_saves(self):
        """List all save files"""
        saves = []
        try:
            for filename in sorted(os.listdir(self.save_dir), reverse=True):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.save_dir, filename)
                    saves.append(filepath)
        except Exception as e:
            print(f"Error listing saves: {e}")
        
        return saves
    
    def delete_save(self, filepath):
        """Delete a save file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except Exception as e:
            print(f"Error deleting save: {e}")
        
        return False
