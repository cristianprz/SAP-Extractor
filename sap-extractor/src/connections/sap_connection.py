from pyrfc import Connection
from config.sap_config import SAP_CONFIG

class SAPConnection:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        """Establish connection to SAP system"""
        try:
            self.conn = Connection(**SAP_CONFIG)
            print("SAP connection established successfully")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SAP: {e}")

    def call_function(self, function_name, **parameters):
        """Execute SAP RFC function"""
        try:
            return self.conn.call(function_name, **parameters)
        except Exception as e:
            raise Exception(f"Error calling SAP function {function_name}: {e}")

    def close(self):
        """Close SAP connection"""
        if self.conn:
            self.conn.close()