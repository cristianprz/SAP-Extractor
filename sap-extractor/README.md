# README.md

# SAP-Extractor

A Python application for extracting BOM (Bill of Materials) data from SAP and storing it in a SQL Server database.

## Features

- SAP RFC connection handling with timeout and auto-commit
- SQL Server connection with configurable settings
- Batch processing of materials
- Error handling and logging
- Automatic database table creation/verification
- Material filtering based on category

## Prerequisites

- Python 3.7+
- SAP RFC SDK
- ODBC Driver 17 for SQL Server
- SAP System Access
- SQL Server Access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SAP-Extractor.git
cd SAP-Extractor
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure your environment:
   - Create `config/sap_config.py` with your SAP credentials
   - Create `config/sql_config.py` with your SQL Server settings

## Configuration

### SAP Configuration (`config/sap_config.py`):
```python
SAP_CONFIG = {
    'ashost': 'your_sap_host',
    'sysnr': '00',
    'client': '100',
    'user': 'your_user',
    'passwd': 'your_password',
    'timeout': '300',
    'auto_commit': True
}
```

### SQL Configuration (`config/sql_config.py`):
```python
SQL_CONFIG = {
    'driver': 'ODBC Driver 17 for SQL Server',
    'server': 'your_server',
    'database': 'your_database',
    'uid': 'your_username',
    'pwd': 'your_password',
    'timeout': 300,
    'autocommit': True
}
```

## Usage

Run the main script:
```bash
python -m src.main
```

The application will:
1. Connect to SAP and SQL Server
2. Fetch materials from QV database
3. Extract BOM data for each material
4. Save the data to SQL Server

## Project Structure

```
sap-extractor/
├── src/
│   ├── connections/
│   │   ├── __init__.py
│   │   ├── sap_connection.py
│   │   └── sql_connection.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── bom.py
│   │   └── material_query.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── sap_config.py
│   │   └── sql_config.py
│   └── utils/
│       ├── __init__.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   └── test_connections.py
├── README.md
└── requirements.txt
```

## Testing

Run tests using:
```bash
python -m unittest discover -s tests -v
```

## Error Handling

The application includes comprehensive error handling for:
- SAP connection issues
- SQL Server connection problems
- Invalid materials
- Database access permissions
- Network timeouts

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.