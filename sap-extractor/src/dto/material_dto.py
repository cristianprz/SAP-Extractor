# src/dto/material_dto.py
class MaterialDTO:
    """DTO para transferência de dados de Material entre camadas"""
    
    def __init__(self, codigo, descricao, tipo="", grupo_mercadoria="", 
                 umb="", peso_bruto=0.0, centro="", grupo_compradores="", status=""):
        self.codigo = codigo
        self.descricao = descricao
        self.tipo = tipo
        self.grupo_mercadoria = grupo_mercadoria
        self.umb = umb
        self.peso_bruto = peso_bruto
        self.centro = centro
        self.grupo_compradores = grupo_compradores
        self.status = status
        
    def to_tuple(self):
        """Converte o objeto para uma tupla para persistência"""
        return (
            str(self.codigo),
            str(self.descricao),
            str(self.tipo),
            str(self.grupo_mercadoria),
            str(self.umb),
            float(self.peso_bruto) if self.peso_bruto else 0.0,
            str(self.centro),
            str(self.grupo_compradores),
            str(self.status)
        )
        
    @classmethod
    def from_sap_data(cls, sap_data):
        """Cria um MaterialDTO a partir de dados do SAP"""
        return cls(
            codigo=sap_data.get('MATNR', ''),
            descricao=sap_data.get('MAKTX', ''),
            tipo=sap_data.get('MTART', ''),
            grupo_mercadoria=sap_data.get('MATKL', ''),
            umb=sap_data.get('MEINS', ''),
            peso_bruto=float(sap_data.get('BRGEW', 0.0)),
            centro=sap_data.get('WERKS', ''),
            grupo_compradores=sap_data.get('EKGRP', ''),
            status=sap_data.get('MMSTA', '')
        )