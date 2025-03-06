class BOM:
    def __init__(self, material, alt_text, base_unit, bom_no, base_quan, item_no, component, comp_qty, comp_unit):
        self.material = material
        self.alt_text = alt_text
        self.base_unit = base_unit
        self.bom_no = bom_no
        self.base_quan = base_quan
        self.item_no = item_no
        self.component = component
        self.comp_qty = comp_qty
        self.comp_unit = comp_unit

    def save_to_db(self, sql_connection):
        dados = (
            self.material,
            self.alt_text,
            self.base_unit,
            self.bom_no,
            self.base_quan,
            self.item_no,
            self.component,
            self.comp_qty,
            self.comp_unit
        )
        sql_connection.insert_bom_data(dados)

    @staticmethod
    def from_sap_data(material, result):
        bom_items = []
        for item in result['T_STPO']:
            bom_item = BOM(
                material,
                result['T_STKO'][0]['ALT_TEXT'],
                result['T_STKO'][0]['BASE_UNIT'],
                result['T_STKO'][0]['BOM_NO'],
                float(result['T_STKO'][0]['BASE_QUAN']),
                item['ITEM_NO'],
                item['COMPONENT'],
                float(item['COMP_QTY']),
                item['COMP_UNIT']
            )
            bom_items.append(bom_item)
        return bom_items

class BOMExtractor:
    def __init__(self, sap_conn, sql_conn):
        self.sap_conn = sap_conn
        self.sql_conn = sql_conn
        self.batch_size = 15000
 
    def setup_database(self):
        """Create or verify the BOM table"""
        try:
            self.sql_conn.execute("""
                IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[SAP_BOM]') AND type in (N'U'))
                BEGIN
                    CREATE TABLE [dbo].[SAP_BOM](
                        [ID] [int] IDENTITY(1,1) PRIMARY KEY,
                        [Codigo] [varchar](50),
                        [Material] [varchar](255),
                        [Unidade] [varchar](10),
                        [Nr_BOM] [varchar](50),
                        [Quantidade_Base] [varchar](50),
                        [Item] [varchar](50),
                        [Componente] [varchar](50),
                        [Quantidade] [varchar](50),
                        [Unidade_Comp] [varchar](10),
                        [Data_Insert] [datetime] DEFAULT GETDATE()
                    )
                END
                ELSE
                BEGIN
                    TRUNCATE TABLE [dbo].[SAP_BOM]
                END
            """)
            return True
        except Exception as e:
            print(f"Error setting up database: {e}")
            return False

    def extract_bom_batch(self, materials):
        """Extract BOM data for multiple materials in batches"""
        batch_data = []
        
        for material in materials:
            try:
                result = self.sap_conn.call_function('CSAP_MAT_BOM_READ',
                    MATERIAL=str(material),
                    PLANT='0050',
                    BOM_USAGE='1'
                )

                if 'T_STKO' in result and 'T_STPO' in result:
                    for item in result['T_STPO']:
                        bom_data = (
                            material,
                            result['T_STKO'][0]['ALT_TEXT'],
                            result['T_STKO'][0]['BASE_UNIT'],
                            result['T_STKO'][0]['BOM_NO'],
                            result['T_STKO'][0]['BASE_QUAN'],
                            item['ITEM_NO'],
                            item['COMPONENT'],
                            item['COMP_QTY'],
                            item['COMP_UNIT']
                        )
                        batch_data.append(bom_data)

                        if len(batch_data) >= self.batch_size:
                            self._save_batch(batch_data)
                            batch_data = []

            except Exception as e:
                print(f"Error processing material {material}: {e}")
                continue

        # Save any remaining records
        if batch_data:
            self._save_batch(batch_data)

    def _save_batch(self, batch_data):
        """Save a batch of BOM data to SQL Server"""
        try:
            query = """
                INSERT INTO SAP_BOM (
                    Codigo, Material, Unidade, Nr_BOM, 
                    Quantidade_Base, Item, Componente, 
                    Quantidade, Unidade_Comp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Convert any numeric values to strings to match varchar columns
            formatted_batch = [
                (
                    str(row[0]),  # Codigo
                    str(row[1]),  # Material
                    str(row[2]),  # Unidade
                    str(row[3]),  # Nr_BOM
                    str(row[4]),  # Quantidade_Base
                    str(row[5]),  # Item
                    str(row[6]),  # Componente
                    str(row[7]),  # Quantidade
                    str(row[8])   # Unidade_Comp
                )
                for row in batch_data
            ]
            
            self.sql_conn.executemany(query, formatted_batch)
            print(f"Successfully saved batch of {len(batch_data)} records")
            
        except Exception as e:
            print(f"Error saving batch data: {e}")
            raise