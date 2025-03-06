# README.md

# SAP Extractor

## Overview
The SAP Extractor is a Python application designed to connect to SAP systems and SQL Server databases to extract and process Bill of Materials (BOM) data. This project provides a modular structure that separates configuration, connection handling, and data processing, making it easy to maintain and extend.

## Project Structure
```
sap-extractor
├── src
│   ├── config
│   │   ├── __init__.py
│   │   ├── sap_config.py
│   │   └── sql_config.py
│   ├── connections
│   │   ├── __init__.py
│   │   ├── sap_connection.py
│   │   └── sql_connection.py
│   ├── models
│   │   ├── __init__.py
│   │   └── bom.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── validators.py
│   └── main.py
├── tests
│   ├── __init__.py
│   └── test_connections.py
├── requirements.txt
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd sap-extractor
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration
- Update the `sap_config.py` file with your SAP connection details.
- Update the `sql_config.py` file with your SQL Server connection details.

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## Testing
To run the unit tests, use:
```
pytest tests/
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.