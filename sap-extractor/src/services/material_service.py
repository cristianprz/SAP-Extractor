# src/services/material_service.py
from models.material_query import MaterialQuery
from dto.material_dto import MaterialDTO

class MaterialService:
    """Serviço para gerenciamento de materiais"""
    
    def __init__(self, material_repository):
        self.material_repository = material_repository
        self.material_query = MaterialQuery(material_repository.sql_conn)
        
    def get_materials(self):
        """Obtém a lista de materiais para processamento"""
        try:
            # Obtém materiais do banco QV (fonte de dados externa)
            materials = self.material_query.get_materials_from_db()
            
            if not materials:
                print("No materials found in source database")
                return []
                
            return materials
            
        except Exception as e:
            print(f"Error fetching materials: {e}")
            return []
            
    def get_materials_by_type(self, material_type):
        """Obtém materiais por tipo"""
        return self.material_repository.get_materials_by_type(material_type)
            
    def update_material_details(self, material_code):
        """Atualiza detalhes de um material específico a partir do SAP"""
        # Implementação futura para buscar detalhes do SAP
        pass
        
    def ensure_material_table(self):
        """Garante que a tabela de materiais exista"""
        return self.material_repository.setup_table()