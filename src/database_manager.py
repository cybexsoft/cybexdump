import mysql.connector
from rich.console import Console

console = Console()

class DatabaseManager:
    def __init__(self, db_config):
        self.config = db_config
        self.type = db_config["type"]
        
    def list_databases(self):
        """List all available databases"""
        if self.type == "mysql":
            return self._list_mysql_databases()
        # Add support for other databases here
        return []
        
    def _list_mysql_databases(self):
        """List MySQL databases"""
        try:
            conn = mysql.connector.connect(
                host=self.config["host"],
                user=self.config["username"],
                password=self.config["password"],
                port=self.config["port"]
            )
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall() 
                       if db[0] not in ['information_schema', 'performance_schema', 'mysql', 'sys']]
            cursor.close()
            conn.close()
            return databases
        except Exception as e:
            console.print(f"[red]Error connecting to MySQL: {str(e)}[/red]")
            return []
