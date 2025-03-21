# src/services/bom_service.py
from dto.bom_dto import BOMItem
from repositories.bom_repository import BOMRepository
from services.sap_extractor_service import SAPExtractorService

class BOMService:
    """Orquestra o processo de extração e persistência de BOMs"""
    
    def __init__(self, sap_extractor_service, bom_repository):
        self.sap_extractor = sap_extractor_service
        self.bom_repository = bom_repository
        self.batch_size = 100
        
    def process_materials(self, materials):
        """Processa uma lista de materiais, extraindo e salvando seus BOMs"""
        results = {
            'processed': 0,
            'failed': 0,
            'total': len(materials)
        }
        
        batch_data = []
        
        for material in materials:
            try:
                # Extrai os dados do SAP
                bom_items = self.sap_extractor.extract_bom(material)
                
                if not bom_items:
                    continue
                    
                # Converte para formato adequado para persistência
                formatted_items = [item.to_tuple() for item in bom_items]
                batch_data.extend(formatted_items)
                
                # Salva em lotes para melhor performance
                if len(batch_data) >= self.batch_size:
                    self.bom_repository.save_batch(batch_data)
                    batch_data = []
                
                results['processed'] += 1
                
            except Exception as e:
                print(f"Error processing material {material}: {e}")
                results['failed'] += 1
                continue
                
        # Salva os itens restantes
        if batch_data:
            self.bom_repository.save_batch(batch_data)
            
        return results