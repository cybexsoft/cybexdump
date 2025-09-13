from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config_manager import ConfigManager

class NotificationManager:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        self.notification_config = self.config.get("notification", {})
        
    def send_backup_notification(self, success, database_name, error_message=None):
        """Send backup status notification"""
        if not self.notification_config.get("enabled"):
            return
            
        subject = f"Backup {'Success' if success else 'Failed'} - {database_name}"
        
        if success:
            body = f"Database backup completed successfully for {database_name}"
        else:
            body = f"Database backup failed for {database_name}\nError: {error_message}"
            
        self._send_email(subject, body)
        
    def _send_email(self, subject, body):
        """Send email using configured SMTP settings"""
        msg = MIMEMultipart()
        msg["From"] = self.notification_config["smtp_username"]
        msg["To"] = self.notification_config["email"]
        msg["Subject"] = subject
        
        msg.attach(MIMEText(body, "plain"))
        
        try:
            server = smtplib.SMTP(
                self.notification_config["smtp_server"],
                self.notification_config["smtp_port"]
            )
            server.starttls()
            server.login(
                self.notification_config["smtp_username"],
                self.notification_config["smtp_password"]
            )
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Failed to send notification email: {str(e)}")
