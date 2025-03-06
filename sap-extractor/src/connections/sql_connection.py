import pyodbc
from config.sql_config import SQL_CONFIG

class SQLConnection:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        """Establish connection to SQL Server"""
        conn_str = (
            f"Driver={{{SQL_CONFIG['driver']}}};"
            f"Server={SQL_CONFIG['server']};"
            f"Database={SQL_CONFIG['database']};"
            f"UID={SQL_CONFIG['uid']};"
            f"PWD={SQL_CONFIG['pwd']};"
        )
        try:
            self.conn = pyodbc.connect(conn_str,autocommit=True)
            print("SQL Server connection established successfully")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SQL Server: {e}")

    def execute(self, query, params=None):
        """Execute SQL query"""
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return cursor
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error executing SQL query: {e}")
        
    def executemany(self, query, batch_data):
        """Execute batch SQL query with multiple parameter sets"""
        cursor = self.conn.cursor()
        try:
            # Use fast_executemany for better performance
            cursor.fast_executemany = True
            cursor.executemany(query, batch_data)
            self.conn.commit()
            return cursor
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error executing batch SQL query: {e}")

    def close(self):
        """Close SQL connection"""
        if self.conn:
            self.conn.close()