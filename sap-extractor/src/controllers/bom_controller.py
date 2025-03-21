class BOMController:
    """Coordena as operações de extração de BOM"""
    
    def __init__(self, bom_service, material_service):
        self.bom_service = bom_service
        self.material_service = material_service
        
    def run_extraction(self):
        """Executa o fluxo completo de extração de BOMs"""
        try:
            # Configuração da tabela
            self.bom_service.bom_repository.setup_table()
            
            # Busca materiais a serem processados
            materials = self.material_service.get_materials()
            
            if not materials:
                print("No materials to process")
                return False
                
            # Processa os materiais
            results = self.bom_service.process_materials(materials)
            
            # Relatório de processamento
            print(f"Processing completed: {results['processed']} processed, "
                  f"{results['failed']} failed out of {results['total']} materials")
                  
            return results['processed'] > 0
            
        except Exception as e:
            print(f"Error in BOM extraction process: {e}")
            return False