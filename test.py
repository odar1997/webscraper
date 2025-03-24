import unittest
import os
import sqlite3
import pandas as pd

class TestFilmAffinityScraper(unittest.TestCase):
    
    def setUp(self):
        """Preparación para las pruebas"""
        # Nombre de los archivos que vamos a probar
        self.db_file = 'peliculas.db'
        self.csv_file = 'cartelera.csv'
    
    def test_csv_exists(self):
        """Verificar que el archivo CSV existe"""
        self.assertTrue(os.path.exists(self.csv_file), 
                       f"El archivo {self.csv_file} no existe")
    
    def test_csv_has_data(self):
        """Verificar que el CSV tiene datos"""
        df = pd.read_csv(self.csv_file)
        self.assertGreater(len(df), 0, "El CSV no contiene datos")
        self.assertEqual(list(df.columns), ["Película", "fecha_estreno"], 
                        "Las columnas del CSV no son las esperadas")
    
    def test_database_exists(self):
        """Verificar que la base de datos existe"""
        self.assertTrue(os.path.exists(self.db_file), 
                       f"La base de datos {self.db_file} no existe")
    
    def test_database_has_data(self):
        """Verificar que la base de datos tiene datos"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Verificar que existe la tabla cartelera
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cartelera'")
        self.assertIsNotNone(cursor.fetchone(), "La tabla 'cartelera' no existe en la base de datos")
        
        # Verificar que la tabla tiene datos
        cursor.execute("SELECT COUNT(*) FROM cartelera")
        count = cursor.fetchone()[0]
        self.assertGreater(count, 0, "La tabla 'cartelera' no contiene datos")
        
        conn.close()
    
    def test_database_and_csv_match(self):
        """Verificar que los datos en la base de datos y el CSV coinciden"""
        # Leer datos del CSV
        df_csv = pd.read_csv(self.csv_file)
        
        # Leer datos de la base de datos
        conn = sqlite3.connect(self.db_file)
        df_db = pd.read_sql_query("SELECT * FROM cartelera", conn)
        conn.close()
        
        # Verificar que tienen la misma cantidad de filas
        self.assertEqual(len(df_csv), len(df_db), 
                        "El número de películas en el CSV y la base de datos no coincide")

if __name__ == '__main__':
    unittest.main()