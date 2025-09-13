from crontab import CronTab
from datetime import datetime, timedelta
import schedule
import time
from pathlib import Path
from .config_manager import ConfigManager
from .backup_manager import BackupManager

class BackupScheduler:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.backup_manager = BackupManager()
        
    def setup_default_schedule(self):
        """Setup default schedule using crontab"""
        config = self.config_manager.load_config()
        cron = CronTab(user=True)
        
        # Remove existing cybexdump jobs
        cron.remove_all(comment='cybexdump')
        
        for db_config in config.get("databases", []):
            frequency = db_config["schedule"]["frequency"]
            time_parts = db_config["schedule"]["time"].split(":")
            hour, minute = map(int, time_parts)
            
            job = cron.new(command=f'cybexdump backup --database-id {db_config["id"]}',
                          comment='cybexdump')
                          
            if frequency == "hourly":
                job.hour.every(1)
            elif frequency == "daily":
                job.hour.on(hour)
                job.minute.on(minute)
            elif frequency == "weekly":
                job.dow.on(0)  # Sunday
                job.hour.on(hour)
                job.minute.on(minute)
                
        cron.write()
        
    def run_continuous(self):
        """Run backup scheduler in continuous mode"""
        config = self.config_manager.load_config()
        
        for db_config in config.get("databases", []):
            frequency = db_config["schedule"]["frequency"]
            time_str = db_config["schedule"]["time"]
            
            if frequency == "hourly":
                schedule.every().hour.at(time_str).do(
                    self.backup_manager.perform_backup, db_config["id"]
                )
            elif frequency == "daily":
                schedule.every().day.at(time_str).do(
                    self.backup_manager.perform_backup, db_config["id"]
                )
            elif frequency == "weekly":
                schedule.every().sunday.at(time_str).do(
                    self.backup_manager.perform_backup, db_config["id"]
                )
                
        while True:
            schedule.run_pending()
            time.sleep(60)
