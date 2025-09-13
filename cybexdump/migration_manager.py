import json
import shutil
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.prompt import Confirm
from .config_manager import ConfigManager

console = Console()

class MigrationManager:
    def __init__(self):
        self.config_manager = ConfigManager()
        
    def backup_configuration(self, backup_path=None):
        """Backup entire configuration including settings and credentials"""
        config = self.config_manager.load_config()
        if not config:
            console.print("[yellow]No configuration found to backup[/yellow]")
            return False
            
        if not backup_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = Path.home() / f"cybexdump_config_backup_{timestamp}.json"
        else:
            backup_path = Path(backup_path)
            
        try:
            # Create backup of configuration
            with open(backup_path, 'w') as f:
                json.dump(config, f, indent=4)
                
            console.print(f"[green]Configuration successfully backed up to: {backup_path}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Failed to backup configuration: {str(e)}[/red]")
            return False
            
    def restore_configuration(self, backup_path):
        """Restore configuration from backup file"""
        backup_path = Path(backup_path)
        
        if not backup_path.exists():
            console.print(f"[red]Backup file not found: {backup_path}[/red]")
            return False
            
        try:
            # Read backup file
            with open(backup_path) as f:
                config = json.load(f)
                
            # Validate backup structure
            required_keys = ["backup_location", "notification", "databases"]
            if not all(key in config for key in required_keys):
                console.print("[red]Invalid backup file format[/red]")
                return False
                
            # Save configuration
            self.config_manager.save_config(config)
            console.print("[green]Configuration successfully restored![/green]")
            return True
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON format in backup file[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Failed to restore configuration: {str(e)}[/red]")
            return False
            
    def clean_configuration(self):
        """Clean all configuration after confirmation"""
        config_dir = Path.home() / ".cybexdump"
        
        if not config_dir.exists():
            console.print("[yellow]No configuration exists to clean[/yellow]")
            return True
            
        if not Confirm.ask("[bold red]Are you sure you want to remove all configuration?[/bold red]"):
            console.print("Configuration cleanup cancelled")
            return False
            
        if Confirm.ask("[bold red]Would you like to backup the configuration first?[/bold red]"):
            self.backup_configuration()
            
        try:
            # Remove configuration directory
            shutil.rmtree(config_dir)
            console.print("[green]Configuration successfully cleaned[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Failed to clean configuration: {str(e)}[/red]")
            return False
