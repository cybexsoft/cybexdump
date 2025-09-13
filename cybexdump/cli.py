import click
import json
import os
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from cybexdump.config_manager import ConfigManager
from cybexdump.scheduler import BackupScheduler
from cybexdump.database_manager import DatabaseManager
from cybexdump.migration_manager import MigrationManager

console = Console()
config_manager = ConfigManager()
migration_manager = MigrationManager()

@click.group()
@click.version_option(version='0.1.0')
def cli():
    """CybexDump - Database Backup Utility"""
    pass

@cli.command()
def configure():
    """Initial configuration of CybexDump"""
    console.print("[bold blue]Welcome to CybexDump Configuration![/bold blue]")
    
    # Create config directory if it doesn't exist
    config_dir = Path.home() / ".cybexdump"
    config_dir.mkdir(exist_ok=True)
    
    # Basic Configuration
    config = {
        "backup_location": "",
        "notification": {
            "enabled": False,
            "email": "",
            "smtp_server": "",
            "smtp_port": 587,
            "smtp_username": "",
            "smtp_password": ""
        },
        "databases": []
    }
    
    # Backup Location
    config["backup_location"] = Prompt.ask(
        "Enter backup location path",
        default=str(Path.home() / "backups")
    )
    Path(config["backup_location"]).mkdir(exist_ok=True)
    
    # Notification Setup
    if Confirm.ask("Do you want to enable email notifications?"):
        config["notification"]["enabled"] = True
        config["notification"]["email"] = Prompt.ask("Enter notification email")
        config["notification"]["smtp_server"] = Prompt.ask("Enter SMTP server")
        config["notification"]["smtp_port"] = int(Prompt.ask("Enter SMTP port", default="587"))
        config["notification"]["smtp_username"] = Prompt.ask("Enter SMTP username")
        config["notification"]["smtp_password"] = Prompt.ask("Enter SMTP password", password=True)
    
    # Database Setup
    if Confirm.ask("Do you want to add a database now?"):
        db_config = _add_database()
        if db_config:
            config["databases"].append(db_config)
    
    # Save Configuration
    config_manager.save_config(config)
    
    # Setup Scheduler
    scheduler = BackupScheduler()
    scheduler.setup_default_schedule()
    
    console.print("[bold green]Configuration completed successfully![/bold green]")

def _add_database():
    """Helper function to add database configuration"""
    db_types = ["mysql", "postgresql", "mongodb"]
    db_type = Prompt.ask("Select database type", choices=db_types)
    
    db_config = {
        "type": db_type,
        "host": Prompt.ask("Enter host"),
        "port": int(Prompt.ask("Enter port", default="3306" if db_type == "mysql" else "5432")),
        "username": Prompt.ask("Enter username"),
        "password": Prompt.ask("Enter password", password=True),
        "databases": [],
        "schedule": {
            "frequency": "daily",
            "time": "00:00",
            "retention_days": 7
        }
    }
    
    # Get available databases
    db_manager = DatabaseManager(db_config)
    available_dbs = db_manager.list_databases()
    
    console.print("\nAvailable databases:")
    for i, db in enumerate(available_dbs, 1):
        console.print(f"{i}. {db}")
    console.print("A. All databases")
    
    choice = Prompt.ask("Select databases (comma separated numbers or A for all)")
    db_config["databases"] = "all" if choice.upper() == "A" else [
        available_dbs[int(i)-1] for i in choice.split(",")
    ]
    
    # Backup Schedule
    db_config["schedule"]["frequency"] = Prompt.ask(
        "Enter backup frequency",
        choices=["hourly", "daily", "weekly"],
        default="daily"
    )
    
    db_config["schedule"]["time"] = Prompt.ask(
        "Enter backup time (HH:MM)",
        default="00:00"
    )
    
    db_config["schedule"]["retention_days"] = int(Prompt.ask(
        "Enter backup retention period in days",
        default="7"
    ))
    
    return db_config

@cli.command()
@click.option('--file', '-f', help='Output file path for backup (default: cybexdump_backup_YYYYMMDD_HHMMSS.json)')
@click.option('--config-only', is_flag=True, help='Backup only configuration without database dumps')
def backup(file, config_only):
    """Backup databases and/or configuration"""
    if config_only:
        migration_manager.backup_configuration(file)
    else:
        backup_manager = BackupManager()
        config = config_manager.load_config()
        
        if not config.get("databases"):
            console.print("[yellow]No databases configured for backup[/yellow]")
            return
            
        for db_config in config["databases"]:
            backup_manager.perform_backup(db_config["id"], output_file=file)

@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--config-only', is_flag=True, help='Restore only configuration without database restoration')
@click.option('--force', is_flag=True, help='Force restore without confirmation')
def restore(file, config_only, force):
    """Restore databases and/or configuration from backup"""
    if not force and not Confirm.ask("[bold yellow]This will overwrite existing configuration. Continue?[/bold yellow]"):
        console.print("Restore cancelled")
        return
        
    if config_only:
        if migration_manager.restore_configuration(file):
            # Reconfigure scheduler after restore
            scheduler = BackupScheduler()
            scheduler.setup_default_schedule()
    else:
        backup_manager = BackupManager()
        backup_manager.restore_from_backup(file)

@cli.command()
def clean():
    """Clean all configuration (with confirmation)"""
    migration_manager.clean_configuration()

def main():
    """Main entry point for the CLI"""
    try:
        cli()
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise click.Abort()

if __name__ == "__main__":
    main()
