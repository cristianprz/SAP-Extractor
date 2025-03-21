from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """Classe base para todos os extractors"""
    
    @property
    def name(self):
        """Nome do extractor para referência"""
        return self.__class__.__name__
        
    @property
    def description(self):
        """Descrição do que o extractor faz"""
        return "Extractor base"
    
    @abstractmethod
    def extract(self):
        """Executa a extração de dados. Deve ser implementado pelas subclasses."""
        pass