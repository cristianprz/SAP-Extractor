import sys
from connections.sap_connection import SAPConnection
from connections.sql_connection import SQLConnection
from models.bom import BOMExtractor
from models.material_query import MaterialQuery
from utils.validators import validate_environment

def main():
    """Main function to orchestrate the SAP data extraction process"""
    
    # Validate environment setup
    if not validate_environment():
        sys.exit(1)

    try:
        # Initialize connections
        sap_conn = SAPConnection()
        sql_conn = SQLConnection()         

        # Fetch materials from database
        material_query = MaterialQuery(sql_conn)
        materials = material_query.get_materials_from_db()
        
        # Create BOM extractor instance
        bom_extractor = BOMExtractor(sap_conn, sql_conn)

        # Create/verify SQL table
        if not bom_extractor.setup_database():
            raise Exception("Failed to setup database table")

        # Process materials
        bom_extractor.extract_bom_batch(materials)

    except Exception as e:
        print(f"Error in main execution: {e}")
        sys.exit(1)
    finally:
        # Ensure connections are closed
        if 'sap_conn' in locals():
            sap_conn.close()
        if 'sql_conn' in locals():
            sql_conn.close()

if __name__ == "__main__":
    main()