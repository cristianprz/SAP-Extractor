import sys
import argparse
from connections.sap_connection import SAPConnection
from connections.sql_connection import SQLConnection
from repositories.bom_repository import BOMRepository
from repositories.material_repository import MaterialRepository
from services.bom_service import BOMService
from services.material_service import MaterialService
from services.sap_extractor_service import SAPExtractorService
from controllers.bom_controller import BOMController
from controllers.material_controller import MaterialController
from extractors.registry import ExtractorRegistry
from utils.validators import validate_environment

def initialize_dependencies():
    """Inicializa todas as dependências necessárias para os extractors"""
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
    
    # Retorna objetos criados
    return {
        'connections': {
            'sap': sap_conn,
            'sql': sql_conn
        },
        'repositories': {
            'bom': bom_repository,
            'material': material_repository
        },
        'services': {
            'sap_extractor': sap_extractor,
            'material': material_service,
            'bom': bom_service
        }
    }

def register_extractors(dependencies):
    """Registra todos os extractors disponíveis"""
    
    # Registra o extrator de BOM
    bom_controller = BOMController(
        dependencies['services']['bom'],
        dependencies['services']['material']
    )
    ExtractorRegistry.register(bom_controller)
    
    # Registra o extrator de Material
    # material_controller = MaterialController(
    #     dependencies['services']['material'],
    #     dependencies['repositories']['material']
    # )
    # ExtractorRegistry.register(material_controller)
    
    # Registre novos extractors aqui conforme necessário

def main():
    """Script principal para orquestrar o processo de extração de dados"""
    
    # Parse dos argumentos da linha de comando
    parser = argparse.ArgumentParser(
        description='SAP Extractor - Sistema de Extração de Dados do SAP'
    )
    parser.add_argument('--extractor', '-e', 
                      help='Nome do extractor para executar')
    parser.add_argument('--list', '-l', action='store_true', 
                      help='Listar extractors disponíveis')
    args = parser.parse_args()
    
    # Validação de ambiente
    if not validate_environment():
        sys.exit(1)

    # Inicialização de dependências
    dependencies = None
    try:
        dependencies = initialize_dependencies()
        
        # Registro de extractors
        register_extractors(dependencies)
        
        # Listar extractors disponíveis se solicitado
        if args.list:
            print("\nExtractors disponíveis:")
            for name, extractor in ExtractorRegistry.list_extractors().items():
                print(f"  - {extractor.name}: {extractor.description}")
            return 0
        
        # Executar extractor específico se fornecido
        if args.extractor:
            extractor_name = args.extractor
            extractor = ExtractorRegistry.get_extractor(extractor_name)
            
            if not extractor:
                print(f"Erro: Extractor '{extractor_name}' não encontrado.")
                print("Use --list para ver os extractors disponíveis.")
                return 1
                
            print(f"Executando extractor: {extractor.name}")
            success = extractor.extract()
            
            if not success:
                print("Extração completada com erros.")
                return 1
                
            print("Extração completada com sucesso.")
            return 0
        
        # Se nenhum extractor foi especificado, executar o BOM (comportamento padrão)
        bom_extractor = ExtractorRegistry.get_extractor("bom")
        if bom_extractor:
            print("Executando extração padrão (BOM)...")
            success = bom_extractor.extract()
            
            if not success:
                print("Extração completada com erros.")
                return 1
                
            print("Extração completada com sucesso.")
            return 0
        
    except Exception as e:
        print(f"Erro na execução principal: {e}")
        return 1
    finally:
        # Fechamento de conexões
        if dependencies:
            for conn_name, conn in dependencies['connections'].items():
                try:
                    conn.close()
                except:
                    pass

if __name__ == "__main__":
    sys.exit(main())