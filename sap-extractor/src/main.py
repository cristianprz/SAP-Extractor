import sys
from connections.sap_connection import SAPConnection
from connections.sql_connection import SQLConnection
from repositories.bom_repository import BOMRepository
from repositories.material_repository import MaterialRepository
from services.bom_service import BOMService
from services.material_service import MaterialService
from services.sap_extractor_service import SAPExtractorService
from controllers.bom_controller import BOMController
from utils.validators import validate_environment

def main():
    """Script principal para orquestrar o processo de extração de dados"""
    
    # Validação de ambiente
    if not validate_environment():
        sys.exit(1)

    try:
        # Inicialização de conexões
        sap_conn = SAPConnection()
        sql_conn = SQLConnection()
        
        # Inicialização de repositórios
        bom_repository = BOMRepository(sql_conn)
        material_repository = MaterialRepository(sql_conn)
        
        # Inicialização de serviços
        sap_extractor = SAPExtractorService(sap_conn)
        material_service = MaterialService(material_repository)
        bom_service = BOMService(sap_extractor, bom_repository)
        
        # Inicialização e execução do controller
        controller = BOMController(bom_service, material_service)
        success = controller.run_extraction()
        
        # Resultado da execução
        if not success:
            print("Extraction process completed with errors")
            sys.exit(1)
            
        print("Extraction process completed successfully")

    except Exception as e:
        print(f"Error in main execution: {e}")
        sys.exit(1)
    finally:
        # Fechamento de conexões
        if 'sap_conn' in locals():
            sap_conn.close()
        if 'sql_conn' in locals():
            sql_conn.close()

if __name__ == "__main__":
    main()