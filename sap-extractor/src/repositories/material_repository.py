class MaterialRepository:
    """Responsável pelo acesso aos dados de materiais no banco de dados"""
    
    def __init__(self, sql_conn):
        self.sql_conn = sql_conn
        
    def setup_table(self):
        """Cria ou verifica a tabela de materiais no banco"""
        query = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='SAP_MATERIAL' AND xtype='U')
        CREATE TABLE SAP_MATERIAL (
            Codigo VARCHAR(18) NOT NULL PRIMARY KEY,
            Descricao VARCHAR(40) NOT NULL,
            Tipo VARCHAR(4),
            Grupo_Mercadoria VARCHAR(9),
            UMB VARCHAR(3),
            Peso_Bruto DECIMAL(13,3),
            Centro VARCHAR(4),
            Grupo_Compradores VARCHAR(3),
            Status VARCHAR(1),
            Data_Insert DATETIME DEFAULT GETDATE()
        )
        """
        return self.sql_conn.execute(query)
        
    def get_all_materials(self):
        """Retorna todos os materiais do banco de dados"""
        try:
            query = """
                SELECT Codigo FROM SAP_MATERIAL
            """
            
            cursor = self.sql_conn.execute(query)
            return [row[0] for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"Error fetching materials: {e}")
            return []
            
    def get_materials_by_type(self, material_type):
        """Retorna materiais de um tipo específico"""
        try:
            query = """
                SELECT Codigo FROM SAP_MATERIAL
                WHERE Tipo = ?
            """
            
            cursor = self.sql_conn.execute(query, (material_type,))
            return [row[0] for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"Error fetching materials by type {material_type}: {e}")
            return []
            
    def material_exists(self, material_code):
        """Verifica se um material existe no banco de dados"""
        try:
            query = """
                SELECT COUNT(1) FROM SAP_MATERIAL
                WHERE Codigo = ?
            """
            
            cursor = self.sql_conn.execute(query, (material_code,))
            return cursor.fetchone()[0] > 0
            
        except Exception as e:
            print(f"Error checking if material {material_code} exists: {e}")
            return False
            
    def save_material(self, material_data):
        """Salva ou atualiza um material no banco de dados"""
        try:
            # Verifica se o material já existe
            if self.material_exists(material_data.codigo):
                # Atualiza o material existente
                query = """
                    UPDATE SAP_MATERIAL
                    SET Descricao = ?, 
                        Tipo = ?,
                        Grupo_Mercadoria = ?,
                        UMB = ?,
                        Peso_Bruto = ?,
                        Centro = ?,
                        Grupo_Compradores = ?,
                        Status = ?
                    WHERE Codigo = ?
                """
                params = (
                    material_data.descricao,
                    material_data.tipo,
                    material_data.grupo_mercadoria,
                    material_data.umb,
                    material_data.peso_bruto,
                    material_data.centro,
                    material_data.grupo_compradores,
                    material_data.status,
                    material_data.codigo
                )
            else:
                # Insere um novo material
                query = """
                    INSERT INTO SAP_MATERIAL (
                        Codigo, Descricao, Tipo, Grupo_Mercadoria,
                        UMB, Peso_Bruto, Centro, Grupo_Compradores, Status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    material_data.codigo,
                    material_data.descricao,
                    material_data.tipo,
                    material_data.grupo_mercadoria,
                    material_data.umb,
                    material_data.peso_bruto,
                    material_data.centro,
                    material_data.grupo_compradores,
                    material_data.status
                )
                
            self.sql_conn.execute(query, params)
            return True
            
        except Exception as e:
            print(f"Error saving material {material_data.codigo}: {e}")
            raise
            
    def save_batch(self, materials):
        """Salva um lote de materiais no banco de dados"""
        try:
            query = """
                INSERT INTO SAP_MATERIAL (
                    Codigo, Descricao, Tipo, Grupo_Mercadoria,
                    UMB, Peso_Bruto, Centro, Grupo_Compradores, Status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            self.sql_conn.executemany(query, materials)
            return True
            
        except Exception as e:
            print(f"Error saving batch of materials: {e}")
            raise