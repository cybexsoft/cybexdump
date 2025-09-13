import subprocess
from datetime import datetime
import os
import json
from pathlib import Path
import mysql.connector
from rich.console import Console
from rich.prompt import Confirm
from .config_manager import ConfigManager

console = Console()

class BackupManager:
    def __init__(self):
        self.config_manager = ConfigManager()
        
    def perform_backup(self, database_id, output_file=None):
        """Perform backup for a specific database configuration"""
        config = self.config_manager.load_config()
        db_config = None
        
        # Find the database config with matching ID
        for db in config.get("databases", []):
            if db.get("id") == database_id:
                db_config = db
                break
                
        if not db_config:
            console.print(f"[red]No database configuration found with ID {database_id}[/red]")
            return
            
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = Path(f"cybexdump_backup_{timestamp}.sql")
            
        if db_config["type"] == "mysql":
            return self._backup_mysql(db_config, output_file)
            
    def _backup_mysql(self, db_config, output_file):
        """Perform MySQL backup"""
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        databases = db_config["databases"]
        if databases == "all":
            try:
                conn = mysql.connector.connect(
                    host=db_config["host"],
                    user=db_config["username"],
                    password=db_config["password"],
                    port=db_config["port"]
                )
                cursor = conn.cursor()
                cursor.execute("SHOW DATABASES")
                databases = [db[0] for db in cursor.fetchall()
                           if db[0] not in ['information_schema', 'performance_schema', 'mysql', 'sys']]
                cursor.close()
                conn.close()
            except Exception as e:
                console.print(f"[red]Error connecting to MySQL: {str(e)}[/red]")
                return
                
        for db in databases:
            backup_file = output_file
            
            cmd = [
                "mysqldump",
                f"-h{db_config['host']}",
                f"-P{db_config['port']}",
                f"-u{db_config['username']}",
                f"-p{db_config['password']}",
                "--single-transaction",
                "--quick",
                "--routines",
                "--triggers",
                "--events",
                db,
                f"> {str(backup_file)}"
            ]
            
            try:
                subprocess.run(" ".join(cmd), shell=True, check=True)
                console.print(f"[green]Successfully backed up {db} to {backup_file}[/green]")
                
                # Compress the backup
                compress_cmd = f"gzip {str(backup_file)}"
                subprocess.run(compress_cmd, shell=True, check=True)
                
            except subprocess.CalledProcessError as e:
                console.print(f"[red]Error backing up {db}: {str(e)}[/red]")
                
        self._cleanup_old_backups(backup_dir, db_config["schedule"]["retention_days"])
        
    def _cleanup_old_backups(self, backup_dir, retention_days):
        """Remove backups older than retention period"""
        current_time = datetime.now()
        for backup_file in backup_dir.glob("*.sql.gz"):
            file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
            if (current_time - file_time).days > retention_days:
                backup_file.unlink()
                console.print(f"[yellow]Removed old backup: {backup_file}[/yellow]")
                
    def restore_from_backup(self, backup_file):
        """Restore database from backup file"""
        backup_file = Path(backup_file)
        
        if not backup_file.exists():
            console.print(f"[red]Backup file not found: {backup_file}[/red]")
            return False
            
        # Check if it's a gzipped file
        is_gzipped = backup_file.suffix == '.gz'
        
        config = self.config_manager.load_config()
        if not config.get("databases"):
            console.print("[red]No database configurations found[/red]")
            return False
            
        # Ask user which database to restore to
        console.print("\nAvailable database configurations:")
        for i, db in enumerate(config["databases"], 1):
            console.print(f"{i}. {db['type']} - {db['host']}:{db['port']}")
            
        try:
            choice = int(Prompt.ask("Select database configuration number")) - 1
            db_config = config["databases"][choice]
        except (ValueError, IndexError):
            console.print("[red]Invalid selection[/red]")
            return False
            
        if db_config["type"] == "mysql":
            try:
                # If file is gzipped, decompress it first
                if is_gzipped:
                    temp_file = backup_file.with_suffix('')
                    subprocess.run(f"gzip -dk {backup_file}", shell=True, check=True)
                    backup_file = temp_file
                
                cmd = [
                    "mysql",
                    f"-h{db_config['host']}",
                    f"-P{db_config['port']}",
                    f"-u{db_config['username']}",
                    f"-p{db_config['password']}",
                    f"< {str(backup_file)}"
                ]
                
                subprocess.run(" ".join(cmd), shell=True, check=True)
                console.print("[green]Database restored successfully![/green]")
                
                # Clean up temporary file if we decompressed
                if is_gzipped:
                    backup_file.unlink()
                    
                return True
                
            except subprocess.CalledProcessError as e:
                console.print(f"[red]Error restoring database: {str(e)}[/red]")
                return False
