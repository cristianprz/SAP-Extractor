# src/services/sap_extractor_service.py
from dto.bom_dto import BOMItem

class SAPExtractorService:
    """Responsável pela comunicação com o SAP e extração de dados"""
    
    def __init__(self, sap_conn):
        self.sap_conn = sap_conn
        
    def extract_bom(self, material):
        """Extrai os dados de BOM do SAP para um material específico"""
        try:
            # Parâmetros para a função RFC
            params = {
                'MATERIAL': material,
                'PLANT': '0050',
                'BOM_USAGE': '1',
                'ALTERNATIVE': '1'
            }
            
            # Chamada da função RFC no SAP
            result = self.sap_conn.call_function('CSAP_MAT_BOM_READ', **params)
            
            bom_items = []
            
            # Processa os resultados
            if 'T_STKO' in result and 'T_STPO' in result:
                header = result['T_STKO'][0] if result['T_STKO'] else None
                
                if header:
                    base_qty = header.get('BASE_QUAN', '1')
                    bom_no = header.get('BOM_NO', '')
                    base_und = header.get('BASE_UNIT', '')
                    material_name = header.get('ALT_TEXT', '')
                    
                    for item in result['T_STPO']:
                        bom_item = BOMItem(
                            codigo=material,
                            material=material_name,
                            unidade=base_und,
                            nr_bom=bom_no,
                            quantidade_base=base_qty,
                            item=item.get('ITEM_NO', ''),
                            componente=item.get('COMPONENT', ''),
                            quantidade=item.get('COMP_QTY', ''),
                            unidade_comp=item.get('COMP_UNIT', '')
                        )
                        bom_items.append(bom_item)
            
            return bom_items
            
        except Exception as e:
            print(f"Error extracting BOM from SAP for material {material}: {e}")
            raise