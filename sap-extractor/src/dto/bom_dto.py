# src/dto/bom_dto.py
class BOMItem:
    """DTO para transferência de dados de BOM entre camadas"""
    
    def __init__(self, codigo, material, unidade, nr_bom, quantidade_base, 
                 item, componente, quantidade, unidade_comp):
        self.codigo = codigo
        self.material = material
        self.unidade = unidade
        self.nr_bom = nr_bom
        self.quantidade_base = quantidade_base
        self.item = item
        self.componente = componente
        self.quantidade = quantidade
        self.unidade_comp = unidade_comp
        
    def to_tuple(self):
        """Converte o objeto para uma tupla para persistência"""
        return (
            str(self.codigo),
            str(self.material),
            str(self.unidade),
            str(self.nr_bom),
            str(self.quantidade_base),
            str(self.item),
            str(self.componente),
            str(self.quantidade),
            str(self.unidade_comp)
        )