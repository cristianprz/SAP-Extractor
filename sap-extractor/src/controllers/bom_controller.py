from extractors.base_extractor import BaseExtractor

class BOMController(BaseExtractor):
    """Coordena operações de extração de BOM"""
    
    def __init__(self, bom_service, material_service):
        self.bom_service = bom_service
        self.material_service = material_service
    
    @property
    def name(self):
        return "BOM"
    
    @property
    def description(self):
        return "Extrai dados de Bill of Materials do SAP e salva no banco de dados"
        
    def extract(self):
        """Executa o processo de extração de BOM"""
        print(f"Iniciando extração: {self.name}")
        
        try:
            # Verifica/cria tabela BOM
            if not self.bom_service.bom_repository.setup_table():
                print("Falha ao configurar tabela BOM")
                return False
            
            # Busca materiais para processar
            materials = self.material_service.get_materials()
            
            if not materials:
                print("Nenhum material encontrado para processar")
                return False
            
            # Processa os materiais
            results = self.bom_service.process_materials(materials)
            
            # Relatório do processamento
            print(f"Processamento concluído: {results['processed']} processados, "
                  f"{results['failed']} falhas de um total de {results['total']} materiais")
            
            return results['processed'] > 0
            
        except Exception as e:
            print(f"Erro no processo de extração: {e}")
            return False