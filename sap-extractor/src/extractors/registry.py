class ExtractorRegistry:
    """Registro de extractors disponíveis"""
    
    _extractors = {}
    
    @classmethod
    def register(cls, extractor_instance):
        """Registra um extractor"""
        cls._extractors[extractor_instance.name.lower()] = extractor_instance
    
    @classmethod
    def get_extractor(cls, name):
        """Obtém um extractor pelo nome"""
        return cls._extractors.get(name.lower())
    
    @classmethod
    def list_extractors(cls):
        """Lista todos os extractors disponíveis"""
        return cls._extractors