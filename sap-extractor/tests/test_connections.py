import unittest
from unittest.mock import Mock, patch
from src.connections.sap_connection import SAPConnection
from src.connections.sql_connection import SQLConnection
from src.config.sap_config import SAP_CONFIG
from src.config.sql_config import SQL_CONFIG

class TestSAPConnection(unittest.TestCase):
    """Test cases for SAP connection handling"""

    @patch('src.connections.sap_connection.Connection')
    def setUp(self, mock_sap_conn):
        self.mock_sap = mock_sap_conn
        self.sap_connection = SAPConnection()

    def test_sap_connection_success(self):
        """Test successful SAP connection"""
        self.mock_sap.assert_called_once_with(**SAP_CONFIG)
        self.assertIsNotNone(self.sap_connection.conn)

    def test_sap_connection_failure(self):
        """Test SAP connection failure"""
        self.mock_sap.side_effect = Exception("Connection failed")
        with self.assertRaises(ConnectionError):
            SAPConnection()

    def test_sap_function_call(self):
        """Test SAP function call"""
        test_params = {'MATERIAL': '1000', 'PLANT': '0050'}
        self.sap_connection.call_function('TEST_FUNCTION', **test_params)
        self.sap_connection.conn.call.assert_called_once_with('TEST_FUNCTION', **test_params)

    def test_sap_close_connection(self):
        """Test SAP connection closure"""
        self.sap_connection.close()
        self.sap_connection.conn.close.assert_called_once()

class TestSQLConnection(unittest.TestCase):
    """Test cases for SQL Server connection handling"""

    @patch('src.connections.sql_connection.pyodbc')
    def setUp(self, mock_pyodbc):
        self.mock_sql = mock_pyodbc
        self.sql_connection = SQLConnection()

    def test_sql_connection_success(self):
        """Test successful SQL connection"""
        self.mock_sql.connect.assert_called_once()