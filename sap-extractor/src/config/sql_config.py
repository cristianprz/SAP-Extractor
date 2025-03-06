# Configuration settings for the SQL Server connection

SQL_CONFIG = {
    # Connection parameters
    'driver': 'ODBC Driver 17 for SQL Server',
    'server': '******',
    'database': 'LOG',
    'uid': '*******',
    'pwd': '*******',
    
    # Performance and stability settings
    'timeout': 300,              # Connection timeout in seconds (5 minutes)
    'login_timeout': 60,         # Login timeout in seconds
    'connection_timeout': 30,    # Initial connection timeout
    'autocommit': True,         # Enable automatic transaction commit
    
    # Additional settings
    'TrustServerCertificate': 'yes',  # Trust SQL Server certificate
    'ApplicationIntent': 'ReadWrite'   # Specify application workload type
}