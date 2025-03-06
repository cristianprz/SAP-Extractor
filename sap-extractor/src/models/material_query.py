class MaterialQuery:
    def __init__(self, sql_conn):
        self.sql_conn = sql_conn
 

    def check_database_access(self):
        """Check if we have access to QV database"""
        try:
            test_query = """
                SELECT TOP 1 1 AS access_check
                FROM [QV].[dbo].[MATERIAL_GERAL] WITH (NOLOCK)
            """
            results = self.sql_conn.execute(test_query).fetchall()
            return results is not None and len(results) > 0
        except Exception as e:
            print(f"Error accessing QV database: {e}")
            return False

    def get_materials_from_db(self):
        """Fetch material numbers from QV database"""
        try:
            if not self.check_database_access():
                raise PermissionError("No access to QV database")

            query = """
                SELECT DISTINCT [MAT_NUMERO_DO_MATERIAL]
                FROM [QV].[dbo].[MATERIAL_GERAL] WITH (NOLOCK)
                WHERE [MAT_CATEGORIA_GERAL] = '1- PRODUTO ACABADO'
                ORDER BY [MAT_NUMERO_DO_MATERIAL]
            """
            
            rows = self.sql_conn.execute(query).fetchall()
            if not rows:
                print("No materials found in database")
                return []

            materials = [
                str(row[0]).strip()
                for row in rows if row[0] is not None
            ]

            print(f"Found {len(materials)} materials to process")
            return materials

        except Exception as e:
            print(f"Error fetching materials from database: {e}")
            raise