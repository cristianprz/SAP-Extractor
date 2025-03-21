# src/repositories/bom_repository.py
class BOMRepository:
    """Responsável pelo acesso aos dados de BOM no banco de dados"""
    
    def __init__(self, sql_conn):
        self.sql_conn = sql_conn
        
    def setup_table(self):
        """Cria ou verifica a tabela de BOM no banco e limpa dados existentes"""
        try:
            # Primeiro verifica se a tabela existe
            check_query = """
            IF EXISTS (SELECT * FROM sysobjects WHERE name='SAP_BOM' AND xtype='U')
                SELECT 1 AS table_exists
            ELSE
                SELECT 0 AS table_exists
            """
            cursor = self.sql_conn.execute(check_query)
            result = cursor.fetchone()
            table_exists = result[0] if result else 0
            
            if table_exists:
                # Se a tabela existe, trunca os dados
                print("SAP_BOM table exists. Cleaning existing data...")
                truncate_query = "TRUNCATE TABLE SAP_BOM"
                self.sql_conn.execute(truncate_query)
                print("SAP_BOM table cleared successfully.")
            else:
                # Se a tabela não existe, cria ela
                print("Creating SAP_BOM table...")
                create_query = """
                CREATE TABLE SAP_BOM (
                    Codigo VARCHAR(18) NOT NULL,
                    Material VARCHAR(40) NOT NULL,
                    Unidade VARCHAR(3),
                    Nr_BOM VARCHAR(8),
                    Quantidade_Base VARCHAR(13),
                    Item VARCHAR(4),
                    Componente VARCHAR(18),
                    Quantidade VARCHAR(13),
                    Unidade_Comp VARCHAR(3),
                    Data_Insert DATETIME DEFAULT GETDATE()
                )
                """
                self.sql_conn.execute(create_query)
                print("SAP_BOM table created successfully.")
            
            return True
            
        except Exception as e:
            print(f"Error setting up BOM table: {e}")
            raise
        
    def save_batch(self, bom_items):
        """Salva um lote de itens de BOM no banco de dados"""
        try:
            query = """
                INSERT INTO SAP_BOM (
                    Codigo, Material, Unidade, Nr_BOM, 
                    Quantidade_Base, Item, Componente, 
                    Quantidade, Unidade_Comp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            self.sql_conn.executemany(query, bom_items)
            return True
            
        except Exception as e:
            print(f"Error saving batch data: {e}")
            raise
            
    def get_by_material(self, material_code):
        """Busca os registros de BOM para um material específico"""
        try:
            query = """
                SELECT * FROM SAP_BOM 
                WHERE Codigo = ?
                ORDER BY Item
            """
            
            cursor = self.sql_conn.execute(query, (material_code,))
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Error fetching BOM for material {material_code}: {e}")
            return []