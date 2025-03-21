from extractors.base_extractor import BaseExtractor

class MaterialController(BaseExtractor):
    """Coordena operações de extração de Materiais"""
    
    def __init__(self, material_service, material_repository):
        self.material_service = material_service
        self.material_repository = material_repository
    
    @property
    def name(self):
        return "Material"
    
    @property
    def description(self):
        return "Extrai dados de materiais do SAP e salva no banco de dados"
        
    def extract(self):
        """Executa o processo de extração de materiais"""
        print(f"Iniciando extração: {self.name}")
        
        try:
            # Verifica/cria tabela de materiais
            if not self.material_repository.setup_table():
                print("Falha ao configurar tabela de materiais")
                return False
            
            # Extração simplificada
            materials = self.material_service.get_sap_materials()
            
            if not materials:
                print("Nenhum material encontrado para extrair")
                return False
            
            # Salva os materiais
            saved = self.material_repository.save_materials(materials)
            
            print(f"Extração concluída: {len(saved)} materiais salvos")
            
            return len(saved) > 0
            
        except Exception as e:
            print(f"Erro no processo de extração: {e}")
            return False