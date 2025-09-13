import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".cybexdump"
        self.config_file = self.config_dir / "config.json"
        
    def load_config(self):
        """Load configuration from JSON file"""
        if not self.config_file.exists():
            return {}
            
        with open(self.config_file) as f:
            return json.load(f)
            
    def save_config(self, config):
        """Save configuration to JSON file"""
        self.config_dir.mkdir(exist_ok=True)
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
            
    def get_database_configs(self):
        """Get all database configurations"""
        config = self.load_config()
        return config.get("databases", [])
